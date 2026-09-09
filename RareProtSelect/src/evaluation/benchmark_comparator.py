"""Thực hiện Công đoạn 7.1 trong Tài liệu 1 và Module 3.7 (benchmark_comparator.py) trong Tài liệu 2."""

from __future__ import annotations

import logging
from typing import Any
import numpy as np

logger = logging.getLogger(__name__)


def evaluate_benchmark_identity(
    selected_seq_ids: list[str],
    benchmark_seq_ids: list[str],
    sim_matrix: np.ndarray | None = None,
    id_to_idx: dict[str, int] | None = None,
) -> dict[str, Any]:
    """Đo lường độ trùng khớp và tương đồng giữa tập đại diện thuật toán chọn (S_algo)
    và tập chuẩn do chuyên gia lựa chọn thủ công (S_expert / Gold Standard Benchmark):
    - exact_match_count / overlap_count: Số lượng chuỗi trùng khớp chính xác (|S_algo ∩ S_expert|)
    - exact_match_recall / overlap_ratio: Tỷ lệ bao phủ tập chuyên gia (|S_algo ∩ S_expert| / |S_expert|)
    - exact_match_precision: Tỷ lệ chuẩn xác của thuật toán (|S_algo ∩ S_expert| / |S_algo|)
    - f1_score: Điểm F1 kết hợp Precision và Recall đối chuẩn
    - jaccard_similarity: Hệ số tương đồng Jaccard (|S_algo ∩ S_expert| / |S_algo ∪ S_expert|)
    - semantic_benchmark_coverage / mean_max_similarity: Độ bao phủ ngữ nghĩa trung bình trong không gian ESM-2
    - overlapping_ids: Danh sách các ID trùng khớp
    - missing_benchmark_ids: Danh sách các ID chuyên gia chưa được chọn trực tiếp

    Tham số:
        selected_seq_ids: Danh sách ID các protein được thuật toán lựa chọn.
        benchmark_seq_ids: Danh sách ID các protein trong tập chuẩn chuyên gia.
        sim_matrix: (Tùy chọn) Ma trận tương đồng không âm shape (N, N).
        id_to_idx: (Tùy chọn) Từ điển ánh xạ từ protein ID sang chỉ số hàng/cột trong sim_matrix.

    Trả về:
        dict[str, Any]: Từ điển chứa toàn bộ các chỉ số so sánh đối chuẩn.
    """
    # Chuẩn hóa chuỗi ID (loại bỏ khoảng trắng đầu/cuối)
    clean_selected = [str(s).strip() for s in selected_seq_ids if str(s).strip()]
    clean_benchmark = [str(b).strip() for b in benchmark_seq_ids if str(b).strip()]

    selected_set = set(clean_selected)
    benchmark_set = set(clean_benchmark)

    intersection = selected_set & benchmark_set
    union = selected_set | benchmark_set

    exact_match_count = len(intersection)
    num_selected = len(selected_set)
    num_benchmark = len(benchmark_set)

    # Tính Precision, Recall, F1, Jaccard
    recall = float(exact_match_count / num_benchmark) if num_benchmark > 0 else 0.0
    precision = float(exact_match_count / num_selected) if num_selected > 0 else 0.0

    if (precision + recall) > 0:
        f1 = float(2.0 * precision * recall / (precision + recall))
    else:
        f1 = 0.0

    if num_selected == 0 and num_benchmark == 0:
        jaccard_similarity = 1.0
    elif len(union) > 0:
        jaccard_similarity = float(exact_match_count / len(union))
    else:
        jaccard_similarity = 0.0

    overlapping_ids = sorted(list(intersection))
    missing_benchmark_ids = sorted(list(benchmark_set - selected_set))

    # Tính Semantic Coverage nếu có sim_matrix và id_to_idx
    semantic_benchmark_coverage: float | None = None
    if sim_matrix is not None and id_to_idx is not None:
        valid_b_indices: list[int] = []
        for b_id in clean_benchmark:
            if b_id in id_to_idx:
                valid_b_indices.append(id_to_idx[b_id])
            else:
                logger.warning("Expert ID '%s' does not exist in id_to_idx mapping.", b_id)

        valid_s_indices: list[int] = []
        for s_id in clean_selected:
            if s_id in id_to_idx:
                valid_s_indices.append(id_to_idx[s_id])
            else:
                logger.warning("Algorithm ID '%s' does not exist in id_to_idx mapping.", s_id)

        if len(valid_b_indices) == 0 or len(valid_s_indices) == 0:
            semantic_benchmark_coverage = 0.0
        else:
            sub_sim = sim_matrix[np.ix_(valid_b_indices, valid_s_indices)]
            max_sims = np.max(sub_sim, axis=1)
            semantic_benchmark_coverage = float(np.mean(max_sims))

    mean_max_sim = (
        float(semantic_benchmark_coverage)
        if semantic_benchmark_coverage is not None
        else 0.0
    )

    return {
        "exact_match_count": int(exact_match_count),
        "overlap_count": int(exact_match_count),
        "exact_match_recall": float(recall),
        "overlap_ratio": float(recall),
        "exact_match_precision": float(precision),
        "f1_score": float(f1),
        "jaccard_similarity": float(jaccard_similarity),
        "semantic_benchmark_coverage": semantic_benchmark_coverage,
        "mean_max_similarity": float(mean_max_sim),
        "overlapping_ids": overlapping_ids,
        "missing_benchmark_ids": missing_benchmark_ids,
        "num_selected": int(num_selected),
        "num_benchmark": int(num_benchmark),
    }
