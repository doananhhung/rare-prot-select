"""Thực hiện Tích hợp Giai đoạn 1 trong Tài liệu 1 và Module 3.2 (dataset_loader.py) trong Tài liệu 2."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.config.settings import ExperimentConfig
from src.data.annotation_mapper import AnnotationMapper
from src.data.fasta_parser import FastaParser, ProteinRecord
from src.data.quality_filter import QualityFilter

logger = logging.getLogger(__name__)


@dataclass
class DatasetBundle:
    """Tập hợp dữ liệu đã qua tiền xử lý, kiểm định chất lượng và ánh xạ nhãn."""
    records: list[ProteinRecord]
    cleaned_records: list[ProteinRecord]
    label_map: dict[str, str]
    subfamily_counts: dict[str, int]
    rare_subfamilies: list[str]
    qc_stats: dict[str, Any]

    @property
    def num_raw(self) -> int:
        return len(self.records)

    @property
    def num_cleaned(self) -> int:
        return len(self.cleaned_records)

    @property
    def num_subfamilies(self) -> int:
        return len(self.subfamily_counts)

    @property
    def num_rare_subfamilies(self) -> int:
        return len(self.rare_subfamilies)


class DatasetLoader:
    """Bộ nạp và tiền xử lý toàn diện cho dữ liệu protein."""

    @staticmethod
    def resolve_path(path_str: str) -> Path:
        """Chuẩn hóa và tìm kiếm đường dẫn tệp tin thực tế."""
        p = Path(path_str)
        if p.exists():
            return p.resolve()

        # Check relative to project root or current working dir
        cwd = Path.cwd()
        candidate = (cwd / p).resolve()
        if candidate.exists():
            return candidate

        # Check if running from RareProtSelect subfolder
        candidate_parent = (cwd.parent / p).resolve()
        if candidate_parent.exists():
            return candidate_parent

        return p

    @classmethod
    def load_and_preprocess_dataset(
        cls,
        config: ExperimentConfig,
        mapping_table: dict[str, str] | None = None,
    ) -> DatasetBundle:
        """Thực thi pipeline Giai đoạn 1: Đọc FASTA -> Lọc QC -> Ánh xạ phân họ."""
        resolved_fasta_path = cls.resolve_path(config.fasta_path)
        logger.info(f"Loading FASTA data from: {resolved_fasta_path}")

        # 1. Đọc FASTA thô
        raw_records = FastaParser.read_fasta(resolved_fasta_path)
        logger.info(f"Parsed {len(raw_records)} raw sequences from {config.dataset_name}.")

        # 2. Kiểm soát chất lượng (QC)
        qc_filter = QualityFilter(
            min_len=config.min_seq_len,
            max_len=config.max_seq_len,
            max_ambiguous_ratio=config.max_ambiguous_ratio,
            deduplicate=True,
        )
        qc_result = qc_filter.filter_sequences(raw_records)
        cleaned_records = qc_result.cleaned_records
        qc_stats = qc_result.qc_stats
        logger.info(
            f"QC completed: {qc_stats['passed_qc']}/{qc_stats['total_input']} sequences passed "
            f"({qc_stats['pass_rate'] * 100:.1f}%)."
        )

        # 3. Ánh xạ nhãn phân họ & phân định nhóm hiếm
        mapping_result = AnnotationMapper.map_annotations(
            records=cleaned_records,
            dataset_name=config.dataset_name,
            mapping_table=mapping_table,
            rare_threshold=config.rare_threshold,
        )

        logger.info(
            f"Label mapping complete: {len(mapping_result.subfamily_counts)} families. "
            f"Rare families (<= {config.rare_threshold}): {len(mapping_result.rare_subfamilies)}, "
            f"Imbalance ratio: {mapping_result.imbalance_ratio}x."
        )

        return DatasetBundle(
            records=raw_records,
            cleaned_records=cleaned_records,
            label_map=mapping_result.label_map,
            subfamily_counts=mapping_result.subfamily_counts,
            rare_subfamilies=mapping_result.rare_subfamilies,
            qc_stats=qc_stats,
        )


def load_dataset_pipeline(
    config: ExperimentConfig,
    mapping_table: dict[str, str] | None = None,
) -> DatasetBundle:
    """Nạp và tiền xử lý toàn diện tập dữ liệu theo cấu hình ExperimentConfig."""
    return DatasetLoader.load_and_preprocess_dataset(config, mapping_table)
