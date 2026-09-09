"""Thực hiện Công đoạn 3.1 trong Tài liệu 1 và Module 3.4 trong Tài liệu 2."""

from src.similarity.dense_similarity import (
    DenseSimilarity,
    compute_cosine_similarity_matrix,
)
from src.similarity.sparse_knn import (
    SparseKNNSimilarity,
    compute_sparse_knn_similarity,
)

__all__ = [
    "DenseSimilarity",
    "compute_cosine_similarity_matrix",
    "SparseKNNSimilarity",
    "compute_sparse_knn_similarity",
]
