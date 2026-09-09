"""Thực hiện Công đoạn 5.2 trong Tài liệu 1 và Module 3.7 (annotation_transfer.py) trong Tài liệu 2."""

from __future__ import annotations

import logging
from typing import Any
import numpy as np

logger = logging.getLogger(__name__)


def evaluate_annotation_transfer_1nn(
    sim_matrix: np.ndarray,
    selected_indices: list[int],
    labels: list[str],
) -> dict[str, Any]:
    r"""Sử dụng tập đại diện S làm mẫu tham chiếu 1-NN gán nhãn cho tập còn lại V \ S và đo đạc:
    - accuracy: Độ chính xác phân loại tổng thể
    - macro_f1: Điểm Macro-F1 trung bình qua tất cả các phân họ
    - per_class_f1: Từ điển ánh xạ từng nhãn phân họ sang F1-score tương ứng
    - y_true: Danh sách nhãn thực tế của tập kiểm thử V \ S
    - y_pred: Danh sách nhãn dự đoán của tập kiểm thử V \ S

    Tham số:
        sim_matrix: Ma trận tương đồng không âm shape (N, N).
        selected_indices: Danh sách chỉ số các protein trong tập đại diện S (Reference Set).
        labels: Danh sách nhãn phân họ tương ứng với từng hàng/cột của ma trận.

    Trả về:
        dict[str, Any]: Từ điển chứa các chỉ số đo lường tác vụ chuyển giao chú giải.
    """
    if sim_matrix.ndim != 2 or sim_matrix.shape[0] != sim_matrix.shape[1]:
        raise ValueError(f"sim_matrix phải là ma trận vuông 2 chiều, nhận được shape={sim_matrix.shape}.")

    n_total = sim_matrix.shape[0]
    if len(labels) != n_total:
        raise ValueError(
            f"Kích thước không khớp: len(labels)={len(labels)} != sim_matrix.shape[0]={n_total}."
        )

    for idx in selected_indices:
        if not (0 <= idx < n_total):
            raise IndexError(f"Chỉ số selected_index={idx} vượt ngoài phạm vi [0, {n_total - 1}].")

    # Trường hợp biên 1: Không có mẫu đại diện nào được chọn (S = rỗng)
    if len(selected_indices) == 0:
        return {
            "accuracy": 0.0,
            "macro_f1": 0.0,
            "per_class_f1": {},
            "y_true": [],
            "y_pred": [],
            "num_test_samples": 0,
            "num_classes_evaluated": 0,
        }

    selected_set = set(selected_indices)

    # Trường hợp biên 2: Toàn bộ tập dữ liệu được chọn làm đại diện (S = V => V \ S = rỗng)
    if len(selected_set) >= n_total:
        unique_classes = sorted(list(set(labels)))
        return {
            "accuracy": 1.0,
            "macro_f1": 1.0,
            "per_class_f1": {c: 1.0 for c in unique_classes},
            "y_true": [],
            "y_pred": [],
            "num_test_samples": 0,
            "num_classes_evaluated": len(unique_classes),
        }

    # Tập kiểm thử (Unlabeled Query Set): U = V \ S
    test_indices = [i for i in range(n_total) if i not in selected_set]

    # Gán nhãn 1-NN cho từng u in U với tie-breaking tất định (chọn s có chỉ số nhỏ nhất khi đồng hạng)
    y_true: list[str] = [labels[u] for u in test_indices]
    y_pred: list[str] = []

    for u in test_indices:
        best_s = -1
        best_sim = -1.0
        for s in selected_indices:
            sim_val = float(sim_matrix[u, s])
            if sim_val > best_sim:
                best_sim = sim_val
                best_s = s
            elif sim_val == best_sim:
                if best_s == -1 or s < best_s:
                    best_s = s
        y_pred.append(labels[best_s])

    num_test = len(test_indices)
    correct_count = sum(1 for yt, yp in zip(y_true, y_pred) if yt == yp)
    accuracy = float(correct_count / num_test) if num_test > 0 else 0.0

    # Tính Precision, Recall, F1 cho từng phân họ xuất hiện trong tập kiểm thử
    unique_test_classes = sorted(list(set(y_true)))
    per_class_f1: dict[str, float] = {}

    for c in unique_test_classes:
        tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == c and yp == c)
        fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt != c and yp == c)
        fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == c and yp != c)

        prec = float(tp / (tp + fp)) if (tp + fp) > 0 else 0.0
        rec = float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0

        if (prec + rec) > 0:
            f1 = float(2.0 * prec * rec / (prec + rec))
        else:
            f1 = 0.0

        per_class_f1[c] = f1

    if len(unique_test_classes) > 0:
        macro_f1 = float(np.mean(list(per_class_f1.values())))
    else:
        macro_f1 = 0.0

    return {
        "accuracy": float(accuracy),
        "macro_f1": float(macro_f1),
        "per_class_f1": per_class_f1,
        "y_true": y_true,
        "y_pred": y_pred,
        "num_test_samples": int(num_test),
        "num_classes_evaluated": int(len(unique_test_classes)),
    }
