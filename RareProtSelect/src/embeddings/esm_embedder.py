"""Thực hiện Công đoạn 2.1 & 2.2 trong Tài liệu 1 và Module 3.3 (esm_embedder.py) trong Tài liệu 2."""

from __future__ import annotations

import logging
from typing import Any, Sequence
import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer

logger = logging.getLogger(__name__)

# Model name normalization map
MODEL_ALIASES: dict[str, str] = {
    "esm2_t6_8M_UR50D": "facebook/esm2_t6_8M_UR50D",
    "esm2_t12_35M_UR50D": "facebook/esm2_t12_35M_UR50D",
    "esm2_t30_150M_UR50D": "facebook/esm2_t30_150M_UR50D",
    "esm2_t33_650M_UR50D": "facebook/esm2_t33_650M_UR50D",
    "esm2_t36_3B_UR50D": "facebook/esm2_t36_3B_UR50D",
}


class ESMEmbedder:
    """Bộ sinh vector nhúng Protein qua mô hình ngôn ngữ ESM-2 (Facebook/Meta AI).

    Thực hiện mã hóa chuỗi amino acid thành biểu diễn tiềm ẩn (Công đoạn 2.1),
    gộp trung bình Mean Pooling trên chiều dài chuỗi và chuẩn hóa L2 (Công đoạn 2.2).
    """

    def __init__(
        self,
        model_name: str = "facebook/esm2_t12_35M_UR50D",
        device: str = "auto",
        torch_dtype: Any | None = None,
    ) -> None:
        """Khởi tạo ESMEmbedder với mô hình ESM-2 và cấu hình thiết bị phần cứng.

        Args:
            model_name: Tên mô hình HuggingFace hoặc alias (ví dụ 'facebook/esm2_t12_35M_UR50D').
            device: Thiết bị tính toán ('auto', 'cuda', 'cuda:0', 'cpu').
            torch_dtype: Kiểu dữ liệu PyTorch tùy chọn (ví dụ torch.float32, torch.float16).
        """
        self.raw_model_name = model_name
        self.model_name = MODEL_ALIASES.get(model_name, model_name)

        if device == "auto":
            if torch.cuda.is_available():
                self.device_str = "cuda:0"
                self.device = torch.device("cuda:0")
            else:
                self.device_str = "cpu"
                self.device = torch.device("cpu")
        elif device.startswith("cuda"):
            if torch.cuda.is_available():
                self.device_str = device
                self.device = torch.device(device)
            else:
                logger.warning(
                    "CUDA requested (%s) but not available. Falling back to CPU.",
                    device,
                )
                self.device_str = "cpu"
                self.device = torch.device("cpu")
        else:
            self.device_str = device
            self.device = torch.device(device)

        self.torch_dtype = torch_dtype

        logger.info(
            "Loading ESM-2 model '%s' on device '%s'...",
            self.model_name,
            self.device_str,
        )

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(
            self.model_name,
            torch_dtype=self.torch_dtype,
        )
        self.model.to(self.device)
        self.model.eval()

        self._embedding_dim = self.model.config.hidden_size
        logger.info(
            "ESM-2 model ready. Latent dimension d = %d.",
            self._embedding_dim,
        )

    @property
    def embedding_dim(self) -> int:
        """Số chiều vector nhúng ngữ nghĩa (ví dụ 480 cho 35M, 640 cho 150M)."""
        return self._embedding_dim

    def get_embedding_dim(self) -> int:
        """Trả về số chiều vector nhúng (tương thích hàm getter)."""
        return self._embedding_dim

    def embed_sequences(
        self,
        sequences: list[str] | Sequence[str],
        batch_size: int = 16,
        max_len: int = 1024,
        show_progress: bool = False,
    ) -> np.ndarray:
        r"""Sinh vector nhúng cho danh sách chuỗi: Mean Pooling + Chuẩn hóa L2.

        Quy trình xử lý:
        1. Tokenize danh sách chuỗi với padding và truncation theo max_len (1024).
        2. Chạy qua Transformer Attention của ESM-2 ở chế độ torch.no_grad().
        3. Trích xuất hidden states ở tầng cuối, gộp trung bình (Mean Pooling)
           chỉ trên các vị trí amino acid (loại bỏ token đặc biệt <cls>, <eos> và <pad>).
        4. Chuẩn hóa L2 cho mỗi vector: \hat{z} = z / ||z||_2, có bảo vệ chống chia cho 0.

        Args:
            sequences: Danh sách các chuỗi axit amin (ví dụ: ['MKWLL...', 'ACDEF...']).
            batch_size: Kích thước batch inference trên GPU/CPU.
            max_len: Chiều dài tối đa cho phép của context window ESM-2.
            show_progress: Có hiển thị thanh tiến trình tqdm hay không.

        Returns:
            np.ndarray: Mảng numpy kích thước (N, d) kiểu float32 với chuẩn L2 mỗi hàng = 1.0.
        """
        if len(sequences) == 0:
            return np.empty((0, self._embedding_dim), dtype=np.float32)

        all_embeddings: list[np.ndarray] = []
        n_seqs = len(sequences)

        batch_indices = range(0, n_seqs, batch_size)
        if show_progress:
            try:
                from tqdm import tqdm

                batch_indices = tqdm(
                    batch_indices,
                    desc=f"ESM-2 Embedding ({self.device_str})",
                    total=(n_seqs + batch_size - 1) // batch_size,
                )
            except ImportError:
                pass

        with torch.no_grad():
            for i in batch_indices:
                batch_seqs = list(sequences[i : i + batch_size])

                encoded_inputs = self.tokenizer(
                    batch_seqs,
                    padding=True,
                    truncation=True,
                    max_length=max_len,
                    return_tensors="pt",
                )

                input_ids = encoded_inputs["input_ids"].to(self.device)
                attention_mask = encoded_inputs["attention_mask"].to(self.device)

                outputs = self.model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                )
                hidden_states = outputs.last_hidden_state  # shape: (B, L_tokens, d)

                # Mean pooling over amino acid residues (excluding <cls> at idx 0, <eos>, and <pad>)
                residue_mask = attention_mask.clone()
                residue_mask[:, 0] = 0  # Exclude <cls> token at index 0

                seq_lengths = attention_mask.sum(dim=1)  # Total tokens per sequence
                for row_idx, r_len in enumerate(seq_lengths):
                    if r_len > 1:
                        residue_mask[row_idx, r_len - 1] = 0  # Exclude <eos> token

                # Compute mean over amino acid residues
                mask_expanded = residue_mask.unsqueeze(-1).expand_as(hidden_states).float()
                sum_embeddings = torch.sum(hidden_states * mask_expanded, dim=1)
                residue_counts = mask_expanded.sum(dim=1).clamp(min=1e-9)

                pooled = sum_embeddings / residue_counts  # shape: (B, d)

                # L2 Normalization with safe zero-division guard
                norms = torch.norm(pooled, p=2, dim=-1, keepdim=True)
                normalized = torch.where(
                    norms > 1e-12,
                    pooled / norms,
                    torch.zeros_like(pooled),
                )

                batch_np = normalized.detach().cpu().numpy().astype(np.float32)
                all_embeddings.append(batch_np)

        return np.vstack(all_embeddings)

    def embed_single_sequence(self, sequence: str, max_len: int = 1024) -> np.ndarray:
        """Sinh vector nhúng chuẩn hóa L2 cho một chuỗi protein đơn lẻ.

        Args:
            sequence: Chuỗi axit amin đơn lẻ.
            max_len: Giới hạn chiều dài context window.

        Returns:
            np.ndarray: Vector nhúng 1D kích thước (d,) với chuẩn L2 = 1.0.
        """
        result = self.embed_sequences([sequence], batch_size=1, max_len=max_len)
        return result[0]
