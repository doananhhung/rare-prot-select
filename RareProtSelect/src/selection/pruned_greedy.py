"""Thực hiện Công đoạn 2.1, 2.2 trong Tài liệu 1 và Module 3.4 trong Tài liệu 2:
Thuật toán Pruned Greedy 90% (1,000-Shuffle Consensus Ranking) có trọng số ưu tiên nhóm hiếm
(Rare-Aware Weighted Facility Location) kết hợp giám sát thanh tiến trình tqdm.
"""

from __future__ import annotations

import logging
import time
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from tqdm import tqdm

logger = logging.getLogger("src.selection.pruned_greedy")


def compute_subfamily_weights(
    seq_ids: list[str],
    id_to_family: dict[str, str],
    alpha: float,
) -> np.ndarray:
    """Tính toán vector trọng số mẫu w_v = (n_{g(v)})^(-alpha) cho từng protein.

    Thực hiện Công đoạn 2.1 trong Tài liệu 1:
    - Khi alpha = 0.00: w_v = 1.0 cho mọi v (suy biến về bài toán không trọng số của Nguyen et al.).
    - Khi alpha = 0.50: w_v = 1 / sqrt(n_g) (cân bằng Pareto giữa độ nhạy toàn cục và nhóm hiếm).
    - Khi alpha = 1.00: w_v = 1 / n_g (tổng trọng số của mỗi phân họ bằng 1.0, công bằng tuyệt đối).

    Args:
        seq_ids: Danh sách ID protein của tập dữ liệu sạch V.
        id_to_family: Từ điển ánh xạ từ protein ID sang mã phân họ (subfamily).
        alpha: Hệ số phạt quy mô nhóm (Rareness Penalty Exponent) trong khoảng [0.0, 1.0].

    Returns:
        np.ndarray: Mảng 1 chiều float32 có kích thước len(seq_ids) chứa trọng số w_v.
    """
    if alpha < 0.0:
        raise ValueError(f"Hệ số alpha không được âm, nhận được: {alpha}")

    # Đếm số lượng protein trong từng phân họ
    family_list = [id_to_family.get(sid, "UNKNOWN") for sid in seq_ids]
    family_counts = Counter(family_list)

    if alpha == 0.0:
        weights = np.ones(len(seq_ids), dtype=np.float32)
        return weights

    weights_list: list[float] = []
    for sid, fam in zip(seq_ids, family_list):
        n_g = family_counts[fam]
        w_v = float(n_g ** (-alpha))
        weights_list.append(w_v)

    weights = np.array(weights_list, dtype=np.float32)

    # Đảm bảo không có NaN hoặc Inf
    if not np.all(np.isfinite(weights)):
        raise ValueError("Phát hiện giá trị không hợp lệ (NaN hoặc Inf) trong vector trọng số!")

    return weights


def run_pruned_greedy_1000_shuffles(
    sim_matrix: np.ndarray,
    seq_ids: list[str],
    prune_threshold: float = 0.90,
    num_shuffles: int = 1000,
    sample_weights: np.ndarray | None = None,
    seed: int = 42,
    budget_per_shuffle: int = 76,
    cache_path: Path | None = None,
    force_recompute: bool = False,
    desc_label: str = "Pruned Greedy",
    show_progress: bool = True,
) -> tuple[list[str], pd.DataFrame]:
    """Cài đặt thuật toán 1,000-Shuffle Consensus Ranking có trọng số mẫu:
    - Trong mỗi vòng j in 1..num_shuffles:
      1. Hoán vị ngẫu nhiên danh sách ứng viên để phá vỡ thế hòa khách quan.
      2. Chạy thuật toán Greedy cắt tỉa cứng với prune_threshold = 0.90 và tối ưu hóa hàm mục tiêu có trọng số:
         Delta(u | S) = sum_{v in V} w_v * max(0, sim(u, v) - max_{s in S} sim(s, v))
      3. Ghi nhận danh sách repID và rank thứ tự chọn (1, 2, ..., budget_per_shuffle).
    - Tổng hợp kết quả: Tính tần suất xuất hiện (count) và tổng thứ hạng (rank_sum).
    - Sắp xếp giảm dần theo count, tăng dần theo rank_sum (order(-count, rank_sum)) để sinh bảng xếp hạng đồng thuận.

    Tối ưu hóa: Cập nhật lợi ích cận biên trực tiếp (Incremental Marginal Gain Update) trên GPU PyTorch CUDA
    (hoặc NumPy BLAS đa luồng), bảo toàn 100% kết quả toán học, tích hợp thanh tiến trình tqdm.

    Args:
        sim_matrix: Ma trận tương đồng chuỗi BLASTp Identity không âm (N, N).
        seq_ids: Danh sách protein IDs theo thứ tự ban đầu.
        prune_threshold: Ngưỡng cắt tỉa tương đồng (mặc định 0.90 theo Greedy.R).
        num_shuffles: Số lần xáo trộn ngẫu nhiên (mặc định 1000 theo Greedy.R).
        sample_weights: Vector trọng số mẫu w_v (N,), nếu None thì gán w_v = 1.0.
        seed: Hạt giống ngẫu nhiên để tái hiện kết quả.
        budget_per_shuffle: Số đại diện tối đa cần chọn mỗi vòng (mặc định 76 bằng tổng số phân họ).
        cache_path: Đường dẫn lưu cache kết quả xáo trộn.
        force_recompute: Bắt buộc tính lại từ đầu kể cả khi đã có cache.
        desc_label: Nhãn mô tả cho thanh tiến trình tqdm.
        show_progress: Bật/tắt thanh tiến trình tqdm.

    Returns:
        tuple[list[str], pd.DataFrame]:
            - consensus_ids: Danh sách protein IDs sắp xếp theo mức độ đồng thuận toàn cục.
            - df_agg: Bảng DataFrame tổng hợp count và rank_sum của từng protein.
    """
    if cache_path is not None and cache_path.exists() and not force_recompute:
        cached_data = np.load(cache_path, allow_pickle=True)
        cached_budget = 15
        if "metadata" in cached_data:
            meta_raw: object = cached_data["metadata"].item()
            if isinstance(meta_raw, dict) and "budget_per_shuffle" in meta_raw:
                cached_budget = int(meta_raw["budget_per_shuffle"])

        if cached_budget >= budget_per_shuffle:
            logger.info(
                "Nạp kết quả xếp hạng đồng thuận từ cache: %s (budget_per_shuffle=%d)",
                cache_path.name,
                cached_budget,
            )
            consensus_ids = [str(x) for x in cached_data["consensus_ids"]]
            df_agg = pd.DataFrame({
                "repID": [str(x) for x in cached_data["rep_ids"]],
                "count": [int(x) for x in cached_data["counts"]],
                "rank_sum": [int(x) for x in cached_data["rank_sums"]],
            })
            logger.info("Đã nạp thành công %d chuỗi đại diện từ cache.", len(consensus_ids))
            return consensus_ids, df_agg

        logger.info(
            "Cache %s có budget_per_shuffle=%d < %d yêu cầu; tiến hành tính lại...",
            cache_path.name,
            cached_budget,
            budget_per_shuffle,
        )

    n = len(seq_ids)
    rng = np.random.default_rng(seed)
    all_results: list[dict[str, object]] = []

    # Khởi tạo vector trọng số
    if sample_weights is not None:
        if len(sample_weights) != n:
            raise ValueError(f"Độ dài sample_weights ({len(sample_weights)}) không khớp với số chuỗi n={n}!")
        weights_arr = np.asarray(sample_weights, dtype=np.float32)
    else:
        weights_arr = np.ones(n, dtype=np.float32)

    # Tính sẵn vector lợi ích cận biên cơ sở g^(0) = w^T * S ở độ chính xác float64
    weights_f64_cpu = weights_arr.astype(np.float64)
    m_arr = np.asarray(sim_matrix, dtype=np.float32)
    base_gains_f64_cpu = weights_f64_cpu @ m_arr.astype(np.float64)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    use_gpu = (device == "cuda")

    if use_gpu:
        m_tensor = torch.from_numpy(m_arr).to(device=device, dtype=torch.float32)
        weights_f64 = torch.from_numpy(weights_f64_cpu).to(device=device, dtype=torch.float64)
        base_gains_f64 = torch.from_numpy(base_gains_f64_cpu).to(device=device, dtype=torch.float64)

    t_start = time.perf_counter()

    # Vòng lặp xáo trộn tích hợp tqdm
    iterator = range(num_shuffles)
    if show_progress:
        iterator = tqdm(
            iterator,
            desc=desc_label,
            unit="shuffle",
            dynamic_ncols=True,
            leave=False,
        )

    for _ in iterator:
        # Hoán vị ngẫu nhiên danh sách ứng viên
        perm = rng.permutation(n)

        if use_gpu:
            perm_t = torch.from_numpy(perm).to(device=device, dtype=torch.long)
            current_max_sim = torch.zeros(n, device=device, dtype=torch.float32)
            active = torch.ones(n, device=device, dtype=torch.bool)
            gains_f64 = base_gains_f64.clone()
            selected_orig: list[int] = []

            for _ in range(budget_per_shuffle):
                if not torch.any(active):
                    break
                gains_f32 = gains_f64.to(dtype=torch.float32)
                gains_perm = torch.where(active[perm_t], gains_f32[perm_t], -1.0)
                best_pos = int(torch.argmax(gains_perm).item())
                best_cand = int(perm_t[best_pos].item())
                selected_orig.append(best_cand)

                col_c = m_tensor[:, best_cand]
                changed_rows = torch.where(col_c > current_max_sim)[0]
                if len(changed_rows) > 0:
                    m_sub = m_tensor[changed_rows, :].to(dtype=torch.float64)
                    old_sub = current_max_sim[changed_rows].to(dtype=torch.float64).unsqueeze(1)
                    new_sub = col_c[changed_rows].to(dtype=torch.float64).unsqueeze(1)
                    delta_diff = torch.clamp(m_sub - old_sub, min=0.0) - torch.clamp(m_sub - new_sub, min=0.0)
                    gain_drop = torch.matmul(weights_f64[changed_rows], delta_diff)
                    gains_f64 = torch.clamp(gains_f64 - gain_drop, min=0.0)
                    current_max_sim[changed_rows] = col_c[changed_rows]

                active = active & (m_tensor[best_cand, :] <= prune_threshold)

            for rank, orig_idx in enumerate(selected_orig, start=1):
                rep_id = seq_ids[orig_idx]
                all_results.append({"repID": rep_id, "rank": rank})
        else:
            current_max_sim_cpu = np.zeros(n, dtype=np.float32)
            active_cpu = np.ones(n, dtype=bool)
            gains_cpu = base_gains_f64_cpu.copy()
            selected_orig_cpu: list[int] = []

            for _ in range(budget_per_shuffle):
                if not np.any(active_cpu):
                    break
                gains_f32_cpu = gains_cpu.astype(np.float32)
                gains_perm_cpu = np.where(active_cpu[perm], gains_f32_cpu[perm], -1.0)
                best_pos_cpu = int(np.argmax(gains_perm_cpu))
                best_cand_cpu = int(perm[best_pos_cpu])
                selected_orig_cpu.append(best_cand_cpu)

                col_c_cpu = m_arr[:, best_cand_cpu]
                changed_rows_cpu = np.where(col_c_cpu > current_max_sim_cpu)[0]
                if len(changed_rows_cpu) > 0:
                    m_sub_cpu = m_arr[changed_rows_cpu, :].astype(np.float64)
                    old_sub_cpu = current_max_sim_cpu[changed_rows_cpu].astype(np.float64)[:, None]
                    new_sub_cpu = col_c_cpu[changed_rows_cpu].astype(np.float64)[:, None]
                    delta_diff_cpu = np.maximum(0.0, m_sub_cpu - old_sub_cpu) - np.maximum(0.0, m_sub_cpu - new_sub_cpu)
                    gain_drop_cpu = weights_f64_cpu[changed_rows_cpu] @ delta_diff_cpu
                    gains_cpu = np.maximum(0.0, gains_cpu - gain_drop_cpu)
                    current_max_sim_cpu[changed_rows_cpu] = col_c_cpu[changed_rows_cpu]

                active_cpu = active_cpu & (m_arr[best_cand_cpu, :] <= prune_threshold)

            for rank, orig_idx in enumerate(selected_orig_cpu, start=1):
                rep_id = seq_ids[orig_idx]
                all_results.append({"repID": rep_id, "rank": rank})

    if use_gpu:
        torch.cuda.synchronize()

    total_time = time.perf_counter() - t_start

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
                "budget_per_shuffle": budget_per_shuffle,
                "total_time_seconds": total_time,
                "seed": seed,
            },
        )

    return consensus_ids, df_agg
