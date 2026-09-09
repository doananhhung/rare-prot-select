"""Thực hiện Công đoạn 7.2 trong Tài liệu 1 và Module 4.2 (run_core_merops.py) trong Tài liệu 2."""

from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Add parent directory to sys.path if running as script
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from src.config.settings import ExperimentConfig, load_config
from src.data.dataset_loader import DatasetLoader
from src.embeddings.cache_manager import CacheManager
from src.embeddings.esm_embedder import ESMEmbedder
from src.evaluation.annotation_transfer import evaluate_annotation_transfer_1nn
from src.evaluation.intrinsic_metrics import evaluate_intrinsic_metrics
# Baseline selectors removed for strict 1-1 comparison
from src.selection.lazy_greedy import LazyGreedySelector
from src.similarity.dense_similarity import compute_cosine_similarity_matrix
from src.utils.exporter import ResultExporter
from src.utils.memory_tracker import MemoryTracker
from src.utils.timer import Timer
from src.utils.visualizer import Visualizer
from src.weighting.rare_weighting import compute_rare_aware_weights

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("run_core_merops")


def run_core_merops(config_path: str = "configs/config_core_merops.yaml") -> dict[str, Any]:
    """Thực thi kịch bản Thực nghiệm Trọng tâm trên 13,847 chuỗi Peptidase A1 (MEROPS A1A)."""
    logger.info("=" * 70)
    logger.info("STARTING CORE EXPERIMENT: MEROPS A1A (76 SUBFAMILIES)")
    logger.info("=" * 70)

    # 1. Nạp cấu hình
    resolved_config_path = Path(config_path)
    if not resolved_config_path.exists():
        candidate = parent_dir / config_path
        if candidate.exists():
            resolved_config_path = candidate

    config: ExperimentConfig = load_config(resolved_config_path)
    logger.info(f"Loaded configuration from: {resolved_config_path}")
    logger.info(f"Dataset: {config.dataset_name}, FASTA: {config.fasta_path}")
    logger.info(f"Budget k list: {config.budget_k_list}")

    # Tạo thư mục outputs
    outputs_dir = Path(config.output_dir)
    tables_dir = outputs_dir / "tables"
    figures_dir = outputs_dir / "figures"
    cache_dir = Path(config.cache_dir)

    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    # 2. Nạp và tiền xử lý dữ liệu FASTA
    logger.info("\n--- STEP 1: LOADING AND PREPROCESSING FASTA DATA ---")
    bundle = DatasetLoader.load_and_preprocess_dataset(config)
    cleaned_records = bundle.cleaned_records
    seq_ids = [rec.id for rec in cleaned_records]
    sequences = [rec.sequence for rec in cleaned_records]
    labels = [bundle.label_map[sid] for sid in seq_ids]

    logger.info(f"Sequences passed QC: {len(cleaned_records)} proteins.")
    logger.info(f"Extracted subfamilies: {len(bundle.subfamily_counts)} families.")
    logger.info(f"Rare subfamilies (<= {config.rare_threshold}): {len(bundle.rare_subfamilies)} families.")

    # 3. Trích xuất / Nạp Vector Nhúng ESM-2
    logger.info("\n--- STEP 2: EXTRACTING / LOADING ESM-2 EMBEDDINGS ON GPU ---")
    cache_mgr = CacheManager(cache_dir=cache_dir)
    if cache_mgr.is_cached(config.dataset_name, config.model_name, expected_ids=seq_ids):
        logger.info("Valid cache found. Loading embeddings from disk...")
        embeddings, _, _ = cache_mgr.load(config.dataset_name, config.model_name)
    else:
        logger.info(f"No cache found. Initializing ESM-2 model '{config.model_name}'...")
        embedder = ESMEmbedder(model_name=config.model_name, device=config.device)
        logger.info(f"Generating embeddings for {len(sequences)} sequences with batch_size={config.batch_size}...")
        embeddings = embedder.embed_sequences(
            sequences=sequences,
            batch_size=config.batch_size,
            show_progress=True,
        )
        cache_mgr.save(
            dataset_name=config.dataset_name,
            model_name=config.model_name,
            embeddings=embeddings,
            seq_ids=seq_ids,
            metadata={"num_sequences": len(seq_ids), "dataset": config.dataset_name},
        )

    logger.info(f"Embeddings shape: {embeddings.shape}, dtype: {embeddings.dtype}")

    # 4. Tính Ma trận Tương đồng Cosine
    logger.info("\n--- STEP 3: COMPUTING COSINE SIMILARITY MATRIX ---")
    with Timer("Cosine Similarity Matrix", auto_log=True):
        sim_matrix = compute_cosine_similarity_matrix(embeddings)
    logger.info(f"Similarity matrix shape: {sim_matrix.shape}, Min: {sim_matrix.min():.4f}, Max: {sim_matrix.max():.4f}")

    # 5. Tính Trọng số Rare-Aware
    logger.info("\n--- STEP 4: COMPUTING WEIGHT VECTORS ---")
    rare_weights = compute_rare_aware_weights(
        seq_ids=seq_ids,
        label_map=bundle.label_map,
        scheme=config.weighting_scheme,
        alpha=config.weighting_alpha,
    )
    uniform_weights = compute_rare_aware_weights(
        seq_ids=seq_ids,
        label_map=bundle.label_map,
        scheme="uniform",
        alpha=0.0,
    )
    logger.info(f"Rare weights min: {rare_weights.min():.4f}, max: {rare_weights.max():.4f}, mean: {rare_weights.mean():.4f}")

    # 6. Chạy thực nghiệm so sánh đối đầu toàn diện
    logger.info("\n--- STEP 5: HEAD-TO-HEAD COMPARISON ACROSS BUDGET k ---")
    results: list[dict[str, Any]] = []

    methods = [
        ("RareProtSelect (WFL)", "lazy_greedy", rare_weights),
        ("Unweighted FL (Nguyen et al., 2025)", "lazy_greedy", uniform_weights),
    ]

    for k in config.budget_k_list:
        logger.info(f"\n>>> Evaluating Budget k = {k} <<<")

        for method_name, method_type, weights in methods:
            timer = Timer()
            mem_tracker = MemoryTracker()

            mem_tracker.start()
            timer.start()

            selector = LazyGreedySelector(sim_matrix=sim_matrix, weights=weights, seq_ids=seq_ids)
            res = selector.select(budget_k=k)
            selected_indices = res.selected_indices
            selected_ids = res.selected_ids

            runtime_sec = timer.stop()
            peak_ram_mb, _ = mem_tracker.stop()

            # Đánh giá Intrinsic Metrics
            intrinsic = evaluate_intrinsic_metrics(
                sim_matrix=sim_matrix,
                selected_indices=selected_indices,
                labels=labels,
                rare_threshold=config.rare_threshold,
            )

            # Đánh giá Annotation Transfer 1-NN
            annot_transfer = evaluate_annotation_transfer_1nn(
                sim_matrix=sim_matrix,
                selected_indices=selected_indices,
                labels=labels,
            )

            row = {
                "dataset": config.dataset_name,
                "method": method_name,
                "budget_k": int(k),
                "overall_coverage": round(intrinsic["overall_coverage"], 4),
                "macro_coverage": round(intrinsic["macro_coverage"], 4),
                "worst_group_coverage": round(intrinsic["worst_group_coverage"], 4),
                "rare_representation_rate": round(intrinsic["rare_group_representation_rate"], 4),
                "pairwise_redundancy": round(intrinsic["pairwise_redundancy"], 4),
                "transfer_accuracy": round(annot_transfer["accuracy"], 4),
                "transfer_macro_f1": round(annot_transfer["macro_f1"], 4),
                "runtime_seconds": round(runtime_sec, 4),
                "peak_ram_mb": round(peak_ram_mb, 2),
            }
            results.append(row)

            logger.info(
                f"  [{method_name:35s}] Worst-Cov: {row['worst_group_coverage']:.4f} | "
                f"Macro-Cov: {row['macro_coverage']:.4f} | "
                f"Overall-Cov: {row['overall_coverage']:.4f} | "
                f"Rare-Rep: {row['rare_representation_rate'] * 100:.1f}% | "
                f"Macro-F1: {row['transfer_macro_f1']:.4f} | "
                f"Time: {row['runtime_seconds']:.2f}s"
            )

    # 7. Xuất bảng kết quả
    logger.info("\n--- STEP 6: EXPORTING RESULT TABLES AND SCIENTIFIC REPORTS ---")
    df_results = pd.DataFrame(results)

    table_csv = tables_dir / "merops_core_comparison.csv"
    table_json = tables_dir / "merops_core_comparison.json"
    table_md = tables_dir / "merops_core_comparison.md"

    ResultExporter.export_to_csv(df_results, table_csv)
    ResultExporter.export_to_json(results, table_json)
    ResultExporter.export_to_markdown(
        df_results,
        table_md,
        title="MEROPS A1A Core Experiment: Head-to-Head Baseline Comparison",
    )

    # 8. Vẽ đồ thị
    logger.info("\n--- STEP 7: VISUALIZING SCIENTIFIC FIGURES ---")
    fig_cov_png = figures_dir / "merops_coverage_vs_k.png"
    fig_cov_svg = figures_dir / "merops_coverage_vs_k.svg"
    fig_rare_png = figures_dir / "merops_rare_rep_vs_k.png"
    fig_rare_svg = figures_dir / "merops_rare_rep_vs_k.svg"
    fig_f1_png = figures_dir / "merops_macro_f1_vs_k.png"
    fig_f1_svg = figures_dir / "merops_macro_f1_vs_k.svg"

    # Trích xuất dữ liệu cho các biểu đồ
    method_names = [m[0] for m in methods]
    worst_cov_data: dict[str, list[float]] = {}
    macro_cov_data: dict[str, list[float]] = {}
    rare_rep_data: dict[str, list[float]] = {}
    macro_f1_data: dict[str, list[float]] = {}

    for m_name in method_names:
        sub = df_results[df_results["method"] == m_name]
        worst_cov_data[m_name] = sub["worst_group_coverage"].tolist()
        macro_cov_data[m_name] = sub["macro_coverage"].tolist()
        rare_rep_data[m_name] = sub["rare_representation_rate"].tolist()
        macro_f1_data[m_name] = sub["transfer_macro_f1"].tolist()

    # 1. Worst-Group Coverage vs k
    Visualizer.plot_coverage_vs_budget(
        budget_k_list=config.budget_k_list,
        metrics_by_method=worst_cov_data,
        output_path=fig_cov_png,
        title="MEROPS A1A: Worst-Group Coverage vs Budget $k$",
        metric_name="Worst-Group Coverage",
    )
    Visualizer.plot_coverage_vs_budget(
        budget_k_list=config.budget_k_list,
        metrics_by_method=worst_cov_data,
        output_path=fig_cov_svg,
        title="MEROPS A1A: Worst-Group Coverage vs Budget $k$",
        metric_name="Worst-Group Coverage",
    )

    # 2. Rare Group Representation Rate vs k
    Visualizer.plot_rare_representation(
        budget_k_list=config.budget_k_list,
        rare_rep_by_method=rare_rep_data,
        output_path=fig_rare_png,
    )
    Visualizer.plot_rare_representation(
        budget_k_list=config.budget_k_list,
        rare_rep_by_method=rare_rep_data,
        output_path=fig_rare_svg,
    )

    # 3. Macro-F1 vs k
    Visualizer.plot_coverage_vs_budget(
        budget_k_list=config.budget_k_list,
        metrics_by_method=macro_f1_data,
        output_path=fig_f1_png,
        title="MEROPS A1A: 1-NN Annotation Transfer Macro-F1 vs Budget $k$",
        metric_name="Macro-F1 Score",
    )
    Visualizer.plot_coverage_vs_budget(
        budget_k_list=config.budget_k_list,
        metrics_by_method=macro_f1_data,
        output_path=fig_f1_svg,
        title="MEROPS A1A: 1-NN Annotation Transfer Macro-F1 vs Budget $k$",
        metric_name="Macro-F1 Score",
    )


    logger.info("\n" + "=" * 70)
    logger.info("EXPERIMENT COMPLETED: MEROPS A1A core benchmark finished successfully!")
    logger.info(f"Outputs saved to: {tables_dir} and {figures_dir}")
    logger.info("=" * 70)

    return {
        "status": "SUCCESS",
        "dataset": config.dataset_name,
        "num_records": len(cleaned_records),
        "num_subfamilies": len(bundle.subfamily_counts),
        "results_table_csv": str(table_csv),
        "results_table_md": str(table_md),
        "figure_coverage_png": str(fig_cov_png),
    }


def main() -> None:
    """Entry point cho CLI."""
    parser = argparse.ArgumentParser(description="Run Core MEROPS A1A experiment.")
    parser.add_argument(
        "--config",
        type=str,
        default="configs/config_core_merops.yaml",
        help="Đường dẫn tới tệp cấu hình YAML.",
    )
    args = parser.parse_args()
    run_core_merops(config_path=args.config)


if __name__ == "__main__":
    main()
