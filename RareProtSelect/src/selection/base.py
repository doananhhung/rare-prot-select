"""Thực hiện Công đoạn 4.1 trong Tài liệu 1 và Module 3.6 (base.py) trong Tài liệu 2."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class SelectionResult:
    """Cấu trúc dữ liệu chứa kết quả đầu ra chuẩn mực của thuật toán chọn tập đại diện Submodular.

    Thuộc tính:
        selected_indices: Danh sách chỉ số phần tử được chọn vào tập S theo đúng thứ tự duyệt tham lam.
        selected_ids: Danh sách mã định danh protein (Protein IDs) tương ứng với selected_indices.
        marginal_gains: Lợi ích biên Delta F(s_t | S_{t-1}) thu được tại mỗi bước chọn t in [1..k].
        objective_history: Lịch sử giá trị hàm mục tiêu F(S_t) tích lũy qua từng bước chọn t in [1..k].
        total_evaluations: Tổng số lần đánh giá hàm lợi ích biên (phép tính dot product hoặc tương tự).
        runtime_seconds: Thời gian thực thi thực tế (giây).
    """

    selected_indices: list[int] = field(default_factory=list)
    selected_ids: list[str] = field(default_factory=list)
    marginal_gains: list[float] = field(default_factory=list)
    objective_history: list[float] = field(default_factory=list)
    total_evaluations: int = 0
    runtime_seconds: float = 0.0

    def to_dict(self) -> dict[str, object]:
        """Chuyển đổi kết quả sang từ điển Python."""
        return {
            "selected_indices": self.selected_indices,
            "selected_ids": self.selected_ids,
            "marginal_gains": self.marginal_gains,
            "objective_history": self.objective_history,
            "total_evaluations": self.total_evaluations,
            "runtime_seconds": self.runtime_seconds,
        }


class BaseSubmodularSelector(ABC):
    """Lớp cơ sở trừu tượng quy định giao diện chuẩn cho mọi bộ chọn tập đại diện Submodular."""

    @abstractmethod
    def select(self, budget_k: int) -> SelectionResult:
        """Thực thi thuật toán chọn k protein đại diện tối ưu.

        Tham số:
            budget_k: Ngân sách số lượng protein đại diện cần chọn (k >= 0).

        Trả về:
            SelectionResult: Đối tượng chứa đầy đủ chỉ số, IDs, lợi ích biên và lịch sử hàm mục tiêu.
        """
        pass
