"""Thực hiện Phương pháp Nền (Unweighted Facility Location - Nguyen et al., 2025).
Công đoạn 4.1 & 4.3 trong Tài liệu 1 và Module 3.6 (unweighted_selector.py) trong Tài liệu 2.
"""

from __future__ import annotations

import logging
from typing import Literal
import numpy as np

from src.selection.base import BaseSubmodularSelector, SelectionResult
from src.selection.standard_greedy import StandardGreedySolver

logger = logging.getLogger(__name__)


class UnweightedFLSelector(BaseSubmodularSelector):
    """Bộ chọn tập đại diện Unweighted Facility Location (Mô hình nền - Nguyen et al., 2025).

    Đặc trưng khoa học:
    - Hàm mục tiêu: F(S) = sum_{v in V} 1.0 * max_{s in S} Sim(v, s) (Không trọng số, w_v = 1.0 đồng nhất).
    - Bộ giải (Solver):
        + 'standard': Thuật toán Standard Greedy quét vét cạn O(k*n^2) nguyên bản của bài báo nền.
        + 'lazy': Thuật toán Lazy Greedy tăng tốc Max-Heap O(k*n log n) cho tập dữ liệu lớn (nghiệm toán học tương đương 100%).

    Ghi chú kiến trúc (Architectural Note):
    - Đây là lớp Public API Wrapper cấp cao phục vụ người dùng cuối khi muốn chạy trọn gói một lệnh.
    - Các kịch bản thực nghiệm chuyên sâu (Exp 2, Exp 3) có thể gọi trực tiếp StandardGreedySolver hoặc LazyGreedySolver
      để phục vụ profiling và đo đạc tài nguyên vi mô từng giai đoạn (gain_evals, time_seconds).
    """

    def __init__(
        self,
        sim_matrix: np.ndarray,
        seq_ids: list[str] | None = None,
        solver: Literal["standard", "lazy"] = "standard",
    ) -> None:
        """Khởi tạo UnweightedFLSelector.

        Tham số:
            sim_matrix: Ma trận tương đồng không âm kích thước (N, N), giá trị in [0, 1].
            seq_ids: Danh sách định danh protein theo thứ tự hàng/cột (N phần tử).
            solver: Lựa chọn bộ giải tham lam ('standard' hoặc 'lazy'). Mặc định là 'standard'.
        """
        if sim_matrix.ndim != 2 or sim_matrix.shape[0] != sim_matrix.shape[1]:
            raise ValueError(f"sim_matrix phải là ma trận vuông 2 chiều (N, N), nhận được shape={sim_matrix.shape}")

        self.n: int = sim_matrix.shape[0]
        self.sim_matrix: np.ndarray = np.asarray(sim_matrix, dtype=np.float64)
        self.solver_type: Literal["standard", "lazy"] = solver

        if seq_ids is None:
            self.seq_ids: list[str] = [str(i) for i in range(self.n)]
        else:
            if len(seq_ids) != self.n:
                raise ValueError(f"Số lượng seq_ids ({len(seq_ids)}) không khớp với sim_matrix ({self.n})")
            self.seq_ids = list(seq_ids)

        # Trọng số đồng nhất w_v = 1.0 cho toàn bộ protein (Unweighted baseline)
        self.weights: np.ndarray = np.ones(self.n, dtype=np.float64)

        # Khởi tạo bộ giải tương ứng
        if self.solver_type == "lazy":
            raise NotImplementedError("Bộ giải 'lazy' hiện chưa được hỗ trợ trong phạm vi hiện tại.")
        elif self.solver_type == "standard":
            self._solver: BaseSubmodularSelector = StandardGreedySolver(
                sim_matrix=self.sim_matrix,
                weights=self.weights,
                seq_ids=self.seq_ids,
            )
        else:
            raise ValueError(f"solver không hợp lệ: {self.solver_type}. Kỳ vọng 'standard' hoặc 'lazy'.")

    def select(self, budget_k: int) -> SelectionResult:
        """Thực thi chọn k protein đại diện theo mô hình Unweighted Facility Location.

        Tham số:
            budget_k: Ngân sách số lượng protein đại diện cần chọn (k >= 0).

        Trả về:
            SelectionResult: Đối tượng chứa kết quả lựa chọn, số lần đánh giá và thời gian chạy.
        """
        logger.debug(
            "Chạy UnweightedFLSelector với budget k=%d bằng solver='%s'",
            budget_k,
            self.solver_type,
        )
        return self._solver.select(budget_k=budget_k)
