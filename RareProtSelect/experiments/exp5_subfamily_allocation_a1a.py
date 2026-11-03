"""Thực hiện Công đoạn 5.1, 5.2, 5.3 trong Tài liệu 1 và Mục 4.10 trong Tài liệu 2:
Phân tích Cấu trúc Đại diện Trực tiếp & Độ Dư thừa Phân bổ Phân họ trong Tập đại diện S_k
giữa BLASTp-Selected (Nhánh 2) và ESM2-Selected (Nhánh 3, beta = 0.70) trên Tập Dữ Liệu Chuẩn Hóa Phương Án 3B
Siêu họ Peptidase A1 (MEROPS_A1A_curated: 4,120 chuỗi, 115 phân họ, 45 họ hiếm <= 5 chuỗi, họ lớn nhất A01.009 = 329 chuỗi).

Kịch bản thực hiện các nhiệm vụ khoa học cốt lõi:
1. Tuân thủ triệt để nguyên tắc Ceteris Paribus (/controlled-scientific-experiment):
   - Giữ nguyên 100% tập dữ liệu chuẩn hóa Phương án 3B MEROPS_A1A_curated (4,120 chuỗi sạch, 115 phân họ, 45 phân họ hiếm <= 5 chuỗi, họ lớn nhất A01.009 có 329 chuỗi).
   - Nạp trực tiếp 6 tệp cache danh sách đại diện đồng thuận 1,000 lần xáo trộn (budget_per_shuffle = 115) đã lưu đệm từ Nhánh 2 (BLASTp) và Nhánh 3 (ESM-2, beta = 0.70).
2. Đo đạc Bộ 4 chỉ số Cấu trúc Đại diện Trực tiếp & Độ Dư thừa Phân họ (kèm 4 cột số đếm nguyên) trên 120 cấu hình (2 không gian x 3 mức alpha x 20 mốc k):
   - subfamilies_represented_count & subfamily_repr_rate_pct (/115 phân họ)
   - rare_subfamilies_represented_count & rare_repr_rate_pct (/45 phân họ hiếm <= 5 chuỗi)
   - redundant_slots_count & subfamily_redundancy_pct (% ghế trong k bị lặp lại phân họ)
   - dominant_a01_009_count & dominant_a01_009_share_pct (% ghế trong k thuộc họ lớn nhất A01.009)
3. Kiểm định tự động (Sanity Check) 3 bất biến toán học trên toàn bộ 120 dòng dữ liệu.
4. Xuất duy nhất tệp CSV kết quả: outputs/tables/exp5_subfamily_allocation_a1a.csv (120 dòng x 11 cột).
5. Xuất hệ thống 2 biểu đồ công bố khoa học (PNG 300 DPI và SVG vector):
   - outputs/figures/exp5_allocation_metrics_vs_k.png & .svg
   - outputs/figures/exp5_allocation_summary_k11_k76.png & .svg
"""

from __future__ import annotations

import argparse
import logging
import sys
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml
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

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("exp5_subfamily_allocation_a1a")

EXPECTED_COLUMNS: list[str] = [
    "selection_space",
    "alpha",
    "budget_k",
    "subfamilies_represented_count",
    "subfamily_repr_rate_pct",
    "rare_subfamilies_represented_count",
    "rare_repr_rate_pct",
    "redundant_slots_count",
    "subfamily_redundancy_pct",
    "dominant_a01_009_count",
    "dominant_a01_009_share_pct",
]


def load_cached_consensus_ids(cache_file: Path, expected_budget: int = 115) -> list[str]:
    """Nạp danh sách đại diện đồng thuận 1,000 lần xáo trộn từ tệp cache .npz của Nhánh 2 hoặc Nhánh 3."""
    if not cache_file.exists():
        raise FileNotFoundError(
            f"Không tìm thấy tệp cache đồng thuận: {cache_file}. "
            "Vui lòng đảm bảo Nhánh 2 và Nhánh 3 đã được chạy trước đó."
        )

    cached_data = np.load(cache_file, allow_pickle=True)
    cached_budget: int = 15
    if "metadata" in cached_data:
        meta_raw: object = cached_data["metadata"].item()
        if isinstance(meta_raw, dict) and "budget_per_shuffle" in meta_raw:
            budget_obj: object = meta_raw["budget_per_shuffle"]
            if isinstance(budget_obj, (int, float, np.integer)):
                cached_budget = int(budget_obj)

    if cached_budget < expected_budget:
        raise ValueError(
            f"Tệp cache {cache_file.name} có budget_per_shuffle={cached_budget} < {expected_budget} yêu cầu!"
        )

    consensus_ids: list[str] = [str(x) for x in cached_data["consensus_ids"]]
    if len(consensus_ids) < expected_budget:
        raise ValueError(
            f"Tệp cache {cache_file.name} chỉ chứa {len(consensus_ids)} đại diện < {expected_budget} yêu cầu!"
        )

    logger.info(
        "Loaded %d consensus IDs from %s (budget_per_shuffle=%d)",
        len(consensus_ids),
        cache_file.name,
        cached_budget,
    )
    return consensus_ids


def evaluate_subfamily_allocation_metrics(
    selected_ids: list[str],
    id_to_family: dict[str, str],
    total_subfamilies: int,
    rare_subfamilies_set: set[str],
    dominant_subfamily_id: str = "A01.009",
) -> dict[str, int | float]:
    """Đo đạc trực tiếp Bộ 4 chỉ số tỷ lệ phần trăm (%) và 4 cột số đếm nguyên (count)
    phản ánh cấu trúc đại diện phân họ và độ dư thừa phân bổ trong tập đại diện S_k.
    """
    k: int = len(selected_ids)
    if k <= 0:
        raise ValueError(f"Ngân sách k = len(selected_ids) phải > 0, nhận được k={k}.")
    if total_subfamilies <= 0:
        raise ValueError(f"Tổng số phân họ total_subfamilies phải > 0, nhận được {total_subfamilies}.")
    total_rare: int = len(rare_subfamilies_set)
    if total_rare <= 0:
        raise ValueError("Tập phân họ hiếm rare_subfamilies_set không được rỗng.")

    family_list: list[str] = []
    for sid in selected_ids:
        if sid not in id_to_family:
            raise KeyError(f"Sequence ID '{sid}' trong S_k không tồn tại trong ánh xạ id_to_family!")
        family_list.append(id_to_family[sid])

    family_counts: Counter[str] = Counter(family_list)
    represented_subfamilies: set[str] = set(family_counts.keys())

    # 1. Tỷ lệ phân họ trên 115 họ có đại diện trực tiếp trong S_k
    subfamilies_represented_count: int = len(represented_subfamilies)
    subfamily_repr_rate_pct: float = round((subfamilies_represented_count / total_subfamilies) * 100.0, 2)

    # 2. Tỷ lệ phân họ hiếm (<= 5 chuỗi, trên 45 họ hiếm) có đại diện trực tiếp trong S_k
    rare_subfamilies_represented_count: int = len(represented_subfamilies & rare_subfamilies_set)
    rare_repr_rate_pct: float = round((rare_subfamilies_represented_count / total_rare) * 100.0, 2)

    # 3. Độ dư thừa phân bổ phân họ (số ghế bị lặp lại ở các phân họ có c_g >= 2)
    redundant_slots_count: int = sum(count - 1 for count in family_counts.values() if count >= 2)
    if subfamilies_represented_count + redundant_slots_count != k:
        raise AssertionError(
            f"Vi phạm bất biến tổng số ghế tại k={k}: "
            f"{subfamilies_represented_count} + {redundant_slots_count} != {k}"
        )
    subfamily_redundancy_pct: float = round((redundant_slots_count / k) * 100.0, 2)

    # 4. Tỷ trọng độc chiếm ngân sách của phân họ lớn nhất A01.009 (Cathepsin D, 329 chuỗi)
    dominant_a01_009_count: int = int(family_counts.get(dominant_subfamily_id, 0))
    dominant_a01_009_share_pct: float = round((dominant_a01_009_count / k) * 100.0, 2)

    return {
        "subfamilies_represented_count": subfamilies_represented_count,
        "subfamily_repr_rate_pct": subfamily_repr_rate_pct,
        "rare_subfamilies_represented_count": rare_subfamilies_represented_count,
        "rare_repr_rate_pct": rare_repr_rate_pct,
        "redundant_slots_count": redundant_slots_count,
        "subfamily_redundancy_pct": subfamily_redundancy_pct,
        "dominant_a01_009_count": dominant_a01_009_count,
        "dominant_a01_009_share_pct": dominant_a01_009_share_pct,
    }


def verify_exp5_mathematical_invariants(
    df: pd.DataFrame,
    total_subfamilies: int = 115,
    total_rare: int = 45,
) -> None:
    """Kiểm định tự động (Sanity Check) 3 bất biến toán học trên toàn bộ 120 dòng của bảng kết quả Nhánh 5."""
    if len(df) != 120:
        raise AssertionError(f"Bảng kết quả Nhánh 5 phải có đúng 120 dòng, nhưng nhận được {len(df)} dòng.")

    actual_cols: list[str] = list(df.columns)
    if actual_cols != EXPECTED_COLUMNS:
        raise AssertionError(
            f"Danh sách cột CSV không khớp thiết kế!\nThực tế: {actual_cols}\nKỳ vọng: {EXPECTED_COLUMNS}"
        )

    for idx, row in df.iterrows():
        k_val = int(row["budget_k"])
        sub_cnt = int(row["subfamilies_represented_count"])
        rare_cnt = int(row["rare_subfamilies_represented_count"])
        red_cnt = int(row["redundant_slots_count"])
        dom_cnt = int(row["dominant_a01_009_count"])
        sub_pct = float(row["subfamily_repr_rate_pct"])
        red_pct = float(row["subfamily_redundancy_pct"])

        # Bất biến 1: Bảo toàn tổng số ghế ngân sách k
        if sub_cnt + red_cnt != k_val:
            raise AssertionError(
                f"Dòng {idx} (space={row['selection_space']}, alpha={row['alpha']}, k={k_val}) "
                f"vi phạm Bất biến 1: {sub_cnt} + {red_cnt} != {k_val}"
            )

        # Bất biến 2: Hằng đẳng thức bù 100.0% tại k == total_subfamilies == 115
        if k_val == total_subfamilies:
            sum_pct = sub_pct + red_pct
            if abs(sum_pct - 100.0) > 0.05:
                raise AssertionError(
                    f"Dòng {idx} tại k={k_val} vi phạm Bất biến 2: "
                    f"subfamily_repr_rate_pct ({sub_pct}%) + subfamily_redundancy_pct ({red_pct}%) = {sum_pct}% != 100.0%"
                )

        # Bất biến 3: Ràng buộc tập con của phân họ hiếm và phân họ thống trị A01.009
        if not (0 <= rare_cnt <= min(total_rare, sub_cnt)):
            raise AssertionError(
                f"Dòng {idx} vi phạm Bất biến 3a: rare_cnt={rare_cnt} vượt ngoài [0, min({total_rare}, {sub_cnt})]"
            )
        if not (0 <= dom_cnt <= 1 + red_cnt):
            raise AssertionError(
                f"Dòng {idx} vi phạm Bất biến 3b: dom_cnt={dom_cnt} vượt ngoài [0, 1 + {red_cnt}]"
            )

    logger.info(
        "SANITY CHECK PASSED: Toàn bộ 120/120 dòng thỏa mãn tuyệt đối 3 Bất biến Toán học "
        "(Slot Conservation, k=%d Complementarity 100%%, và Subset Bounds).",
        total_subfamilies,
    )


def plot_exp5_allocation_metrics_vs_k(
    df: pd.DataFrame,
    alphas: list[float],
    budget_k_list: list[int],
    output_png: Path,
    output_svg: Path,
    total_subfamilies: int = 115,
    total_rare: int = 45,
) -> None:
    """Vẽ Hình 5.1 (1 ảnh 4 góc 2x2): Diễn tiến 4 chỉ số tỷ lệ % theo ngân sách k in [1..115]
    giữa ESM-2 Selected (nét liền, marker 'o') và BLASTp Selected (nét đứt, marker 's')
    qua 3 mức alpha in {0.0, 0.5, 1.0}.
    """
    k_max: int = max(budget_k_list)
    palette: dict[float, str] = {0.0: "#555555", 0.5: "#ff7f0e", 1.0: "#2ca02c"}

    fig, axes = plt.subplots(2, 2, figsize=(15.5, 11.0), sharex=True)
    panels: list[tuple[plt.Axes, str, str, str]] = [
        (
            axes[0, 0],
            "subfamily_repr_rate_pct",
            f"A. Direct Subfamily Representation Rate (/{total_subfamilies} Subfamilies) (%)",
            "Subfamily Repr Rate (%)",
        ),
        (
            axes[0, 1],
            "rare_repr_rate_pct",
            f"B. Direct Rare Subfamily Representation Rate (<= 5 seqs, /{total_rare} Rare) (%)",
            "Rare Subfamily Repr Rate (%)",
        ),
        (
            axes[1, 0],
            "subfamily_redundancy_pct",
            "C. Subfamily Allocation Redundancy (% of Budget k Repeated)",
            "Subfamily Redundancy (%)",
        ),
        (
            axes[1, 1],
            "dominant_a01_009_share_pct",
            "D. Dominant Subfamily A01.009 Share (% of Budget k Occupied)",
            "Dominant A01.009 Share (%)",
        ),
    ]

    k_arr = np.array(sorted(budget_k_list), dtype=np.float64)
    ideal_repr_pct = (k_arr / float(total_subfamilies)) * 100.0
    axes[0, 0].plot(
        k_arr,
        ideal_repr_pct,
        color="#1f77b4",
        linestyle=":",
        linewidth=1.8,
        alpha=0.85,
        label=f"Ideal 1-per-subfamily ($k/{total_subfamilies}$)",
    )

    for ax_p, col_name, title_str, ylabel_str in panels:
        for a_val in alphas:
            color = palette.get(a_val, "#1f77b4")
            df_esm = df[(df["selection_space"] == "ESM-2") & (df["alpha"] == a_val)].sort_values("budget_k")
            df_bls = df[(df["selection_space"] == "BLASTp") & (df["alpha"] == a_val)].sort_values("budget_k")

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
                markersize=4.2,
                alpha=0.85,
                label=f"BLASTp Selected ($\\alpha={a_val}$)",
            )

        if 11 in budget_k_list:
            ax_p.axvline(11, color="#1f77b4", linestyle=":", linewidth=1.2, alpha=0.7)
        ax_p.axvline(k_max, color="#d62728", linestyle=":", linewidth=1.2, alpha=0.7)
        ax_p.set_title(title_str, fontsize=11.5, fontweight="bold")
        ax_p.set_ylabel(ylabel_str, fontsize=10.5, fontweight="bold")
        ax_p.set_ylim(-3.0, 105.0)
        ax_p.grid(True, linestyle="--", alpha=0.5)

    axes[1, 0].set_xlabel(f"Representative Budget $k$ (1 to {k_max})", fontsize=11, fontweight="bold")
    axes[1, 1].set_xlabel(f"Representative Budget $k$ (1 to {k_max})", fontsize=11, fontweight="bold")
    axes[0, 0].legend(loc="upper left", fontsize=8.2, ncol=2, frameon=True)
    axes[0, 1].legend(loc="upper left", fontsize=8.2, ncol=2, frameon=True)
    axes[1, 0].legend(loc="upper right", fontsize=8.2, ncol=2, frameon=True)
    axes[1, 1].legend(loc="upper right", fontsize=8.2, ncol=2, frameon=True)

    plt.suptitle(
        "Branch 5 Direct Subfamily Representation & Allocation Redundancy vs. Budget k — ESM-2 (Solid) vs. BLASTp (Dashed)",
        fontsize=13,
        fontweight="bold",
        y=1.01,
    )
    plt.tight_layout()

    fig.savefig(output_png, dpi=300, bbox_inches="tight")
    fig.savefig(output_svg, bbox_inches="tight")
    plt.close(fig)


def plot_exp5_allocation_summary_k11_k76(
    df: pd.DataFrame,
    alphas: list[float],
    output_png: Path,
    output_svg: Path,
    k_max: int = 115,
    total_subfamilies: int = 115,
    total_rare: int = 45,
) -> None:
    """Vẽ Hình 5.2 (1 ảnh 4 góc 2x2): Biểu đồ cột ghép (4 cột tại mỗi mức alpha:
    BLASTp k=11, ESM-2 k=11, BLASTp k=115, ESM-2 k=115) đối chiếu trực diện 4 chỉ số
    kèm nhãn `count (pct%)` trên đỉnh mỗi cột.
    """
    fig, axes = plt.subplots(2, 2, figsize=(17.5, 11.5))
    x_idx = np.arange(len(alphas), dtype=np.float64)
    w4: float = 0.20

    panel_specs: list[tuple[plt.Axes, str, str, str, str]] = [
        (
            axes[0, 0],
            "subfamily_repr_rate_pct",
            "subfamilies_represented_count",
            f"A. Direct Subfamily Representation Rate (/{total_subfamilies} Subfamilies) at $k=11$ vs. $k={k_max}$",
            "Subfamily Repr Rate (%)",
        ),
        (
            axes[0, 1],
            "rare_repr_rate_pct",
            "rare_subfamilies_represented_count",
            f"B. Direct Rare Subfamily Representation Rate (/{total_rare} Rare <= 5 seqs) at $k=11$ vs. $k={k_max}$",
            "Rare Subfamily Repr Rate (%)",
        ),
        (
            axes[1, 0],
            "subfamily_redundancy_pct",
            "redundant_slots_count",
            f"C. Subfamily Allocation Redundancy (% of $k$ Slots Repeated) at $k=11$ vs. $k={k_max}$",
            "Subfamily Redundancy (%)",
        ),
        (
            axes[1, 1],
            "dominant_a01_009_share_pct",
            "dominant_a01_009_count",
            f"D. Dominant Subfamily A01.009 Share (% of $k$ Slots Occupied) at $k=11$ vs. $k={k_max}$",
            "Dominant A01.009 Share (%)",
        ),
    ]

    df_b11 = df[(df["selection_space"] == "BLASTp") & (df["budget_k"] == 11)].sort_values("alpha").reset_index(drop=True)
    df_e11 = df[(df["selection_space"] == "ESM-2") & (df["budget_k"] == 11)].sort_values("alpha").reset_index(drop=True)
    df_b_max = df[(df["selection_space"] == "BLASTp") & (df["budget_k"] == k_max)].sort_values("alpha").reset_index(drop=True)
    df_e_max = df[(df["selection_space"] == "ESM-2") & (df["budget_k"] == k_max)].sort_values("alpha").reset_index(drop=True)

    bar_configs: list[tuple[pd.DataFrame, float, str, str]] = [
        (df_b11, -1.5 * w4, "#6baed6", "BLASTp ($k=11$)"),
        (df_e11, -0.5 * w4, "#fd8d3c", "ESM-2 ($k=11$)"),
        (df_b_max, 0.5 * w4, "#08519c", f"BLASTp ($k={k_max}$)"),
        (df_e_max, 1.5 * w4, "#d94801", f"ESM-2 ($k={k_max}$)"),
    ]

    for ax_p, pct_col, cnt_col, title_str, ylabel_str in panel_specs:
        for df_sub, offset, color_hex, label_str in bar_configs:
            pct_vals = df_sub[pct_col].to_numpy(dtype=np.float64)
            cnt_vals = df_sub[cnt_col].to_numpy(dtype=np.int64)
            bars = ax_p.bar(
                x_idx + offset,
                pct_vals,
                width=w4,
                color=color_hex,
                edgecolor="black",
                linewidth=0.8,
                label=label_str,
            )
            for bar, cnt_v, pct_v in zip(bars, cnt_vals, pct_vals):
                h_val = float(bar.get_height())
                ax_p.annotate(
                    f"{int(cnt_v)}\n({pct_v:.1f}%)",
                    xy=(bar.get_x() + bar.get_width() / 2.0, h_val),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                    fontsize=7.8,
                    fontweight="bold",
                )

        ax_p.set_xticks(x_idx)
        ax_p.set_xticklabels([f"$\\alpha={a:.1f}$" for a in alphas], fontsize=10.5, fontweight="bold")
        ax_p.set_ylim(0.0, 118.0)
        ax_p.set_ylabel(ylabel_str, fontsize=10.5, fontweight="bold")
        ax_p.set_title(title_str, fontsize=11.2, fontweight="bold")
        ax_p.grid(True, linestyle="--", alpha=0.5, axis="y")
        ax_p.legend(loc="upper right", fontsize=8.5, ncol=2, frameon=True)

    plt.suptitle(
        f"Branch 5 Strategic Milestone Comparison ($k=11$ vs. $k={k_max}$): Direct Subfamily Allocation Count & Percentage",
        fontsize=13.5,
        fontweight="bold",
        y=1.01,
    )
    plt.tight_layout()

    fig.savefig(output_png, dpi=300, bbox_inches="tight")
    fig.savefig(output_svg, bbox_inches="tight")
    plt.close(fig)


def log_strategic_milestone_summary(df: pd.DataFrame, milestones: tuple[int, ...] = (11, 115)) -> None:
    """In bảng đối chiếu tóm tắt toàn bộ 6 phương pháp tại các mốc ngân sách chiến lược (k=11 và k=115) ra màn hình console."""
    for k_m in milestones:
        logger.info("=" * 115)
        logger.info("SUMMARY TABLE AT STRATEGIC BUDGET MILESTONE k = %d (6 METHODS COMPARISON)", k_m)
        logger.info("-" * 115)
        logger.info(
            "%-8s | %-5s | %-4s | %-18s | %-18s | %-18s | %-18s",
            "Space",
            "Alpha",
            "k",
            "Subfamily Repr(/115)",
            "Rare Repr(/45,<=5)",
            "Redundant Slots(/k)",
            "A01.009 Share(/k)",
        )
        logger.info("-" * 115)
        df_k = df[df["budget_k"] == k_m].sort_values(["selection_space", "alpha"])
        for _, r in df_k.iterrows():
            logger.info(
                "%-8s | %5.1f | %4d | %3d (%6.2f%%)      | %3d (%6.2f%%)      | %3d (%6.2f%%)      | %3d (%6.2f%%)",
                str(r["selection_space"]),
                float(r["alpha"]),
                int(r["budget_k"]),
                int(r["subfamilies_represented_count"]),
                float(r["subfamily_repr_rate_pct"]),
                int(r["rare_subfamilies_represented_count"]),
                float(r["rare_repr_rate_pct"]),
                int(r["redundant_slots_count"]),
                float(r["subfamily_redundancy_pct"]),
                int(r["dominant_a01_009_count"]),
                float(r["dominant_a01_009_share_pct"]),
            )
        logger.info("=" * 115)


def run_exp5_subfamily_allocation_a1a(
    config_path: str | Path = "configs/config_exp5_subfamily_allocation_a1a.yaml",
) -> dict[str, object]:
    """Điều phối toàn bộ quy trình thực nghiệm Nhánh 5."""
    logger.info("=" * 110)
    logger.info(
        "BRANCH 5: DIRECT SUBFAMILY REPRESENTATION & ALLOCATION REDUNDANCY ANALYSIS ON CURATED MEROPS A1A (120 CONFIGS)"
    )
    logger.info("=" * 110)

    # 1. Nạp cấu hình YAML
    cfg_file = Path(config_path)
    if not cfg_file.exists():
        cfg_file = parent_dir / config_path
    if not cfg_file.exists():
        raise FileNotFoundError(f"Không tìm thấy tệp cấu hình: {config_path}")

    with open(cfg_file, "r", encoding="utf-8") as f:
        cfg_raw: object = yaml.safe_load(f)
    if not isinstance(cfg_raw, dict):
        raise ValueError(f"Nội dung tệp cấu hình YAML không hợp lệ: {cfg_file}")

    logger.info("Loaded config from: %s", cfg_file)

    dataset_name: str = str(cfg_raw.get("dataset_name", "MEROPS_A1A_curated"))
    fasta_path: Path = Path(str(cfg_raw.get("fasta_path", "../baseline_repo/MEROPS_A1A.fasta")))
    if not fasta_path.is_absolute():
        fasta_path = (parent_dir / fasta_path).resolve()

    dominant_subfamily_id: str = str(cfg_raw.get("dominant_subfamily_id", "A01.009"))
    default_ks: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15, 20, 25, 30, 40, 50, 60, 75, 115]
    raw_ks: object = cfg_raw.get("budget_k_list", default_ks)
    budget_k_list: list[int] = [int(k) for k in raw_ks] if isinstance(raw_ks, list) else default_ks

    raw_alphas: object = cfg_raw.get("alphas", [0.0, 0.5, 1.0])
    alphas: list[float] = [float(a) for a in raw_alphas] if isinstance(raw_alphas, list) else [0.0, 0.5, 1.0]

    raw_spaces: object = cfg_raw.get("selection_spaces", ["BLASTp", "ESM-2"])
    selection_spaces: list[str] = (
        [str(s) for s in raw_spaces] if isinstance(raw_spaces, list) else ["BLASTp", "ESM-2"]
    )

    num_shuffles: int = int(cfg_raw.get("num_shuffles", 1000))
    budget_per_shuffle: int = int(cfg_raw.get("budget_per_shuffle", max(budget_k_list)))

    outputs_dir: Path = parent_dir / str(cfg_raw.get("output_dir", "outputs"))
    tables_dir: Path = outputs_dir / "tables"
    figures_dir: Path = outputs_dir / "figures"
    cache_dir: Path = outputs_dir / "similarity_cache"

    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    # 2. Đọc và lọc QC chuỗi MEROPS A1A theo Phương án 3B (4,120 chuỗi sạch, 115 phân họ, 45 phân họ hiếm)
    logger.info("Loading and preprocessing MEROPS A1A FASTA dataset (Option 3B Curated)...")
    bundle_a1a = DatasetLoader.load_and_preprocess_dataset(
        cfg_file, override_fasta=str(fasta_path), override_dataset_name=dataset_name
    )
    records: list[ProteinRecord] = bundle_a1a.cleaned_records
    total_cleaned: int = len(records)
    id_to_family: dict[str, str] = bundle_a1a.label_map
    rare_subfamilies_set: set[str] = set(bundle_a1a.rare_subfamilies)

    family_to_ids: dict[str, list[str]] = defaultdict(list)
    for r in records:
        fam = id_to_family.get(r.id, "UNKNOWN")
        family_to_ids[fam].append(r.id)

    total_subfamilies: int = len(family_to_ids)
    total_rare: int = len(rare_subfamilies_set)
    dominant_count_ground: int = len(family_to_ids.get(dominant_subfamily_id, []))

    logger.info(
        "Dataset '%s': %d cleaned curated seqs, %d subfamilies, %d rare subfamilies (<= %d seqs), "
        "dominant '%s' has %d seqs (%.2f%%).",
        dataset_name,
        total_cleaned,
        total_subfamilies,
        total_rare,
        int(cfg_raw.get("rare_threshold", 5)),
        dominant_subfamily_id,
        dominant_count_ground,
        (dominant_count_ground / total_cleaned) * 100.0 if total_cleaned > 0 else 0.0,
    )

    # 3. Quét qua 2 không gian chọn x 3 mức alpha x 20 mốc k (120 cấu hình)
    all_rows: list[dict[str, int | float | str]] = []

    for sel_space in selection_spaces:
        for alpha in tqdm(alphas, desc=f"Evaluating Space={sel_space}", unit="alpha", dynamic_ncols=True):
            alpha_str = f"{alpha:.2f}"
            if sel_space == "BLASTp":
                cache_file = cache_dir / f"{dataset_name}_{num_shuffles}_shuffles_alpha_{alpha_str}.npz"
            elif sel_space == "ESM-2":
                cache_file = cache_dir / f"{dataset_name}_esm2_{num_shuffles}_shuffles_alpha_{alpha_str}.npz"
            else:
                raise ValueError(f"selection_space không hợp lệ: {sel_space}")

            consensus_ids = load_cached_consensus_ids(
                cache_file=cache_file,
                expected_budget=budget_per_shuffle,
            )

            for k_val in budget_k_list:
                sub_selected_ids = consensus_ids[:k_val]
                metrics = evaluate_subfamily_allocation_metrics(
                    selected_ids=sub_selected_ids,
                    id_to_family=id_to_family,
                    total_subfamilies=total_subfamilies,
                    rare_subfamilies_set=rare_subfamilies_set,
                    dominant_subfamily_id=dominant_subfamily_id,
                )

                row: dict[str, int | float | str] = {
                    "selection_space": sel_space,
                    "alpha": float(alpha),
                    "budget_k": int(k_val),
                    "subfamilies_represented_count": int(metrics["subfamilies_represented_count"]),
                    "subfamily_repr_rate_pct": float(metrics["subfamily_repr_rate_pct"]),
                    "rare_subfamilies_represented_count": int(metrics["rare_subfamilies_represented_count"]),
                    "rare_repr_rate_pct": float(metrics["rare_repr_rate_pct"]),
                    "redundant_slots_count": int(metrics["redundant_slots_count"]),
                    "subfamily_redundancy_pct": float(metrics["subfamily_redundancy_pct"]),
                    "dominant_a01_009_count": int(metrics["dominant_a01_009_count"]),
                    "dominant_a01_009_share_pct": float(metrics["dominant_a01_009_share_pct"]),
                }
                all_rows.append(row)

    # 4. Kiểm định tự động 3 bất biến toán học trên toàn bộ 120 dòng
    df_all = pd.DataFrame(all_rows, columns=EXPECTED_COLUMNS)
    verify_exp5_mathematical_invariants(
        df=df_all,
        total_subfamilies=total_subfamilies,
        total_rare=total_rare,
    )

    # 5. Xuất tệp CSV kết quả duy nhất (120 dòng x 11 cột)
    csv_file = tables_dir / "exp5_subfamily_allocation_a1a.csv"
    df_all.to_csv(csv_file, index=False, encoding="utf-8-sig")
    logger.info(
        "Đã lưu bảng số liệu thực nghiệm Nhánh 5 (%d dòng x %d cột) vào:\n  - %s",
        len(df_all),
        len(df_all.columns),
        csv_file,
    )

    # 6. In bảng tổng hợp đối chiếu tại k = 11 và k = 115 ra màn hình console
    k_max = max(budget_k_list)
    log_strategic_milestone_summary(df=df_all, milestones=(11, k_max))

    # 7. Xuất hệ thống 2 biểu đồ công bố khoa học (PNG 300 DPI & SVG vector)
    fig1_png = figures_dir / "exp5_allocation_metrics_vs_k.png"
    fig1_svg = figures_dir / "exp5_allocation_metrics_vs_k.svg"
    plot_exp5_allocation_metrics_vs_k(
        df=df_all,
        alphas=alphas,
        budget_k_list=budget_k_list,
        output_png=fig1_png,
        output_svg=fig1_svg,
        total_subfamilies=total_subfamilies,
        total_rare=total_rare,
    )

    fig2_png = figures_dir / "exp5_allocation_summary_k11_k76.png"
    fig2_svg = figures_dir / "exp5_allocation_summary_k11_k76.svg"
    plot_exp5_allocation_summary_k11_k76(
        df=df_all,
        alphas=alphas,
        output_png=fig2_png,
        output_svg=fig2_svg,
        k_max=k_max,
        total_subfamilies=total_subfamilies,
        total_rare=total_rare,
    )

    logger.info("Saved 2 publication figures (PNG & SVG) to:\n  - %s\n  - %s", fig1_png, fig2_png)
    logger.info("=" * 110)
    logger.info("BRANCH 5 SUBFAMILY ALLOCATION & REDUNDANCY ANALYSIS COMPLETED SUCCESSFULLY!")
    logger.info("=" * 110)

    return {
        "status": "SUCCESS",
        "csv_path": str(csv_file),
        "fig1_png": str(fig1_png),
        "fig1_svg": str(fig1_svg),
        "fig2_png": str(fig2_png),
        "fig2_svg": str(fig2_svg),
        "total_rows": len(df_all),
        "total_columns": len(df_all.columns),
    }


def main() -> None:
    """Điểm vào CLI nhận tham số --config và kích hoạt run_exp5_subfamily_allocation_a1a."""
    parser = argparse.ArgumentParser(
        description="Exp 5: Direct Subfamily Representation & Allocation Redundancy Analysis on Curated Peptidase A1"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="configs/config_exp5_subfamily_allocation_a1a.yaml",
        help="Path to YAML configuration file.",
    )
    args = parser.parse_args()
    run_exp5_subfamily_allocation_a1a(config_path=args.config)


if __name__ == "__main__":
    main()
