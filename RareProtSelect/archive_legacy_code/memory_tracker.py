"""Thực hiện Công đoạn 5.3 trong Tài liệu 1 và Module 3.8 (memory_tracker.py) trong Tài liệu 2."""

from __future__ import annotations

import logging
import tracemalloc
from types import TracebackType

import torch

logger = logging.getLogger(__name__)


class MemoryTracker:
    """Bộ theo dõi mức sử dụng bộ nhớ đỉnh (Peak RAM qua tracemalloc và Peak VRAM qua torch.cuda)."""

    def __init__(self, name: str = "MemoryTracker", auto_log: bool = False) -> None:
        self.name = name
        self.auto_log = auto_log
        self._is_tracking: bool = False
        self.peak_ram_mb: float = 0.0
        self.peak_vram_mb: float = 0.0

    def start(self) -> MemoryTracker:
        """Bắt đầu theo dõi bộ nhớ."""
        # RAM Tracking
        if not tracemalloc.is_tracing():
            tracemalloc.start()
        tracemalloc.reset_peak()

        # VRAM Tracking
        if torch.cuda.is_available():
            torch.cuda.reset_peak_memory_stats()
            torch.cuda.empty_cache()

        self._is_tracking = True
        self.peak_ram_mb = 0.0
        self.peak_vram_mb = 0.0
        return self

    def stop(self) -> tuple[float, float]:
        """Dừng theo dõi và trả về bộ nhớ đỉnh (peak_ram_mb, peak_vram_mb)."""
        if not self._is_tracking:
            return 0.0, 0.0

        # Read Peak RAM
        if tracemalloc.is_tracing():
            _, peak_bytes = tracemalloc.get_traced_memory()
            self.peak_ram_mb = round(peak_bytes / (1024 * 1024), 2)

        # Read Peak VRAM
        if torch.cuda.is_available():
            peak_vram_bytes = torch.cuda.max_memory_allocated()
            self.peak_vram_mb = round(peak_vram_bytes / (1024 * 1024), 2)
        else:
            self.peak_vram_mb = 0.0

        self._is_tracking = False

        if self.auto_log:
            logger.info(
                f"[{self.name}] Peak RAM: {self.peak_ram_mb} MB | Peak VRAM: {self.peak_vram_mb} MB"
            )

        return self.peak_ram_mb, self.peak_vram_mb

    def get_peak_ram_mb(self) -> float:
        """Lấy mức RAM đỉnh hiện tại (MB)."""
        if tracemalloc.is_tracing():
            _, peak_bytes = tracemalloc.get_traced_memory()
            return round(peak_bytes / (1024 * 1024), 2)
        return self.peak_ram_mb

    def get_peak_vram_mb(self) -> float:
        """Lấy mức VRAM GPU đỉnh hiện tại (MB)."""
        if torch.cuda.is_available():
            peak_vram_bytes = torch.cuda.max_memory_allocated()
            return round(peak_vram_bytes / (1024 * 1024), 2)
        return self.peak_vram_mb

    def reset(self) -> None:
        """Khởi tạo lại trạng thái theo dõi."""
        if tracemalloc.is_tracing():
            tracemalloc.reset_peak()
        if torch.cuda.is_available():
            torch.cuda.reset_peak_memory_stats()
        self.peak_ram_mb = 0.0
        self.peak_vram_mb = 0.0

    def __enter__(self) -> MemoryTracker:
        self.start()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.stop()
