"""Thực hiện Công đoạn 4.1, 4.2, 4.3 trong Tài liệu 1 và Module 4.8 trong Tài liệu 2:
Kiểm tra chéo hai chiều (Full 2x2 Cross-Space Within-Subfamily Evaluation) giữa Tập đại diện chọn bởi BLASTp (Nhánh 2)
và Tập đại diện chọn bởi ESM-2 Mean-Centered Cosine (Nhánh 3) trên Tập Dữ Liệu Chuẩn Hóa Phương Án 3B
(4,120 Chuỗi, 115 Phân Họ, 45 Họ Hiếm <= 5 Chuỗi) qua 3 Mốc Alpha và 20 Mốc k đến 115.

Kịch bản thực hiện các nhiệm vụ khoa học cốt lõi:
1. Tuân thủ triệt để nguyên tắc Ceteris Paribus (/controlled-scientific-experiment):
   - Giữ nguyên 100% tập dữ liệu chuẩn hóa Phương án 3B MEROPS_A1A_curated (4,120 chuỗi sạch, 115 phân họ, 45 phân họ hiếm <= 5 chuỗi).
   - Giữ nguyên 100% hai bộ danh sách đại diện đồng thuận 1,000 lần xáo trộn (budget_per_shuffle = 115) đã lưu đệm từ Nhánh 2 (BLASTp) và Nhánh 3 (ESM-2, beta = 0.70).
   - Đặt cả hai bộ đại diện lên cùng hai mặt trận thước đo Truy vấn ngược nội phân họ (S_k cap V_g -> V_g) để khử hoàn toàn nhiễu biến giữa không gian chọn và không gian đánh giá.
2. Mặt trận 1 — Đánh giá bằng bộ 5 chỉ số Live BLASTp Sensitivity (%) nội phân họ (E <= 1e-7):
   - overall_sensitivity_blast_pct
   - worst_group_sensitivity_blast_pct
   - rare_sensitivity_blast_pct (45 nhóm hiếm <= 5 chuỗi)
   - macro_sensitivity_blast_pct (115 nhóm bình đẳng)
   - zero_cov_subfamilies_count (số nhóm có độ nhạy 0.0% trên 115 nhóm)
3. Mặt trận 2 — Đánh giá bằng bộ 4 chỉ số liên tục Coverage ESM (%) nội phân họ trên S_ESM^(beta=0.70):
   - overall_coverage_esm_pct
   - worst_group_coverage_esm_pct
   - rare_coverage_esm_pct (45 nhóm hiếm <= 5 chuỗi)
   - macro_coverage_esm_pct (115 nhóm bình đẳng)
4. Kiểm định tự động (Sanity Check) 2 ô đường chéo khớp 100.00% với exp2_rare_weighted_a1a.csv và exp3_esm_coverage_a1a.csv (60/60 dòng).
5. Xuất duy nhất tệp CSV hợp nhất: outputs/tables/exp4_cross_eval_a1a.csv (120 hàng = 2 selection_space x 3 alpha x 20 k).
6. Xuất hệ thống 3 biểu đồ đối đầu trực diện (PNG và SVG):
   - outputs/figures/exp4_blast_eval_comparison_vs_k.png & .svg
   - outputs/figures/exp4_esm_eval_comparison_vs_k.png & .svg
   - outputs/figures/exp4_cross_space_summary_k11_k76.png & .svg
"""

from __future__ import annotations

import argparse
import logging
import sys
import tempfile
from collections import defaultdict
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
from src.similarity.blast_similarity import BLASTSimilarityMatrix
from src.similarity.dense_similarity import ESM2SimilarityMatrix

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("exp4_cross_eval_a1a")


def load_cached_consensus_ids(cache_file: Path, expected_budget: int = 115) -> list[str]:
    """Nạp danh sách đại diện đồng thuận 1,000 lần xáo trộn từ tệp cache .npz của Nhánh 2 hoặc Nhánh 3."""
    if not cache_file.exists():
        raise FileNotFoundError(
            f"Không tìm thấy tệp cache đồng thuận: {cache_file}. "
            "Vui lòng đảm bảo Nhánh 2 và Nhánh 3 đã được chạy trước đó."
        )

    cached_data = np.load(cache_file, allow_pickle=True)
    cached_budget = 15
    if "metadata" in cached_data:
        meta_raw: object = cached_data["metadata"].item()
        if isinstance(meta_raw, dict) and "budget_per_shuffle" in meta_raw:
            cached_budget = int(meta_raw["budget_per_shuffle"])

    if cached_budget < expected_budget:
        raise ValueError(
            f"Tệp cache {cache_file.name} có budget_per_shuffle={cached_budget} < {expected_budget} yêu cầu!"
        )

    consensus_ids = [str(x) for x in cached_data["consensus_ids"]]
    logger.info(
        "Loaded %d consensus IDs from %s (budget_per_shuffle=%d)",
        len(consensus_ids),
        cache_file.name,
        cached_budget,
    )
    return consensus_ids


def evaluate_rare_aware_representatives(
    selected_ids: list[str],
    id_to_record: dict[str, ProteinRecord],
    seq_ids: list[str],
    id_to_family: dict[str, str],
    family_to_ids: dict[str, list[str]],
    rare_subfamilies: list[str],
    blast_calc: BLASTSimilarityMatrix,
    db_prefix: Path,
    tmpdir: Path,
    k_val: int,
    live_evalue: float = 1e-7,
    live_max_targets: int = 999999,
    live_threads: int = 24,
    precomputed_hit_pairs: set[tuple[str, str]] | None = None,
) -> dict[str, float | int]:
    """Đo đạc Live BLASTp thực tế (E <= 1e-7) theo cơ chế Truy vấn ngược nội phân họ (S_k cap V_g -> V_g)
    và tính toán 5 chỉ số phân rã nhóm hiếm cho tập k đại diện.
    """
    valid_seq_set: set[str] = set(seq_ids)
    selected_clean_ids: list[str] = [sid for sid in selected_ids if sid in valid_seq_set]
    selected_set: set[str] = set(selected_clean_ids)
    total_cleaned: int = len(seq_ids)

    if len(selected_clean_ids) == 0 or total_cleaned == 0:
        return {
            "budget_k": int(k_val),
            "num_selected": 0,
            "overall_sensitivity_blast_pct": 0.0,
            "worst_group_sensitivity_blast_pct": 0.0,
            "rare_sensitivity_blast_pct": 0.0,
            "macro_sensitivity_blast_pct": 0.0,
            "zero_cov_subfamilies_count": len(family_to_ids),
            "retrieved_hits_count": 0,
            "total_cleaned_sequences": total_cleaned,
        }

    if precomputed_hit_pairs is not None:
        hit_pairs = precomputed_hit_pairs
    else:
        selected_records = [id_to_record[sid] for sid in selected_clean_ids if sid in id_to_record]
        query_fasta = tmpdir / f"query_k{k_val}.fasta"
        SeqIO.write(
            [SeqRecord(Seq(r.sequence), id=r.id, description=r.header) for r in selected_records],
            query_fasta,
            "fasta",
        )
        hit_pairs = blast_calc.retrieve_blast_hit_pairs(
            query_fasta=query_fasta,
            db_prefix=db_prefix,
            evalue=live_evalue,
            max_target_seqs=live_max_targets,
            num_threads=live_threads,
        )

    covered_clean_ids: set[str] = set(selected_set)
    for q_id, s_id in hit_pairs:
        if q_id in selected_set and s_id in valid_seq_set:
            if id_to_family.get(q_id) == id_to_family.get(s_id):
                covered_clean_ids.add(s_id)

    # 1. Overall Within-Subfamily Sensitivity BLAST (%)
    overall_sens_pct = round((len(covered_clean_ids) / total_cleaned) * 100.0, 2) if total_cleaned > 0 else 0.0

    # 2. Tính độ nhạy nội phân họ cho từng phân họ trong số 115 phân họ
    fam_sensitivities: dict[str, float] = {}
    zero_cov_count = 0

    for fam, f_ids in family_to_ids.items():
        if len(f_ids) == 0:
            fam_sensitivities[fam] = 0.0
            continue
        covered_in_fam = sum(1 for sid in f_ids if sid in covered_clean_ids)
        sens = (covered_in_fam / len(f_ids)) * 100.0
        fam_sensitivities[fam] = sens
        if covered_in_fam == 0:
            zero_cov_count += 1

    # 3. Worst-Group Sensitivity BLAST (%)
    all_sens_values = list(fam_sensitivities.values())
    worst_group_sens_pct = round(float(np.min(all_sens_values)), 2) if all_sens_values else 0.0

    # 4. Rare Sensitivity BLAST (%) (trên 45 nhóm hiếm <= 5 chuỗi)
    rare_sens_values = [fam_sensitivities[fam] for fam in rare_subfamilies if fam in fam_sensitivities]
    rare_sens_pct = round(float(np.mean(rare_sens_values)), 2) if rare_sens_values else 0.0

    # 5. Macro-Average Sensitivity BLAST (%) (115 nhóm bình đẳng)
    macro_sens_pct = round(float(np.mean(all_sens_values)), 2) if all_sens_values else 0.0

    return {
        "budget_k": int(k_val),
        "num_selected": len(selected_clean_ids),
        "overall_sensitivity_blast_pct": overall_sens_pct,
        "worst_group_sensitivity_blast_pct": worst_group_sens_pct,
        "rare_sensitivity_blast_pct": rare_sens_pct,
        "macro_sensitivity_blast_pct": macro_sens_pct,
        "zero_cov_subfamilies_count": int(zero_cov_count),
        "retrieved_hits_count": len(covered_clean_ids),
        "total_cleaned_sequences": total_cleaned,
    }


def evaluate_esm_coverage_representatives(
    selected_indices: list[int],
    sim_matrix: np.ndarray,
    family_to_indices: dict[str, list[int]],
    rare_subfamilies: list[str],
    k_val: int,
    total_cleaned: int,
) -> dict[str, float | int]:
    """Đo đạc trực tiếp 4 chỉ số Độ bao phủ ngữ nghĩa liên tục nội phân họ (Within-Subfamily Coverage ESM %)
    trên ma trận tương đồng Partial Mean-Centered Cosine ESM-2 (beta = 0.70) cho tập k đại diện.
    """
    if len(selected_indices) == 0 or total_cleaned == 0:
        return {
            "budget_k": int(k_val),
            "num_selected": 0,
            "overall_coverage_esm_pct": 0.0,
            "worst_group_coverage_esm_pct": 0.0,
            "rare_coverage_esm_pct": 0.0,
            "macro_coverage_esm_pct": 0.0,
            "total_cleaned_sequences": int(total_cleaned),
        }

    selected_set: set[int] = set(selected_indices)
    seq_cov = np.zeros(total_cleaned, dtype=np.float64)
    fam_coverages: dict[str, float] = {}

    for fam, f_indices in family_to_indices.items():
        if len(f_indices) == 0:
            fam_coverages[fam] = 0.0
            continue
        rep_in_fam = [idx for idx in f_indices if idx in selected_set]
        if len(rep_in_fam) == 0:
            fam_coverages[fam] = 0.0
            continue
        sub_sim_fam = sim_matrix[np.ix_(f_indices, rep_in_fam)]
        fam_seq_cov = np.max(sub_sim_fam, axis=1).astype(np.float64)
        seq_cov[f_indices] = fam_seq_cov
        fam_coverages[fam] = float(np.mean(fam_seq_cov) * 100.0)

    # 1. Overall Within-Subfamily Coverage ESM (%)
    overall_cov_pct = round(float(np.mean(seq_cov) * 100.0), 2)

    all_cov_values = list(fam_coverages.values())

    # 2. Worst-Group Within-Subfamily Coverage ESM (%)
    worst_group_cov_pct = round(float(np.min(all_cov_values)), 2) if all_cov_values else 0.0

    # 3. Rare Within-Subfamily Coverage ESM (%) (trên 45 nhóm hiếm <= 5 chuỗi)
    rare_cov_values = [fam_coverages[fam] for fam in rare_subfamilies if fam in fam_coverages]
    rare_cov_pct = round(float(np.mean(rare_cov_values)), 2) if rare_cov_values else 0.0

    # 4. Macro-Average Within-Subfamily Coverage ESM (%) (115 nhóm bình đẳng)
    macro_cov_pct = round(float(np.mean(all_cov_values)), 2) if all_cov_values else 0.0

    return {
        "budget_k": int(k_val),
        "num_selected": len(selected_indices),
        "overall_coverage_esm_pct": overall_cov_pct,
        "worst_group_coverage_esm_pct": worst_group_cov_pct,
        "rare_coverage_esm_pct": rare_cov_pct,
        "macro_coverage_esm_pct": macro_cov_pct,
        "total_cleaned_sequences": int(total_cleaned),
    }


def verify_diagonal_consistency(
    df_exp4: pd.DataFrame,
    exp2_csv_path: Path,
    exp3_csv_path: Path,
) -> None:
    """Kiểm định tính toàn vẹn 100.00% của 2 ô đường chéo so với kết quả Nhánh 2 và Nhánh 3."""
    if exp2_csv_path.exists():
        df_exp2 = pd.read_csv(exp2_csv_path)
        df_b = df_exp4[df_exp4["selection_space"] == "BLASTp"].sort_values(["alpha", "budget_k"]).reset_index(drop=True)
        df_e2 = df_exp2.sort_values(["alpha", "budget_k"]).reset_index(drop=True)
        blast_cols = [
            "overall_sensitivity_blast_pct",
            "worst_group_sensitivity_blast_pct",
            "rare_sensitivity_blast_pct",
            "macro_sensitivity_blast_pct",
            "zero_cov_subfamilies_count",
            "retrieved_hits_count",
        ]
        for col in blast_cols:
            max_diff = float(np.max(np.abs(df_b[col].to_numpy(dtype=np.float64) - df_e2[col].to_numpy(dtype=np.float64))))
            if max_diff > 1e-6:
                raise AssertionError(f"Sai lệch ô đường chéo BLASTp tại cột {col}: max_diff={max_diff}")
        logger.info("SANITY CHECK PASSED: Ô đường chéo (BLASTp -> Live BLASTp) khớp 100.00%% với %s (%d/%d dòng).", exp2_csv_path.name, len(df_b), len(df_e2))

    if exp3_csv_path.exists():
        df_exp3 = pd.read_csv(exp3_csv_path)
        df_e = df_exp4[df_exp4["selection_space"] == "ESM-2"].sort_values(["alpha", "budget_k"]).reset_index(drop=True)
        df_e3 = df_exp3.sort_values(["alpha", "budget_k"]).reset_index(drop=True)
        esm_cols = [
            "overall_coverage_esm_pct",
            "worst_group_coverage_esm_pct",
            "rare_coverage_esm_pct",
            "macro_coverage_esm_pct",
        ]
        for col in esm_cols:
            max_diff = float(np.max(np.abs(df_e[col].to_numpy(dtype=np.float64) - df_e3[col].to_numpy(dtype=np.float64))))
            if max_diff > 1e-6:
                raise AssertionError(f"Sai lệch ô đường chéo ESM-2 tại cột {col}: max_diff={max_diff}")
        logger.info("SANITY CHECK PASSED: Ô đường chéo (ESM-2 -> Coverage ESM) khớp 100.00%% với %s (%d/%d dòng).", exp3_csv_path.name, len(df_e), len(df_e3))


def plot_exp4_figures(
    df_all: pd.DataFrame,
    alphas: list[float],
    budget_k_list: list[int],
    figures_dir: Path,
    total_subfamilies: int = 115,
    total_rare: int = 45,
) -> tuple[Path, Path, Path]:
    """Vẽ và xuất hệ thống 3 biểu đồ đối đầu trực diện giữa BLASTp-Selected và ESM2-Selected (PNG & SVG)."""
    k_max = max(budget_k_list)
    palette: dict[float, str] = {0.0: "#555555", 0.5: "#ff7f0e", 1.0: "#d62728"}

    # =========================================================================
    # Biểu đồ 1: Mặt trận 1 — Live BLASTp Sensitivity (%) vs. Budget k (4 ô 2x2)
    # =========================================================================
    fig1, axes1 = plt.subplots(2, 2, figsize=(15, 10.5), sharex=True)
    blast_panels = [
        (axes1[0, 0], "overall_sensitivity_blast_pct", "A. Overall Within-Subfamily Sensitivity BLAST (%)"),
        (axes1[0, 1], "worst_group_sensitivity_blast_pct", "B. Worst-Group Within-Subfamily Sensitivity BLAST (%)"),
        (axes1[1, 0], "rare_sensitivity_blast_pct", f"C. Rare Subfamily Sensitivity BLAST ({total_rare} groups <= 5 seqs) (%)"),
        (axes1[1, 1], "macro_sensitivity_blast_pct", f"D. Macro-Average Sensitivity BLAST ({total_subfamilies} groups) (%)"),
    ]

    for ax_p, col_name, title_str in blast_panels:
        for a_val in alphas:
            color = palette.get(a_val, "#1f77b4")
            df_esm = df_all[(df_all["selection_space"] == "ESM-2") & (df_all["alpha"] == a_val)].sort_values("budget_k")
            df_bls = df_all[(df_all["selection_space"] == "BLASTp") & (df_all["alpha"] == a_val)].sort_values("budget_k")

            ax_p.plot(
                df_esm["budget_k"],
                df_esm[col_name],
                marker="o",
                color=color,
                linestyle="-",
                linewidth=2.2,
                markersize=5,
                label=f"ESM-2 Selected ($\\alpha={a_val}$)",
            )
            ax_p.plot(
                df_bls["budget_k"],
                df_bls[col_name],
                marker="s",
                color=color,
                linestyle="--",
                linewidth=1.8,
                markersize=4,
                alpha=0.85,
                label=f"BLASTp Selected ($\\alpha={a_val}$)",
            )

        if 11 in budget_k_list:
            ax_p.axvline(11, color="#1f77b4", linestyle=":", linewidth=1.2, alpha=0.75)
        ax_p.axvline(k_max, color="#2ca02c", linestyle=":", linewidth=1.2, alpha=0.75)
        ax_p.set_title(title_str, fontsize=11.5, fontweight="bold")
        ax_p.set_ylabel("Sensitivity BLAST (%)", fontsize=10.5, fontweight="bold")
        ax_p.grid(True, linestyle="--", alpha=0.5)

    axes1[1, 0].set_xlabel(f"Representative Budget $k$ (1 to {k_max})", fontsize=11, fontweight="bold")
    axes1[1, 1].set_xlabel(f"Representative Budget $k$ (1 to {k_max})", fontsize=11, fontweight="bold")
    axes1[0, 0].legend(loc="lower right", fontsize=8.5, ncol=2, frameon=True)

    plt.suptitle(
        "Cross-Space Evaluation Arena 1: Within-Subfamily Live BLASTp Sensitivity (%) — ESM-2 Selected (Solid) vs. BLASTp Selected (Dashed)",
        fontsize=12.5,
        fontweight="bold",
        y=1.01,
    )
    plt.tight_layout()

    fig1_png = figures_dir / "exp4_blast_eval_comparison_vs_k.png"
    fig1_svg = figures_dir / "exp4_blast_eval_comparison_vs_k.svg"
    fig1.savefig(fig1_png, dpi=300, bbox_inches="tight")
    fig1.savefig(fig1_svg, bbox_inches="tight")
    plt.close(fig1)

    # =========================================================================
    # Biểu đồ 2: Mặt trận 2 — Coverage ESM (%) vs. Budget k (4 ô 2x2)
    # =========================================================================
    fig2, axes2 = plt.subplots(2, 2, figsize=(15, 10.5), sharex=True)
    esm_panels = [
        (axes2[0, 0], "overall_coverage_esm_pct", "A. Overall Within-Subfamily Coverage ESM (%)"),
        (axes2[0, 1], "worst_group_coverage_esm_pct", "B. Worst-Group Within-Subfamily Coverage ESM (%)"),
        (axes2[1, 0], "rare_coverage_esm_pct", f"C. Rare Subfamily Coverage ESM ({total_rare} groups <= 5 seqs) (%)"),
        (axes2[1, 1], "macro_coverage_esm_pct", f"D. Macro-Average Coverage ESM ({total_subfamilies} groups) (%)"),
    ]

    for ax_p, col_name, title_str in esm_panels:
        for a_val in alphas:
            color = palette.get(a_val, "#1f77b4")
            df_esm = df_all[(df_all["selection_space"] == "ESM-2") & (df_all["alpha"] == a_val)].sort_values("budget_k")
            df_bls = df_all[(df_all["selection_space"] == "BLASTp") & (df_all["alpha"] == a_val)].sort_values("budget_k")

            ax_p.plot(
                df_esm["budget_k"],
                df_esm[col_name],
                marker="o",
                color=color,
                linestyle="-",
                linewidth=2.2,
                markersize=5,
                label=f"ESM-2 Selected ($\\alpha={a_val}$)",
            )
            ax_p.plot(
                df_bls["budget_k"],
                df_bls[col_name],
                marker="s",
                color=color,
                linestyle="--",
                linewidth=1.8,
                markersize=4,
                alpha=0.85,
                label=f"BLASTp Selected ($\\alpha={a_val}$)",
            )

        if 11 in budget_k_list:
            ax_p.axvline(11, color="#1f77b4", linestyle=":", linewidth=1.2, alpha=0.75)
        ax_p.axvline(k_max, color="#2ca02c", linestyle=":", linewidth=1.2, alpha=0.75)
        ax_p.set_title(title_str, fontsize=11.5, fontweight="bold")
        ax_p.set_ylabel("Coverage ESM (%)", fontsize=10.5, fontweight="bold")
        ax_p.grid(True, linestyle="--", alpha=0.5)

    axes2[1, 0].set_xlabel(f"Representative Budget $k$ (1 to {k_max})", fontsize=11, fontweight="bold")
    axes2[1, 1].set_xlabel(f"Representative Budget $k$ (1 to {k_max})", fontsize=11, fontweight="bold")
    axes2[0, 0].legend(loc="lower right", fontsize=8.5, ncol=2, frameon=True)

    plt.suptitle(
        "Cross-Space Evaluation Arena 2: Within-Subfamily Semantic Coverage ESM (%) — ESM-2 Selected (Solid) vs. BLASTp Selected (Dashed)",
        fontsize=12.5,
        fontweight="bold",
        y=1.01,
    )
    plt.tight_layout()

    fig2_png = figures_dir / "exp4_esm_eval_comparison_vs_k.png"
    fig2_svg = figures_dir / "exp4_esm_eval_comparison_vs_k.svg"
    fig2.savefig(fig2_png, dpi=300, bbox_inches="tight")
    fig2.savefig(fig2_svg, bbox_inches="tight")
    plt.close(fig2)

    # =========================================================================
    # Biểu đồ 3: Tổng hợp đối chiếu 2x2 tại k=11 và k=115 (3 Panels)
    # =========================================================================
    fig3, axes3 = plt.subplots(1, 3, figsize=(19.5, 6.0))
    x_idx = np.arange(len(alphas))
    width = 0.35

    ax_a = axes3[0]
    df_b_max = df_all[(df_all["selection_space"] == "BLASTp") & (df_all["budget_k"] == k_max)].sort_values("alpha")
    df_e_max = df_all[(df_all["selection_space"] == "ESM-2") & (df_all["budget_k"] == k_max)].sort_values("alpha")

    bars_b_wst = ax_a.bar(x_idx - width / 2, df_b_max["worst_group_sensitivity_blast_pct"], width=width, color="#1f77b4", edgecolor="black", label="BLASTp Selected (Worst-Group)")
    bars_e_wst = ax_a.bar(x_idx + width / 2, df_e_max["worst_group_sensitivity_blast_pct"], width=width, color="#ff7f0e", edgecolor="black", label="ESM-2 Selected (Worst-Group)")
    ax_a.plot(x_idx - width / 2, df_b_max["rare_sensitivity_blast_pct"], marker="s", color="#0b3c68", linestyle="--", linewidth=2.0, label=f"BLASTp Selected (Rare <={5})")
    ax_a.plot(x_idx + width / 2, df_e_max["rare_sensitivity_blast_pct"], marker="o", color="#993d00", linestyle="-", linewidth=2.0, label=f"ESM-2 Selected (Rare <={5})")

    for bar_grp in (bars_b_wst, bars_e_wst):
        for bar in bar_grp:
            h_val = float(bar.get_height())
            ax_a.annotate(f"{h_val:.1f}%", xy=(bar.get_x() + bar.get_width() / 2, h_val), xytext=(0, 4), textcoords="offset points", ha="center", fontsize=8.5, fontweight="bold")

    ax_a.set_xticks(x_idx)
    ax_a.set_xticklabels([f"$\\alpha={a:.1f}$" for a in alphas], fontsize=10.5, fontweight="bold")
    ax_a.set_ylim(0, 110)
    ax_a.set_ylabel(f"Sensitivity BLAST (%) at $k={k_max}$", fontsize=11, fontweight="bold")
    ax_a.set_title(f"A. Within-Subfamily BLASTp Sensitivity at $k={k_max}$", fontsize=12, fontweight="bold")
    ax_a.grid(True, linestyle="--", alpha=0.5, axis="y")
    ax_a.legend(loc="best", fontsize=8.5, frameon=True)

    ax_b = axes3[1]
    bars_b_cov = ax_b.bar(x_idx - width / 2, df_b_max["worst_group_coverage_esm_pct"], width=width, color="#1f77b4", edgecolor="black", label="BLASTp Selected (Worst-Group)")
    bars_e_cov = ax_b.bar(x_idx + width / 2, df_e_max["worst_group_coverage_esm_pct"], width=width, color="#ff7f0e", edgecolor="black", label="ESM-2 Selected (Worst-Group)")
    ax_b.plot(x_idx - width / 2, df_b_max["rare_coverage_esm_pct"], marker="s", color="#0b3c68", linestyle="--", linewidth=2.0, label="BLASTp Selected (Rare <=5)")
    ax_b.plot(x_idx + width / 2, df_e_max["rare_coverage_esm_pct"], marker="o", color="#993d00", linestyle="-", linewidth=2.0, label="ESM-2 Selected (Rare <=5)")

    for bar_grp in (bars_b_cov, bars_e_cov):
        for bar in bar_grp:
            h_val = float(bar.get_height())
            ax_b.annotate(f"{h_val:.1f}%", xy=(bar.get_x() + bar.get_width() / 2, h_val), xytext=(0, 4), textcoords="offset points", ha="center", fontsize=8.5, fontweight="bold")

    ax_b.set_xticks(x_idx)
    ax_b.set_xticklabels([f"$\\alpha={a:.1f}$" for a in alphas], fontsize=10.5, fontweight="bold")
    ax_b.set_ylim(0, 110)
    ax_b.set_ylabel(f"Coverage ESM (%) at $k={k_max}$", fontsize=11, fontweight="bold")
    ax_b.set_title(f"B. Within-Subfamily Semantic Coverage ESM at $k={k_max}$", fontsize=12, fontweight="bold")
    ax_b.grid(True, linestyle="--", alpha=0.5, axis="y")
    ax_b.legend(loc="best", fontsize=8.5, frameon=True)

    ax_c = axes3[2]
    df_b11 = df_all[(df_all["selection_space"] == "BLASTp") & (df_all["budget_k"] == 11)].sort_values("alpha")
    df_e11 = df_all[(df_all["selection_space"] == "ESM-2") & (df_all["budget_k"] == 11)].sort_values("alpha")

    w4 = 0.20
    b1 = ax_c.bar(x_idx - 1.5 * w4, df_b11["zero_cov_subfamilies_count"], width=w4, color="#6baed6", edgecolor="black", label="BLASTp ($k=11$)")
    b2 = ax_c.bar(x_idx - 0.5 * w4, df_e11["zero_cov_subfamilies_count"], width=w4, color="#fd8d3c", edgecolor="black", label="ESM-2 ($k=11$)")
    b3 = ax_c.bar(x_idx + 0.5 * w4, df_b_max["zero_cov_subfamilies_count"], width=w4, color="#08519c", edgecolor="black", label=f"BLASTp ($k={k_max}$)")
    b4 = ax_c.bar(x_idx + 1.5 * w4, df_e_max["zero_cov_subfamilies_count"], width=w4, color="#a63603", edgecolor="black", label=f"ESM-2 ($k={k_max}$)")

    for bar_grp in (b1, b2, b3, b4):
        for bar in bar_grp:
            h_int = int(bar.get_height())
            ax_c.annotate(f"{h_int}", xy=(bar.get_x() + bar.get_width() / 2, h_int), xytext=(0, 3), textcoords="offset points", ha="center", fontsize=8.0, fontweight="bold")

    max_z = int(max(
        df_b11["zero_cov_subfamilies_count"].max(),
        df_e11["zero_cov_subfamilies_count"].max(),
        df_b_max["zero_cov_subfamilies_count"].max(),
        df_e_max["zero_cov_subfamilies_count"].max(),
    ))
    ax_c.set_xticks(x_idx)
    ax_c.set_xticklabels([f"$\\alpha={a:.1f}$" for a in alphas], fontsize=10.5, fontweight="bold")
    ax_c.set_ylim(0, max(max_z + 12, 20))
    ax_c.set_ylabel(f"Zero-Sensitivity Subfamilies Count (/{total_subfamilies})", fontsize=11, fontweight="bold")
    ax_c.set_title(f"C. Zero-Sensitivity Subfamilies ($k=11$ vs. $k={k_max}$)", fontsize=12, fontweight="bold")
    ax_c.grid(True, linestyle="--", alpha=0.5, axis="y")
    ax_c.legend(loc="upper right", fontsize=8.5, frameon=True)

    plt.suptitle(
        f"2x2 Cross-Space Within-Subfamily Summary at Strategic Milestones ($k=11$ and $k={k_max}$): BLASTp Selected vs. ESM-2 Selected",
        fontsize=13,
        fontweight="bold",
        y=1.02,
    )
    plt.tight_layout()

    fig3_png = figures_dir / "exp4_cross_space_summary_k11_k76.png"
    fig3_svg = figures_dir / "exp4_cross_space_summary_k11_k76.svg"
    fig3.savefig(fig3_png, dpi=300, bbox_inches="tight")
    fig3.savefig(fig3_svg, bbox_inches="tight")
    plt.close(fig3)

    return fig1_png, fig2_png, fig3_png


def run_exp4_cross_eval_a1a(
    config_path: str = "configs/config_exp4_cross_eval_a1a.yaml",
    force_recompute: bool = False,
) -> dict[str, object]:
    """Thực thi toàn bộ pipeline Nhánh 4: Kiểm tra chéo 2x2 nội phân họ giữa BLASTp-Selected và ESM2-Selected trên 20 mốc k và 3 mức alpha."""
    logger.info("=" * 105)
    logger.info(
        "BRANCH 4: FULL 2x2 CROSS-SPACE WITHIN-SUBFAMILY EVALUATION (BLASTp-SELECTED vs. ESM2-SELECTED ON CURATED MEROPS A1A)"
    )
    logger.info("=" * 105)

    # 1. Nạp cấu hình YAML
    cfg_file = Path(config_path)
    if not cfg_file.exists():
        cfg_file = parent_dir / config_path
    if not cfg_file.exists():
        raise FileNotFoundError(f"Không tìm thấy tệp cấu hình: {config_path}")

    with open(cfg_file, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    logger.info("Loaded config from: %s", cfg_file)

    dataset_name: str = str(cfg.get("dataset_name", "MEROPS_A1A_curated"))
    fasta_path: Path = Path(str(cfg.get("fasta_path", "../baseline_repo/MEROPS_A1A.fasta")))
    if not fasta_path.is_absolute():
        fasta_path = (parent_dir / fasta_path).resolve()

    blast_bin_path: Path = Path(str(cfg.get("blast_bin_path", "tools/blast/bin/blastp.exe")))
    if not blast_bin_path.is_absolute():
        blast_bin_path = (parent_dir / blast_bin_path).resolve()

    default_ks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15, 20, 25, 30, 40, 50, 60, 75, 115]
    budget_k_list: list[int] = [int(k) for k in cfg.get("budget_k_list", default_ks)]
    alphas: list[float] = [float(a) for a in cfg.get("alphas", [0.0, 0.5, 1.0])]
    selection_spaces: list[str] = [str(s) for s in cfg.get("selection_spaces", ["BLASTp", "ESM-2"])]
    num_shuffles: int = int(cfg.get("num_shuffles", 1000))
    budget_per_shuffle: int = int(cfg.get("budget_per_shuffle", max(budget_k_list)))

    outputs_dir = parent_dir / str(cfg.get("output_dir", "outputs"))
    embeddings_cache_dir = parent_dir / str(cfg.get("embeddings_cache_dir", "outputs/embeddings_cache"))
    tables_dir = outputs_dir / "tables"
    figures_dir = outputs_dir / "figures"
    cache_dir = outputs_dir / "similarity_cache"

    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)
    embeddings_cache_dir.mkdir(parents=True, exist_ok=True)

    # 2. Đọc và lọc QC chuỗi MEROPS A1A theo Phương án 3B (4,120 chuỗi sạch, 115 phân họ, 45 phân họ hiếm)
    logger.info("Loading and preprocessing MEROPS A1A FASTA dataset (Option 3B Curated)...")
    bundle_a1a = DatasetLoader.load_and_preprocess_dataset(
        cfg_file, override_fasta=str(fasta_path), override_dataset_name=dataset_name
    )
    records: list[ProteinRecord] = bundle_a1a.cleaned_records
    total_cleaned: int = len(records)
    seq_ids: list[str] = [r.id for r in records]
    id_to_idx: dict[str, int] = {sid: idx for idx, sid in enumerate(seq_ids)}
    id_to_record: dict[str, ProteinRecord] = {r.id: r for r in records}
    id_to_family: dict[str, str] = bundle_a1a.label_map
    rare_subfamilies: list[str] = bundle_a1a.rare_subfamilies

    family_to_ids: dict[str, list[str]] = defaultdict(list)
    family_to_indices: dict[str, list[int]] = defaultdict(list)
    for idx, sid in enumerate(seq_ids):
        fam = id_to_family.get(sid, "UNKNOWN")
        family_to_ids[fam].append(sid)
        family_to_indices[fam].append(idx)

    total_subfamilies: int = len(family_to_ids)
    logger.info(
        "Dataset '%s': %d cleaned curated seqs, %d subfamilies, %d rare subfamilies (<= %d seqs).",
        dataset_name,
        total_cleaned,
        total_subfamilies,
        len(rare_subfamilies),
        int(cfg.get("rare_threshold", 5)),
    )

    # 3. Nạp ma trận tương đồng ngữ nghĩa liên tục ESM-2 (beta = 0.70) phục vụ Mặt trận 2
    esm_cfg = cfg.get("esm_representation", {})
    esm_model_name: str = str(esm_cfg.get("model_name", "facebook/esm2_t12_35M_UR50D"))
    esm_batch_size: int = int(esm_cfg.get("batch_size", 16))
    esm_device: str = str(esm_cfg.get("device", "auto"))
    esm_beta: float = float(esm_cfg.get("center_shift_beta", 0.70))

    esm_calc = ESM2SimilarityMatrix(
        model_name=esm_model_name,
        embeddings_cache_dir=embeddings_cache_dir,
        similarity_cache_dir=cache_dir,
        batch_size=esm_batch_size,
        device=esm_device,
        center_shift_beta=esm_beta,
    )
    sim_matrix_esm = esm_calc.get_similarity_matrix(
        records=records,
        seq_ids=seq_ids,
        dataset_name=dataset_name,
        force_recompute=False,
    )

    # 4. Chuẩn bị cơ sở dữ liệu BLAST phục vụ Mặt trận 1 (Live BLASTp E <= 1e-7)
    live_cfg = cfg.get("blast_live_coverage_evaluation", {})
    live_evalue: float = float(live_cfg.get("evalue", 1e-7))
    live_max_targets: int = int(live_cfg.get("max_target_seqs", 999999))
    live_threads: int = int(live_cfg.get("num_threads", 24))

    blast_calc = BLASTSimilarityMatrix(
        blastp_bin_path=blast_bin_path,
        num_threads=live_threads,
        cache_dir=cache_dir,
    )

    cleaned_fasta_path = cache_dir / f"{dataset_name}_cleaned_qc.fasta"
    if not cleaned_fasta_path.exists():
        SeqIO.write([SeqRecord(Seq(r.sequence), id=r.id, description=r.header) for r in records], cleaned_fasta_path, "fasta")

    db_prefix = cache_dir / f"{dataset_name}_live_db"
    db_prefix = blast_calc.build_blast_db(fasta_path=cleaned_fasta_path, db_prefix=db_prefix)

    exp2_csv_path = tables_dir / "exp2_rare_weighted_a1a.csv"
    exp3_csv_path = tables_dir / "exp3_esm_coverage_a1a.csv"
    exp2_lookup: dict[tuple[float, int], dict[str, float | int]] = {}
    if exp2_csv_path.exists() and not force_recompute:
        df_exp2_cached = pd.read_csv(exp2_csv_path)
        for _, r_row in df_exp2_cached.iterrows():
            key = (round(float(r_row["alpha"]), 2), int(r_row["budget_k"]))
            exp2_lookup[key] = {
                "overall_sensitivity_blast_pct": float(r_row["overall_sensitivity_blast_pct"]),
                "worst_group_sensitivity_blast_pct": float(r_row["worst_group_sensitivity_blast_pct"]),
                "rare_sensitivity_blast_pct": float(r_row["rare_sensitivity_blast_pct"]),
                "macro_sensitivity_blast_pct": float(r_row["macro_sensitivity_blast_pct"]),
                "zero_cov_subfamilies_count": int(r_row["zero_cov_subfamilies_count"]),
                "retrieved_hits_count": int(r_row["retrieved_hits_count"]),
            }
        logger.info("Loaded %d cached Live BLASTp entries from %s for diagonal (BLASTp -> BLASTp).", len(exp2_lookup), exp2_csv_path.name)

    # 5. Vòng lặp chính quét qua 2 không gian chọn x 3 mức alpha x 20 mốc k (120 cấu hình)
    all_rows: list[dict[str, object]] = []

    with tempfile.TemporaryDirectory() as tmpdir_str:
        tmpdir = Path(tmpdir_str)

        for sel_space in selection_spaces:
            logger.info("-" * 95)
            logger.info("EVALUATING SELECTION SPACE: %s ACROSS ALPHAS %s AND %d BUDGET MILESTONES", sel_space, alphas, len(budget_k_list))
            logger.info("-" * 95)

            alpha_pbar = tqdm(alphas, desc=f"Space={sel_space} Alphas", unit="alpha", dynamic_ncols=True)
            for alpha in alpha_pbar:
                alpha_str = f"{alpha:.2f}"
                alpha_key = round(float(alpha), 2)
                alpha_pbar.set_postfix_str(f"alpha={alpha_str}")

                if sel_space == "BLASTp":
                    cache_file = cache_dir / f"{dataset_name}_{num_shuffles}_shuffles_alpha_{alpha_str}.npz"
                elif sel_space == "ESM-2":
                    cache_file = cache_dir / f"{dataset_name}_esm2_{num_shuffles}_shuffles_alpha_{alpha_str}.npz"
                else:
                    raise ValueError(f"selection_space không hợp lệ: {sel_space}")

                consensus_ids = load_cached_consensus_ids(cache_file=cache_file, expected_budget=budget_per_shuffle)

                # Truy vấn Live BLASTp 1 lần cho toàn bộ top k_max đại diện của (sel_space, alpha)
                k_max_eval = max(budget_k_list)
                top_kmax_ids = [sid for sid in consensus_ids[:k_max_eval] if sid in id_to_record]
                space_alpha_query_fasta = tmpdir / f"query_{sel_space}_{alpha_str}_top{k_max_eval}.fasta"
                SeqIO.write(
                    [SeqRecord(Seq(id_to_record[sid].sequence), id=sid, description=id_to_record[sid].header) for sid in top_kmax_ids],
                    space_alpha_query_fasta,
                    "fasta",
                )
                space_alpha_hit_pairs = blast_calc.retrieve_blast_hit_pairs(
                    query_fasta=space_alpha_query_fasta,
                    db_prefix=db_prefix,
                    evalue=live_evalue,
                    max_target_seqs=live_max_targets,
                    num_threads=live_threads,
                )

                k_pbar = tqdm(
                    budget_k_list,
                    desc=f"{sel_space} alpha={alpha_str}",
                    unit="k",
                    leave=False,
                    dynamic_ncols=True,
                )

                for k_val in k_pbar:
                    sub_selected_ids = consensus_ids[:k_val]
                    selected_indices = [id_to_idx[sid] for sid in sub_selected_ids if sid in id_to_idx]

                    # Mặt trận 1: Bộ 5 chỉ số Live BLASTp Sensitivity (%) nội phân họ
                    if sel_space == "BLASTp" and (alpha_key, k_val) in exp2_lookup and not force_recompute:
                        blast_metrics = exp2_lookup[(alpha_key, k_val)]
                    else:
                        blast_metrics = evaluate_rare_aware_representatives(
                            selected_ids=sub_selected_ids,
                            id_to_record=id_to_record,
                            seq_ids=seq_ids,
                            id_to_family=id_to_family,
                            family_to_ids=family_to_ids,
                            rare_subfamilies=rare_subfamilies,
                            blast_calc=blast_calc,
                            db_prefix=db_prefix,
                            tmpdir=tmpdir,
                            k_val=k_val,
                            live_evalue=live_evalue,
                            live_max_targets=live_max_targets,
                            live_threads=live_threads,
                            precomputed_hit_pairs=space_alpha_hit_pairs,
                        )

                    # Mặt trận 2: Bộ 4 chỉ số Coverage ESM (%) nội phân họ
                    esm_metrics = evaluate_esm_coverage_representatives(
                        selected_indices=selected_indices,
                        sim_matrix=sim_matrix_esm,
                        family_to_indices=family_to_indices,
                        rare_subfamilies=rare_subfamilies,
                        k_val=k_val,
                        total_cleaned=total_cleaned,
                    )

                    row: dict[str, object] = {
                        "selection_space": sel_space,
                        "alpha": alpha,
                        "budget_k": int(k_val),
                        "overall_sensitivity_blast_pct": blast_metrics["overall_sensitivity_blast_pct"],
                        "worst_group_sensitivity_blast_pct": blast_metrics["worst_group_sensitivity_blast_pct"],
                        "rare_sensitivity_blast_pct": blast_metrics["rare_sensitivity_blast_pct"],
                        "macro_sensitivity_blast_pct": blast_metrics["macro_sensitivity_blast_pct"],
                        "zero_cov_subfamilies_count": blast_metrics["zero_cov_subfamilies_count"],
                        "overall_coverage_esm_pct": esm_metrics["overall_coverage_esm_pct"],
                        "worst_group_coverage_esm_pct": esm_metrics["worst_group_coverage_esm_pct"],
                        "rare_coverage_esm_pct": esm_metrics["rare_coverage_esm_pct"],
                        "macro_coverage_esm_pct": esm_metrics["macro_coverage_esm_pct"],
                        "retrieved_hits_count": blast_metrics["retrieved_hits_count"],
                        "total_cleaned_sequences": total_cleaned,
                    }
                    all_rows.append(row)

                    k_pbar.set_postfix({
                        "BLAST_Ov": f"{blast_metrics['overall_sensitivity_blast_pct']}%",
                        "BLAST_Rare": f"{blast_metrics['rare_sensitivity_blast_pct']}%",
                        "ESM_Rare": f"{esm_metrics['rare_coverage_esm_pct']}%",
                    })

                for milestone_k in (11, max(budget_k_list)):
                    matching = [
                        r for r in all_rows
                        if r["selection_space"] == sel_space and r["alpha"] == alpha and r["budget_k"] == milestone_k
                    ]
                    if matching:
                        rm = matching[-1]
                        logger.info(
                            "[%6s | alpha=%s | k=%3d] BLAST Sens (Ov/Wst/Rare/Macro/Zero): %6.2f%% / %5.2f%% / %5.2f%% / %5.2f%% / %3d | "
                            "ESM Cov (Ov/Wst/Rare/Macro): %6.2f%% / %5.2f%% / %5.2f%% / %5.2f%%",
                            sel_space,
                            alpha_str,
                            milestone_k,
                            rm["overall_sensitivity_blast_pct"],
                            rm["worst_group_sensitivity_blast_pct"],
                            rm["rare_sensitivity_blast_pct"],
                            rm["macro_sensitivity_blast_pct"],
                            rm["zero_cov_subfamilies_count"],
                            rm["overall_coverage_esm_pct"],
                            rm["worst_group_coverage_esm_pct"],
                            rm["rare_coverage_esm_pct"],
                            rm["macro_coverage_esm_pct"],
                        )

    # 6. Kiểm định tự động 2 ô đường chéo và xuất DUY NHẤT một tệp CSV kết quả (120 dòng)
    df_all = pd.DataFrame(all_rows)
    verify_diagonal_consistency(df_exp4=df_all, exp2_csv_path=exp2_csv_path, exp3_csv_path=exp3_csv_path)

    csv_file = tables_dir / "exp4_cross_eval_a1a.csv"
    df_all.to_csv(csv_file, index=False, encoding="utf-8-sig")
    logger.info("\nĐã lưu bảng số liệu thực nghiệm kiểm tra chéo 2x2 (%d dòng) vào:\n  - %s", len(df_all), csv_file)

    # 7. Vẽ hệ thống 3 biểu đồ công bố khoa học (PNG & SVG)
    logger.info("Đang tạo hệ thống 3 biểu đồ đối đầu trực diện cho Nhánh 4...")
    fig1_png, fig2_png, fig3_png = plot_exp4_figures(
        df_all=df_all,
        alphas=alphas,
        budget_k_list=budget_k_list,
        figures_dir=figures_dir,
        total_subfamilies=total_subfamilies,
        total_rare=len(rare_subfamilies),
    )
    logger.info("Saved 3 publication figures to:\n  - %s\n  - %s\n  - %s", fig1_png, fig2_png, fig3_png)
    logger.info("=" * 105)
    logger.info("BRANCH 4 FULL 2x2 CROSS-SPACE EVALUATION COMPLETED SUCCESSFULLY!")
    logger.info("=" * 105)

    return {
        "status": "SUCCESS",
        "csv_path": str(csv_file),
        "fig1_png": str(fig1_png),
        "fig2_png": str(fig2_png),
        "fig3_png": str(fig3_png),
        "total_rows": len(df_all),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Exp 4: Full 2x2 Cross-Space Within-Subfamily Evaluation (BLASTp-Selected vs. ESM2-Selected on Curated Peptidase A1)"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="configs/config_exp4_cross_eval_a1a.yaml",
        help="Path to YAML config",
    )
    parser.add_argument(
        "--force-recompute",
        action="store_true",
        help="Force recomputing Live BLASTp for all configurations",
    )
    args = parser.parse_args()

    run_exp4_cross_eval_a1a(
        config_path=args.config,
        force_recompute=args.force_recompute,
    )


if __name__ == "__main__":
    main()
