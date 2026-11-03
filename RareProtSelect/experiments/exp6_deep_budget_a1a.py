"""Thực hiện Công đoạn 6 trong Tài liệu 1 và Module 4.6 trong Tài liệu 2:
Khảo sát Ngân Sách Sâu k in [115..380] và Phân tích Độ Bão Hòa 100% Nội Họ của 38 Phân Họ Lớn và A01.009
giữa BLASTp-Selected và ESM2-Selected (beta = 0.70) trên Tập Chuẩn Hóa Phương Án 3B
Siêu họ Peptidase A1 (MEROPS_A1A_curated: 4,120 chuỗi, 115 phân họ, họ lớn nhất A01.009 = 329 chuỗi).
"""

from __future__ import annotations

import argparse
import logging
import sys
import tempfile
import time
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from tqdm import tqdm

# Đảm bảo UTF-8 trên Windows console
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Thêm thư mục RareProtSelect vào sys.path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from src.data.dataset_loader import DatasetLoader
from src.data.fasta_parser import ProteinRecord
from src.selection.pruned_greedy import compute_subfamily_weights, run_pruned_greedy_1000_shuffles
from src.similarity.blast_similarity import BLASTSimilarityMatrix

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("exp6_deep_budget_a1a")

EXPECTED_COLUMNS: list[str] = [
    "selection_space",
    "alpha",
    "budget_k",
    "subfamilies_represented_count",
    "subfamily_repr_rate_pct",
    "redundant_slots_count",
    "subfamily_redundancy_pct",
    "dominant_a01_009_seats",
    "dominant_a01_009_share_pct",
    "dominant_a01_009_blast_sens_pct",
    "dominant_a01_009_esm_cov_pct",
    "large_subfamilies_mean_blast_sens_pct",
    "large_subfamilies_mean_esm_cov_pct",
    "medium_subfamilies_mean_blast_sens_pct",
    "rare_subfamilies_mean_blast_sens_pct",
    "full_saturation_count_blast",
    "full_saturation_count_esm",
    "overall_sensitivity_blast_pct",
]


def _compute_seat_allocation_metrics(
    selected_ids: list[str],
    id_to_family: dict[str, str],
    total_subfamilies: int,
    dominant_subfamily_id: str,
    k_val: int,
) -> dict[str, int | float]:
    """Tính toán các chỉ số phân bổ ghế và độ dư thừa phân họ trong tập đại diện."""
    family_list = [id_to_family[sid] for sid in selected_ids if sid in id_to_family]
    family_counts = Counter(family_list)
    represented_subfamilies = set(family_counts.keys())

    subfamilies_represented_count = len(represented_subfamilies)
    subfamily_repr_rate_pct = round((subfamilies_represented_count / total_subfamilies) * 100.0, 2)
    redundant_slots_count = sum(c - 1 for c in family_counts.values() if c >= 2)

    if subfamilies_represented_count + redundant_slots_count != k_val:
        raise AssertionError(
            f"Vi phạm bất biến bảo toàn ghế tại k={k_val}: "
            f"{subfamilies_represented_count} + {redundant_slots_count} != {k_val}"
        )
    subfamily_redundancy_pct = round((redundant_slots_count / k_val) * 100.0, 2)
    dominant_a01_009_seats = int(family_counts.get(dominant_subfamily_id, 0))
    dominant_a01_009_share_pct = round((dominant_a01_009_seats / k_val) * 100.0, 2)

    return {
        "subfamilies_represented_count": subfamilies_represented_count,
        "subfamily_repr_rate_pct": subfamily_repr_rate_pct,
        "redundant_slots_count": redundant_slots_count,
        "subfamily_redundancy_pct": subfamily_redundancy_pct,
        "dominant_a01_009_seats": dominant_a01_009_seats,
        "dominant_a01_009_share_pct": dominant_a01_009_share_pct,
    }


def _compute_blast_within_subfamily_metrics(
    selected_set: set[str],
    hit_pairs: set[tuple[str, str]],
    id_to_family: dict[str, str],
    family_to_ids: dict[str, list[str]],
    large_subfamilies_set: set[str],
    medium_subfamilies_set: set[str],
    rare_subfamilies_set: set[str],
    dominant_subfamily_id: str,
    total_cleaned: int,
) -> dict[str, float | int]:
    """Tính toán các chỉ số độ nhạy Live BLASTp nội phân họ và bão hòa 100%."""
    covered_blast_ids: set[str] = set(selected_set)
    for q_id, s_id in hit_pairs:
        if q_id in selected_set and s_id in id_to_family:
            if id_to_family.get(q_id) == id_to_family.get(s_id):
                covered_blast_ids.add(s_id)

    overall_sens = round((len(covered_blast_ids) / total_cleaned) * 100.0, 2) if total_cleaned > 0 else 0.0
    fam_sens: dict[str, float] = {}
    full_sat_cnt = 0

    for fam, f_ids in family_to_ids.items():
        if len(f_ids) == 0:
            fam_sens[fam] = 0.0
            continue
        covered_cnt = sum(1 for sid in f_ids if sid in covered_blast_ids)
        sens = (covered_cnt / len(f_ids)) * 100.0
        fam_sens[fam] = sens
        if covered_cnt == len(f_ids):
            full_sat_cnt += 1

    large_vals = [fam_sens[f] for f in large_subfamilies_set if f in fam_sens]
    med_vals = [fam_sens[f] for f in medium_subfamilies_set if f in fam_sens]
    rare_vals = [fam_sens[f] for f in rare_subfamilies_set if f in fam_sens]

    return {
        "dominant_a01_009_blast_sens_pct": round(fam_sens.get(dominant_subfamily_id, 0.0), 2),
        "large_subfamilies_mean_blast_sens_pct": round(float(np.mean(large_vals)), 2) if large_vals else 0.0,
        "medium_subfamilies_mean_blast_sens_pct": round(float(np.mean(med_vals)), 2) if med_vals else 0.0,
        "rare_subfamilies_mean_blast_sens_pct": round(float(np.mean(rare_vals)), 2) if rare_vals else 0.0,
        "full_saturation_count_blast": full_sat_cnt,
        "overall_sensitivity_blast_pct": overall_sens,
    }


def _compute_esm_coverage_metrics(
    selected_set: set[str],
    sim_matrix_esm: np.ndarray,
    seq_id_to_idx: dict[str, int],
    family_to_ids: dict[str, list[str]],
    large_subfamilies_set: set[str],
    dominant_subfamily_id: str,
    esm_sat_threshold: float = 99.5,
) -> dict[str, float | int]:
    """Tính toán các chỉ số độ bao phủ ngữ nghĩa ESM-2 nội phân họ và bão hòa."""
    fam_esm_cov: dict[str, float] = {}
    full_sat_esm_cnt = 0

    for fam, f_ids in family_to_ids.items():
        if len(f_ids) == 0:
            fam_esm_cov[fam] = 0.0
            continue
        f_indices = [seq_id_to_idx[sid] for sid in f_ids if sid in seq_id_to_idx]
        rep_indices = [seq_id_to_idx[sid] for sid in f_ids if sid in selected_set and sid in seq_id_to_idx]
        if len(rep_indices) == 0:
            fam_esm_cov[fam] = 0.0
        else:
            sub_sim = sim_matrix_esm[np.ix_(f_indices, rep_indices)]
            cov_mean = float(np.mean(np.max(sub_sim, axis=1))) * 100.0
            fam_esm_cov[fam] = cov_mean
            if cov_mean >= esm_sat_threshold:
                full_sat_esm_cnt += 1

    large_esm_vals = [fam_esm_cov[fam] for fam in large_subfamilies_set if fam in fam_esm_cov]
    return {
        "dominant_a01_009_esm_cov_pct": round(fam_esm_cov.get(dominant_subfamily_id, 0.0), 2),
        "large_subfamilies_mean_esm_cov_pct": round(float(np.mean(large_esm_vals)), 2) if large_esm_vals else 0.0,
        "full_saturation_count_esm": full_sat_esm_cnt,
    }


def evaluate_deep_budget_metrics_for_k(
    selected_ids: list[str],
    id_to_family: dict[str, str],
    family_to_ids: dict[str, list[str]],
    large_subfamilies_set: set[str],
    medium_subfamilies_set: set[str],
    rare_subfamilies_set: set[str],
    dominant_subfamily_id: str,
    hit_pairs: set[tuple[str, str]],
    sim_matrix_esm: np.ndarray,
    seq_id_to_idx: dict[str, int],
    k_val: int,
    selection_space: str,
    alpha: float,
    esm_sat_threshold: float = 99.5,
) -> dict[str, int | float | str]:
    """Hàm điều phối tính toán 18 chỉ số đo đạc phân tầng cho tập k đại diện."""
    total_subfamilies = len(family_to_ids)
    selected_set = set(selected_ids)
    total_cleaned = sum(len(ids) for ids in family_to_ids.values())

    seat_m = _compute_seat_allocation_metrics(
        selected_ids, id_to_family, total_subfamilies, dominant_subfamily_id, k_val
    )
    blast_m = _compute_blast_within_subfamily_metrics(
        selected_set, hit_pairs, id_to_family, family_to_ids,
        large_subfamilies_set, medium_subfamilies_set, rare_subfamilies_set,
        dominant_subfamily_id, total_cleaned,
    )
    esm_m = _compute_esm_coverage_metrics(
        selected_set, sim_matrix_esm, seq_id_to_idx, family_to_ids,
        large_subfamilies_set, dominant_subfamily_id, esm_sat_threshold,
    )

    result: dict[str, int | float | str] = {
        "selection_space": selection_space,
        "alpha": float(alpha),
        "budget_k": int(k_val),
    }
    result.update(seat_m)
    result.update(blast_m)
    result.update(esm_m)
    return result


def _plot_dominant_a01_009_saturation(
    df: pd.DataFrame,
    figures_dir: Path,
    alphas: list[float],
    dominant_subfamily_id: str,
    palette: dict[float, str],
) -> list[Path]:
    """Vẽ Biểu đồ 1: Bão hòa phân họ thống trị A01.009 (Độ nhạy & Số ghế)."""
    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(15.0, 6.0))
    for a_val in alphas:
        col = palette.get(a_val, "#1f77b4")
        df_esm = df[(df["selection_space"] == "ESM-2") & (df["alpha"] == a_val)].sort_values("budget_k")
        df_bls = df[(df["selection_space"] == "BLASTp") & (df["alpha"] == a_val)].sort_values("budget_k")
        ax_l.plot(df_esm["budget_k"], df_esm["dominant_a01_009_blast_sens_pct"], marker="o", color=col, linewidth=2.2, label=f"ESM-2 ($\\alpha={a_val}$)")
        ax_l.plot(df_bls["budget_k"], df_bls["dominant_a01_009_blast_sens_pct"], marker="s", color=col, linestyle="--", linewidth=1.8, alpha=0.85, label=f"BLASTp ($\\alpha={a_val}$)")
        ax_r.plot(df_esm["budget_k"], df_esm["dominant_a01_009_seats"], marker="o", color=col, linewidth=2.2, label=f"ESM-2 ($\\alpha={a_val}$)")
        ax_r.plot(df_bls["budget_k"], df_bls["dominant_a01_009_seats"], marker="s", color=col, linestyle="--", linewidth=1.8, alpha=0.85, label=f"BLASTp ($\\alpha={a_val}$)")

    ax_l.set_title(f"A. Within-Subfamily Live BLASTp Sensitivity of Dominant {dominant_subfamily_id} (%)", fontsize=11.5, fontweight="bold")
    ax_l.set_xlabel("Extended Representative Budget $k$ (115 to 380)", fontsize=11, fontweight="bold")
    ax_l.set_ylabel("Within-Subfamily Sensitivity (%)", fontsize=11, fontweight="bold")
    ax_l.set_ylim(60.0, 102.0)
    ax_l.axhline(100.0, color="#d62728", linestyle=":", linewidth=1.5, alpha=0.8, label="100% Full Saturation")
    ax_l.grid(True, linestyle="--", alpha=0.5)
    ax_l.legend(loc="lower right", fontsize=8.5, ncol=2)

    ax_r.set_title(f"B. Cumulative Representative Seats of Dominant {dominant_subfamily_id} ($n=329$)", fontsize=11.5, fontweight="bold")
    ax_r.set_xlabel("Extended Representative Budget $k$ (115 to 380)", fontsize=11, fontweight="bold")
    ax_r.set_ylabel("Seats Allocated to A01.009 in $S_k$", fontsize=11, fontweight="bold")
    ax_r.grid(True, linestyle="--", alpha=0.5)
    ax_r.legend(loc="upper left", fontsize=8.5, ncol=2)

    plt.suptitle(f"Branch 6: Deep Budget Saturation of Dominant Subfamily {dominant_subfamily_id} across $k \\in [115..380]$", fontsize=13, fontweight="bold", y=0.99)
    plt.tight_layout()
    p_png = figures_dir / "exp6_dominant_a01_009_saturation_vs_k.png"
    p_svg = figures_dir / "exp6_dominant_a01_009_saturation_vs_k.svg"
    fig.savefig(p_png, dpi=300, bbox_inches="tight")
    fig.savefig(p_svg, bbox_inches="tight")
    plt.close(fig)
    return [p_png, p_svg]


def _plot_stratified_coverage(
    df: pd.DataFrame,
    figures_dir: Path,
    alphas: list[float],
    palette: dict[float, str],
) -> list[Path]:
    """Vẽ Biểu đồ 2: So sánh độ phủ nội họ phân tầng giữa 3 khối quy mô."""
    fig, axes = plt.subplots(1, 3, figsize=(18.0, 5.5), sharey=True)
    strat_panels = [
        (axes[0], "large_subfamilies_mean_blast_sens_pct", "A. 38 Large Subfamilies (n_g >= 20)"),
        (axes[1], "medium_subfamilies_mean_blast_sens_pct", "B. 32 Medium Subfamilies (6 <= n_g <= 19)"),
        (axes[2], "rare_subfamilies_mean_blast_sens_pct", "C. 45 Rare Subfamilies (n_g <= 5)"),
    ]
    for ax_s, metric_col, title_s in strat_panels:
        for a_val in alphas:
            col = palette.get(a_val, "#1f77b4")
            df_esm = df[(df["selection_space"] == "ESM-2") & (df["alpha"] == a_val)].sort_values("budget_k")
            df_bls = df[(df["selection_space"] == "BLASTp") & (df["alpha"] == a_val)].sort_values("budget_k")
            ax_s.plot(df_esm["budget_k"], df_esm[metric_col], marker="o", color=col, linewidth=2.0, label=f"ESM-2 ($\\alpha={a_val}$)")
            ax_s.plot(df_bls["budget_k"], df_bls[metric_col], marker="s", color=col, linestyle="--", linewidth=1.8, alpha=0.85, label=f"BLASTp ($\\alpha={a_val}$)")
        ax_s.set_title(title_s, fontsize=11.5, fontweight="bold")
        ax_s.set_xlabel("Representative Budget $k$ (115 to 380)", fontsize=11, fontweight="bold")
        ax_s.set_ylabel("Mean Within-Subfamily Sensitivity (%)", fontsize=11, fontweight="bold")
        ax_s.set_ylim(40.0, 103.0)
        ax_s.grid(True, linestyle="--", alpha=0.5)
        ax_s.legend(loc="lower right", fontsize=8.2, ncol=2)

    plt.suptitle("Branch 6: Stratified Subfamily Sensitivity vs. Deep Budget $k \\in [115..380]$ across 3 Size Regimes", fontsize=13, fontweight="bold", y=1.01)
    plt.tight_layout()
    p_png = figures_dir / "exp6_stratified_coverage_vs_k.png"
    p_svg = figures_dir / "exp6_stratified_coverage_vs_k.svg"
    fig.savefig(p_png, dpi=300, bbox_inches="tight")
    fig.savefig(p_svg, bbox_inches="tight")
    plt.close(fig)
    return [p_png, p_svg]


def _plot_full_saturation_count(
    df: pd.DataFrame,
    figures_dir: Path,
    alphas: list[float],
    palette: dict[float, str],
) -> list[Path]:
    """Vẽ Biểu đồ 3: Tốc độ bão hòa 100% của toàn bộ 115 phân họ."""
    fig, ax = plt.subplots(figsize=(10.0, 6.0))
    for a_val in alphas:
        col = palette.get(a_val, "#1f77b4")
        df_esm = df[(df["selection_space"] == "ESM-2") & (df["alpha"] == a_val)].sort_values("budget_k")
        df_bls = df[(df["selection_space"] == "BLASTp") & (df["alpha"] == a_val)].sort_values("budget_k")
        ax.plot(df_esm["budget_k"], df_esm["full_saturation_count_blast"], marker="o", color=col, linewidth=2.2, label=f"ESM-2 Selected ($\\alpha={a_val}$)")
        ax.plot(df_bls["budget_k"], df_bls["full_saturation_count_blast"], marker="s", color=col, linestyle="--", linewidth=1.8, alpha=0.85, label=f"BLASTp Selected ($\\alpha={a_val}$)")

    ax.axhline(115, color="#d62728", linestyle=":", linewidth=1.5, alpha=0.8, label="115 Subfamilies (Total Ceiling)")
    ax.set_title("Branch 6: Count of Subfamilies Achieving Exactly 100.0% Within-Subfamily Live BLASTp Sensitivity", fontsize=12, fontweight="bold", pad=10)
    ax.set_xlabel("Extended Representative Budget $k$ (115 to 380)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Count of Fully Saturated Subfamilies (/115)", fontsize=11, fontweight="bold")
    ax.set_ylim(20, 120)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="lower right", fontsize=9, ncol=2)

    plt.tight_layout()
    p_png = figures_dir / "exp6_full_saturation_count_vs_k.png"
    p_svg = figures_dir / "exp6_full_saturation_count_vs_k.svg"
    fig.savefig(p_png, dpi=300, bbox_inches="tight")
    fig.savefig(p_svg, bbox_inches="tight")
    plt.close(fig)
    return [p_png, p_svg]


def plot_exp6_figures(
    df: pd.DataFrame,
    figures_dir: Path,
    alphas: list[float],
    dominant_subfamily_id: str = "A01.009",
) -> list[Path]:
    """Hàm điều phối vẽ 3 biểu đồ chuyên sâu cho Nhánh 6."""
    palette = {0.0: "#7f7f7f", 0.5: "#ff7f0e", 1.0: "#2ca02c"}
    created_plots: list[Path] = []
    created_plots.extend(_plot_dominant_a01_009_saturation(df, figures_dir, alphas, dominant_subfamily_id, palette))
    created_plots.extend(_plot_stratified_coverage(df, figures_dir, alphas, palette))
    created_plots.extend(_plot_full_saturation_count(df, figures_dir, alphas, palette))
    return created_plots


def _setup_exp6_environment(config_path: str | Path) -> tuple[dict[str, object], Path, Path, Path, Path, Path]:
    """Nạp cấu hình và thiết lập các thư mục làm việc."""
    cfg_file = Path(config_path)
    if not cfg_file.exists():
        cfg_file = parent_dir / config_path
    if not cfg_file.exists():
        raise FileNotFoundError(f"Không tìm thấy tệp cấu hình: {config_path}")

    with open(cfg_file, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    outputs_dir = parent_dir / str(cfg.get("output_dir", "outputs"))
    tables_dir = outputs_dir / "tables"
    figures_dir = outputs_dir / "figures"
    cache_dir = outputs_dir / "similarity_cache"
    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    return cfg, cfg_file, outputs_dir, tables_dir, figures_dir, cache_dir


def _build_or_load_similarity_and_db(
    cache_dir: Path,
    dataset_name: str,
    records: list[ProteinRecord],
    blast_bin_path: Path,
) -> tuple[np.ndarray, np.ndarray, BLASTSimilarityMatrix, Path]:
    """Nạp ma trận tương đồng đã lưu đệm và chuẩn bị Live BLAST DB."""
    blast_mat_path = cache_dir / f"{dataset_name}_blastp_sim_matrix.npz"
    esm_mat_path = cache_dir / f"{dataset_name}_esm2_mc_cosine_sim_matrix.npz"

    blast_data = np.load(blast_mat_path)
    blast_sim = blast_data["sim_matrix"] if "sim_matrix" in blast_data else blast_data["similarity_matrix"]
    esm_data = np.load(esm_mat_path)
    esm_sim = esm_data["sim_matrix"] if "sim_matrix" in esm_data else esm_data["similarity_matrix"]

    blast_calc = BLASTSimilarityMatrix(blastp_bin_path=blast_bin_path, cache_dir=cache_dir)
    cleaned_fasta_path = cache_dir / f"{dataset_name}_cleaned_qc.fasta"
    if not cleaned_fasta_path.exists():
        SeqIO.write([SeqRecord(Seq(r.sequence), id=r.id, description=r.header) for r in records], cleaned_fasta_path, "fasta")
    db_prefix = blast_calc.build_blast_db(fasta_path=cleaned_fasta_path, db_prefix=cache_dir / f"{dataset_name}_live_db")
    return blast_sim, esm_sim, blast_calc, db_prefix


def _run_single_alpha_evaluation(
    space_name: str,
    cur_sim: np.ndarray,
    alpha: float,
    seq_ids: list[str],
    id_to_family: dict[str, str],
    family_to_ids: dict[str, list[str]],
    id_to_record: dict[str, ProteinRecord],
    large_subfamilies_set: set[str],
    medium_subfamilies_set: set[str],
    rare_subfamilies_set: set[str],
    dominant_subfamily_id: str,
    esm_sim: np.ndarray,
    seq_id_to_idx: dict[str, int],
    blast_calc: BLASTSimilarityMatrix,
    db_prefix: Path,
    tmpdir: Path,
    cache_dir: Path,
    dataset_name: str,
    budget_per_shuffle: int,
    budget_k_list: list[int],
    num_shuffles: int,
    prune_threshold: float,
    seed: int,
    evalue_th: float,
    esm_sat_th: float,
) -> list[dict[str, int | float | str]]:
    """Tối ưu hóa và đánh giá cho một tổ hợp không gian và alpha trên các mốc k."""
    alpha_str = f"{alpha:.2f}"
    prefix_tag = "esm2" if space_name == "ESM-2" else "blastp"
    cache_file = cache_dir / f"{dataset_name}_{prefix_tag}_deep_shuffles_alpha_{alpha_str}_b{budget_per_shuffle}.npz"
    weights = compute_subfamily_weights(seq_ids=seq_ids, id_to_family=id_to_family, alpha=alpha)

    consensus_ids, _ = run_pruned_greedy_1000_shuffles(
        sim_matrix=cur_sim, seq_ids=seq_ids, prune_threshold=prune_threshold,
        num_shuffles=num_shuffles, sample_weights=weights, seed=seed,
        budget_per_shuffle=budget_per_shuffle, cache_path=cache_file,
        desc_label=f"{space_name} a={alpha_str} (b={budget_per_shuffle})", show_progress=True,
    )
    top_ids = [sid for sid in consensus_ids[:budget_per_shuffle] if sid in id_to_record]
    query_fasta = tmpdir / f"query_{space_name}_{alpha_str}_top{budget_per_shuffle}.fasta"
    SeqIO.write([SeqRecord(Seq(id_to_record[sid].sequence), id=sid, description=id_to_record[sid].header) for sid in top_ids], query_fasta, "fasta")
    hit_pairs = blast_calc.retrieve_blast_hit_pairs(query_fasta=query_fasta, db_prefix=db_prefix, evalue=evalue_th, max_target_seqs=999999, num_threads=24)

    rows: list[dict[str, int | float | str]] = []
    for k_val in budget_k_list:
        sub_ids = consensus_ids[:k_val]
        metrics = evaluate_deep_budget_metrics_for_k(
            sub_ids, id_to_family, family_to_ids, large_subfamilies_set,
            medium_subfamilies_set, rare_subfamilies_set, dominant_subfamily_id,
            hit_pairs, esm_sim, seq_id_to_idx, k_val, space_name, alpha, esm_sat_th,
        )
        rows.append(metrics)
    return rows


def _log_strategic_milestones(df_results: pd.DataFrame) -> None:
    """In bảng tóm tắt đối chiếu các mốc chiến lược k=115 và k=380."""
    logger.info("=" * 115)
    logger.info("BRANCH 6 STRATEGIC MILESTONE SUMMARY (k=115 Baseline vs k=380 Deep Saturation)")
    logger.info("-" * 115)
    logger.info("%-7s | %-5s | %-4s | %-13s | %-13s | %-13s | %-14s | %-14s", "Space", "Alpha", "k", "A01.009 Seats", "A01.009 Sens", "A01.009 Cov", "Large Sens(38)", "100% Sat Count")
    logger.info("-" * 115)
    df_sub = df_results[df_results["budget_k"].isin([115, 380])].sort_values(["selection_space", "alpha", "budget_k"])
    for _, r in df_sub.iterrows():
        logger.info(
            "%-7s | %5.1f | %4d | %3d (%5.2f%%) | %6.2f%%      | %6.2f%%      | %6.2f%%       | %3d / 115",
            str(r["selection_space"]), float(r["alpha"]), int(r["budget_k"]),
            int(r["dominant_a01_009_seats"]), float(r["dominant_a01_009_share_pct"]),
            float(r["dominant_a01_009_blast_sens_pct"]), float(r["dominant_a01_009_esm_cov_pct"]),
            float(r["large_subfamilies_mean_blast_sens_pct"]), int(r["full_saturation_count_blast"]),
        )
    logger.info("=" * 115)


def run_deep_budget_experiment(
    config_path: str | Path = "configs/config_exp6_deep_budget_a1a.yaml",
) -> tuple[pd.DataFrame, list[Path]]:
    """Thực thi toàn bộ quy trình Nhánh 6."""
    logger.info("=" * 115)
    logger.info("BRANCH 6: DEEP BUDGET & DOMINANT SUBFAMILY SATURATION ANALYSIS ON CURATED MEROPS A1A")
    logger.info("=" * 115)

    cfg, cfg_file, outputs_dir, tables_dir, figures_dir, cache_dir = _setup_exp6_environment(config_path)
    dataset_name = str(cfg.get("dataset_name", "MEROPS_A1A_curated"))
    fasta_path = (parent_dir / str(cfg.get("fasta_path", "../baseline_repo/MEROPS_A1A.fasta"))).resolve()
    blast_bin_path = (parent_dir / str(cfg.get("blast_bin_path", "tools/blast/bin/blastp.exe"))).resolve()

    bundle = DatasetLoader.load_and_preprocess_dataset(cfg_file, override_fasta=str(fasta_path), override_dataset_name=dataset_name)
    records = bundle.cleaned_records
    seq_ids = [r.id for r in records]
    seq_id_to_idx = {sid: i for i, sid in enumerate(seq_ids)}
    id_to_record = {r.id: r for r in records}
    id_to_family = bundle.label_map

    family_to_ids: dict[str, list[str]] = defaultdict(list)
    for sid in seq_ids:
        family_to_ids[id_to_family.get(sid, "UNKNOWN")].append(sid)

    strat = cfg.get("stratification", {})
    dom_id = str(strat.get("dominant_subfamily_id", "A01.009"))
    large_set = {fam for fam, ids in family_to_ids.items() if len(ids) >= int(strat.get("large_threshold", 20))}
    med_set = {fam for fam, ids in family_to_ids.items() if int(strat.get("medium_threshold", 6)) <= len(ids) < int(strat.get("large_threshold", 20))}
    rare_set = {fam for fam, ids in family_to_ids.items() if len(ids) <= int(strat.get("rare_threshold", 5))}

    blast_sim, esm_sim, blast_calc, db_prefix = _build_or_load_similarity_and_db(cache_dir, dataset_name, records, blast_bin_path)

    all_rows: list[dict[str, int | float | str]] = []
    with tempfile.TemporaryDirectory() as tmpdir_str:
        tmpdir = Path(tmpdir_str)
        spaces = [s["name"] for s in cfg.get("similarity_spaces", [{"name": "BLASTp"}, {"name": "ESM-2"}])]
        alphas = [float(a) for a in cfg.get("alphas", [0.0, 0.5, 1.0])]
        for space_name in spaces:
            cur_sim = blast_sim if space_name == "BLASTp" else esm_sim
            for alpha in alphas:
                rows = _run_single_alpha_evaluation(
                    space_name, cur_sim, alpha, seq_ids, id_to_family, family_to_ids, id_to_record,
                    large_set, med_set, rare_set, dom_id, esm_sim, seq_id_to_idx, blast_calc, db_prefix, tmpdir,
                    cache_dir, dataset_name, int(cfg.get("budget_per_shuffle", 380)),
                    [int(k) for k in cfg.get("budget_k_list", [115, 150, 200, 270, 340, 380])],
                    int(cfg.get("num_shuffles", 1000)), float(cfg.get("prune_threshold", 0.90)),
                    int(cfg.get("seed", 42)), float(cfg.get("evaluation", {}).get("evalue_threshold", 1.0e-7)),
                    float(cfg.get("evaluation", {}).get("esm_saturation_threshold", 99.5)),
                )
                all_rows.extend(rows)

    df_results = pd.DataFrame(all_rows, columns=EXPECTED_COLUMNS)
    csv_out = tables_dir / "exp6_deep_budget_a1a.csv"
    df_results.to_csv(csv_out, index=False, encoding="utf-8-sig")
    _log_strategic_milestones(df_results)
    created_plots = plot_exp6_figures(df_results, figures_dir, alphas, dom_id)
    return df_results, created_plots


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Exp 6: Deep Budget & Dominant Subfamily Saturation Analysis on Curated Peptidase A1"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="configs/config_exp6_deep_budget_a1a.yaml",
        help="Path to YAML configuration file.",
    )
    args = parser.parse_args()
    run_deep_budget_experiment(config_path=args.config)


if __name__ == "__main__":
    main()
