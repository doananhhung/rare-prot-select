"""Thực hiện Công đoạn 7.1 trong Tài liệu 1 và Module 4.1 (run_pilot_thyme.py) trong Tài liệu 2."""

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
from src.data.fasta_parser import parse_fasta
from src.embeddings.cache_manager import CacheManager
from src.embeddings.esm_embedder import ESMEmbedder
from src.evaluation.annotation_transfer import evaluate_annotation_transfer_1nn
from src.evaluation.benchmark_comparator import evaluate_benchmark_identity
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
logger = logging.getLogger("run_pilot_thyme")


def run_pilot_thyme(config_path: str = "configs/config_pilot_thyme.yaml") -> dict[str, Any]:
    """Thực thi kịch bản Pilot Thioesterase (TE27)."""
    logger.info("=" * 70)
    logger.info("STARTING PILOT EXPERIMENT: 27 THIOESTERASE FAMILIES (ThYme DB)")
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
    id_to_idx = {sid: idx for idx, sid in enumerate(seq_ids)}

    logger.info(f"Sequences passed QC: {len(cleaned_records)} proteins.")
    logger.info(f"Extracted subfamilies: {len(bundle.subfamily_counts)} families.")
    logger.info(f"Rare subfamilies (<= {config.rare_threshold}): {len(bundle.rare_subfamilies)} families.")

    # 3. Trích xuất / Nạp Vector Nhúng ESM-2
    logger.info("\n--- STEP 2: EXTRACTING / LOADING ESM-2 EMBEDDINGS ---")
    cache_mgr = CacheManager(cache_dir=cache_dir)
    if cache_mgr.is_cached(config.dataset_name, config.model_name, expected_ids=seq_ids):
        logger.info("Valid cache found. Loading embeddings from disk...")
        embeddings, _, _ = cache_mgr.load(config.dataset_name, config.model_name)
    else:
        logger.info(f"No cache found. Initializing ESM-2 model '{config.model_name}'...")
        embedder = ESMEmbedder(model_name=config.model_name, device=config.device)
        logger.info(f"Generating embeddings for {len(sequences)} sequences...")
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
    with Timer("Cosine Similarity Computation", auto_log=True):
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

    # 6. Xác định tập chuẩn Chuyên gia (Gold Standard Benchmark)
    # Trong ThYme DB, mỗi họ có chuỗi chuẩn đại diện (chọn sequence đầu tiên của mỗi họ hoặc đọc file nếu có)
    benchmark_gold_ids: list[str] = []
    if config.benchmark_gold_path and Path(config.benchmark_gold_path).exists():
        gold_records = parse_fasta(config.benchmark_gold_path)
        benchmark_gold_ids = [r.id for r in gold_records]
        logger.info(f"Loaded {len(benchmark_gold_ids)} expert benchmark sequences from {config.benchmark_gold_path}")
    else:
        # Xây dựng canonical benchmark đại diện từ 27 họ (1 chuỗi canonical đầu tiên mỗi họ)
        seen_fams = set()
        for rec in cleaned_records:
            fam = bundle.label_map[rec.id]
            if fam not in seen_fams:
                seen_fams.add(fam)
                benchmark_gold_ids.append(rec.id)
        logger.info(f"Built canonical expert benchmark: {len(benchmark_gold_ids)} sequences for {len(seen_fams)} families.")

    # 7. Chạy thực nghiệm qua dải ngân sách k
    logger.info("\n--- STEP 5: SUBMODULAR SELECTION & BENCHMARK EVALUATION ---")
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

            # Đánh giá Benchmark Identity với tập chuyên gia
            bench_eval = evaluate_benchmark_identity(
                selected_seq_ids=selected_ids,
                benchmark_seq_ids=benchmark_gold_ids,
                sim_matrix=sim_matrix,
                id_to_idx=id_to_idx,
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
                "benchmark_overlap_count": int(bench_eval["overlap_count"]),
                "benchmark_exact_recall": round(bench_eval["exact_match_recall"], 4),
                "benchmark_f1": round(bench_eval["f1_score"], 4),
                "benchmark_semantic_coverage": round(bench_eval["mean_max_similarity"], 4),
                "runtime_seconds": round(runtime_sec, 4),
                "peak_ram_mb": round(peak_ram_mb, 2),
            }
            results.append(row)

            logger.info(
                f"  [{method_name:35s}] Worst-Cov: {row['worst_group_coverage']:.4f} | "
                f"Macro-Cov: {row['macro_coverage']:.4f} | "
                f"Rare-Rep: {row['rare_representation_rate'] * 100:.1f}% | "
                f"Macro-F1: {row['transfer_macro_f1']:.4f} | "
                f"Bench-Rec: {row['benchmark_exact_recall']:.4f}"
            )

    # 8. Xuất bảng kết quả
    logger.info("\n--- STEP 6: EXPORTING RESULT TABLES AND REPORTS ---")
    df_results = pd.DataFrame(results)

    table_csv = tables_dir / "thyme_pilot_results.csv"
    table_json = tables_dir / "thyme_pilot_results.json"
    table_md = tables_dir / "thyme_pilot_results.md"

    ResultExporter.export_to_csv(df_results, table_csv)
    ResultExporter.export_to_json(results, table_json)
    ResultExporter.export_to_markdown(
        df_results,
        table_md,
        title="Thioesterases (ThYme 27 Families) Pilot Experiment Results",
    )

    # 9. Vẽ đồ thị
    logger.info("\n--- STEP 7: VISUALIZING FIGURES ---")
    fig_coverage_png = figures_dir / "thyme_pilot_coverage.png"
    fig_coverage_svg = figures_dir / "thyme_pilot_coverage.svg"
    fig_rare_png = figures_dir / "thyme_pilot_rare_rep.png"
    fig_rare_svg = figures_dir / "thyme_pilot_rare_rep.svg"

    # Chuẩn bị dữ liệu cho visualizer
    metrics_worst_cov: dict[str, list[float]] = {}
    metrics_macro_cov: dict[str, list[float]] = {}
    metrics_rare_rep: dict[str, list[float]] = {}

    for method_name, _, _ in methods:
        sub_df = df_results[df_results["method"] == method_name]
        metrics_worst_cov[method_name] = sub_df["worst_group_coverage"].tolist()
        metrics_macro_cov[method_name] = sub_df["macro_coverage"].tolist()
        metrics_rare_rep[method_name] = sub_df["rare_representation_rate"].tolist()

    Visualizer.plot_coverage_vs_budget(
        budget_k_list=config.budget_k_list,
        metrics_by_method=metrics_worst_cov,
        output_path=fig_coverage_png,
        title="Thioesterases Pilot: Worst-Group Coverage vs Budget $k$",
        metric_name="Worst-Group Coverage",
    )
    Visualizer.plot_coverage_vs_budget(
        budget_k_list=config.budget_k_list,
        metrics_by_method=metrics_worst_cov,
        output_path=fig_coverage_svg,
        title="Thioesterases Pilot: Worst-Group Coverage vs Budget $k$",
        metric_name="Worst-Group Coverage",
    )

    Visualizer.plot_rare_representation(
        budget_k_list=config.budget_k_list,
        rare_rep_by_method=metrics_rare_rep,
        output_path=fig_rare_png,
    )
    Visualizer.plot_rare_representation(
        budget_k_list=config.budget_k_list,
        rare_rep_by_method=metrics_rare_rep,
        output_path=fig_rare_svg,
    )

    logger.info("\n" + "=" * 70)
    logger.info("EXPERIMENT COMPLETED: Pilot Thioesterase finished successfully!")
    logger.info(f"Outputs saved to: {tables_dir} and {figures_dir}")
    logger.info("=" * 70)

    return {
        "status": "SUCCESS",
        "dataset": config.dataset_name,
        "num_records": len(cleaned_records),
        "num_subfamilies": len(bundle.subfamily_counts),
        "results_table_csv": str(table_csv),
        "results_table_md": str(table_md),
        "figure_coverage_png": str(fig_coverage_png),
    }


def main() -> None:
    """Entry point cho CLI."""
    parser = argparse.ArgumentParser(description="Run Pilot Thioesterase experiment.")
    parser.add_argument(
        "--config",
        type=str,
        default="configs/config_pilot_thyme.yaml",
        help="Đường dẫn tới tệp cấu hình YAML.",
    )
    args = parser.parse_args()
    run_pilot_thyme(config_path=args.config)


if __name__ == "__main__":
    main()
