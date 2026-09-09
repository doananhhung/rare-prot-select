"""Thực hiện Quản lý Cấu hình trong Tài liệu 1 và Module 3.1 trong Tài liệu 2."""

from __future__ import annotations

import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class PathConfig:
    """Cấu hình đường dẫn tệp tin và thư mục dữ liệu/kết quả."""
    fasta_path: str
    benchmark_gold_path: str | None = None
    output_dir: str = "outputs"
    cache_dir: str = "outputs/embeddings_cache"
    similarity_cache_dir: str = "outputs/similarity_cache"
    figures_dir: str = "outputs/figures"
    tables_dir: str = "outputs/tables"
    logs_dir: str = "outputs/logs"


@dataclass
class QualityFilterConfig:
    """Cấu hình tiêu chí kiểm soát chất lượng chuỗi protein (QC)."""
    min_seq_len: int = 30
    max_seq_len: int = 2000
    max_ambiguous_ratio: float = 0.05
    deduplicate: bool = True


@dataclass
class ModelConfig:
    """Cấu hình mô hình ngôn ngữ protein (ESM-2) và phần cứng."""
    model_name: str = "facebook/esm2_t12_35M_UR50D"
    device: str = "auto"  # 'auto', 'cuda', 'cpu'
    batch_size: int = 16


@dataclass
class OptimizationConfig:
    """Cấu hình thuật toán chọn tập đại diện submodular và trọng số."""
    budget_k_list: list[int] = field(default_factory=lambda: [5, 10, 20, 50, 100])
    weighting_scheme: str = "inverse_sqrt"  # 'inverse_sqrt', 'uniform', 'inverse_freq', 'power'
    weighting_alpha: float = 0.5


@dataclass
class EvaluationConfig:
    """Cấu hình đánh giá khoa học và phân định nhóm hiếm."""
    rare_threshold: int = 5
    seed: int = 42


@dataclass
class PlotConfig:
    """Cấu hình trực quan hóa đồ thị."""
    dpi: int = 300
    fig_format: str = "png"
    style: str = "seaborn-v0_8-whitegrid"


@dataclass
class ExperimentConfig:
    """Cấu hình toàn diện cho một thực nghiệm của RareProtSelect."""
    dataset_name: str
    fasta_path: str
    benchmark_gold_path: str | None = None
    model_name: str = "facebook/esm2_t12_35M_UR50D"
    device: str = "auto"  # 'auto', 'cuda', 'cpu'
    batch_size: int = 16
    budget_k_list: list[int] = field(default_factory=lambda: [5, 10, 20, 50, 100])
    weighting_scheme: str = "inverse_sqrt"  # 'inverse_sqrt', 'uniform', 'inverse_freq', 'power'
    weighting_alpha: float = 0.5
    rare_threshold: int = 5
    min_seq_len: int = 30
    max_seq_len: int = 2000
    max_ambiguous_ratio: float = 0.05
    output_dir: str = "outputs"
    cache_dir: str = "outputs/embeddings_cache"
    seed: int = 42
    extra_params: dict[str, Any] = field(default_factory=dict)

    def get_path_config(self) -> PathConfig:
        """Tạo đối tượng PathConfig từ cấu hình thực nghiệm."""
        return PathConfig(
            fasta_path=self.fasta_path,
            benchmark_gold_path=self.benchmark_gold_path,
            output_dir=self.output_dir,
            cache_dir=self.cache_dir,
            similarity_cache_dir=os.path.join(self.output_dir, "similarity_cache"),
            figures_dir=os.path.join(self.output_dir, "figures"),
            tables_dir=os.path.join(self.output_dir, "tables"),
            logs_dir=os.path.join(self.output_dir, "logs"),
        )

    def get_quality_config(self) -> QualityFilterConfig:
        """Tạo đối tượng QualityFilterConfig từ cấu hình thực nghiệm."""
        return QualityFilterConfig(
            min_seq_len=self.min_seq_len,
            max_seq_len=self.max_seq_len,
            max_ambiguous_ratio=self.max_ambiguous_ratio,
        )

    def get_model_config(self) -> ModelConfig:
        """Tạo đối tượng ModelConfig từ cấu hình thực nghiệm."""
        return ModelConfig(
            model_name=self.model_name,
            device=self.device,
            batch_size=self.batch_size,
        )

    def get_optimization_config(self) -> OptimizationConfig:
        """Tạo đối tượng OptimizationConfig từ cấu hình thực nghiệm."""
        return OptimizationConfig(
            budget_k_list=list(self.budget_k_list),
            weighting_scheme=self.weighting_scheme,
            weighting_alpha=self.weighting_alpha,
        )

    def get_evaluation_config(self) -> EvaluationConfig:
        """Tạo đối tượng EvaluationConfig từ cấu hình thực nghiệm."""
        return EvaluationConfig(
            rare_threshold=self.rare_threshold,
            seed=self.seed,
        )

    def to_dict(self) -> dict[str, Any]:
        """Chuyển đổi cấu hình thành từ điển."""
        return asdict(self)


def load_config(yaml_path: str | Path) -> ExperimentConfig:
    """Nạp cấu hình từ tệp YAML và khởi tạo đối tượng ExperimentConfig."""
    yaml_path = Path(yaml_path)
    if not yaml_path.exists():
        raise FileNotFoundError(f"Không tìm thấy tệp cấu hình YAML: {yaml_path}")

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    # Extract known fields
    known_fields = {
        "dataset_name",
        "fasta_path",
        "benchmark_gold_path",
        "model_name",
        "device",
        "batch_size",
        "budget_k_list",
        "weighting_scheme",
        "weighting_alpha",
        "rare_threshold",
        "min_seq_len",
        "max_seq_len",
        "max_ambiguous_ratio",
        "output_dir",
        "cache_dir",
        "seed",
    }

    constructor_kwargs: dict[str, Any] = {}
    extra_params: dict[str, Any] = {}

    for key, value in data.items():
        if key in known_fields:
            constructor_kwargs[key] = value
        else:
            extra_params[key] = value

    if "extra_params" in constructor_kwargs:
        constructor_kwargs["extra_params"].update(extra_params)
    else:
        constructor_kwargs["extra_params"] = extra_params

    config = ExperimentConfig(**constructor_kwargs)
    validate_config(config)
    return config


def validate_config(config: ExperimentConfig) -> bool:
    """Kiểm tra tính hợp lệ toán học và logic của các tham số cấu hình."""
    if not config.dataset_name or not isinstance(config.dataset_name, str):
        raise ValueError("`dataset_name` phải là một chuỗi ký tự không rỗng.")

    if not config.fasta_path or not isinstance(config.fasta_path, str):
        raise ValueError("`fasta_path` phải là đường dẫn tệp tin hợp lệ.")

    if config.min_seq_len <= 0:
        raise ValueError(f"`min_seq_len` phải > 0, nhận được: {config.min_seq_len}")

    if config.max_seq_len < config.min_seq_len:
        raise ValueError(
            f"`max_seq_len` ({config.max_seq_len}) phải >= `min_seq_len` ({config.min_seq_len})"
        )

    if not (0.0 <= config.max_ambiguous_ratio <= 1.0):
        raise ValueError(
            f"`max_ambiguous_ratio` phải nằm trong [0.0, 1.0], nhận được: {config.max_ambiguous_ratio}"
        )

    if config.batch_size <= 0:
        raise ValueError(f"`batch_size` phải > 0, nhận được: {config.batch_size}")

    if not config.budget_k_list or not all(isinstance(k, int) and k > 0 for k in config.budget_k_list):
        raise ValueError("`budget_k_list` phải là danh sách các số nguyên dương.")

    valid_schemes = {"inverse_sqrt", "uniform", "inverse_freq", "power"}
    if config.weighting_scheme not in valid_schemes:
        raise ValueError(
            f"`weighting_scheme` không hợp lệ: '{config.weighting_scheme}'. "
            f"Các lựa chọn hợp lệ: {valid_schemes}"
        )

    if config.rare_threshold < 1:
        raise ValueError(f"`rare_threshold` phải >= 1, nhận được: {config.rare_threshold}")

    return True
