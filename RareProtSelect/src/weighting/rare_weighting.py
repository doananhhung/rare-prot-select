"""Thực hiện Công đoạn 3.2 trong Tài liệu 1 và Module 3.5 (rare_weighting.py) trong Tài liệu 2."""

from __future__ import annotations

from collections import Counter
import logging
import numpy as np

logger = logging.getLogger(__name__)

VALID_WEIGHTING_SCHEMES = {"inverse_sqrt", "uniform", "inverse_freq", "power"}


def compute_rare_aware_weights(
    seq_ids: list[str],
    label_map: dict[str, str],
    scheme: str = "inverse_sqrt",
    alpha: float = 0.5,
) -> np.ndarray:
    """Tính toán vector trọng số thích ứng nhóm hiếm (Rare-Aware Protein Weighting).

    Khuếch đại lực kéo toán học cho các phân họ nhỏ/hiếm trong bài toán tối ưu hóa Submodular,
    ngăn chặn tình trạng tập đại diện dồn hết vào các phân họ chiếm đa số.

    Các lược đồ trọng số (Weighting Schemes):
    1. 'inverse_sqrt' (Mặc định RareProtSelect): w_v = 1.0 / sqrt(n_{g(v)})
    2. 'uniform' (Baseline unweighted): w_v = 1.0
    3. 'inverse_freq' (Nghịch đảo tuyến tính): w_v = 1.0 / n_{g(v)}
    4. 'power' (Lũy thừa tổng quát): w_v = 1.0 / (n_{g(v)} ** alpha) với alpha >= 0.0

    Xử lý an toàn:
    - n_g = max(1, n_g) chống chia cho 0.
    - Singletons (n_g = 1) luôn có w_v = 1.0 trong mọi lược đồ.
    - seq_ids rỗng trả về np.empty((0,), dtype=np.float64).

    Args:
        seq_ids: Danh sách định danh protein trong Ground Set V theo đúng thứ tự hàng/cột.
        label_map: Ánh xạ từ định danh protein sang mã phân họ {seq_id: subfamily_id}.
        scheme: Tên lược đồ trọng số ('inverse_sqrt', 'uniform', 'inverse_freq', 'power').
        alpha: Số mũ suy giảm cho lược đồ 'power' (hoặc tham số kiểm soát khi scheme='power').

    Returns:
        np.ndarray: Vector trọng số w kiểu float64, kích thước (N,).

    Raises:
        ValueError: Nếu scheme không nằm trong danh sách hỗ trợ hoặc alpha < 0.
    """
    if scheme not in VALID_WEIGHTING_SCHEMES:
        raise ValueError(
            f"Lược đồ trọng số không hợp lệ: '{scheme}'. "
            f"Các lựa chọn hợp lệ: {sorted(list(VALID_WEIGHTING_SCHEMES))}"
        )

    if alpha < 0.0:
        raise ValueError(f"Tham số alpha phải không âm (alpha >= 0.0), nhận được: {alpha}")

    n_samples = len(seq_ids)
    if n_samples == 0:
        return np.empty((0,), dtype=np.float64)

    # 1. Trích xuất nhãn cho từng protein trong tập đầu vào và đếm kích thước n_g
    assigned_labels = [label_map.get(sid, sid) if label_map else sid for sid in seq_ids]
    group_counts = Counter(assigned_labels)

    # 2. Tính trọng số cho từng protein
    weights = np.empty(n_samples, dtype=np.float64)

    for i, label in enumerate(assigned_labels):
        raw_count = group_counts.get(label, 1)
        # Phòng vệ chia cho 0
        n_g = max(1, int(raw_count))

        if scheme == "uniform":
            w = 1.0
        elif scheme == "inverse_sqrt":
            w = 1.0 / np.sqrt(float(n_g))
        elif scheme == "inverse_freq":
            w = 1.0 / float(n_g)
        elif scheme == "power":
            if alpha == 0.0:
                w = 1.0
            else:
                w = 1.0 / (float(n_g) ** alpha)
        else:
            w = 1.0

        weights[i] = float(w)

    logger.debug(
        "Đã tính toán trọng số theo scheme '%s' cho %d protein. "
        "Min weight: %.4f, Max weight: %.4f, Mean weight: %.4f",
        scheme,
        n_samples,
        float(weights.min()),
        float(weights.max()),
        float(weights.mean()),
    )

    return weights


class RareWeighting:
    """Bộ tính toán và điều phối trọng số thích ứng nhóm hiếm (Rare-Aware Protein Weighting)."""

    def __init__(self, scheme: str = "inverse_sqrt", alpha: float = 0.5) -> None:
        """Khởi tạo cấu hình bộ tính trọng số.

        Args:
            scheme: Lược đồ trọng số ('inverse_sqrt', 'uniform', 'inverse_freq', 'power').
            alpha: Hệ số mũ suy giảm cho lược đồ 'power'.
        """
        self.scheme = scheme
        self.alpha = float(alpha)
        self._validate()

    def _validate(self) -> None:
        if self.scheme not in VALID_WEIGHTING_SCHEMES:
            raise ValueError(
                f"Lược đồ trọng số không hợp lệ: '{self.scheme}'. "
                f"Các lựa chọn hợp lệ: {sorted(list(VALID_WEIGHTING_SCHEMES))}"
            )
        if self.alpha < 0.0:
            raise ValueError(f"Tham số alpha phải không âm (alpha >= 0.0), nhận được: {self.alpha}")

    def compute_weights(self, seq_ids: list[str], label_map: dict[str, str]) -> np.ndarray:
        """Tính toán vector trọng số cho danh sách protein.

        Args:
            seq_ids: Danh sách protein IDs theo thứ tự.
            label_map: Bảng ánh xạ {seq_id: subfamily_id}.

        Returns:
            np.ndarray: Vector trọng số w kiểu float64, kích thước (N,).
        """
        return compute_rare_aware_weights(
            seq_ids=seq_ids,
            label_map=label_map,
            scheme=self.scheme,
            alpha=self.alpha,
        )

    def get_group_weights(self, group_counts: dict[str, int]) -> dict[str, float]:
        """Tính trọng số vô hướng đại diện cho từng phân họ dựa trên kích thước nhóm.

        Args:
            group_counts: Từ điển thống kê {subfamily_id: count}.

        Returns:
            dict[str, float]: Bảng trọng số {subfamily_id: weight}.
        """
        group_weights: dict[str, float] = {}
        for group, count in group_counts.items():
            n_g = max(1, int(count))
            if self.scheme == "uniform":
                w = 1.0
            elif self.scheme == "inverse_sqrt":
                w = 1.0 / np.sqrt(float(n_g))
            elif self.scheme == "inverse_freq":
                w = 1.0 / float(n_g)
            elif self.scheme == "power":
                w = 1.0 / (float(n_g) ** self.alpha) if self.alpha != 0.0 else 1.0
            else:
                w = 1.0
            group_weights[group] = float(w)
        return group_weights
