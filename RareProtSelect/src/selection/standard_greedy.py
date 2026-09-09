"""Thực hiện Công đoạn 4.3 trong Tài liệu 1 và Module 3.6 (standard_greedy.py) trong Tài liệu 2."""

from __future__ import annotations

import logging
import time
import numpy as np

from src.selection.lazy_greedy import SelectionResult

logger = logging.getLogger(__name__)


class StandardGreedySelector:
    """Bộ chọn tập đại diện tối ưu hóa Submodular Facility Location bằng Standard Greedy (Vét cạn O(k*n^2)).

    Cài đặt thuật toán Standard Greedy nguyên bản của bài báo nền (Nguyen et al., 2025).
    Được sử dụng làm chuẩn đối chứng trực diện 1-1 để chứng minh:
    1. Nghiệm của Lazy Greedy và Standard Greedy trùng khớp 100% về mặt toán học.
    2. Lazy Greedy đem lại độ tăng tốc (Speedup) vượt bậc về thời gian và số lần đánh giá hàm.
    """

    def __init__(
        self,
        sim_matrix: np.ndarray,
        weights: np.ndarray | None = None,
        seq_ids: list[str] | None = None,
    ) -> None:
        """Khởi tạo StandardGreedySelector.

        Args:
            sim_matrix: Ma trận tương đồng Cosine không âm, kích thước (N, N), giá trị in [0, 1].
            weights: Vector trọng số w_v không âm cho từng protein, kích thước (N,).
                     Nếu None, mặc định là vector trọng số đồng nhất 1.0 (Uniform).
            seq_ids: Danh sách định danh protein theo thứ tự hàng/cột.
                     Nếu None, mặc định là ['0', '1', ..., 'N-1'].
        """
        if sim_matrix.ndim != 2 or sim_matrix.shape[0] != sim_matrix.shape[1]:
            raise ValueError(
                f"sim_matrix phải là ma trận vuông 2 chiều (N, N), nhận được shape: {sim_matrix.shape}"
            )

        self.n: int = sim_matrix.shape[0]
        self.sim_matrix: np.ndarray = np.asarray(sim_matrix, dtype=np.float64)

        if weights is None:
            self.weights: np.ndarray = np.ones(self.n, dtype=np.float64)
        else:
            if len(weights) != self.n:
                raise ValueError(
                    f"Kích thước weights ({len(weights)}) không khớp với sim_matrix ({self.n})"
                )
            self.weights = np.asarray(weights, dtype=np.float64)

        if seq_ids is None:
            self.seq_ids: list[str] = [str(i) for i in range(self.n)]
        else:
            if len(seq_ids) != self.n:
                raise ValueError(
                    f"Số lượng seq_ids ({len(seq_ids)}) không khớp với sim_matrix ({self.n})"
                )
            self.seq_ids = list(seq_ids)

    def select(self, budget_k: int) -> SelectionResult:
        """Thực thi thuật toán Standard Greedy (quét vét cạn O(k*n^2)) để chọn k protein đại diện.

        Args:
            budget_k: Ngân sách số lượng protein đại diện cần chọn (k >= 0).

        Returns:
            SelectionResult: Đối tượng chứa danh sách chỉ số, IDs, lợi ích biên,
                            lịch sử hàm mục tiêu, số lần gọi hàm và thời gian chạy.
        """
        start_time = time.perf_counter()

        if self.n == 0 or budget_k <= 0:
            return SelectionResult(
                selected_indices=[],
                selected_ids=[],
                marginal_gains=[],
                objective_history=[],
                total_evaluations=0,
                runtime_seconds=time.perf_counter() - start_time,
            )

        effective_k = min(budget_k, self.n)

        current_max_sim = np.zeros(self.n, dtype=np.float64)
        selected_indices: list[int] = []
        marginal_gains: list[float] = []
        objective_history: list[float] = []
        selected_set: set[int] = set()
        total_evaluations = 0

        for step in range(effective_k):
            best_candidate = -1
            best_gain = -1.0

            for cand in range(self.n):
                if cand in selected_set:
                    continue

                diff = np.maximum(0.0, self.sim_matrix[:, cand] - current_max_sim)
                gain = float(np.dot(self.weights, diff))
                total_evaluations += 1

                # Sử dụng strictly greater than để bảo đảm phá vỡ thế hòa (tie-breaking)
                # luôn ưu tiên chỉ số nhỏ hơn, hoàn toàn nhất quán với Lazy Greedy Max-Heap.
                if gain > best_gain:
                    best_gain = gain
                    best_candidate = cand

            if best_candidate == -1:
                break

            selected_indices.append(best_candidate)
            selected_set.add(best_candidate)
            marginal_gains.append(max(0.0, best_gain))

            current_max_sim = np.maximum(current_max_sim, self.sim_matrix[:, best_candidate])
            current_obj = float(np.dot(self.weights, current_max_sim))
            objective_history.append(current_obj)

        elapsed = time.perf_counter() - start_time
        selected_ids = [self.seq_ids[i] for i in selected_indices]

        logger.debug(
            "Standard Greedy hoàn thành chọn %d/%d phần tử trong %.4fs với %d evaluations",
            len(selected_indices),
            effective_k,
            elapsed,
            total_evaluations,
        )

        return SelectionResult(
            selected_indices=selected_indices,
            selected_ids=selected_ids,
            marginal_gains=marginal_gains,
            objective_history=objective_history,
            total_evaluations=total_evaluations,
            runtime_seconds=elapsed,
        )


def standard_greedy_facility_location(
    sim_matrix: np.ndarray,
    weights: np.ndarray,
    budget_k: int,
    seq_ids: list[str] | None = None,
) -> tuple[list[int], list[float], list[float]]:
    """Thuật toán Standard Greedy gốc (quét vét cạn O(k*n^2) mỗi bước).

    Hiện thực hóa Công đoạn 4.3 trong Tài liệu 1 và Module 3.6 trong Tài liệu 2.

    Args:
        sim_matrix: Ma trận tương đồng Cosine không âm kích thước (N, N).
        weights: Vector trọng số w_v kích thước (N,).
        budget_k: Ngân sách số phần tử cần chọn.
        seq_ids: Danh sách protein IDs (tùy chọn).

    Returns:
        tuple[list[int], list[float], list[float]]:
            - selected_indices: Danh sách chỉ số protein đại diện được chọn.
            - marginal_gains: Lợi ích biên qua từng bước.
            - objective_values: Giá trị hàm mục tiêu F(S) tích lũy qua từng bước.
    """
    selector = StandardGreedySelector(sim_matrix=sim_matrix, weights=weights, seq_ids=seq_ids)
    res = selector.select(budget_k=budget_k)
    return res.selected_indices, res.marginal_gains, res.objective_history
