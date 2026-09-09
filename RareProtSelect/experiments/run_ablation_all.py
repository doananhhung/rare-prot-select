"""Thực hiện Giai đoạn 6 trong Tài liệu 1 và Module 4.4 (run_ablation_all.py) trong Tài liệu 2."""

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
import seaborn as sns

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
logger = logging.getLogger("run_ablation_all")


def run_ablation_all(config_path: str = "configs/config_ablation.yaml") -> dict[str, Any]:
    """Thực thi toàn bộ Ma trận Bóc tách Thành phần (Ablation Studies)."""
    logger.info("=" * 70)
    logger.info("STARTING COMPREHENSIVE ABLATION STUDIES")
    logger.info("=" * 70)

    # 1. Load configuration
    resolved_config_path = Path(config_path)
    if not resolved_config_path.exists():
        candidate = parent_dir / config_path
        if candidate.exists():
            resolved_config_path = candidate

    config: ExperimentConfig = load_config(resolved_config_path)
    logger.info(f"Loaded configuration from: {resolved_config_path}")
    logger.info(f"Dataset: {config.dataset_name}, FASTA: {config.fasta_path}")
    logger.info(f"Budget k list: {config.budget_k_list}")

    # Create outputs directories
    outputs_dir = Path(config.output_dir)
    tables_dir = outputs_dir / "tables" if outputs_dir.name != "outputs" else outputs_dir.parent / "outputs/tables"
    figures_dir = outputs_dir / "figures" if outputs_dir.name != "outputs" else outputs_dir.parent / "outputs/figures"
    
    # Also ensure outputs/tables and outputs/figures in root output_dir
    root_tables_dir = Path("outputs/tables")
    root_figures_dir = Path("outputs/figures")

    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    root_tables_dir.mkdir(parents=True, exist_ok=True)
    root_figures_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = Path(config.cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)

    # 2. Load and preprocess FASTA dataset
    logger.info("\n--- STEP 1: LOADING AND PREPROCESSING FASTA DATASET ---")
    bundle = DatasetLoader.load_and_preprocess_dataset(config)
    cleaned_records = bundle.cleaned_records
    seq_ids = [rec.id for rec in cleaned_records]
    sequences = [rec.sequence for rec in cleaned_records]
    labels = [bundle.label_map[sid] for sid in seq_ids]

    logger.info(f"Total sequences after QC: {len(cleaned_records)} proteins.")
    logger.info(f"Number of subfamilies extracted: {len(bundle.subfamily_counts)} subfamilies.")
    logger.info(f"Number of rare subfamilies (<= {config.rare_threshold}): {len(bundle.rare_subfamilies)} subfamilies.")

    # 3. Extract / Load ESM-2 Embeddings
    logger.info("\n--- STEP 2: EXTRACTING / LOADING ESM-2 EMBEDDINGS ---")
    cache_mgr = CacheManager(cache_dir=cache_dir)
    if cache_mgr.is_cached(config.dataset_name, config.model_name, expected_ids=seq_ids):
        logger.info(f"Valid embeddings cache found. Loading from disk...")
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

    logger.info(f"Embeddings shape: {embeddings.shape}")

    # 4. Compute Cosine Similarity Matrix
    logger.info("\n--- STEP 3: COMPUTING COSINE SIMILARITY MATRIX ---")
    with Timer("Cosine Similarity Matrix", auto_log=True):
        sim_matrix = compute_cosine_similarity_matrix(embeddings)

    # -------------------------------------------------------------------------
    # ABLATION 1: EXPONENT SENSITIVITY ALPHA in [0.0, 0.25, 0.5, 0.75, 1.0]
    # -------------------------------------------------------------------------
    logger.info("\n--- STEP 4: ABLATION ON WEIGHTING DECAY EXPONENT ALPHA ---")
    alpha_configs = [
        ("Uniform (alpha=0.0 / Unweighted)", "power", 0.0),
        ("Power (alpha=0.25)", "power", 0.25),
        ("RareProtSelect (alpha=0.5 / Inverse Sqrt)", "inverse_sqrt", 0.5),
        ("Power (alpha=0.75)", "power", 0.75),
        ("Inverse Freq (alpha=1.0)", "inverse_freq", 1.0),
    ]

    weighting_results: list[dict[str, Any]] = []

    for alpha_label, scheme, alpha_val in alpha_configs:
        logger.info(f"\n>>> Evaluating Scheme: {alpha_label} <<<")
        weights = compute_rare_aware_weights(
            seq_ids=seq_ids,
            label_map=bundle.label_map,
            scheme=scheme,
            alpha=alpha_val,
        )

        for k in config.budget_k_list:
            selector = LazyGreedySelector(sim_matrix=sim_matrix, weights=weights, seq_ids=seq_ids)
            res = selector.select(budget_k=k)

            # Intrinsic Metrics
            intrinsic = evaluate_intrinsic_metrics(
                sim_matrix=sim_matrix,
                selected_indices=res.selected_indices,
                labels=labels,
                rare_threshold=config.rare_threshold,
            )

            # 1-NN Transfer
            annot = evaluate_annotation_transfer_1nn(
                sim_matrix=sim_matrix,
                selected_indices=res.selected_indices,
                labels=labels,
            )

            row = {
                "weighting_scheme": alpha_label,
                "alpha": float(alpha_val),
                "budget_k": int(k),
                "worst_group_coverage": round(intrinsic["worst_group_coverage"], 4),
                "macro_coverage": round(intrinsic["macro_coverage"], 4),
                "overall_coverage": round(intrinsic["overall_coverage"], 4),
                "rare_representation_rate": round(intrinsic["rare_group_representation_rate"], 4),
                "pairwise_redundancy": round(intrinsic["pairwise_redundancy"], 4),
                "transfer_macro_f1": round(annot["macro_f1"], 4),
                "runtime_seconds": round(res.runtime_seconds, 4),
                "function_evaluations": int(res.total_evaluations),
            }
            weighting_results.append(row)

            logger.info(
                f"  k={k:3d} | Worst-Cov: {row['worst_group_coverage']:.4f} | "
                f"Macro-Cov: {row['macro_coverage']:.4f} | "
                f"Rare-Rep: {row['rare_representation_rate'] * 100:.1f}% | "
                f"Macro-F1: {row['transfer_macro_f1']:.4f}"
            )

    # -------------------------------------------------------------------------
    # ABLATION 2: BASELINE METHODS COMPARISON (METHOD ABLATION)
    # -------------------------------------------------------------------------
    logger.info("\n--- STEP 5: ABLATION ON SELECTION ALGORITHMS ---")
    method_results: list[dict[str, Any]] = []

    # Prepare default Rare-Aware weights
    w_rare = compute_rare_aware_weights(seq_ids, bundle.label_map, "inverse_sqrt", 0.5)

    methods = [
        ("RareProtSelect (Lazy WFL)", "lazy_greedy", w_rare),
        ("Unweighted FL (Nguyen et al., 2025)", "lazy_greedy", np.ones(len(seq_ids))),
    ]

    for k in config.budget_k_list:
        for m_name, m_type, m_w in methods:
            selector = LazyGreedySelector(sim_matrix=sim_matrix, weights=m_w, seq_ids=seq_ids)
            res = selector.select(budget_k=k)
            indices = res.selected_indices

            intrinsic = evaluate_intrinsic_metrics(
                sim_matrix=sim_matrix,
                selected_indices=indices,
                labels=labels,
                rare_threshold=config.rare_threshold,
            )
            annot = evaluate_annotation_transfer_1nn(
                sim_matrix=sim_matrix,
                selected_indices=indices,
                labels=labels,
            )

            method_results.append({
                "method": m_name,
                "budget_k": int(k),
                "worst_group_coverage": round(intrinsic["worst_group_coverage"], 4),
                "macro_coverage": round(intrinsic["macro_coverage"], 4),
                "overall_coverage": round(intrinsic["overall_coverage"], 4),
                "rare_representation_rate": round(intrinsic["rare_group_representation_rate"], 4),
                "pairwise_redundancy": round(intrinsic["pairwise_redundancy"], 4),
                "transfer_macro_f1": round(annot["macro_f1"], 4),
            })

    # -------------------------------------------------------------------------
    # 6. EXPORT RESULT TABLES
    # -------------------------------------------------------------------------
    logger.info("\n--- STEP 6: EXPORTING ABLATION RESULT TABLES ---")
    df_weighting = pd.DataFrame(weighting_results)
    df_methods = pd.DataFrame(method_results)

    # Save to both target locations
    for t_dir in [tables_dir, root_tables_dir]:
        ResultExporter.export_to_csv(df_weighting, t_dir / "ablation_weighting_results.csv")
        ResultExporter.export_to_json(weighting_results, t_dir / "ablation_weighting_results.json")
        ResultExporter.export_to_markdown(
            df_weighting,
            t_dir / "ablation_weighting_results.md",
            title="Ablation Study: Weighting Scheme & Alpha Sensitivity Analysis",
        )

        ResultExporter.export_to_csv(df_methods, t_dir / "ablation_methods_results.csv")
        ResultExporter.export_to_json(method_results, t_dir / "ablation_methods_results.json")
        ResultExporter.export_to_markdown(
            df_methods,
            t_dir / "ablation_methods_results.md",
            title="Ablation Study: Selection Algorithms Comparison",
        )

    # -------------------------------------------------------------------------
    # 7. VISUALIZE ABLATION FIGURES
    # -------------------------------------------------------------------------
    logger.info("\n--- STEP 7: VISUALIZING ABLATION FIGURES ---")
    for f_dir in [figures_dir, root_figures_dir]:
        fig_alpha_png = f_dir / "ablation_alpha_comparison.png"
        fig_alpha_svg = f_dir / "ablation_alpha_comparison.svg"
        fig_methods_png = f_dir / "ablation_methods_comparison.png"
        fig_methods_svg = f_dir / "ablation_methods_comparison.svg"

        # 1. Alpha Sensitivity Chart
        plt.figure(figsize=(10, 6))
        sns.barplot(
            data=df_weighting,
            x="weighting_scheme",
            y="worst_group_coverage",
            hue="budget_k",
            palette="viridis",
        )
        plt.title("Ablation: Impact of Weighting Decay Exponent $\\alpha$ on Worst-Group Coverage", fontsize=13, fontweight="bold")
        plt.xlabel("Weighting Scheme ($\\alpha$ exponent)", fontsize=11)
        plt.ylabel("Worst-Group Coverage", fontsize=11)
        plt.xticks(rotation=15, ha="right")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.savefig(fig_alpha_png, dpi=300)
        plt.savefig(fig_alpha_svg, dpi=300)
        plt.close()

        # 2. Methods Comparison Chart
        plt.figure(figsize=(10, 6))
        sns.barplot(
            data=df_methods,
            x="method",
            y="worst_group_coverage",
            hue="budget_k",
            palette="magma",
        )
        plt.title("Ablation: Selection Method Comparison on Worst-Group Coverage", fontsize=13, fontweight="bold")
        plt.xlabel("Selection Algorithm", fontsize=11)
        plt.ylabel("Worst-Group Coverage", fontsize=11)
        plt.xticks(rotation=15, ha="right")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.savefig(fig_methods_png, dpi=300)
        plt.savefig(fig_methods_svg, dpi=300)
        plt.close()

    logger.info("\n" + "=" * 70)
    logger.info("EXPERIMENT COMPLETED: All ablation studies finished successfully!")
    logger.info(f"Results saved to: {tables_dir} and {figures_dir}")
    logger.info("=" * 70)

    return {
        "status": "SUCCESS",
        "dataset": config.dataset_name,
        "results_weighting_csv": str(root_tables_dir / "ablation_weighting_results.csv"),
        "results_methods_csv": str(root_tables_dir / "ablation_methods_results.csv"),
    }


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Run Ablation experiments.")
    parser.add_argument(
        "--config",
        type=str,
        default="configs/config_ablation.yaml",
        help="Path to YAML configuration file.",
    )
    args = parser.parse_args()
    run_ablation_all(config_path=args.config)


if __name__ == "__main__":
    main()
