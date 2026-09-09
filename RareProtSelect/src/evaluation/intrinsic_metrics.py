"""Thực hiện Công đoạn 5.1 trong Tài liệu 1 và Module 3.7 (intrinsic_metrics.py) trong Tài liệu 2."""

from __future__ import annotations

import logging
from typing import Any
import numpy as np

logger = logging.getLogger(__name__)


def compute_group_coverage(
    sim_matrix: np.ndarray,
    selected_indices: list[int],
    group_indices: list[int],
) -> float:
    """Tính toán độ bao phủ Coverage(g) cho một phân họ g cụ thể.

    Công thức: Coverage(g) = 1/|g| * sum_{v in g} max_{s in S} sim(v, s)

    Tham số:
        sim_matrix: Ma trận tương đồng không âm shape (N, N).
        selected_indices: Danh sách chỉ số các protein trong tập đại diện S.
        group_indices: Danh sách chỉ số các protein thuộc phân họ g.

    Trả về:
        float: Điểm bao phủ trong đoạn [0.0, 1.0].
    """
    if len(selected_indices) == 0 or len(group_indices) == 0:
        return 0.0

    n_total = sim_matrix.shape[0]
    for idx in selected_indices:
        if not (0 <= idx < n_total):
            raise IndexError(f"Chỉ số selected_index={idx} vượt ngoài kích thước ma trận {n_total}.")
    for idx in group_indices:
        if not (0 <= idx < n_total):
            raise IndexError(f"Chỉ số group_index={idx} vượt ngoài kích thước ma trận {n_total}.")

    sim_sub = sim_matrix[np.ix_(group_indices, selected_indices)]
    max_sims = np.max(sim_sub, axis=1)
    return float(np.mean(max_sims))


def evaluate_intrinsic_metrics(
    sim_matrix: np.ndarray,
    selected_indices: list[int],
    labels: list[str],
    rare_threshold: int = 5,
) -> dict[str, Any]:
    """Tính toán toàn bộ bộ chỉ số nội tại:
    - overall_coverage: Độ bao phủ toàn họ (Overall Coverage)
    - macro_coverage: Độ bao phủ trung bình đều qua các phân họ (Macro Coverage)
    - worst_group_coverage: Độ bao phủ của phân họ thiệt thòi nhất (Worst-Group Coverage)
    - rare_group_representation_rate: Tỷ lệ phân họ hiếm có đại diện thực thể
    - pairwise_redundancy: Độ trùng lặp nội bộ giữa các đại diện trong tập S

    Tham số:
        sim_matrix: Ma trận tương đồng không âm shape (N, N).
        selected_indices: Danh sách chỉ số các protein được chọn vào tập đại diện S.
        labels: Danh sách nhãn phân họ tương ứng với từng hàng/cột của ma trận.
        rare_threshold: Ngưỡng quy mô tối đa để xác định một phân họ là hiếm (mặc định <= 5).

    Trả về:
        dict[str, Any]: Từ điển chứa 5 chỉ số cốt lõi và các thống kê chi tiết.
    """
    if sim_matrix.ndim != 2 or sim_matrix.shape[0] != sim_matrix.shape[1]:
        raise ValueError(f"sim_matrix phải là ma trận vuông 2 chiều, nhận được shape={sim_matrix.shape}.")

    n_total = sim_matrix.shape[0]
    if len(labels) != n_total:
        raise ValueError(
            f"Kích thước không khớp: len(labels)={len(labels)} != sim_matrix.shape[0]={n_total}."
        )

    if n_total == 0:
        return {
            "overall_coverage": 0.0,
            "macro_coverage": 0.0,
            "worst_group_coverage": 0.0,
            "rare_group_representation_rate": 1.0,
            "pairwise_redundancy": 0.0,
            "num_selected": 0,
            "num_total": 0,
            "num_groups": 0,
            "num_rare_groups": 0,
            "num_represented_rare_groups": 0,
            "group_coverages": {},
        }

    for idx in selected_indices:
        if not (0 <= idx < n_total):
            raise IndexError(f"Chỉ số selected_index={idx} vượt ngoài phạm vi [0, {n_total - 1}].")

    # Gom nhóm chỉ số theo nhãn phân họ
    groups: dict[str, list[int]] = {}
    for idx, label in enumerate(labels):
        groups.setdefault(label, []).append(idx)

    num_groups = len(groups)

    # 1. Tính Coverage cho từng phân họ
    group_coverages: dict[str, float] = {}
    for g_name, g_indices in groups.items():
        group_coverages[g_name] = compute_group_coverage(sim_matrix, selected_indices, g_indices)

    # 2. Overall Coverage (Độ bao phủ toàn họ)
    if len(selected_indices) == 0:
        overall_coverage = 0.0
    else:
        sim_all_selected = sim_matrix[:, selected_indices]
        max_sims_all = np.max(sim_all_selected, axis=1)
        overall_coverage = float(np.mean(max_sims_all))

    # 3. Macro Coverage (Độ bao phủ trung bình đều qua các phân họ)
    if num_groups > 0:
        macro_coverage = float(np.mean(list(group_coverages.values())))
    else:
        macro_coverage = 0.0

    # 4. Worst-Group Coverage (Độ bao phủ của phân họ thiệt thòi nhất)
    if num_groups > 0:
        worst_group_coverage = float(np.min(list(group_coverages.values())))
    else:
        worst_group_coverage = 0.0

    # 5. Rare Group Representation Rate (Tỷ lệ phân họ hiếm có đại diện)
    rare_groups = {g: idxs for g, idxs in groups.items() if len(idxs) <= rare_threshold}
    num_rare_groups = len(rare_groups)

    selected_set = set(selected_indices)
    selected_labels = set(labels[i] for i in selected_set)

    num_represented_rare_groups = sum(1 for g in rare_groups if g in selected_labels)

    if num_rare_groups == 0:
        # Khi không có phân họ hiếm nào trong dữ liệu, quy ước 1.0 để tránh chia cho 0
        rare_group_representation_rate = 1.0
    else:
        rare_group_representation_rate = float(num_represented_rare_groups / num_rare_groups)

    # 6. Pairwise Redundancy (Độ trùng lặp nội bộ giữa các đại diện trong S)
    k = len(selected_indices)
    if k <= 1:
        pairwise_redundancy = 0.0
    else:
        sub_sim = sim_matrix[np.ix_(selected_indices, selected_indices)]
        upper_tri_indices = np.triu_indices(k, k=1)
        num_pairs = k * (k - 1) // 2
        sum_sim = float(np.sum(sub_sim[upper_tri_indices]))
        pairwise_redundancy = float(sum_sim / num_pairs)

    return {
        "overall_coverage": float(overall_coverage),
        "macro_coverage": float(macro_coverage),
        "worst_group_coverage": float(worst_group_coverage),
        "rare_group_representation_rate": float(rare_group_representation_rate),
        "pairwise_redundancy": float(pairwise_redundancy),
        "num_selected": int(k),
        "num_total": int(n_total),
        "num_groups": int(num_groups),
        "num_rare_groups": int(num_rare_groups),
        "num_represented_rare_groups": int(num_represented_rare_groups),
        "group_coverages": group_coverages,
    }
