"""Thực hiện Trực quan hóa Kết quả trong Tài liệu 1 và Module 3.8 (visualizer.py) trong Tài liệu 2."""

from __future__ import annotations

import logging
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for server/script rendering
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

logger = logging.getLogger(__name__)


class Visualizer:
    """Bộ công cụ trực quan hóa kết quả thực nghiệm chuẩn công bố khoa học."""

    DEFAULT_COLORS = [
        "#1f77b4",  # Blue
        "#ff7f0e",  # Orange
        "#2ca02c",  # Green
        "#d62728",  # Red
        "#9467bd",  # Purple
        "#8c564b",  # Brown
        "#e377c2",  # Pink
        "#7f7f7f",  # Gray
    ]

    DEFAULT_MARKERS = ["o", "s", "^", "D", "v", "p", "*", "X"]

    @staticmethod
    def _ensure_dir(output_path: str | Path) -> Path:
        p = Path(output_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

    @classmethod
    def plot_coverage_vs_budget(
        cls,
        budget_k_list: list[int],
        metrics_by_method: dict[str, list[float]],
        output_path: str | Path,
        title: str = "Worst-Group Coverage vs Budget k",
        metric_name: str = "Worst-Group Coverage",
        dpi: int = 300,
    ) -> None:
        """Vẽ biểu đồ đường cong độ bao phủ theo các mức ngân sách k."""
        out_p = cls._ensure_dir(output_path)
        plt.figure(figsize=(8, 5))

        for idx, (method_name, values) in enumerate(metrics_by_method.items()):
            color = cls.DEFAULT_COLORS[idx % len(cls.DEFAULT_COLORS)]
            marker = cls.DEFAULT_MARKERS[idx % len(cls.DEFAULT_MARKERS)]
            plt.plot(
                budget_k_list[: len(values)],
                values,
                label=method_name,
                color=color,
                marker=marker,
                linewidth=2.0,
                markersize=6,
            )

        plt.title(title, fontsize=13, fontweight="bold", pad=12)
        plt.xlabel("Budget $k$ (Representative Set Size)", fontsize=11)
        plt.ylabel(metric_name, fontsize=11)
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.legend(frameon=True, facecolor="white", edgecolor="none", fontsize=10)
        plt.tight_layout()
        plt.savefig(out_p, dpi=dpi)
        plt.close()
        logger.info(f"Saved figure: {out_p}")

    @classmethod
    def plot_coverage_comparison(
        cls,
        budget_k_list: list[int],
        results_by_method: dict[str, dict[str, list[float]]],
        output_path: str | Path,
        dataset_name: str = "",
        dpi: int = 300,
    ) -> None:
        """Vẽ biểu đồ so sánh đa chỉ số: Overall Coverage, Macro Coverage, Worst-Group Coverage."""
        out_p = cls._ensure_dir(output_path)
        metrics = ["overall_coverage", "macro_coverage", "worst_group_coverage"]
        metric_titles = ["Overall Coverage", "Macro Coverage", "Worst-Group Coverage"]

        fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharey=True)

        for col_idx, (metric_key, metric_title) in enumerate(zip(metrics, metric_titles)):
            ax = axes[col_idx]
            for m_idx, (method, method_metrics) in enumerate(results_by_method.items()):
                if metric_key in method_metrics:
                    vals = method_metrics[metric_key]
                    color = cls.DEFAULT_COLORS[m_idx % len(cls.DEFAULT_COLORS)]
                    marker = cls.DEFAULT_MARKERS[m_idx % len(cls.DEFAULT_MARKERS)]
                    ax.plot(
                        budget_k_list[: len(vals)],
                        vals,
                        label=method,
                        color=color,
                        marker=marker,
                        linewidth=2.0,
                    )

            ax.set_title(metric_title, fontsize=12, fontweight="bold")
            ax.set_xlabel("Budget $k$", fontsize=10)
            ax.set_ylabel("Coverage Score" if col_idx == 0 else "", fontsize=10)
            ax.grid(True, linestyle="--", alpha=0.5)
            if col_idx == 0:
                ax.legend(fontsize=9)

        dataset_tag = f" - {dataset_name}" if dataset_name else ""
        fig.suptitle(f"Coverage Comparison across Metrics{dataset_tag}", fontsize=14, fontweight="bold", y=1.02)
        plt.tight_layout()
        plt.savefig(out_p, dpi=dpi, bbox_inches="tight")
        plt.close()
        logger.info(f"Saved multi-metric figure: {out_p}")

    @classmethod
    def plot_rare_representation(
        cls,
        budget_k_list: list[int],
        rare_rep_by_method: dict[str, list[float]],
        output_path: str | Path,
        dpi: int = 300,
    ) -> None:
        """Vẽ biểu đồ tỷ lệ nhóm hiếm có đại diện thực thể (Rare Representation Rate)."""
        cls.plot_coverage_vs_budget(
            budget_k_list=budget_k_list,
            metrics_by_method=rare_rep_by_method,
            output_path=output_path,
            title="Rare-Group Representation Rate vs Budget $k$",
            metric_name="Rare Representation Rate",
            dpi=dpi,
        )

    @classmethod
    def plot_f1_distribution(
        cls,
        f1_scores_by_method: dict[str, list[float]],
        output_path: str | Path,
        dpi: int = 300,
    ) -> None:
        """Vẽ biểu đồ phân bố F1-Score (Boxplot hoặc Violinplot) của các phân họ."""
        out_p = cls._ensure_dir(output_path)
        plt.figure(figsize=(9, 5))

        data_rows = []
        for method, scores in f1_scores_by_method.items():
            for score in scores:
                data_rows.append({"Method": method, "F1-Score": score})

        df = pd.DataFrame(data_rows)
        if not df.empty:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=matplotlib.MatplotlibDeprecationWarning)
                warnings.filterwarnings("ignore", message=".*vert.*")
                sns.boxplot(x="Method", y="F1-Score", hue="Method", data=df, palette="Set2", legend=False)
                sns.stripplot(x="Method", y="F1-Score", data=df, color="black", alpha=0.3, jitter=0.2)

        plt.title("Annotation Transfer Subfamily F1-Score Distribution", fontsize=13, fontweight="bold")
        plt.xlabel("Method", fontsize=11)
        plt.ylabel("1-NN F1-Score", fontsize=11)
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.savefig(out_p, dpi=dpi)
        plt.close()
        logger.info(f"Saved F1 distribution figure: {out_p}")

    @classmethod
    def plot_runtime_scaling(
        cls,
        sizes: list[int],
        runtimes_by_method: dict[str, list[float]],
        output_path: str | Path,
        dpi: int = 300,
    ) -> None:
        """Vẽ biểu đồ thang đo thời gian thực thi (Runtime Scalability) trên thang log-log hoặc semi-log."""
        out_p = cls._ensure_dir(output_path)
        plt.figure(figsize=(8, 5))

        for idx, (method_name, runtimes) in enumerate(runtimes_by_method.items()):
            color = cls.DEFAULT_COLORS[idx % len(cls.DEFAULT_COLORS)]
            marker = cls.DEFAULT_MARKERS[idx % len(cls.DEFAULT_MARKERS)]
            plt.plot(
                sizes[: len(runtimes)],
                runtimes,
                label=method_name,
                color=color,
                marker=marker,
                linewidth=2.0,
            )

        plt.title("Runtime Scalability Comparison (Lazy Greedy vs Standard)", fontsize=13, fontweight="bold")
        plt.xlabel("Ground Set Size $n$ (or Budget $k$)", fontsize=11)
        plt.ylabel("Runtime (seconds)", fontsize=11)
        plt.yscale("log")
        plt.grid(True, which="both", linestyle="--", alpha=0.5)
        plt.legend(fontsize=10)
        plt.tight_layout()
        plt.savefig(out_p, dpi=dpi)
        plt.close()
        logger.info(f"Saved runtime scaling figure: {out_p}")

    @classmethod
    def plot_confusion_matrix(
        cls,
        y_true: list[str],
        y_pred: list[str],
        classes: list[str] | None = None,
        output_path: str | Path = "confusion_matrix.png",
        title: str = "Confusion Matrix",
        dpi: int = 300,
    ) -> None:
        """Vẽ ma trận nhầm lẫn chuẩn hóa theo hàng."""
        out_p = cls._ensure_dir(output_path)
        if classes is None:
            classes = sorted(list(set(y_true) | set(y_pred)))

        class_to_idx = {c: i for i, c in enumerate(classes)}
        cm = np.zeros((len(classes), len(classes)), dtype=np.int64)
        for yt, yp in zip(y_true, y_pred):
            if yt in class_to_idx and yp in class_to_idx:
                cm[class_to_idx[yt], class_to_idx[yp]] += 1
        # Row-normalize to avoid zero division
        cm_norm = cm.astype("float") / np.maximum(cm.sum(axis=1)[:, np.newaxis], 1e-9)

        plt.figure(figsize=(10, 8))
        sns.heatmap(
            cm_norm,
            annot=len(classes) <= 20,
            fmt=".2f",
            cmap="Blues",
            xticklabels=classes if len(classes) <= 30 else False,
            yticklabels=classes if len(classes) <= 30 else False,
        )
        plt.title(title, fontsize=13, fontweight="bold")
        plt.xlabel("Predicted Subfamily", fontsize=11)
        plt.ylabel("True Subfamily", fontsize=11)
        plt.tight_layout()
        plt.savefig(out_p, dpi=dpi)
        plt.close()
        logger.info(f"Saved confusion matrix figure: {out_p}")

    @classmethod
    def plot_ablation_comparison(
        cls,
        results_df: pd.DataFrame,
        output_path: str | Path,
        dpi: int = 300,
    ) -> None:
        """Vẽ biểu đồ bóc tách thành phần (Ablation Study) từ bảng kết quả DataFrame."""
        out_p = cls._ensure_dir(output_path)
        plt.figure(figsize=(10, 6))

        if "weighting_scheme" in results_df.columns and "worst_group_coverage" in results_df.columns:
            sns.barplot(
                data=results_df,
                x="weighting_scheme",
                y="worst_group_coverage",
                hue="budget_k" if "budget_k" in results_df.columns else None,
                palette="viridis",
            )
            plt.title("Ablation: Impact of Weighting Scheme on Worst-Group Coverage", fontsize=13, fontweight="bold")
            plt.xlabel("Weighting Scheme", fontsize=11)
            plt.ylabel("Worst-Group Coverage", fontsize=11)
        elif not results_df.empty:
            results_df.plot(kind="bar", figsize=(10, 6))
            plt.title("Ablation Comparison", fontsize=13, fontweight="bold")

        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.savefig(out_p, dpi=dpi)
        plt.close()
        logger.info(f"Saved ablation figure: {out_p}")


# Standalone function aliases matching Doc 2 specifications
def plot_coverage_vs_budget(
    budget_k_list: list[int],
    metrics_by_method: dict[str, list[float]],
    output_path: str | Path,
    title: str = "Coverage vs Budget k",
    metric_name: str = "Worst-Group Coverage",
) -> None:
    Visualizer.plot_coverage_vs_budget(budget_k_list, metrics_by_method, output_path, title, metric_name)


def plot_coverage_comparison(
    budget_k_list: list[int],
    results_by_method: dict[str, dict[str, list[float]]],
    output_path: str | Path,
    dataset_name: str = "",
) -> None:
    Visualizer.plot_coverage_comparison(budget_k_list, results_by_method, output_path, dataset_name)


def plot_rare_representation(
    budget_k_list: list[int],
    rare_rep_by_method: dict[str, list[float]],
    output_path: str | Path,
) -> None:
    Visualizer.plot_rare_representation(budget_k_list, rare_rep_by_method, output_path)


def plot_f1_distribution(
    f1_scores_by_method: dict[str, list[float]],
    output_path: str | Path,
) -> None:
    Visualizer.plot_f1_distribution(f1_scores_by_method, output_path)


def plot_runtime_scaling(
    sizes: list[int],
    runtimes_by_method: dict[str, list[float]],
    output_path: str | Path,
) -> None:
    Visualizer.plot_runtime_scaling(sizes, runtimes_by_method, output_path)


def plot_confusion_matrix(
    y_true: list[str],
    y_pred: list[str],
    classes: list[str] | None = None,
    output_path: str | Path = "confusion_matrix.png",
    title: str = "Confusion Matrix",
) -> None:
    Visualizer.plot_confusion_matrix(y_true, y_pred, classes, output_path, title)


def plot_ablation_comparison(results_df: pd.DataFrame, output_path: str | Path) -> None:
    Visualizer.plot_ablation_comparison(results_df, output_path)

