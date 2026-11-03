"""Thực hiện Công đoạn 5.3 trong Tài liệu 1 và Module 3.8 (timer.py) trong Tài liệu 2."""

from __future__ import annotations

import functools
import logging
import time
from types import TracebackType
from typing import Callable, ParamSpec, TypeVar

logger = logging.getLogger(__name__)

P = ParamSpec("P")
R = TypeVar("R")


class Timer:
    """Công cụ bấm giờ có độ chính xác cao bằng time.perf_counter()."""

    def __init__(self, name: str = "Task", auto_log: bool = False) -> None:
        self.name = name
        self.auto_log = auto_log
        self._start_time: float | None = None
        self._end_time: float | None = None
        self._elapsed: float = 0.0

    def start(self) -> Timer:
        """Bắt đầu tính giờ."""
        self._start_time = time.perf_counter()
        self._end_time = None
        self._elapsed = 0.0
        return self

    def stop(self) -> float:
        """Dừng tính giờ và trả về thời gian thực thi (giây)."""
        if self._start_time is None:
            raise RuntimeError("Timer chưa được khởi động bằng phương thức .start().")
        self._end_time = time.perf_counter()
        self._elapsed = self._end_time - self._start_time
        if self.auto_log:
            logger.info(f"[{self.name}] Elapsed time: {self._elapsed:.4f}s")
        return self._elapsed

    @property
    def elapsed_seconds(self) -> float:
        """Thời gian trôi qua tính bằng giây."""
        if self._start_time is None:
            return 0.0
        if self._end_time is not None:
            return self._elapsed
        return time.perf_counter() - self._start_time

    @property
    def elapsed_ms(self) -> float:
        """Thời gian trôi qua tính bằng mili-giây (ms)."""
        return self.elapsed_seconds * 1000.0

    def __enter__(self) -> Timer:
        self.start()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.stop()


# Alias for compatibility with ExecutionTimer
ExecutionTimer = Timer


def timeit(name: str | None = None, auto_log: bool = True) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorator đo thời gian chạy của hàm."""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        func_name = name or func.__name__

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            timer = Timer(name=func_name, auto_log=auto_log)
            with timer:
                result = func(*args, **kwargs)
            return result

        return wrapper
    return decorator
