"""Thực hiện Công đoạn 3.1 (Sparse Variant) trong Tài liệu 1 và Module 3.4 (sparse_knn.py) trong Tài liệu 2."""

from __future__ import annotations

import logging
import numpy as np
import scipy.sparse as sp
from sklearn.neighbors import NearestNeighbors

logger = logging.getLogger(__name__)


def compute_sparse_knn_similarity(
    normalized_embeddings: np.ndarray,
    k_neighbors: int = 50,
    symmetric: bool = True,
) -> sp.csr_matrix:
    """Tính ma trận tương đồng Cosine thưa Sparse k-NN (CSR format) cho tập dữ liệu lớn.

    Chỉ giữ lại k láng giềng gần nhất cho mỗi protein để tiết kiệm bộ nhớ khi N > 50,000.

    Args:
        normalized_embeddings: Ma trận vector nhúng đã chuẩn hóa L2 kích thước (N, d).
        k_neighbors: Số lượng láng giềng gần nhất cần lưu giữ cho mỗi phần tử.
        symmetric: Có ép ma trận về dạng đối xứng (Sim = max(Sim, Sim.T)) hay không.

    Returns:
        scipy.sparse.csr_matrix: Ma trận thưa CSR kích thước (N, N) với giá trị trong đoạn [0, 1].
    """
    n_samples = normalized_embeddings.shape[0]
    if n_samples == 0:
        return sp.csr_matrix((0, 0), dtype=np.float64)

    eff_k = min(k_neighbors + 1, n_samples)

    nn = NearestNeighbors(n_neighbors=eff_k, metric="cosine", algorithm="auto")
    nn.fit(normalized_embeddings)
    distances, indices = nn.kneighbors(normalized_embeddings)

    # Convert cosine distance to non-negative cosine similarity: sim = max(0, 1 - distance)
    sim_values = np.maximum(0.0, 1.0 - distances)
    sim_values = np.clip(sim_values, 0.0, 1.0)

    # Build COO sparse matrix
    row_indices = np.repeat(np.arange(n_samples), eff_k)
    col_indices = indices.flatten()
    data_values = sim_values.flatten()

    sparse_sim = sp.coo_matrix(
        (data_values, (row_indices, col_indices)),
        shape=(n_samples, n_samples),
        dtype=np.float64,
    ).tocsr()

    # Enforce unit diagonal
    sparse_sim.setdiag(1.0)

    if symmetric:
        sparse_sim = sparse_sim.maximum(sparse_sim.T).tocsr()

    return sparse_sim


class SparseKNNSimilarity:
    """Bộ tính toán Không gian Tương đồng Thưa Sparse k-NN cho quy mô lớn."""

    def __init__(self, k_neighbors: int = 50, symmetric: bool = True) -> None:
        self.k_neighbors = k_neighbors
        self.symmetric = symmetric

    def compute_sparse_knn_matrix(
        self,
        normalized_embeddings: np.ndarray,
    ) -> sp.csr_matrix:
        """Tính ma trận CSR k-NN từ tập vector nhúng L2-normalized."""
        return compute_sparse_knn_similarity(
            normalized_embeddings,
            k_neighbors=self.k_neighbors,
            symmetric=self.symmetric,
        )
