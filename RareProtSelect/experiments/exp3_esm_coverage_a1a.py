"""Thực hiện Công đoạn 3.1, 3.2, 3.3, 3.4 trong Tài liệu 1 và Module 4.6 trong Tài liệu 2:
Khảo sát Hàm Mục Tiêu Có Trọng Số Ưu Tiên Nhóm Hiếm Trong Không Gian Biểu Diễn Ngữ Nghĩa Liên Tục ESM-2
(Partial Mean-Centered Cosine Similarity, beta=0.70) Trên Tập Dữ Liệu Chuẩn Hóa Phương Án 3B (4,120 Chuỗi, 115 Phân Họ, 45 Họ Hiếm <= 5 Chuỗi)
theo Cơ Chế Bao Phủ Nội Phân Họ (Within-Subfamily Coverage: S_k cap V_g -> V_g) Với 3 Mốc Alpha và 20 Mốc k đến 115.

Kịch bản thực hiện các nhiệm vụ khoa học cốt lõi:
1. Chuyển không gian biểu diễn sang ESM-2 (facebook/esm2_t12_35M_UR50D, 480 chiều) chuẩn hóa bằng
   Partial Mean-Centered Cosine Similarity (beta=0.70): S_ESM(u, v) = max(0, z'_u^T z'_v) để khử suy biến dị hướng (Representation Anisotropy).
2. Giữ nguyên 100% các yếu tố đối chứng với Nhánh 2 (Ceteris Paribus):
   - Tập dữ liệu chuẩn hóa Phương án 3B MEROPS_A1A_curated (4,120 chuỗi sạch, 115 phân họ, 45 phân họ hiếm <= 5 chuỗi).
   - Họ hàm trọng số w_v = (n_g)^(-alpha) với 3 mức alpha in {0.0, 0.5, 1.0}.
   - Giải thuật Pruned Greedy 90% (1,000-Shuffle Consensus Ranking) với budget_per_shuffle = 115.
   - Dải 20 mốc ngân sách k in [1..11, 15, 20, 25, 30, 40, 50, 60, 75, 115].
3. Cô lập bộ nhớ đệm xáo trộn ESM-2 tại: outputs/similarity_cache/MEROPS_A1A_curated_esm2_1000_shuffles_alpha_{alpha:.2f}.npz.
4. Đo đạc chính xác 4 chỉ số phần trăm liên tục Coverage ESM (%) theo cơ chế Bao phủ nội phân họ (S_k cap V_g -> V_g):
   - Overall Coverage ESM (%)
   - Worst-Group Coverage ESM (%)
   - Rare Coverage ESM (%) (45 nhóm hiếm <= 5 chuỗi)
   - Macro-Average Coverage ESM (%) (115 nhóm bình đẳng)
5. Xuất duy nhất tệp CSV kết quả: outputs/tables/exp3_esm_coverage_a1a.csv (60 hàng = 3 alpha x 20 mốc k).
6. Xuất 2 biểu đồ công bố khoa học (PNG và SVG): exp3_pareto_tradeoff và exp3_metrics_vs_k.
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from collections import defaultdict
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
from src.selection.pruned_greedy import compute_subfamily_weights, run_pruned_greedy_1000_shuffles
from src.similarity.dense_similarity import ESM2SimilarityMatrix

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("exp3_esm_coverage_a1a")


def evaluate_esm_coverage_representatives(
    selected_indices: list[int],
    sim_matrix: np.ndarray,
    family_to_indices: dict[str, list[int]],
    rare_subfamilies: list[str],
    k_val: int,
    total_cleaned: int,
) -> dict[str, float | int]:
    """Đo đạc trực tiếp 4 chỉ số Độ bao phủ ngữ nghĩa liên tục nội phân họ (Within-Subfamily Coverage ESM %)
    trên ma trận tương đồng Partial Mean-Centered Cosine ESM-2 (beta=0.70) cho tập k đại diện:
    - Với mỗi phân họ g in 1..115, đặt S_{k,g} = S_k cap V_g:
      + Nếu S_{k,g} = empty -> c_v^within(S_k) = 0.0 với mọi v in V_g và Cov_g^within(S_k) = 0.0%.
      + Nếu S_{k,g} != empty -> c_v^within(S_k) = max_{s in S_{k,g}} S_ESM(v, s) với mọi v in V_g.
    - overall_coverage_esm_pct = mean_{v in V} c_v^within(S_k) * 100
    - worst_group_coverage_esm_pct = min_{g in 1..115} Cov_g^within(S_k)
    - rare_coverage_esm_pct = mean_{g in G_rare} Cov_g^within(S_k)
    - macro_coverage_esm_pct = mean_{g in 1..115} Cov_g^within(S_k)
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

    # Tính điểm bao phủ ngữ nghĩa nội phân họ cho từng phân họ trong số 115 phân họ
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


def run_exp3_esm_coverage_a1a(
    config_path: str = "configs/config_exp3_esm_coverage_a1a.yaml",
    force_recompute: bool = False,
    override_shuffles: int | None = None,
) -> dict[str, object]:
    """Thực thi toàn bộ pipeline Nhánh 3: Khảo sát 3 mức alpha trên 20 mốc k (đến 115) trong không gian ESM-2 Mean-Centered Cosine."""
    logger.info("=" * 105)
    logger.info(
        "BRANCH 3: RARE-AWARE WEIGHTED FACILITY LOCATION IN ESM-2 MEAN-CENTERED COSINE SPACE (4,120 SEQS, 115 SUBFAMILIES, WITHIN-SUBFAMILY COVERAGE)"
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

    default_ks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15, 20, 25, 30, 40, 50, 60, 75, 115]
    budget_k_list: list[int] = [int(k) for k in cfg.get("budget_k_list", default_ks)]
    alphas: list[float] = [float(a) for a in cfg.get("alphas", [0.0, 0.5, 1.0])]
    prune_threshold: float = float(cfg.get("prune_threshold", 0.90))
    num_shuffles: int = int(override_shuffles if override_shuffles is not None else cfg.get("num_shuffles", 1000))
    seed: int = int(cfg.get("seed", 42))
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

    # 2. Đọc và lọc QC chuỗi MEROPS A1A theo Phương án 3B (4,120 chuỗi sạch, 115 phân họ, 45 họ hiếm)
    logger.info("Loading and preprocessing MEROPS A1A FASTA dataset (Option 3B Curated)...")
    bundle_a1a = DatasetLoader.load_and_preprocess_dataset(
        cfg_file, override_fasta=str(fasta_path), override_dataset_name=dataset_name
    )
    records = bundle_a1a.cleaned_records
    total_cleaned: int = len(records)
    seq_ids: list[str] = [r.id for r in records]
    id_to_idx: dict[str, int] = {sid: idx for idx, sid in enumerate(seq_ids)}
    id_to_family: dict[str, str] = bundle_a1a.label_map
    rare_subfamilies: list[str] = bundle_a1a.rare_subfamilies

    family_to_indices: dict[str, list[int]] = defaultdict(list)
    for idx, sid in enumerate(seq_ids):
        fam = id_to_family.get(sid, "UNKNOWN")
        family_to_indices[fam].append(idx)

    total_subfamilies: int = len(family_to_indices)
    logger.info(
        "Dataset '%s': %d cleaned curated seqs, %d subfamilies, %d rare subfamilies (<= %d seqs).",
        dataset_name,
        total_cleaned,
        total_subfamilies,
        len(rare_subfamilies),
        int(cfg.get("rare_threshold", 5)),
    )

    # 3. Nạp vector nhúng ESM-2 và xây dựng ma trận tương đồng Partial Mean-Centered Cosine (4,120 x 4,120)
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

    sim_matrix = esm_calc.get_similarity_matrix(
        records=records,
        seq_ids=seq_ids,
        dataset_name=dataset_name,
        force_recompute=force_recompute,
    )
    logger.info(
        "ESM-2 Partial Mean-Centered Cosine (beta=%.2f) matrix ready: shape=%s, positive_density=%.2f%%, pairs>=0.90=%.4f%%",
        esm_beta,
        str(sim_matrix.shape),
        float((sim_matrix > 0.0).mean() * 100.0),
        float((sim_matrix >= prune_threshold).mean() * 100.0),
    )

    # 4. Vòng lặp chính qua 3 mốc tham số alpha
    all_rows: list[dict[str, object]] = []

    logger.info(
        "\nSTARTING ESM-2 SWEEP OVER %d ALPHA VALUES %s ACROSS %d BUDGET MILESTONES (budget_per_shuffle=%d)",
        len(alphas),
        alphas,
        len(budget_k_list),
        budget_per_shuffle,
    )
    alpha_pbar = tqdm(alphas, desc="Overall Alphas Progress (ESM-2)", unit="alpha", dynamic_ncols=True)

    for alpha in alpha_pbar:
        alpha_str = f"{alpha:.2f}"
        alpha_pbar.set_postfix_str(f"alpha={alpha_str}")

        # 4.1. Tính vector trọng số mẫu cho alpha hiện tại
        weights = compute_subfamily_weights(
            seq_ids=seq_ids,
            id_to_family=id_to_family,
            alpha=alpha,
        )

        # 4.2. Chạy Pruned Greedy 90% (1,000-Shuffle Consensus Ranking) trên S_ESM với budget_per_shuffle = 115
        cache_file = cache_dir / f"{dataset_name}_esm2_{num_shuffles}_shuffles_alpha_{alpha_str}.npz"
        t_greedy_start = time.perf_counter()

        consensus_ids, _ = run_pruned_greedy_1000_shuffles(
            sim_matrix=sim_matrix,
            seq_ids=seq_ids,
            prune_threshold=prune_threshold,
            num_shuffles=num_shuffles,
            sample_weights=weights,
            seed=seed,
            budget_per_shuffle=budget_per_shuffle,
            cache_path=cache_file,
            force_recompute=force_recompute,
            desc_label=f"ESM-2 Alpha={alpha_str} (1,000 Shuffles, b={budget_per_shuffle})",
            show_progress=True,
        )
        greedy_runtime = round(time.perf_counter() - t_greedy_start, 2)

        # 4.3. Đánh giá tuần tự qua 20 mốc ngân sách k bằng bộ 4 chỉ số Coverage ESM (%) nội phân họ
        k_pbar = tqdm(
            budget_k_list,
            desc=f"Alpha={alpha_str} Within-Subfamily ESM Coverage",
            unit="k",
            leave=False,
            dynamic_ncols=True,
        )

        for k_val in k_pbar:
            sub_selected_ids = consensus_ids[:k_val]
            selected_indices = [id_to_idx[sid] for sid in sub_selected_ids if sid in id_to_idx]

            metrics = evaluate_esm_coverage_representatives(
                selected_indices=selected_indices,
                sim_matrix=sim_matrix,
                family_to_indices=family_to_indices,
                rare_subfamilies=rare_subfamilies,
                k_val=k_val,
                total_cleaned=total_cleaned,
            )

            row: dict[str, object] = {
                "alpha": alpha,
                "budget_k": int(k_val),
                "overall_coverage_esm_pct": metrics["overall_coverage_esm_pct"],
                "worst_group_coverage_esm_pct": metrics["worst_group_coverage_esm_pct"],
                "rare_coverage_esm_pct": metrics["rare_coverage_esm_pct"],
                "macro_coverage_esm_pct": metrics["macro_coverage_esm_pct"],
                "num_selected": metrics["num_selected"],
                "total_cleaned_sequences": metrics["total_cleaned_sequences"],
                "greedy_runtime_seconds": greedy_runtime,
            }
            all_rows.append(row)

            k_pbar.set_postfix({
                "Overall": f"{metrics['overall_coverage_esm_pct']}%",
                "Worst": f"{metrics['worst_group_coverage_esm_pct']}%",
                "Rare": f"{metrics['rare_coverage_esm_pct']}%",
            })

        for milestone_k in (11, max(budget_k_list)):
            matching_rows = [r for r in all_rows if r["alpha"] == alpha and r["budget_k"] == milestone_k]
            if matching_rows:
                row_m = matching_rows[-1]
                logger.info(
                    "ESM-2 ALPHA %s AT k=%3d -> Overall Cov: %6.2f%% | Worst-Group Cov: %5.2f%% | Rare Cov: %5.2f%% | Macro Cov: %5.2f%%",
                    alpha_str,
                    milestone_k,
                    row_m["overall_coverage_esm_pct"],
                    row_m["worst_group_coverage_esm_pct"],
                    row_m["rare_coverage_esm_pct"],
                    row_m["macro_coverage_esm_pct"],
                )

    # 5. Xuất DUY NHẤT một tệp CSV kết quả (60 dòng)
    df_all = pd.DataFrame(all_rows)
    csv_file = tables_dir / "exp3_esm_coverage_a1a.csv"
    df_all.to_csv(csv_file, index=False, encoding="utf-8-sig")
    logger.info("\nĐã lưu bảng số liệu thực nghiệm duy nhất (%d dòng) vào:\n  - %s", len(df_all), csv_file)

    # 6. Vẽ hệ thống 2 biểu đồ công bố khoa học (Đối chiếu song song k=11 và k=115)
    k_max = max(budget_k_list)
    logger.info("Đang tạo 2 biểu đồ xuất bản khoa học cho Nhánh 3 (đối chiếu k=11 và k=%d)...", k_max)
    compare_ks = [11, k_max] if 11 in budget_k_list and k_max != 11 else [k_max]

    # Biểu đồ 1: Pareto Trade-off Curve đối chiếu song song tại k=11 và k=115
    fig1, axes1 = plt.subplots(1, len(compare_ks), figsize=(6.5 * len(compare_ks), 5.8), squeeze=False)

    for idx_panel, k_slice in enumerate(compare_ks):
        ax_p = axes1[0, idx_panel]
        df_slice = df_all[df_all["budget_k"] == k_slice].sort_values("alpha")
        alphas_plot = df_slice["alpha"].tolist()
        overall_slice = df_slice["overall_coverage_esm_pct"].tolist()
        worst_slice = df_slice["worst_group_coverage_esm_pct"].tolist()
        rare_slice = df_slice["rare_coverage_esm_pct"].tolist()
        macro_slice = df_slice["macro_coverage_esm_pct"].tolist()

        ax_p.plot(overall_slice, worst_slice, marker="o", color="#d62728", linewidth=2.5, markersize=8, label="Worst-Group Coverage ESM")
        ax_p.plot(overall_slice, rare_slice, marker="s", color="#1f77b4", linewidth=2.0, linestyle="--", markersize=7, label=f"Rare Coverage ESM ({len(rare_subfamilies)} groups <= 5 seqs)")
        ax_p.plot(overall_slice, macro_slice, marker="^", color="#2ca02c", linewidth=2.0, linestyle=":", markersize=7, label=f"Macro Coverage ESM ({total_subfamilies} groups)")

        for a_val, ov_val, wst_val, r_val in zip(alphas_plot, overall_slice, worst_slice, rare_slice):
            ax_p.annotate(
                f"alpha={a_val}",
                xy=(ov_val, wst_val),
                xytext=(6, 6),
                textcoords="offset points",
                fontsize=9,
                fontweight="bold",
            )
            ax_p.annotate(
                f"alpha={a_val} ({r_val:.1f}%)",
                xy=(ov_val, r_val),
                xytext=(6, -12),
                textcoords="offset points",
                fontsize=8,
            )

        panel_tag = chr(65 + idx_panel)
        ax_p.set_xlabel("Overall Within-Subfamily Coverage ESM (%)", fontsize=11, fontweight="bold")
        ax_p.set_ylabel("Subfamily Coverage ESM (%)", fontsize=11, fontweight="bold")
        ax_p.set_title(f"{panel_tag}. ESM-2 Pareto Trade-off at Budget k = {k_slice}", fontsize=12, fontweight="bold", pad=10)
        ax_p.grid(True, linestyle="--", alpha=0.5)
        ax_p.legend(loc="best", frameon=True, fontsize=9)

    plt.suptitle(
        f"ESM-2 Within-Subfamily Pareto Trade-off Comparison: Baseline Budget (k=11) vs. Full Subfamily Budget (k={k_max})",
        fontsize=13,
        fontweight="bold",
        y=1.02,
    )
    plt.tight_layout()

    fig1_png = figures_dir / "exp3_pareto_tradeoff.png"
    fig1_svg = figures_dir / "exp3_pareto_tradeoff.svg"
    fig1.savefig(fig1_png, dpi=300, bbox_inches="tight")
    fig1.savefig(fig1_svg, bbox_inches="tight")
    plt.close(fig1)

    # Biểu đồ 2: Diễn tiến 4 chỉ số Coverage ESM (%) theo ngân sách k (1..115) qua 3 mức alpha
    fig2, axes = plt.subplots(2, 2, figsize=(14, 10), sharex=True)
    palette = {0.0: "#7f7f7f", 0.25: "#2ca02c", 0.5: "#ff7f0e", 0.75: "#9467bd", 1.0: "#d62728"}

    for a_val in alphas:
        df_a = df_all[df_all["alpha"] == a_val].sort_values("budget_k")
        color = palette.get(a_val, "#1f77b4")
        label = f"alpha={a_val}"

        axes[0, 0].plot(df_a["budget_k"], df_a["overall_coverage_esm_pct"], marker="o", color=color, label=label, linewidth=2.0, markersize=5)
        axes[0, 1].plot(df_a["budget_k"], df_a["worst_group_coverage_esm_pct"], marker="s", color=color, label=label, linewidth=2.0, markersize=5)
        axes[1, 0].plot(df_a["budget_k"], df_a["rare_coverage_esm_pct"], marker="^", color=color, label=label, linewidth=2.0, markersize=5)
        axes[1, 1].plot(df_a["budget_k"], df_a["macro_coverage_esm_pct"], marker="d", color=color, label=label, linewidth=2.0, markersize=5)

    for ax_sub in axes.flat:
        if 11 in budget_k_list:
            ax_sub.axvline(11, color="#1f77b4", linestyle=":", linewidth=1.2, alpha=0.8, label="k=11 (Fig.8 Baseline)")
        ax_sub.axvline(k_max, color="#2ca02c", linestyle="--", linewidth=1.2, alpha=0.8, label=f"k={k_max} (G={total_subfamilies} Subfamilies)")

    axes[0, 0].set_title("A. Overall Within-Subfamily Coverage ESM (%)", fontweight="bold")
    axes[0, 0].set_ylabel("Coverage ESM (%)", fontweight="bold")
    axes[0, 0].grid(True, linestyle="--", alpha=0.5)
    axes[0, 0].legend(loc="lower right", fontsize=9)

    axes[0, 1].set_title("B. Worst-Group Within-Subfamily Coverage ESM (%)", fontweight="bold")
    axes[0, 1].set_ylabel("Coverage ESM (%)", fontweight="bold")
    axes[0, 1].grid(True, linestyle="--", alpha=0.5)

    axes[1, 0].set_title(f"C. Rare Subfamily Coverage ESM ({len(rare_subfamilies)} groups <= 5 seqs) (%)", fontweight="bold")
    axes[1, 0].set_xlabel(f"Representative Budget $k$ (1 to {k_max})", fontweight="bold")
    axes[1, 0].set_ylabel("Coverage ESM (%)", fontweight="bold")
    axes[1, 0].grid(True, linestyle="--", alpha=0.5)

    axes[1, 1].set_title(f"D. Macro-Average Coverage ESM ({total_subfamilies} groups) (%)", fontweight="bold")
    axes[1, 1].set_xlabel(f"Representative Budget $k$ (1 to {k_max})", fontweight="bold")
    axes[1, 1].set_ylabel("Coverage ESM (%)", fontweight="bold")
    axes[1, 1].grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    fig2_png = figures_dir / "exp3_metrics_vs_k.png"
    fig2_svg = figures_dir / "exp3_metrics_vs_k.svg"
    fig2.savefig(fig2_png, dpi=300)
    fig2.savefig(fig2_svg)
    plt.close(fig2)

    logger.info("Saved 2 publication figures to:\n  - %s\n  - %s", fig1_png, fig2_png)
    logger.info("=" * 105)
    logger.info("BRANCH 3 ESM-2 COVERAGE EXPERIMENT COMPLETED SUCCESSFULLY!")
    logger.info("=" * 105)

    return {
        "status": "SUCCESS",
        "csv_path": str(csv_file),
        "fig1_png": str(fig1_png),
        "fig2_png": str(fig2_png),
        "total_rows": len(df_all),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Exp 3: Rare-Aware Weighted Facility Location in ESM-2 Mean-Centered Cosine Space (3 Alphas, k up to 115)")
    parser.add_argument(
        "--config",
        type=str,
        default="configs/config_exp3_esm_coverage_a1a.yaml",
        help="Path to YAML config",
    )
    parser.add_argument(
        "--force-recompute",
        action="store_true",
        help="Force recomputing similarity matrix and shuffles even if cache exists",
    )
    parser.add_argument(
        "--num-shuffles",
        type=int,
        default=None,
        help="Override number of random shuffles",
    )
    args = parser.parse_args()

    run_exp3_esm_coverage_a1a(
        config_path=args.config,
        force_recompute=args.force_recompute,
        override_shuffles=args.num_shuffles,
    )


if __name__ == "__main__":
    main()
