"""Thực hiện Công đoạn 2.1, 2.2, 2.3, 2.4 trong Tài liệu 1 và Module 4.4 trong Tài liệu 2:
Khảo sát Hàm Mục Tiêu Có Trọng Số Ưu Tiên Nhóm Hiếm (Rare-Aware Weighted Facility Location)
trên Tập Dữ Liệu Chuẩn Hóa Phương Án 3B (4,120 Chuỗi, 115 Phân Họ, 45 Họ Hiếm <= 5 Chuỗi)
theo Cơ Chế Truy Vấn Ngược Nội Phân Họ (Within-Subfamily Representative Query: S_k cap V_g -> V_g)
với 3 Mốc Alpha và 20 Mốc k đến 115.

Kịch bản thực hiện các nhiệm vụ khoa học cốt lõi:
1. Áp dụng Phương án 3B (exclude_unknown_subfamilies=True): Lọc bỏ hoàn toàn khối chưa định danh [A01.UPA],
   giữ lại 4,120 chuỗi sạch có nhãn phân họ chính thức thuộc 115 phân họ định danh (75 họ mã số + 40 họ mã chữ-số),
   trong đó có 45 phân họ hiếm (<= 5 chuỗi) và phân họ lớn nhất A01.009 (329 chuỗi).
2. Biến số DUY NHẤT thay đổi là hàm mục tiêu: w_v = (n_g)^(-alpha) với 3 mức alpha in {0.0, 0.5, 1.0} và budget_per_shuffle = 115.
3. Đánh giá theo cơ chế Truy vấn ngược nội phân họ (Within-Subfamily Query: S_{k,g} = S_k cap V_g -> V_g) qua Live BLASTp (E <= 1e-7):
   Một chuỗi đích v in V_g chỉ được tính là thu hồi thành công nếu có hit từ một đại diện s in S_k thuộc CÙNG phân họ g.
   Nếu S_k cap V_g = empty -> Sens_g^within(S_k) = 0.0%.
4. Đo đạc chính xác bộ 5 thước đo phân rã nhóm hiếm nội phân họ trên 20 mốc ngân sách k đến 115:
   - Overall Sensitivity BLAST (%)
   - Worst-Group Sensitivity BLAST (%)
   - Rare Sensitivity BLAST (%) (45 nhóm hiếm <= 5 chuỗi)
   - Macro-Average Sensitivity BLAST (%) (115 nhóm bình đẳng)
   - Zero-Sensitivity Subfamilies Count (số nhóm bị bỏ rơi 0% trên 115 nhóm)
5. Xuất duy nhất tệp CSV kết quả: outputs/tables/exp2_rare_weighted_a1a.csv (60 hàng = 3 alpha x 20 mốc k).
6. Xuất 3 biểu đồ công bố khoa học (PNG và SVG) đối chiếu song song k=11 và k=115: Pareto Trade-off, Metrics vs k, và Zero-Sensitivity vs Alpha.
"""

from __future__ import annotations

import argparse
import logging
import sys
import tempfile
import time
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
from src.selection.pruned_greedy import compute_subfamily_weights, run_pruned_greedy_1000_shuffles
from src.similarity.blast_similarity import BLASTSimilarityMatrix

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("exp2_rare_weighted_a1a")


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
) -> dict[str, int | float]:
    """Đo đạc Live BLASTp theo cơ chế Truy vấn ngược nội phân họ (Within-Subfamily Representative Query:
    S_{k,g} = S_k cap V_g -> V_g) và tính toán 5 chỉ số phân rã nhóm hiếm cho tập k đại diện.
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

    # Truy vấn ngược nội phân họ (Within-Subfamily Query: S_{k,g} = S_k cap V_g -> V_g):
    # Chỉ chấp nhận hit (q_id, s_id) khi q_id thuộc tập đại diện S_k và q_id, s_id thuộc CÙNG một phân họ.
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


def run_exp2_rare_weighted_a1a(
    config_path: str = "configs/config_exp2_rare_weighted_a1a.yaml",
    force_recompute: bool = False,
    override_shuffles: int | None = None,
) -> dict[str, object]:
    """Thực thi toàn bộ pipeline Nhánh 2: Khảo sát 3 mức alpha trên 20 mốc k (đến 115) với Pruned Greedy và Live BLASTp Nội Phân Họ."""
    logger.info("=" * 105)
    logger.info(
        "BRANCH 2: RARE-AWARE WEIGHTED FACILITY LOCATION ON CURATED PEPTIDASE A1 (4,120 SEQS, 115 SUBFAMILIES, WITHIN-SUBFAMILY QUERY)"
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
    prune_threshold: float = float(cfg.get("prune_threshold", 0.90))
    num_shuffles: int = int(override_shuffles if override_shuffles is not None else cfg.get("num_shuffles", 1000))
    seed: int = int(cfg.get("seed", 42))
    budget_per_shuffle: int = int(cfg.get("budget_per_shuffle", max(budget_k_list)))

    outputs_dir = parent_dir / str(cfg.get("output_dir", "outputs"))
    tables_dir = outputs_dir / "tables"
    figures_dir = outputs_dir / "figures"
    cache_dir = outputs_dir / "similarity_cache"

    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    # 2. Đọc và lọc QC chuỗi MEROPS A1A theo Phương án 3B (4,120 chuỗi sạch, 115 phân họ, 45 họ hiếm)
    logger.info("Loading and preprocessing MEROPS A1A FASTA dataset (Option 3B Curated)...")
    bundle_a1a = DatasetLoader.load_and_preprocess_dataset(
        cfg_file, override_fasta=str(fasta_path), override_dataset_name=dataset_name
    )
    records: list[ProteinRecord] = bundle_a1a.cleaned_records
    total_cleaned: int = len(records)
    seq_ids: list[str] = [r.id for r in records]
    id_to_record: dict[str, ProteinRecord] = {r.id: r for r in records}
    id_to_family: dict[str, str] = bundle_a1a.label_map
    rare_subfamilies: list[str] = bundle_a1a.rare_subfamilies

    family_to_ids: dict[str, list[str]] = defaultdict(list)
    for sid in seq_ids:
        fam = id_to_family.get(sid, "UNKNOWN")
        family_to_ids[fam].append(sid)

    total_subfamilies: int = len(family_to_ids)
    logger.info(
        "Dataset '%s': %d cleaned curated seqs, %d subfamilies, %d rare subfamilies (<= %d seqs).",
        dataset_name,
        total_cleaned,
        total_subfamilies,
        len(rare_subfamilies),
        int(cfg.get("rare_threshold", 5)),
    )

    # 3. Nạp ma trận tương đồng NCBI BLASTp All-vs-All (4,120 x 4,120)
    sim_cfg = cfg.get("blast_similarity_matrix", {})
    matrix_evalue: float = float(sim_cfg.get("evalue", 0.05))
    matrix_max_targets: int = int(sim_cfg.get("max_target_seqs", 100))
    matrix_word_size: int = int(sim_cfg.get("word_size", 3))
    matrix_threads: int = int(sim_cfg.get("num_threads", 24))

    blast_calc = BLASTSimilarityMatrix(
        blastp_bin_path=blast_bin_path,
        evalue=matrix_evalue,
        max_target_seqs=matrix_max_targets,
        word_size=matrix_word_size,
        num_threads=matrix_threads,
        cache_dir=cache_dir,
    )

    cleaned_fasta_path = cache_dir / f"{dataset_name}_cleaned_qc.fasta"
    if not cleaned_fasta_path.exists() or force_recompute:
        SeqIO.write(
            [SeqRecord(Seq(r.sequence), id=r.id, description=r.header) for r in records],
            cleaned_fasta_path,
            "fasta",
        )

    sim_matrix = blast_calc.get_similarity_matrix(
        fasta_path=cleaned_fasta_path,
        seq_ids=seq_ids,
        dataset_name=dataset_name,
        force_recompute=force_recompute,
        use_db=True,
    )
    logger.info(
        "BLASTp similarity matrix loaded: shape=%s, density=%.2f%%",
        str(sim_matrix.shape),
        float((sim_matrix > 0).mean() * 100.0),
    )

    # 4. Xây dựng cơ sở dữ liệu BLAST database cho Live BLASTp
    live_cfg = cfg.get("blast_live_coverage_evaluation", {})
    live_evalue: float = float(live_cfg.get("evalue", 1e-7))
    live_max_targets: int = int(live_cfg.get("max_target_seqs", 999999))
    live_threads: int = int(live_cfg.get("num_threads", 24))

    db_prefix = cache_dir / f"{dataset_name}_live_db"
    db_prefix = blast_calc.build_blast_db(fasta_path=cleaned_fasta_path, db_prefix=db_prefix)

    # 5. Vòng lặp chính qua 3 mốc tham số alpha
    all_rows: list[dict[str, object]] = []

    logger.info(
        "\nSTARTING SWEEP OVER %d ALPHA VALUES %s ACROSS %d BUDGET MILESTONES (budget_per_shuffle=%d)",
        len(alphas),
        alphas,
        len(budget_k_list),
        budget_per_shuffle,
    )
    alpha_pbar = tqdm(alphas, desc="Overall Alphas Progress", unit="alpha", dynamic_ncols=True)

    with tempfile.TemporaryDirectory() as tmpdir_str:
        tmpdir = Path(tmpdir_str)

        for alpha in alpha_pbar:
            alpha_str = f"{alpha:.2f}"
            alpha_pbar.set_postfix_str(f"alpha={alpha_str}")

            # 5.1. Tính vector trọng số mẫu cho alpha hiện tại
            weights = compute_subfamily_weights(
                seq_ids=seq_ids,
                id_to_family=id_to_family,
                alpha=alpha,
            )

            # 5.2. Chạy Pruned Greedy 90% (1,000-Shuffle Consensus Ranking) với budget_per_shuffle = 115
            cache_file = cache_dir / f"{dataset_name}_{num_shuffles}_shuffles_alpha_{alpha_str}.npz"
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
                desc_label=f"Alpha={alpha_str} (1,000 Shuffles, b={budget_per_shuffle})",
                show_progress=True,
            )
            greedy_runtime = round(time.perf_counter() - t_greedy_start, 2)

            # Truy vấn Live BLASTp 1 lần cho toàn bộ top k_max đại diện của alpha này (vì E-value của từng query độc lập 100%)
            k_max_eval = max(budget_k_list)
            top_kmax_ids = [sid for sid in consensus_ids[:k_max_eval] if sid in id_to_record]
            alpha_query_fasta = tmpdir / f"query_alpha_{alpha_str}_top{k_max_eval}.fasta"
            SeqIO.write(
                [SeqRecord(Seq(id_to_record[sid].sequence), id=sid, description=id_to_record[sid].header) for sid in top_kmax_ids],
                alpha_query_fasta,
                "fasta",
            )
            alpha_hit_pairs = blast_calc.retrieve_blast_hit_pairs(
                query_fasta=alpha_query_fasta,
                db_prefix=db_prefix,
                evalue=live_evalue,
                max_target_seqs=live_max_targets,
                num_threads=live_threads,
            )

            # 5.3. Đánh giá tuần tự qua 20 mốc ngân sách k bằng Live BLASTp Nội Phân Họ
            k_pbar = tqdm(
                budget_k_list,
                desc=f"Alpha={alpha_str} Within-Subfamily BLAST",
                unit="k",
                leave=False,
                dynamic_ncols=True,
            )

            for k_val in k_pbar:
                sub_selected_ids = consensus_ids[:k_val]
                metrics = evaluate_rare_aware_representatives(
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
                    precomputed_hit_pairs=alpha_hit_pairs,
                )

                row: dict[str, object] = {
                    "alpha": alpha,
                    "budget_k": int(k_val),
                    "overall_sensitivity_blast_pct": metrics["overall_sensitivity_blast_pct"],
                    "worst_group_sensitivity_blast_pct": metrics["worst_group_sensitivity_blast_pct"],
                    "rare_sensitivity_blast_pct": metrics["rare_sensitivity_blast_pct"],
                    "macro_sensitivity_blast_pct": metrics["macro_sensitivity_blast_pct"],
                    "zero_cov_subfamilies_count": metrics["zero_cov_subfamilies_count"],
                    "retrieved_hits_count": metrics["retrieved_hits_count"],
                    "total_cleaned_sequences": metrics["total_cleaned_sequences"],
                    "greedy_runtime_seconds": greedy_runtime,
                }
                all_rows.append(row)

                k_pbar.set_postfix({
                    "Overall": f"{metrics['overall_sensitivity_blast_pct']}%",
                    "Rare": f"{metrics['rare_sensitivity_blast_pct']}%",
                    "ZeroCov": metrics["zero_cov_subfamilies_count"],
                })

            for milestone_k in (11, max(budget_k_list)):
                matching_rows = [r for r in all_rows if r["alpha"] == alpha and r["budget_k"] == milestone_k]
                if matching_rows:
                    row_m = matching_rows[-1]
                    logger.info(
                        "ALPHA %s AT k=%3d -> Overall: %6.2f%% | Worst-Group: %5.2f%% | Rare: %5.2f%% | Macro: %5.2f%% | Zero-Cov Groups: %3d / %d",
                        alpha_str,
                        milestone_k,
                        row_m["overall_sensitivity_blast_pct"],
                        row_m["worst_group_sensitivity_blast_pct"],
                        row_m["rare_sensitivity_blast_pct"],
                        row_m["macro_sensitivity_blast_pct"],
                        row_m["zero_cov_subfamilies_count"],
                        total_subfamilies,
                    )

    # 6. Xuất DUY NHẤT một tệp CSV kết quả (60 dòng)
    df_all = pd.DataFrame(all_rows)
    csv_file = tables_dir / "exp2_rare_weighted_a1a.csv"
    df_all.to_csv(csv_file, index=False, encoding="utf-8-sig")
    logger.info("\nĐã lưu bảng số liệu thực nghiệm duy nhất (%d dòng) vào:\n  - %s", len(df_all), csv_file)

    # 7. Vẽ hệ thống 3 biểu đồ công bố khoa học (Đối chiếu song song k=11 và k=115)
    k_max = max(budget_k_list)
    logger.info("Đang tạo 3 biểu đồ xuất bản khoa học (đối chiếu k=11 và k=%d)...", k_max)
    compare_ks = [11, k_max] if 11 in budget_k_list and k_max != 11 else [k_max]

    # Biểu đồ 1: Pareto Trade-off Curve đối chiếu song song tại k=11 và k=115
    plt.rcParams["font.family"] = "DejaVu Sans"
    fig1, axes1 = plt.subplots(1, len(compare_ks), figsize=(11.5, 4.8), squeeze=False)

    for idx_panel, k_slice in enumerate(compare_ks):
        ax_p = axes1[0, idx_panel]
        df_slice = df_all[df_all["budget_k"] == k_slice].sort_values("alpha")
        alphas_plot = df_slice["alpha"].tolist()
        overall_slice = df_slice["overall_sensitivity_blast_pct"].tolist()
        worst_slice = df_slice["worst_group_sensitivity_blast_pct"].tolist()
        rare_slice = df_slice["rare_sensitivity_blast_pct"].tolist()
        macro_slice = df_slice["macro_sensitivity_blast_pct"].tolist()

        ax_p.plot(overall_slice, worst_slice, marker="o", color="#d62728", linewidth=2.8, markersize=8.5, label="Worst-Group Sensitivity")
        ax_p.plot(overall_slice, rare_slice, marker="s", color="#1f77b4", linewidth=2.4, linestyle="--", markersize=8.5, label=f"Rare Sensitivity ({len(rare_subfamilies)} groups $\\leq$ 5)")
        ax_p.plot(overall_slice, macro_slice, marker="^", color="#2ca02c", linewidth=2.4, linestyle=":", markersize=8.5, label=f"Macro Sensitivity ({total_subfamilies} groups)")

        if k_slice == 11:
            ax_p.annotate(r"$\alpha = 1.0$ (4.4%)", xy=(overall_slice[2], rare_slice[2]), xytext=(8, -3), textcoords="offset points",
                          fontsize=10.5, fontweight="bold", color="#1f77b4",
                          bbox=dict(boxstyle="round,pad=0.15", facecolor="white", alpha=0.9, edgecolor="none"))
            ax_p.annotate(r"$\alpha = 1.0$ (9.6%)", xy=(overall_slice[2], macro_slice[2]), xytext=(0, 9), textcoords="offset points",
                          fontsize=10.5, fontweight="bold", color="#2ca02c", ha="center",
                          bbox=dict(boxstyle="round,pad=0.15", facecolor="white", alpha=0.9, edgecolor="none"))
            ax_p.annotate(r"$\alpha = 0.5$ (9.6%)", xy=(overall_slice[1], macro_slice[1]), xytext=(0, 9), textcoords="offset points",
                          fontsize=10.5, fontweight="bold", color="#2ca02c", ha="center",
                          bbox=dict(boxstyle="round,pad=0.15", facecolor="white", alpha=0.9, edgecolor="none"))
            ax_p.annotate(r"$\alpha = 0.0$ (8.7%)", xy=(overall_slice[0], macro_slice[0]), xytext=(8, -3), textcoords="offset points",
                          fontsize=10.5, fontweight="bold", color="#2ca02c",
                          bbox=dict(boxstyle="round,pad=0.15", facecolor="white", alpha=0.9, edgecolor="none"))
            ax_p.annotate(r"Worst-Group = 0.0% ($\alpha = 0.0, 0.5, 1.0$)", xy=(32, 0), xytext=(0, -20), textcoords="offset points",
                          fontsize=10, color="#d62728", fontweight="bold", ha="center",
                          bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.9, edgecolor="#d62728", linewidth=0.5))
            ax_p.set_ylim(-6, 32)
            ax_p.set_xlim(22.5, 42)
            ax_p.legend(loc="upper left", frameon=True, fontsize=10, framealpha=0.9)
        elif k_slice == k_max:
            ax_p.annotate(r"$\mathbf{\alpha = 1.0}$ (91.1%)", xy=(overall_slice[2], rare_slice[2]), xytext=(8, 3), textcoords="offset points",
                          fontsize=11.5, fontweight="bold", color="#1f77b4",
                          bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.9, edgecolor="none"))
            ax_p.annotate(r"$\mathbf{\alpha = 1.0}$ (83.4%)", xy=(overall_slice[2], macro_slice[2]), xytext=(8, -14), textcoords="offset points",
                          fontsize=11, fontweight="bold", color="#2ca02c",
                          bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.9, edgecolor="none"))
            ax_p.legend(loc="lower left", bbox_to_anchor=(0.04, 0.14), frameon=True, fontsize=10, framealpha=0.9)
            ax_p.annotate(r"$\mathbf{\alpha = 0.5\ (59.1\%)}$", xy=(overall_slice[1], rare_slice[1]), xytext=(-12, 3), textcoords="offset points",
                          fontsize=11.5, fontweight="bold", color="#1f77b4", ha="right",
                          bbox=dict(boxstyle="round,pad=0.25", facecolor="#edf4fb", alpha=0.95, edgecolor="#1f77b4", linewidth=0.8))
            ax_p.annotate(r"$\alpha = 0.5$ (78.9%)", xy=(overall_slice[1], macro_slice[1]), xytext=(-12, 3), textcoords="offset points",
                          fontsize=11, fontweight="bold", color="#2ca02c", ha="right",
                          bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.9, edgecolor="none"))
            ax_p.annotate(r"$\alpha = 0.0$ (49.3%)", xy=(overall_slice[0], macro_slice[0]), xytext=(-12, -12), textcoords="offset points",
                          fontsize=11, fontweight="bold", color="#2ca02c", ha="right",
                          bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.9, edgecolor="none"))
            ax_p.annotate(r"$\alpha = 0.0$ (2.2%)", xy=(overall_slice[0], rare_slice[0]), xytext=(-12, 5), textcoords="offset points",
                          fontsize=11, fontweight="bold", color="#1f77b4", ha="right",
                          bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.9, edgecolor="none"))
            ax_p.set_ylim(-6, 105)
            ax_p.set_xlim(76, 97)

        panel_tag = chr(65 + idx_panel)
        ax_p.set_xlabel("Overall Within-Subfamily Sensitivity BLAST (%)", fontsize=11.5, fontweight="bold")
        ax_p.set_ylabel("Subfamily Sensitivity (%)", fontsize=11.5, fontweight="bold")
        ax_p.set_title(f"{panel_tag}. Within-Subfamily Pareto Trade-off at Budget k = {k_slice}", fontsize=12.5, fontweight="bold", pad=8)
        ax_p.grid(True, linestyle="--", alpha=0.55)
        ax_p.tick_params(axis="both", labelsize=10.5)

    plt.suptitle(
        f"Within-Subfamily Pareto Trade-off Comparison: Baseline Budget (k=11) vs. Full Subfamily Budget (k={k_max})",
        fontsize=13.5,
        fontweight="bold",
        y=0.99,
    )
    plt.tight_layout()

    fig1_png = figures_dir / "exp2_pareto_tradeoff.png"
    fig1_svg = figures_dir / "exp2_pareto_tradeoff.svg"
    fig1.savefig(fig1_png, dpi=300, bbox_inches="tight")
    fig1.savefig(fig1_svg, bbox_inches="tight")
    plt.close(fig1)

    # Biểu đồ 2: Diễn tiến 4 chỉ số theo ngân sách k (1..115) qua 3 mức alpha
    fig2, axes = plt.subplots(2, 2, figsize=(14, 10), sharex=True)
    palette = {0.0: "#7f7f7f", 0.25: "#2ca02c", 0.5: "#ff7f0e", 0.75: "#9467bd", 1.0: "#d62728"}

    for a_val in alphas:
        df_a = df_all[df_all["alpha"] == a_val].sort_values("budget_k")
        color = palette.get(a_val, "#1f77b4")
        label = f"alpha={a_val}"

        axes[0, 0].plot(df_a["budget_k"], df_a["overall_sensitivity_blast_pct"], marker="o", color=color, label=label, linewidth=2.0, markersize=5)
        axes[0, 1].plot(df_a["budget_k"], df_a["worst_group_sensitivity_blast_pct"], marker="s", color=color, label=label, linewidth=2.0, markersize=5)
        axes[1, 0].plot(df_a["budget_k"], df_a["rare_sensitivity_blast_pct"], marker="^", color=color, label=label, linewidth=2.0, markersize=5)
        axes[1, 1].plot(df_a["budget_k"], df_a["macro_sensitivity_blast_pct"], marker="d", color=color, label=label, linewidth=2.0, markersize=5)

    for ax_sub in axes.flat:
        if 11 in budget_k_list:
            ax_sub.axvline(11, color="#1f77b4", linestyle=":", linewidth=1.2, alpha=0.8, label="k=11 (Fig.8 Baseline)")
        ax_sub.axvline(k_max, color="#2ca02c", linestyle="--", linewidth=1.2, alpha=0.8, label=f"k={k_max} (G={total_subfamilies} Subfamilies)")

    axes[0, 0].set_title("A. Overall Within-Subfamily Sensitivity BLAST (%)", fontweight="bold")
    axes[0, 0].set_ylabel("Sensitivity (%)", fontweight="bold")
    axes[0, 0].grid(True, linestyle="--", alpha=0.5)
    axes[0, 0].legend(loc="lower right", fontsize=9)

    axes[0, 1].set_title("B. Worst-Group Within-Subfamily Sensitivity BLAST (%)", fontweight="bold")
    axes[0, 1].set_ylabel("Sensitivity (%)", fontweight="bold")
    axes[0, 1].grid(True, linestyle="--", alpha=0.5)

    axes[1, 0].set_title(f"C. Rare Subfamily Sensitivity ({len(rare_subfamilies)} groups <= 5 seqs) (%)", fontweight="bold")
    axes[1, 0].set_xlabel(f"Representative Budget $k$ (1 to {k_max})", fontweight="bold")
    axes[1, 0].set_ylabel("Sensitivity (%)", fontweight="bold")
    axes[1, 0].grid(True, linestyle="--", alpha=0.5)

    axes[1, 1].set_title(f"D. Macro-Average Sensitivity ({total_subfamilies} groups) (%)", fontweight="bold")
    axes[1, 1].set_xlabel(f"Representative Budget $k$ (1 to {k_max})", fontweight="bold")
    axes[1, 1].set_ylabel("Sensitivity (%)", fontweight="bold")
    axes[1, 1].grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    fig2_png = figures_dir / "exp2_metrics_vs_k.png"
    fig2_svg = figures_dir / "exp2_metrics_vs_k.svg"
    fig2.savefig(fig2_png, dpi=300)
    fig2.savefig(fig2_svg)
    plt.close(fig2)

    # Biểu đồ 3: Grouped Bar Chart đối chiếu song song số phân họ 0% Sensitivity tại k=11 và k=115
    fig3, ax3 = plt.subplots(figsize=(8.5, 5.8))
    x_indices = np.arange(len(alphas))
    bar_width = 0.35

    df_k11 = df_all[df_all["budget_k"] == 11].sort_values("alpha")
    df_kmax = df_all[df_all["budget_k"] == k_max].sort_values("alpha")

    zero_k11 = df_k11["zero_cov_subfamilies_count"].tolist() if not df_k11.empty else [0] * len(alphas)
    zero_kmax = df_kmax["zero_cov_subfamilies_count"].tolist() if not df_kmax.empty else [0] * len(alphas)

    bars_11 = ax3.bar(x_indices - bar_width / 2, zero_k11, width=bar_width, color="#1f77b4", edgecolor="black", label="Budget k = 11 (Baseline Limit)")
    bars_max = ax3.bar(x_indices + bar_width / 2, zero_kmax, width=bar_width, color="#ff7f0e", edgecolor="black", label=f"Budget k = {k_max} (Full Subfamily Budget)")

    for bar_group in (bars_11, bars_max):
        for bar in bar_group:
            height = int(bar.get_height())
            ax3.annotate(
                f"{height} / {total_subfamilies}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                fontweight="bold",
                fontsize=9,
            )

    ax3.set_xticks(x_indices)
    ax3.set_xticklabels([f"$\\alpha = {a:.1f}$" for a in alphas], fontsize=11, fontweight="bold")
    ax3.set_xlabel("Rareness Penalty Exponent $\\alpha$", fontsize=12, fontweight="bold")
    ax3.set_ylabel("Count of Subfamilies with 0.0% Within-Subfamily Sensitivity", fontsize=11, fontweight="bold")
    ax3.set_title(f"Zero-Sensitivity Subfamilies vs. $\\alpha$: Budget k=11 vs. k={k_max}", fontsize=13, fontweight="bold", pad=12)
    max_z = max(zero_k11 + zero_kmax) if (zero_k11 or zero_kmax) else 10
    ax3.set_ylim(0, max(max_z + 12, 20))
    ax3.grid(True, linestyle="--", alpha=0.5, axis="y")
    ax3.legend(loc="upper right", frameon=True, fontsize=10)
    plt.tight_layout()

    fig3_png = figures_dir / "exp2_zero_cov_vs_alpha.png"
    fig3_svg = figures_dir / "exp2_zero_cov_vs_alpha.svg"
    fig3.savefig(fig3_png, dpi=300)
    fig3.savefig(fig3_svg)
    plt.close(fig3)

    logger.info("Saved 3 publication figures to:\n  - %s\n  - %s\n  - %s", fig1_png, fig2_png, fig3_png)
    logger.info("=" * 105)
    logger.info("BRANCH 2 RARE-AWARE FACILITY LOCATION EXPERIMENT COMPLETED SUCCESSFULLY!")
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
    parser = argparse.ArgumentParser(description="Exp 2: Rare-Aware Weighted Facility Location on Curated Peptidase A1 (3 Alphas, k up to 115)")
    parser.add_argument(
        "--config",
        type=str,
        default="configs/config_exp2_rare_weighted_a1a.yaml",
        help="Path to YAML config",
    )
    parser.add_argument(
        "--force-recompute",
        action="store_true",
        help="Force recomputing shuffles and live BLAST even if cache exists",
    )
    parser.add_argument(
        "--num-shuffles",
        type=int,
        default=None,
        help="Override number of random shuffles",
    )
    args = parser.parse_args()

    run_exp2_rare_weighted_a1a(
        config_path=args.config,
        force_recompute=args.force_recompute,
        override_shuffles=args.num_shuffles,
    )


if __name__ == "__main__":
    main()
