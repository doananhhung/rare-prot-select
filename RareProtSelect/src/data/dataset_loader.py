"""Thực hiện Tích hợp Giai đoạn 1 trong Tài liệu 1 và Module 3.2 (dataset_loader.py) trong Tài liệu 2."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from src.config.settings import ExperimentConfig, load_config
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
    qc_stats: dict[str, int | float | str | bool]

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

        # Check in baseline_repo relative to cwd or parent
        candidate_baseline_parent = (cwd.parent / "baseline_repo" / p.name).resolve()
        if candidate_baseline_parent.exists():
            return candidate_baseline_parent

        candidate_baseline_cwd = (cwd / "baseline_repo" / p.name).resolve()
        if candidate_baseline_cwd.exists():
            return candidate_baseline_cwd

        return p

    @classmethod
    def load_and_preprocess_dataset(
        cls,
        config: ExperimentConfig | Path | str,
        mapping_table: dict[str, str] | None = None,
        override_fasta: str | Path | None = None,
        override_dataset_name: str | None = None,
        exclude_unknown_subfamilies: bool | None = None,
    ) -> DatasetBundle:
        """Thực thi pipeline Giai đoạn 1: Đọc FASTA -> Lọc QC -> Ánh xạ phân họ (& lọc bỏ Unknown nếu Phương án 3B)."""
        if isinstance(config, (str, Path)):
            cfg_path = Path(config)
            if not cfg_path.exists():
                cwd = Path.cwd()
                candidate = cwd / cfg_path
                if candidate.exists():
                    cfg_path = candidate
                elif (cwd.parent / cfg_path).exists():
                    cfg_path = cwd.parent / cfg_path
            cfg = load_config(cfg_path)
        elif isinstance(config, ExperimentConfig):
            cfg = config
        else:
            raise TypeError(f"Expected ExperimentConfig, Path, or str, got {type(config)}")

        target_fasta = str(override_fasta) if override_fasta else cfg.fasta_path
        target_dataset_name = str(override_dataset_name) if override_dataset_name else cfg.dataset_name
        should_exclude_unknown: bool = (
            bool(exclude_unknown_subfamilies)
            if exclude_unknown_subfamilies is not None
            else bool(cfg.exclude_unknown_subfamilies)
        )

        resolved_fasta_path = cls.resolve_path(target_fasta)
        logger.info("Loading FASTA data from: %s", resolved_fasta_path)

        # 1. Đọc FASTA thô
        raw_records = FastaParser.read_fasta(resolved_fasta_path)
        logger.info("Parsed %d raw sequences from %s.", len(raw_records), target_dataset_name)

        # 2. Kiểm soát chất lượng (QC)
        qc_filter = QualityFilter(
            min_len=cfg.min_seq_len,
            max_len=cfg.max_seq_len,
            max_ambiguous_ratio=cfg.max_ambiguous_ratio,
            deduplicate=True,
        )
        qc_result = qc_filter.filter_sequences(raw_records)
        cleaned_records = qc_result.cleaned_records
        qc_stats = dict(qc_result.qc_stats)
        logger.info(
            "QC completed: %d/%d sequences passed (%.1f%%).",
            qc_stats["passed_qc"],
            qc_stats["total_input"],
            float(qc_stats["pass_rate"]) * 100.0,
        )

        # 3. Ánh xạ nhãn phân họ & lọc bỏ Unknown theo Phương án 3B (nếu bật exclude_unknown_subfamilies)
        mapping_result = AnnotationMapper.map_annotations(
            records=cleaned_records,
            dataset_name=target_dataset_name,
            mapping_table=mapping_table,
            rare_threshold=cfg.rare_threshold,
        )

        if should_exclude_unknown:
            before_curated = len(cleaned_records)
            cleaned_records = [
                r
                for r in cleaned_records
                if not AnnotationMapper.is_unknown_label(mapping_result.label_map.get(r.id, "UNKNOWN"))
            ]
            excluded_unknown_count = before_curated - len(cleaned_records)
            qc_stats["excluded_unknown_subfamily"] = excluded_unknown_count
            qc_stats["curated_passed_qc"] = len(cleaned_records)
            mapping_result = AnnotationMapper.map_annotations(
                records=cleaned_records,
                dataset_name=target_dataset_name,
                mapping_table=mapping_table,
                rare_threshold=cfg.rare_threshold,
            )
            logger.info(
                "Curated Option 3B applied (exclude_unknown_subfamilies=True): "
                "removed %d Unknown/UPA sequences -> retained %d curated sequences across %d subfamilies.",
                excluded_unknown_count,
                len(cleaned_records),
                len(mapping_result.subfamily_counts),
            )
        else:
            qc_stats["excluded_unknown_subfamily"] = 0
            qc_stats["curated_passed_qc"] = len(cleaned_records)

        logger.info(
            "Label mapping complete: %d families. Rare families (<= %d): %d, Imbalance ratio: %.1fx.",
            len(mapping_result.subfamily_counts),
            cfg.rare_threshold,
            len(mapping_result.rare_subfamilies),
            mapping_result.imbalance_ratio,
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
    config: ExperimentConfig | Path | str,
    mapping_table: dict[str, str] | None = None,
    override_fasta: str | Path | None = None,
    override_dataset_name: str | None = None,
    exclude_unknown_subfamilies: bool | None = None,
) -> DatasetBundle:
    """Nạp và tiền xử lý toàn diện tập dữ liệu theo cấu hình ExperimentConfig."""
    return DatasetLoader.load_and_preprocess_dataset(
        config=config,
        mapping_table=mapping_table,
        override_fasta=override_fasta,
        override_dataset_name=override_dataset_name,
        exclude_unknown_subfamilies=exclude_unknown_subfamilies,
    )
