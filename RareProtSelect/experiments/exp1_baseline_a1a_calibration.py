"""Thực hiện Công đoạn 1 trong Tài liệu 1 và Module 1 trong Tài liệu 2:
Tái hiện Hình 8 Bài báo gốc trên Peptidase A1 (Baseline Replication of Figure 8 on MEROPS A1A).

Kịch bản thực hiện duy nhất nhiệm vụ khoa học cốt lõi:
1. Tái hiện trung thực 100% Hình 8 (Figure 8 Panel A) trong bài báo nền (Nguyen et al., Nature Sci Rep 2025)
   trên 13,847 chuỗi Peptidase A1 (MEROPS A1A) qua thuật toán Pruned Greedy 90% kết hợp 1,000 lần xáo trộn
   ngẫu nhiên (1,000-Shuffle Consensus Ranking) theo đúng Algorithm 1 và mã nguồn gốc Greedy.R.
2. Khảo sát đúng 11 mốc ngân sách nguyên văn trên trục hoành của Hình 8: k in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11].
3. Đo lường DUY NHẤT một thước đo chính thống của bài báo gốc:
   - Overall Sensitivity BLAST (%): Tỷ lệ chuỗi được tìm thấy khi dùng tập đại diện S làm query Live BLAST (E <= 1e-7).
4. Xuất bảng dữ liệu chuẩn hóa (CSV, JSON, MD) và biểu đồ 1 panel xuất bản (PNG, SVG) đối chiếu 1-1 với Hình 8 Panel A.
"""

from __future__ import annotations

import argparse
import logging
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import yaml
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

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
from src.similarity.blast_similarity import BLASTSimilarityMatrix
from src.utils.exporter import ResultExporter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("exp1_baseline_a1a_calibration")


def run_pruned_greedy_1000_shuffles(
    sim_matrix: np.ndarray,
    seq_ids: list[str],
    prune_threshold: float = 0.90,
    num_shuffles: int = 1000,
    seed: int = 42,
    budget_per_shuffle: int = 15,
    cache_path: Path | None = None,
    force_recompute: bool = False,
) -> tuple[list[str], pd.DataFrame]:
    """Cài đặt chính xác 100% thuật toán 1,000-Shuffle Consensus Ranking từ Greedy.R (Nguyen et al., 2025):
    - Trong mỗi vòng j in 1..num_shuffles:
      1. Hoán vị ngẫu nhiên danh sách ứng viên để phá vỡ thế hòa khách quan.
      2. Chạy thuật toán Greedy cắt tỉa cứng với prune_threshold = 0.90.
      3. Ghi nhận danh sách repID và rank thứ tự chọn (1, 2, ...).
    - Tổng hợp kết quả: Tính tần suất xuất hiện (count) và tổng thứ hạng (rank_sum).
    - Sắp xếp giảm dần theo count, tăng dần theo rank_sum (order(-count, rank_sum)) để sinh bảng xếp hạng đồng thuận.

    Tối ưu hóa tính toán: Hỗ trợ tăng tốc bằng PyTorch CUDA (nếu có GPU) hoặc NumPy BLAS đa luồng
    cho phép hoàn thành 1,000 lần xáo trộn ma trận 13,307 x 13,307 trong vài phút.

    Args:
        sim_matrix: Ma trận tương đồng chuỗi BLASTp Identity không âm (N, N).
        seq_ids: Danh sách protein IDs theo thứ tự ban đầu.
        prune_threshold: Ngưỡng cắt tỉa tương đồng (mặc định 0.90 theo Greedy.R).
        num_shuffles: Số lần xáo trộn ngẫu nhiên (mặc định 1000 theo Greedy.R).
        seed: Hạt giống ngẫu nhiên để tái hiện kết quả.
        budget_per_shuffle: Số đại diện tối đa cần chọn mỗi vòng (mặc định 15, đủ bao phủ 11 mốc của Hình 8).
        cache_path: Đường dẫn lưu cache kết quả xáo trộn.
        force_recompute: Bắt buộc tính lại từ đầu kể cả khi đã có cache.

    Returns:
        tuple[list[str], pd.DataFrame]:
            - consensus_ids: Danh sách protein IDs sắp xếp theo mức độ đồng thuận toàn cục.
            - df_agg: Bảng DataFrame tổng hợp count và rank_sum của từng protein.
    """
    if cache_path is not None and cache_path.exists() and not force_recompute:
        logger.info("Loading cached consensus ranking from: %s", cache_path.name)
        cached_data = np.load(cache_path, allow_pickle=True)
        consensus_ids = list(cached_data["consensus_ids"])
        df_agg = pd.DataFrame({
            "repID": list(cached_data["rep_ids"]),
            "count": list(cached_data["counts"]),
            "rank_sum": list(cached_data["rank_sums"]),
        })
        logger.info("Loaded consensus ranking for %d sequences from cache.", len(consensus_ids))
        return consensus_ids, df_agg

    n = len(seq_ids)
    rng = np.random.default_rng(seed)
    all_results: list[dict[str, object]] = []

    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info(
        "Executing %d-Shuffle Consensus Ranking on %s (prune_threshold=%.2f, n=%d, budget_per_shuffle=%d)...",
        num_shuffles,
        device.upper(),
        prune_threshold,
        n,
        budget_per_shuffle,
    )
    t_start = time.perf_counter()

    use_gpu = (device == "cuda")
    if use_gpu:
        m_tensor = torch.from_numpy(sim_matrix).to(device=device, dtype=torch.float32)
        weights_tensor = torch.ones(n, device=device, dtype=torch.float32)
    else:
        m_arr = np.asarray(sim_matrix, dtype=np.float32)
        weights_arr = np.ones(n, dtype=np.float32)

    for j in range(num_shuffles):
        if (j + 1) % 100 == 0 or j == 0 or (j + 1) == num_shuffles:
            elapsed = time.perf_counter() - t_start
            logger.info("Progress: Shuffle %d / %d (elapsed: %.1fs)...", j + 1, num_shuffles, elapsed)

        # Hoán vị ngẫu nhiên danh sách ứng viên
        perm = rng.permutation(n)

        if use_gpu:
            perm_t = torch.from_numpy(perm).to(device=device)
            m_perm = m_tensor[perm_t][:, perm_t]
            w_perm = weights_tensor[perm_t]

            current_max_sim = torch.zeros(n, device=device, dtype=torch.float32)
            active = torch.ones(n, device=device, dtype=torch.bool)
            selected_local: list[int] = []

            for _ in range(budget_per_shuffle):
                cand_indices = torch.where(active)[0]
                if len(cand_indices) == 0:
                    break
                sub_m = m_perm[:, cand_indices]
                diff = torch.clamp(sub_m - current_max_sim.unsqueeze(1), min=0.0)
                gains = torch.matmul(w_perm, diff)
                best_sub_idx = torch.argmax(gains)
                best_cand = cand_indices[best_sub_idx].item()
                selected_local.append(best_cand)

                current_max_sim = torch.maximum(current_max_sim, m_perm[:, best_cand])
                active = active & (m_perm[best_cand, :] <= prune_threshold)

            for rank, local_idx in enumerate(selected_local, start=1):
                orig_idx = int(perm[local_idx])
                rep_id = seq_ids[orig_idx]
                all_results.append({"repID": rep_id, "rank": rank})
        else:
            m_perm = m_arr[perm][:, perm]
            w_perm = weights_arr[perm]

            current_max_sim = np.zeros(n, dtype=np.float32)
            active = np.ones(n, dtype=bool)
            selected_local = []

            for _ in range(budget_per_shuffle):
                cand_indices = np.where(active)[0]
                if len(cand_indices) == 0:
                    break
                sub_m = m_perm[:, cand_indices]
                diff = np.maximum(0.0, sub_m - current_max_sim[:, None])
                gains = w_perm @ diff
                best_sub_idx = np.argmax(gains)
                best_cand = cand_indices[best_sub_idx]
                selected_local.append(best_cand)

                current_max_sim = np.maximum(current_max_sim, m_perm[:, best_cand])
                active = active & (m_perm[best_cand, :] <= prune_threshold)

            for rank, local_idx in enumerate(selected_local, start=1):
                orig_idx = int(perm[local_idx])
                rep_id = seq_ids[orig_idx]
                all_results.append({"repID": rep_id, "rank": rank})

    if use_gpu:
        torch.cuda.synchronize()

    total_time = time.perf_counter() - t_start
    logger.info("Completed %d shuffles in %.2f seconds (%.3fs per shuffle).", num_shuffles, total_time, total_time / num_shuffles)

    df_res = pd.DataFrame(all_results)
    df_agg = (
        df_res.groupby("repID")
        .agg(rank_sum=("rank", "sum"), count=("rank", "count"))
        .reset_index()
    )
    # Khớp 100% Greedy.R dòng 161: df <- df[order(-df$count, df$rank), ]
    df_agg = df_agg.sort_values(by=["count", "rank_sum"], ascending=[False, True]).reset_index(drop=True)
    selected_in_shuffles = df_agg["repID"].tolist()

    # Bổ sung các chuỗi chưa từng được chọn vào cuối danh sách
    seen_set = set(selected_in_shuffles)
    remaining_ids = [sid for sid in seq_ids if sid not in seen_set]
    consensus_ids = selected_in_shuffles + remaining_ids

    if cache_path is not None:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            cache_path,
            consensus_ids=np.array(consensus_ids, dtype=object),
            rep_ids=np.array(df_agg["repID"].tolist(), dtype=object),
            counts=np.array(df_agg["count"].tolist(), dtype=int),
            rank_sums=np.array(df_agg["rank_sum"].tolist(), dtype=int),
            metadata={
                "num_shuffles": num_shuffles,
                "prune_threshold": prune_threshold,
                "total_time_seconds": total_time,
                "seed": seed,
            },
        )
        logger.info("Saved consensus ranking cache to: %s", cache_path.name)

    return consensus_ids, df_agg


def load_published_fig8a_benchmark(csv_path: Path) -> dict[int, float]:
    """Đọc tệp CSV Nguồn sự thật (SSOT) chứa 11 mốc ước lượng từ Hình 8 Panel A (Nguyen et al., 2025).

    Args:
        csv_path: Đường dẫn tuyệt đối đến tệp nguyen2025_fig8a_benchmark.csv.

    Returns:
        dict[int, float]: Từ điển ánh xạ mốc ngân sách k (int) -> giá trị độ nhạy ước lượng (%) (float).

    Raises:
        FileNotFoundError: Nếu tệp CSV Nguồn sự thật không tồn tại tại csv_path.
        ValueError: Nếu thiếu cột bắt buộc ('budget_k', 'published_fig8_sensitivity_pct') hoặc dữ liệu rỗng.
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"Không tìm thấy tệp CSV Nguồn sự thật bài báo gốc: {csv_path}")

    df_bench = pd.read_csv(csv_path)
    required_cols = {"budget_k", "published_fig8_sensitivity_pct"}
    if not required_cols.issubset(set(df_bench.columns)):
        raise ValueError(
            f"Tệp CSV chuẩn {csv_path.name} thiếu cột bắt buộc. Cần có: {required_cols}"
        )
    if df_bench.empty:
        raise ValueError(f"Tệp CSV chuẩn {csv_path.name} không có dữ liệu.")

    bench_map: dict[int, float] = {}
    for _, row in df_bench.iterrows():
        k_int = int(row["budget_k"])
        val_float = round(float(row["published_fig8_sensitivity_pct"]), 2)
        bench_map[k_int] = val_float

    return bench_map


def run_exp1_baseline_a1a_calibration(
    config_path: str = "configs/config_exp1_baseline_a1a_calibration.yaml",
    force_recompute: bool = False,
    override_shuffles: int | None = None,
) -> dict[str, object]:
    """Thực thi kịch bản Nhánh 1: Tái hiện Hình 8 Bài báo gốc trên Peptidase A1 (MEROPS A1A)."""
    logger.info("=" * 90)
    logger.info("BRANCH 1: BASELINE REPLICATION OF FIGURE 8 ON PEPTIDASE A1 (MEROPS A1A)")
    logger.info("=" * 90)

    # 1. Nạp cấu hình YAML
    cfg_file = Path(config_path)
    if not cfg_file.exists():
        cfg_file = parent_dir / config_path
    if not cfg_file.exists():
        raise FileNotFoundError(f"Không tìm thấy tệp cấu hình: {config_path}")

    with open(cfg_file, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    logger.info("Loaded config from: %s", cfg_file)

    dataset_name: str = cfg.get("dataset_name", "MEROPS_A1A")
    fasta_path: Path = Path(cfg.get("fasta_path", "../baseline_repo/MEROPS_A1A.fasta"))
    if not fasta_path.is_absolute():
        fasta_path = (parent_dir / fasta_path).resolve()

    blast_bin_path: Path = Path(cfg.get("blast_bin_path", "tools/blast/bin/blastp.exe"))
    if not blast_bin_path.is_absolute():
        blast_bin_path = (parent_dir / blast_bin_path).resolve()

    # Dải ngân sách duy nhất: đúng 11 mốc nguyên văn Hình 8
    budget_k_list: list[int] = [int(k) for k in cfg.get("budget_k_list", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])]
    prune_threshold: float = float(cfg.get("prune_threshold", 0.90))
    num_shuffles: int = int(override_shuffles if override_shuffles is not None else cfg.get("num_shuffles", 1000))
    seed: int = int(cfg.get("seed", 42))

    outputs_dir = parent_dir / cfg.get("output_dir", "outputs")
    tables_dir = outputs_dir / "tables"
    figures_dir = outputs_dir / "figures"
    cache_dir = outputs_dir / "similarity_cache"

    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    # Nạp tệp CSV Nguồn sự thật 11 mốc Hình 8 Panel A (Nguyen et al., 2025)
    bench_csv_cfg = str(cfg.get("published_benchmark_csv", "outputs/tables/nguyen2025_fig8a_benchmark.csv"))
    bench_csv_path = Path(bench_csv_cfg)
    if not bench_csv_path.is_absolute():
        bench_csv_path = (parent_dir / bench_csv_path).resolve()
    published_benchmarks = load_published_fig8a_benchmark(bench_csv_path)
    logger.info("Loaded %d published Fig. 8A benchmark points from SSOT CSV: %s", len(published_benchmarks), bench_csv_path.name)

    # 2. Đọc và lọc QC chuỗi MEROPS A1A
    logger.info("Loading and preprocessing MEROPS A1A FASTA dataset...")
    bundle_a1a = DatasetLoader.load_and_preprocess_dataset(
        cfg_file, override_fasta=str(fasta_path), override_dataset_name=dataset_name
    )
    records = bundle_a1a.cleaned_records
    total_cleaned: int = len(records)
    total_raw: int = bundle_a1a.num_raw
    seq_ids = [r.id for r in records]
    id_to_record = {r.id: r for r in records}

    logger.info(
        "Dataset '%s': %d cleaned sequences (from %d raw).",
        dataset_name,
        total_cleaned,
        total_raw,
    )

    # 3. Nạp ma trận tương đồng NCBI BLASTp All-vs-All
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
        SeqIO.write([SeqRecord(Seq(r.sequence), id=r.id, description=r.header) for r in records], cleaned_fasta_path, "fasta")

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
        (sim_matrix > 0).mean() * 100,
    )

    # 4. Thực thi 1,000-Shuffle Consensus Ranking
    consensus_cache_file = cache_dir / f"{dataset_name}_{num_shuffles}_shuffles_consensus.npz"
    consensus_ids, df_consensus = run_pruned_greedy_1000_shuffles(
        sim_matrix=sim_matrix,
        seq_ids=seq_ids,
        prune_threshold=prune_threshold,
        num_shuffles=num_shuffles,
        seed=seed,
        budget_per_shuffle=15,
        cache_path=consensus_cache_file,
        force_recompute=force_recompute,
    )

    # 5. Xây dựng cơ sở dữ liệu BLAST database phục vụ đo lường Live BLAST Sensitivity
    live_cfg = cfg.get("blast_live_coverage_evaluation", {})
    live_evalue: float = float(live_cfg.get("evalue", 1e-7))
    live_max_targets: int = int(live_cfg.get("max_target_seqs", 999999))
    live_threads: int = int(live_cfg.get("num_threads", 24))

    db_prefix = cache_dir / f"{dataset_name}_live_db"
    db_prefix = blast_calc.build_blast_db(fasta_path=cleaned_fasta_path, db_prefix=db_prefix)

    # 6. Đánh giá tuần tự qua 11 mốc ngân sách k nguyên văn Hình 8
    logger.info("\nEvaluating Consensus Representatives across 11 budget points k in %s...", budget_k_list)
    rows: list[dict[str, object]] = []

    with tempfile.TemporaryDirectory() as tmpdir_str:
        tmpdir = Path(tmpdir_str)

        for k_val in budget_k_list:
            selected_ids = consensus_ids[:k_val]
            selected_records = [id_to_record[sid] for sid in selected_ids if sid in id_to_record]

            # Ghi file query FASTA cho tập k đại diện
            query_fasta = tmpdir / f"query_k{k_val}.fasta"
            SeqIO.write(
                [SeqRecord(Seq(r.sequence), id=r.id, description=r.header) for r in selected_records],
                query_fasta,
                "fasta",
            )

            # Thực thi blastp truy xuất độ nhạy trên toàn bộ DB
            hits = blast_calc.retrieve_blast_hits(
                query_fasta=query_fasta,
                db_prefix=db_prefix,
                evalue=live_evalue,
                max_target_seqs=live_max_targets,
                num_threads=live_threads,
            )

            covered_clean_ids = set(hits) & set(seq_ids)
            clean_sens = float(len(covered_clean_ids) / total_cleaned) if total_cleaned > 0 else 0.0
            clean_sens_pct = round(clean_sens * 100.0, 2)

            published_val = published_benchmarks.get(int(k_val), None)
            deviation = round(clean_sens_pct - published_val, 2) if published_val is not None else None

            row_data: dict[str, object] = {
                "budget_k": int(k_val),
                "num_selected": len(selected_ids),
                "overall_sensitivity_blast_pct": clean_sens_pct,
                "retrieved_hits_count": len(covered_clean_ids),
                "total_cleaned_sequences": total_cleaned,
                "published_fig8_sensitivity_pct": published_val,
                "deviation_pct": deviation,
            }
            rows.append(row_data)

            dev_str = f" (Fig.8A: {published_val:.1f}%, deviation: {deviation:+.2f}%)" if published_val is not None and deviation is not None else ""
            logger.info(
                "k=%2d: Overall Sensitivity BLAST = %6.2f%% (%d/%d seqs)%s",
                k_val,
                clean_sens_pct,
                len(covered_clean_ids),
                total_cleaned,
                dev_str,
            )

    df_results = pd.DataFrame(rows)

    # 7. Xuất bảng kết quả ra CSV, JSON, MD
    csv_file = tables_dir / "exp1_baseline_a1a_calibration.csv"
    json_file = tables_dir / "exp1_baseline_a1a_calibration.json"
    md_file = tables_dir / "exp1_baseline_a1a_calibration.md"

    df_results.to_csv(csv_file, index=False, encoding="utf-8-sig")
    ResultExporter.export_to_json(rows, json_file)

    row_k1 = df_results[df_results["budget_k"] == 1].iloc[0]
    row_k5 = df_results[df_results["budget_k"] == 5].iloc[0]
    row_k10 = df_results[df_results["budget_k"] == 10].iloc[0]
    row_k11 = df_results[df_results["budget_k"] == 11].iloc[0]

    with open(md_file, "w", encoding="utf-8") as f:
        f.write("# Bảng Thực Nghiệm Nhánh 1: Tái Hiện Hình 8 Bài Báo Gốc Trên Peptidase A1 (MEROPS A1A)\n\n")
        f.write("*(Thực hiện Công đoạn 1 trong Tài liệu 1 và Module 1 trong Tài liệu 2)*\n\n")
        f.write("### 1. Bảng Số Liệu Đo Đạc Thực Nghiệm (1,000-Shuffle Consensus Ranking)\n\n")
        f.write(df_results.to_markdown(index=False))
        f.write("\n\n### 2. Đối Chiếu Định Lượng Trực Diện Với 11 Mốc Hình 8 Panel A (Nguyen et al., 2025)\n\n")
        f.write(f"- Nguồn sự thật 11 mốc ước lượng từ Hình 8 Panel A: `outputs/tables/nguyen2025_fig8a_benchmark.csv`\n")
        f.write(f"- **Mốc $k = 1$**: Đạt **{row_k1['overall_sensitivity_blast_pct']}%** (Hình 8A: $\\approx {row_k1['published_fig8_sensitivity_pct']}\\%$, lệch: {row_k1['deviation_pct']:+.2f}%)\n")
        f.write(f"- **Mốc $k = 5$**: Đạt **{row_k5['overall_sensitivity_blast_pct']}%** (Hình 8A: $\\approx {row_k5['published_fig8_sensitivity_pct']}\\%$, lệch: {row_k5['deviation_pct']:+.2f}%)\n")
        f.write(f"- **Mốc $k = 10$**: Đạt **{row_k10['overall_sensitivity_blast_pct']}%** (Hình 8A: $\\approx {row_k10['published_fig8_sensitivity_pct']}\\%$, lệch: {row_k10['deviation_pct']:+.2f}%)\n")
        f.write(f"- **Mốc $k = 11$**: Đạt **{row_k11['overall_sensitivity_blast_pct']}%** (Hình 8A: $\\approx {row_k11['published_fig8_sensitivity_pct']}\\%$, lệch: {row_k11['deviation_pct']:+.2f}%)\n")

    logger.info("Saved result tables to:\n  - %s\n  - %s\n  - %s", csv_file, json_file, md_file)

    # 8. Vẽ đồ thị xuất bản 1 panel duy nhất đối chiếu trực tiếp với 11 mốc Hình 8 Panel A
    fig, ax = plt.subplots(figsize=(8, 5.5))

    ks = df_results["budget_k"].tolist()
    sens_blast = df_results["overall_sensitivity_blast_pct"].tolist()
    pub_vals = df_results["published_fig8_sensitivity_pct"].tolist()

    ax.plot(
        ks,
        sens_blast,
        marker="o",
        color="#1f77b4",
        linewidth=2.5,
        markersize=7,
        label="Our Reproduction: Pruned Greedy 90% (Live BLAST Sensitivity)",
    )

    # Đường đối chuẩn 11 điểm của tác giả trong Hình 8 Panel A (nạp từ nguyen2025_fig8a_benchmark.csv)
    ax.plot(
        ks,
        pub_vals,
        marker="s",
        linestyle="--",
        color="#d62728",
        linewidth=1.8,
        markersize=6,
        zorder=5,
        label="Nguyen et al. (2025) Fig. 8A (11 Digitized Points)",
    )

    ax.axhline(90.0, color="gray", linestyle=":", linewidth=1.2, label="90% Sensitivity Threshold")
    ax.axvline(10, color="darkorange", linestyle=":", linewidth=1.2, label="k = 10 (>90% target)")

    ax.set_xlabel("Representative Budget $k$", fontsize=12, fontweight="bold")
    ax.set_ylabel("Overall Sensitivity BLAST (%) on Peptidase A1", fontsize=12, fontweight="bold")
    ax.set_title("Figure 8A Reproduction: Sensitivity vs. Budget $k$ on MEROPS A1A", fontsize=13, fontweight="bold", pad=12)
    ax.set_xticks(budget_k_list)
    ax.set_ylim(75, 100)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="lower right", frameon=True, fontsize=10)

    # Chú thích giá trị
    for k_val, s_val in zip(ks, sens_blast):
        ax.annotate(
            f"{s_val:.1f}%",
            xy=(k_val, s_val),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            fontsize=8,
            fontweight="bold",
        )

    plt.tight_layout()
    fig_png = figures_dir / "exp1_a1a_sensitivity_vs_k.png"
    fig_svg = figures_dir / "exp1_a1a_sensitivity_vs_k.svg"
    fig.savefig(fig_png, dpi=300)
    fig.savefig(fig_svg)
    plt.close(fig)

    logger.info("Saved publication figures to:\n  - %s\n  - %s", fig_png, fig_svg)
    logger.info("\n" + "=" * 90)
    logger.info("BRANCH 1 BASELINE A1A CALIBRATION COMPLETED SUCCESSFULLY!")
    logger.info("=" * 90)

    return {
        "status": "SUCCESS",
        "csv_path": str(csv_file),
        "json_path": str(json_file),
        "md_path": str(md_file),
        "fig_png": str(fig_png),
        "fig_svg": str(fig_svg),
        "sensitivity_k1": float(row_k1["overall_sensitivity_blast_pct"]),
        "sensitivity_k5": float(row_k5["overall_sensitivity_blast_pct"]),
        "sensitivity_k10": float(row_k10["overall_sensitivity_blast_pct"]),
        "sensitivity_k11": float(row_k11["overall_sensitivity_blast_pct"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Exp 1: Baseline Replication of Figure 8 on Peptidase A1 (MEROPS A1A)")
    parser.add_argument(
        "--config",
        type=str,
        default="configs/config_exp1_baseline_a1a_calibration.yaml",
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

    run_exp1_baseline_a1a_calibration(
        config_path=args.config,
        force_recompute=args.force_recompute,
        override_shuffles=args.num_shuffles,
    )


if __name__ == "__main__":
    main()
