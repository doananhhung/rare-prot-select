"""Thực hiện Công đoạn 2.3 trong Tài liệu 1 và Module 3.3 (cache_manager.py) trong Tài liệu 2."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import numpy as np

logger = logging.getLogger(__name__)


def save_embeddings_cache(
    cache_path: str | Path,
    embeddings: np.ndarray,
    seq_ids: list[str],
    metadata: dict[str, Any] | None = None,
) -> None:
    """Lưu trữ vector nhúng .npy kèm metadata .json xuống đĩa.

    Args:
        cache_path: Đường dẫn tới tệp cache (có thể có hoặc không có đuôi .npy).
        embeddings: Mảng numpy chứa ma trận vector nhúng kích thước (N, d).
        seq_ids: Danh sách ID tương ứng với từng hàng của ma trận embeddings.
        metadata: Từ điển chứa siêu dữ liệu bổ sung (model_name, dataset_name, v.v.).
    """
    path_obj = Path(cache_path)
    if path_obj.suffix != ".npy":
        npy_path = path_obj.with_suffix(".npy")
        json_path = path_obj.with_suffix(".json")
    else:
        npy_path = path_obj
        json_path = path_obj.with_suffix(".json")

    npy_path.parent.mkdir(parents=True, exist_ok=True)

    if len(seq_ids) != embeddings.shape[0]:
        raise ValueError(
            f"Số lượng seq_ids ({len(seq_ids)}) không khớp với số hàng của embeddings ({embeddings.shape[0]})."
        )

    # Save binary npy array
    np.save(npy_path, embeddings)

    # Build metadata payload
    meta_payload = {
        "num_sequences": int(embeddings.shape[0]),
        "embedding_dim": int(embeddings.shape[1]) if embeddings.ndim > 1 else 0,
        "shape": list(embeddings.shape),
        "dtype": str(embeddings.dtype),
        "seq_ids": seq_ids,
        "saved_at": datetime.now(timezone.utc).isoformat(),
        "metadata": metadata or {},
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(meta_payload, f, indent=2, ensure_ascii=False)

    logger.info(
        "Successfully saved embeddings cache: %s (%d sequences, dim=%d)",
        npy_path.name,
        embeddings.shape[0],
        embeddings.shape[1] if embeddings.ndim > 1 else 0,
    )


def load_embeddings_cache(
    cache_path: str | Path,
) -> tuple[np.ndarray, list[str], dict[str, Any]]:
    """Nạp vector nhúng .npy và metadata .json từ đĩa.

    Args:
        cache_path: Đường dẫn tới tệp cache .npy hoặc .json.

    Returns:
        tuple[np.ndarray, list[str], dict[str, Any]]:
            - embeddings: Ma trận vector nhúng shape (N, d).
            - seq_ids: Danh sách ID chuỗi tương ứng.
            - metadata: Siêu dữ liệu lưu kèm.

    Raises:
        FileNotFoundError: Nếu tệp npy hoặc json không tồn tại.
        ValueError: Nếu cấu trúc cache bị hỏng hoặc không đồng bộ.
    """
    path_obj = Path(cache_path)
    npy_path = path_obj.with_suffix(".npy")
    json_path = path_obj.with_suffix(".json")

    if not npy_path.exists():
        raise FileNotFoundError(f"Không tìm thấy tệp embeddings .npy tại: {npy_path}")
    if not json_path.exists():
        raise FileNotFoundError(f"Không tìm thấy tệp metadata .json tại: {json_path}")

    embeddings = np.load(npy_path)

    with open(json_path, "r", encoding="utf-8") as f:
        meta_payload = json.load(f)

    seq_ids = meta_payload.get("seq_ids", [])
    if len(seq_ids) != embeddings.shape[0]:
        raise ValueError(
            f"Lỗi không đồng bộ cache: metadata có {len(seq_ids)} IDs nhưng npy có {embeddings.shape[0]} hàng."
        )

    logger.info(
        "Successfully loaded embeddings cache: %s (%d sequences, shape=%s)",
        npy_path.name,
        embeddings.shape[0],
        embeddings.shape,
    )
    return embeddings, seq_ids, meta_payload.get("metadata", {})


def is_cache_valid(
    cache_path: str | Path,
    expected_ids: list[str] | None = None,
) -> bool:
    """Kiểm tra tính hợp lệ và toàn vẹn của tệp đệm cache.

    Args:
        cache_path: Đường dẫn tới tệp cache.
        expected_ids: Danh sách ID kỳ vọng cần đối chiếu thứ tự và số lượng.

    Returns:
        bool: True nếu cache tồn tại, hợp lệ và khớp với expected_ids; ngược lại False.
    """
    path_obj = Path(cache_path)
    npy_path = path_obj.with_suffix(".npy")
    json_path = path_obj.with_suffix(".json")

    if not npy_path.exists() or not json_path.exists():
        return False

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            meta = json.load(f)

        cached_ids = meta.get("seq_ids", [])
        if expected_ids is not None:
            if cached_ids != expected_ids:
                logger.warning(
                    "Cache IDs do not match expected_ids (cached=%d, expected=%d).",
                    len(cached_ids),
                    len(expected_ids),
                )
                return False

        # Verify npy file readability and shape
        arr = np.load(npy_path, mmap_mode="r")
        if arr.shape[0] != len(cached_ids):
            return False

        return True
    except Exception as exc:
        logger.warning("Error checking cache validity: %s", exc)
        return False


class CacheManager:
    """Bộ quản lý bộ đệm Vector Nhúng cho toàn bộ các tập thực nghiệm của đề tài."""

    def __init__(self, cache_dir: str | Path = "outputs/embeddings_cache") -> None:
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_cache_path(self, dataset_name: str, model_name: str) -> Path:
        """Tạo đường dẫn chuẩn hóa cho tệp cache dựa trên tên dataset và model."""
        sanitized_model = model_name.replace("/", "_").replace("\\", "_")
        filename = f"{dataset_name}_{sanitized_model}.npy"
        return self.cache_dir / filename

    def save(
        self,
        dataset_name: str,
        model_name: str,
        embeddings: np.ndarray,
        seq_ids: list[str],
        metadata: dict[str, Any] | None = None,
    ) -> Path:
        """Lưu vector nhúng vào thư mục cache chuẩn hóa."""
        cache_path = self.get_cache_path(dataset_name, model_name)
        full_metadata = {
            "dataset_name": dataset_name,
            "model_name": model_name,
            **(metadata or {}),
        }
        save_embeddings_cache(cache_path, embeddings, seq_ids, full_metadata)
        return cache_path

    def load(
        self,
        dataset_name: str,
        model_name: str,
    ) -> tuple[np.ndarray, list[str], dict[str, Any]]:
        """Nạp vector nhúng từ thư mục cache chuẩn hóa."""
        cache_path = self.get_cache_path(dataset_name, model_name)
        return load_embeddings_cache(cache_path)

    def is_cached(
        self,
        dataset_name: str,
        model_name: str,
        expected_ids: list[str] | None = None,
    ) -> bool:
        """Kiểm tra xem dataset và model đã được lưu đệm hợp lệ hay chưa."""
        cache_path = self.get_cache_path(dataset_name, model_name)
        return is_cache_valid(cache_path, expected_ids)
