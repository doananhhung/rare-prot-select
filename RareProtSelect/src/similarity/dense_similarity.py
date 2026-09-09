"""Thực hiện Công đoạn 3.1 trong Tài liệu 1 và Module 3.4 (dense_similarity.py) trong Tài liệu 2."""

from __future__ import annotations

import logging
import numpy as np

logger = logging.getLogger(__name__)


def compute_cosine_similarity_matrix(normalized_embeddings: np.ndarray) -> np.ndarray:
    """Tính ma trận tương đồng Cosine không âm: Sim(u, v) = max(0, z(u)^T @ z(v)).

    Bảo đảm các tính chất toán học chuẩn mực cho bài toán Submodular Facility Location:
    1. Không âm (Non-negative): Sim[u, v] >= 0.0 với mọi u, v (điều kiện cần cho tính Monotone Submodular).
    2. Đối xứng (Symmetric): Sim[u, v] = Sim[v, u].
    3. Đường chéo tự tương đồng (Self-similarity): Sim[v, v] = 1.0.
    4. Giới hạn chuẩn: Sim[u, v] in [0.0, 1.0].

    Args:
        normalized_embeddings: Ma trận vector nhúng đã chuẩn hóa L2 (||z||_2 = 1.0),
                               kích thước (N, d).

    Returns:
        np.ndarray: Ma trận tương đồng đối xứng kích thước (N, N) kiểu float64 trong đoạn [0, 1].
    """
    n_samples = normalized_embeddings.shape[0]
    if n_samples == 0:
        return np.empty((0, 0), dtype=np.float64)

    # Fast GPU acceleration via PyTorch CUDA when available
    try:
        import torch
        if torch.cuda.is_available():
            with torch.no_grad():
                tensor_emb = torch.from_numpy(normalized_embeddings).to("cuda", dtype=torch.float32)
                raw_sim_t = torch.matmul(tensor_emb, tensor_emb.T)
                sim_t = torch.clamp(raw_sim_t, min=0.0, max=1.0)
                sim_t = 0.5 * (sim_t + sim_t.T)
                sim_t.fill_diagonal_(1.0)
                return sim_t.cpu().numpy().astype(np.float64)
    except Exception as e:
        logger.debug("Torch CUDA acceleration skipped: %s. Using NumPy fallback.", e)

    # NumPy Fallback
    raw_sim = np.dot(normalized_embeddings, normalized_embeddings.T)
    sim_matrix = np.maximum(0.0, raw_sim)
    sim_matrix = np.clip(sim_matrix, 0.0, 1.0)
    sim_matrix = 0.5 * (sim_matrix + sim_matrix.T)
    np.fill_diagonal(sim_matrix, 1.0)
    return sim_matrix.astype(np.float64)


class DenseSimilarity:
    """Bộ tính toán Không gian Tương đồng Ngữ nghĩa Cosine Đầy đủ (Dense Similarity Space)."""

    def __init__(self) -> None:
        pass

    def compute_similarity_matrix(self, normalized_embeddings: np.ndarray) -> np.ndarray:
        """Tính ma trận tương đồng Cosine không âm từ tập vector nhúng L2-normalized."""
        return compute_cosine_similarity_matrix(normalized_embeddings)

    def compute_pairwise_similarity(self, z1: np.ndarray, z2: np.ndarray) -> float:
        """Tính độ tương đồng Cosine không âm giữa hai vector protein đơn lẻ.

        Args:
            z1: Vector nhúng thứ nhất (đã chuẩn hóa L2).
            z2: Vector nhúng thứ hai (đã chuẩn hóa L2).

        Returns:
            float: Giá trị tương đồng trong đoạn [0.0, 1.0].
        """
        v1 = z1.flatten()
        v2 = z2.flatten()
        dot_val = float(np.dot(v1, v2))
        return float(np.clip(max(0.0, dot_val), 0.0, 1.0))
