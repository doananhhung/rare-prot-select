"""Thực hiện Công đoạn 3.1 trong Tài liệu 1 và Module 3.3 (dense_similarity.py) trong Tài liệu 2."""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
from tqdm import tqdm

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


def compute_mean_centered_cosine_matrix(
    raw_embeddings: np.ndarray,
    beta: float = 0.70,
) -> np.ndarray:
    """Tính ma trận tương đồng Partial Mean-Centered Cosine không âm trên không gian ESM-2:
    1. Dịch tâm có kiểm soát: z_centered = z - beta * mean(z, axis=0) (với beta in [0.0, 1.0])
    2. Chuẩn hóa L2: z_norm = z_centered / ||z_centered||_2
    3. Tương đồng không âm: S_ESM(u, v) = max(0.0, z_norm(u)^T @ z_norm(v)) in [0.0, 1.0], S_ESM(v, v) = 1.0

    Thực hiện Công đoạn 3.1 trong Tài liệu 1 để khử hiện tượng Suy biến Dị hướng (Representation Anisotropy)
    trong khi bảo toàn tín hiệu đồng nguyên của Siêu họ Peptidase A1.

    Args:
        raw_embeddings: Ma trận vector nhúng ESM-2 kích thước (N, D), kiểu float32/float64.
        beta: Hệ số dịch tâm đám mây (mặc định 0.70).

    Returns:
        np.ndarray: Ma trận tương đồng đối xứng kích thước (N, N) kiểu float32 trong đoạn [0.0, 1.0].
    """
    n_samples = raw_embeddings.shape[0]
    if n_samples == 0:
        return np.empty((0, 0), dtype=np.float32)

    emb_f64 = np.asarray(raw_embeddings, dtype=np.float64)
    if not np.all(np.isfinite(emb_f64)):
        raise ValueError("Phát hiện giá trị NaN hoặc Inf trong ma trận vector nhúng ESM-2!")

    beta_val = float(beta)
    if not (0.0 <= beta_val <= 1.0):
        raise ValueError(f"Hệ số dịch tâm beta phải nằm trong [0.0, 1.0], nhận được: {beta_val}")

    # 1. Dịch tâm có kiểm soát theo vector tâm đám mây toàn cục mu = mean(Z, axis=0)
    mean_vec = np.mean(emb_f64, axis=0, keepdims=True)
    centered_f64 = emb_f64 - beta_val * mean_vec

    # 2. Chuẩn hóa đơn vị L2 cho từng vector đã dịch tâm
    norms = np.linalg.norm(centered_f64, axis=1, keepdims=True)
    norms = np.maximum(norms, 1e-12)
    z_norm = (centered_f64 / norms).astype(np.float32)

    # 3. Tính tích vô hướng và chiếu không âm max(0, cos) trên GPU PyTorch CUDA nếu khả dụng
    sim_matrix: np.ndarray | None = None
    try:
        import torch
        if torch.cuda.is_available():
            with torch.no_grad():
                tensor_emb = torch.from_numpy(z_norm).to("cuda", dtype=torch.float32)
                raw_sim_t = torch.matmul(tensor_emb, tensor_emb.T)
                sim_t = torch.clamp(raw_sim_t, min=0.0, max=1.0)
                sim_t = 0.5 * (sim_t + sim_t.T)
                sim_t.fill_diagonal_(1.0)
                sim_matrix = sim_t.cpu().numpy().astype(np.float32)
    except Exception as e:
        logger.debug("Torch CUDA acceleration skipped in compute_mean_centered_cosine_matrix: %s", e)

    if sim_matrix is None:
        raw_sim = np.matmul(z_norm, z_norm.T)
        sim_matrix = np.clip(raw_sim, 0.0, 1.0).astype(np.float32)
        sim_matrix = (0.5 * (sim_matrix + sim_matrix.T)).astype(np.float32)
        np.fill_diagonal(sim_matrix, 1.0)

    prune_ratio_pct = float((sim_matrix >= 0.90).mean() * 100.0)
    positive_density_pct = float((sim_matrix > 0.0).mean() * 100.0)
    logger.info(
        "Partial Mean-Centered Cosine ESM-2 matrix (beta=%.2f) constructed: shape=%s, positive_density=%.2f%%, "
        "mean_sim=%.4f, pairs>=0.90=%.4f%%",
        beta_val,
        str(sim_matrix.shape),
        positive_density_pct,
        float(sim_matrix.mean()),
        prune_ratio_pct,
    )
    return sim_matrix


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


class ESM2SimilarityMatrix:
    """Quản lý nạp vector nhúng ESM-2, chuẩn hóa Partial Mean-Centered Cosine và lưu đệm ma trận tương đồng."""

    def __init__(
        self,
        model_name: str = "facebook/esm2_t12_35M_UR50D",
        embeddings_cache_dir: str | Path = "outputs/embeddings_cache",
        similarity_cache_dir: str | Path = "outputs/similarity_cache",
        batch_size: int = 16,
        device: str = "auto",
        center_shift_beta: float = 0.70,
    ) -> None:
        self.model_name = str(model_name)
        self.embeddings_cache_dir = Path(embeddings_cache_dir)
        self.similarity_cache_dir = Path(similarity_cache_dir)
        self.batch_size = int(batch_size)
        self.device = str(device)
        self.center_shift_beta = float(center_shift_beta)
        self.embeddings_cache_dir.mkdir(parents=True, exist_ok=True)
        self.similarity_cache_dir.mkdir(parents=True, exist_ok=True)

    def load_or_extract_embeddings(
        self,
        records: list[object],
        dataset_name: str,
        force_recompute: bool = False,
    ) -> np.ndarray:
        """Nạp ma trận nhúng (N, D) từ outputs/embeddings_cache/{dataset_name}_{model_slug}.npy
        hoặc trích xuất bằng mô hình HuggingFace ESM-2 trên GPU nếu chưa có cache.
        Kiểm tra nghiêm ngặt shape[0] == len(records) và không chứa NaN/Inf.
        """
        model_slug = self.model_name.replace("/", "_")
        emb_file = self.embeddings_cache_dir / f"{dataset_name}_{model_slug}.npy"
        expected_n = len(records)

        if not force_recompute and emb_file.exists():
            emb = np.load(emb_file)
            if emb.ndim == 2 and emb.shape[0] == expected_n and np.all(np.isfinite(emb)):
                logger.info(
                    "Loaded cached ESM-2 embeddings from %s: shape=%s, dtype=%s",
                    emb_file,
                    str(emb.shape),
                    str(emb.dtype),
                )
                return emb.astype(np.float32)
            logger.warning(
                "Cached embeddings %s shape=%s mismatch with expected N=%d; recomputing...",
                emb_file,
                str(emb.shape),
                expected_n,
            )

        import torch
        from transformers import AutoModel, AutoTokenizer

        target_device = self.device
        if target_device == "auto":
            target_device = "cuda" if torch.cuda.is_available() else "cpu"

        logger.info("Extracting ESM-2 embeddings using %s on %s...", self.model_name, target_device)
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        model = AutoModel.from_pretrained(self.model_name).to(target_device)
        model.eval()

        sequences: list[str] = [str(getattr(r, "sequence")) for r in records]
        all_vecs: list[np.ndarray] = []

        with torch.no_grad():
            for start_idx in tqdm(
                range(0, expected_n, self.batch_size),
                desc="Extracting ESM-2 Embeddings",
                unit="batch",
                dynamic_ncols=True,
            ):
                batch_seqs = sequences[start_idx : start_idx + self.batch_size]
                encoded = tokenizer(
                    batch_seqs,
                    return_tensors="pt",
                    padding=True,
                    truncation=True,
                    max_length=1024,
                ).to(target_device)
                outputs = model(**encoded)
                hidden = outputs.last_hidden_state  # (B, L, D)
                mask = encoded["attention_mask"].unsqueeze(-1).to(hidden.dtype)  # (B, L, 1)
                # Loại bỏ token CLS (đầu) và EOS (cuối mỗi chuỗi) hoặc mean-pool trên các vị trí có attention_mask
                summed = torch.sum(hidden * mask, dim=1)
                counts = torch.clamp(torch.sum(mask, dim=1), min=1.0)
                pooled = (summed / counts).cpu().numpy().astype(np.float32)
                all_vecs.append(pooled)

        emb_matrix = np.vstack(all_vecs).astype(np.float32)
        np.save(emb_file, emb_matrix)
        logger.info("Saved extracted ESM-2 embeddings to %s (shape=%s)", emb_file, str(emb_matrix.shape))
        return emb_matrix

    def get_similarity_matrix(
        self,
        records: list[object],
        seq_ids: list[str],
        dataset_name: str,
        force_recompute: bool = False,
    ) -> np.ndarray:
        """Nạp hoặc tính toán ma trận tương đồng Partial Mean-Centered Cosine (N, N) kiểu float32,
        lưu đệm tại outputs/similarity_cache/{dataset_name}_esm2_mc_cosine_sim_matrix.npz.
        """
        cache_file = self.similarity_cache_dir / f"{dataset_name}_esm2_mc_cosine_sim_matrix.npz"
        expected_n = len(seq_ids)

        if not force_recompute and cache_file.exists():
            try:
                data = np.load(cache_file, allow_pickle=True)
                cached_matrix = data["sim_matrix"]
                cached_ids = [str(x) for x in data["seq_ids"]]
                meta_obj = data["metadata"].item() if "metadata" in data else {}
                cached_beta = float(meta_obj.get("center_shift_beta", -1.0)) if isinstance(meta_obj, dict) else -1.0
                if (
                    cached_matrix.shape == (expected_n, expected_n)
                    and cached_ids == seq_ids
                    and abs(cached_beta - self.center_shift_beta) < 1e-6
                ):
                    logger.info(
                        "Loaded ESM-2 Partial Mean-Centered Cosine (beta=%.2f) similarity matrix from cache: %s",
                        self.center_shift_beta,
                        cache_file,
                    )
                    return cached_matrix.astype(np.float32)
                logger.info(
                    "Cached ESM-2 matrix beta=%.2f differs from requested beta=%.2f; recomputing...",
                    cached_beta,
                    self.center_shift_beta,
                )
            except Exception as e:
                logger.warning("Failed to load cached ESM-2 matrix from %s: %s. Recomputing...", cache_file, e)

        raw_embeddings = self.load_or_extract_embeddings(
            records=records,
            dataset_name=dataset_name,
            force_recompute=False,
        )
        sim_matrix = compute_mean_centered_cosine_matrix(raw_embeddings, beta=self.center_shift_beta)

        np.savez_compressed(
            cache_file,
            sim_matrix=sim_matrix,
            seq_ids=np.array(seq_ids, dtype=object),
            metadata={
                "dataset": dataset_name,
                "num_sequences": expected_n,
                "model_name": self.model_name,
                "normalization": "partial_mean_centered_cosine",
                "center_shift_beta": self.center_shift_beta,
            },
        )
        logger.info(
            "Saved ESM-2 Partial Mean-Centered Cosine (beta=%.2f) similarity matrix to cache: %s",
            self.center_shift_beta,
            cache_file,
        )
        return sim_matrix

