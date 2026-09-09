"""Thực hiện Công đoạn 4.1 & 4.2 trong Tài liệu 1 và Module 3.6 (lazy_greedy.py) trong Tài liệu 2."""

from __future__ import annotations

from dataclasses import dataclass, field
import heapq
import logging
import time
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class SelectionResult:
    """Cấu trúc dữ liệu chứa kết quả lựa chọn tập đại diện protein."""

    selected_indices: list[int]
    selected_ids: list[str] = field(default_factory=list)
    marginal_gains: list[float] = field(default_factory=list)
    objective_history: list[float] = field(default_factory=list)
    total_evaluations: int = 0
    runtime_seconds: float = 0.0


class LazyGreedySelector:
    """Bộ chọn tập đại diện tối ưu hóa Submodular Weighted Facility Location bằng Lazy Greedy.

    Sử dụng cấu trúc Hàng đợi ưu tiên cực đại (Max-Heap) qua thư viện `heapq` để tận dụng
    triệt để tính chất Lợi ích biên giảm dần (Diminishing Marginal Returns / Submodularity):
        Nếu A subseteq B subseteq V và e notin B thì: Delta(e | A) >= Delta(e | B).

    Cơ chế tối ưu:
    1. Ban đầu đẩy tất cả n phần tử vào Max-Heap với giá trị lợi ích ban đầu:
       Delta(e | emptyset) = sum_{v in V} w_v * Sim(v, e).
    2. Ở mỗi bước chọn, rút đỉnh Heap (ứng viên có Gain lưu trữ lớn nhất).
    3. Nếu đỉnh này đã được cập nhật ở vòng lặp hiện tại (last_step == current_step),
       theo tính chất Submodular, không phần tử nào khác trong Heap có thể vượt qua nó ->
       chọn ngay lập tức mà KHÔNG cần đánh giá lại các phần tử còn lại.
    4. Nếu chưa cập nhật ở vòng hiện tại, tính lại Gain mới:
       Delta(e | S) = sum_{v in V} w_v * max(0.0, Sim(v, e) - current_max_sim[v]),
       rồi đẩy lại vào Heap.
    """

    def __init__(
        self,
        sim_matrix: np.ndarray,
        weights: np.ndarray | None = None,
        seq_ids: list[str] | None = None,
    ) -> None:
        """Khởi tạo LazyGreedySelector.

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
        """Thực thi thuật toán Lazy Greedy để chọn k protein đại diện.

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

        # Mảng theo dõi độ tương đồng cực đại hiện tại từ mỗi protein v đến tập S
        current_max_sim = np.zeros(self.n, dtype=np.float64)

        # Khởi tạo Max-Heap (sử dụng min-heap với -gain)
        # Tuple lưu trữ: (-gain, element_index, last_updated_step)
        heap: list[tuple[float, int, int]] = []
        total_evaluations = 0

        # Tính lợi ích ban đầu khi S = emptyset: Delta(i | emptyset) = sum_v w_v * Sim(v, i)
        for i in range(self.n):
            gain_0 = float(np.dot(self.weights, np.maximum(0.0, self.sim_matrix[:, i])))
            total_evaluations += 1
            heap.append((-gain_0, i, 0))

        heapq.heapify(heap)

        selected_indices: list[int] = []
        marginal_gains: list[float] = []
        objective_history: list[float] = []
        selected_set: set[int] = set()

        for step in range(effective_k):
            chosen = False
            while heap and not chosen:
                neg_gain, best_idx, last_step = heapq.heappop(heap)
                stored_gain = -neg_gain

                # Bỏ qua nếu phần tử đã được chọn trước đó
                if best_idx in selected_set:
                    continue

                if last_step == step:
                    # Đỉnh Heap đã được cập nhật ở vòng lặp hiện tại!
                    # Do tính chất Submodular, đây chính là phần tử tối ưu toàn cục của bước này.
                    e = best_idx
                    gain = max(0.0, stored_gain)
                    selected_indices.append(e)
                    selected_set.add(e)
                    marginal_gains.append(gain)

                    # Cập nhật mảng khoảng cách gần nhất
                    current_max_sim = np.maximum(current_max_sim, self.sim_matrix[:, e])
                    current_obj = float(np.dot(self.weights, current_max_sim))
                    objective_history.append(current_obj)
                    chosen = True
                else:
                    # Tính lại lợi ích biên thực tế tại trạng thái S hiện tại
                    diff = np.maximum(0.0, self.sim_matrix[:, best_idx] - current_max_sim)
                    new_gain = float(np.dot(self.weights, diff))
                    total_evaluations += 1
                    # Đẩy lại vào Heap với mốc thời gian là bước hiện tại
                    heapq.heappush(heap, (-new_gain, best_idx, step))

            if not chosen:
                break

        elapsed = time.perf_counter() - start_time
        selected_ids = [self.seq_ids[i] for i in selected_indices]

        logger.debug(
            "Lazy Greedy hoàn thành chọn %d/%d phần tử trong %.4fs với %d evaluations",
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


def lazy_greedy_facility_location(
    sim_matrix: np.ndarray,
    weights: np.ndarray,
    budget_k: int,
    seq_ids: list[str] | None = None,
) -> tuple[list[int], list[float], list[float]]:
    """Thuật toán Lazy Greedy tối ưu hóa Weighted Facility Location qua Max-Heap.

    Hiện thực hóa Công đoạn 4.1 & 4.2 trong Tài liệu 1 và Module 3.6 trong Tài liệu 2.

    Args:
        sim_matrix: Ma trận tương đồng Cosine không âm kích thước (N, N).
        weights: Vector trọng số w_v kích thước (N,).
        budget_k: Ngân sách số phần tử cần chọn.
        seq_ids: Danh sách protein IDs (tùy chọn).

    Returns:
        tuple[list[int], list[float], list[float]]:
            - selected_indices: Danh sách chỉ số protein đại diện được chọn [s_1, s_2, ..., s_k].
            - marginal_gains: Lợi ích biên thu được tại mỗi bước [Delta_1, Delta_2, ..., Delta_k].
            - objective_values: Giá trị hàm mục tiêu F(S) tích lũy qua từng bước.
    """
    selector = LazyGreedySelector(sim_matrix=sim_matrix, weights=weights, seq_ids=seq_ids)
    res = selector.select(budget_k=budget_k)
    return res.selected_indices, res.marginal_gains, res.objective_history
