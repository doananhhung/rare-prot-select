"""Thực hiện Công đoạn 1.2 trong Tài liệu 1 và Module 3.2 (quality_filter.py) trong Tài liệu 2."""

from __future__ import annotations

from dataclasses import dataclass

from src.data.fasta_parser import ProteinRecord

# 20 axit amin tiêu chuẩn
STANDARD_AMINO_ACIDS = frozenset("ACDEFGHIKLMNPQRSTVWY")


@dataclass
class QualityFilterResult:
    """Kết quả kiểm soát chất lượng (QC) cho tập protein."""
    cleaned_records: list[ProteinRecord]
    qc_stats: dict[str, int | float]


class QualityFilter:
    """Bộ kiểm soát chất lượng chuỗi protein (Quality Control)."""

    def __init__(
        self,
        min_len: int = 30,
        max_len: int = 2000,
        max_ambiguous_ratio: float = 0.05,
        deduplicate: bool = True,
    ) -> None:
        self.min_len = min_len
        self.max_len = max_len
        self.max_ambiguous_ratio = max_ambiguous_ratio
        self.deduplicate = deduplicate

    def filter_sequences(self, records: list[ProteinRecord]) -> QualityFilterResult:
        """Lọc bỏ các chuỗi rác, phân mảnh hoặc chứa quá nhiều ký tự lạ.

        Tiêu chí kiểm định:
        1. Độ dài: L in [min_len, max_len]
        2. Tỷ lệ axit amin không xác định (ngoài 20 axit amin chuẩn) <= max_ambiguous_ratio
        3. Khử trùng lặp chuỗi và ID (nếu deduplicate=True)
        """
        total_input = len(records)
        passed_records: list[ProteinRecord] = []

        filtered_too_short = 0
        filtered_too_long = 0
        filtered_ambiguous = 0
        filtered_duplicates = 0

        seen_ids: set[str] = set()
        seen_seqs: set[str] = set()

        for rec in records:
            # 1. Kiểm tra trùng lặp
            if self.deduplicate:
                if rec.id in seen_ids or rec.sequence in seen_seqs:
                    filtered_duplicates += 1
                    continue

            # 2. Kiểm tra độ dài
            seq_len = rec.length
            if seq_len < self.min_len:
                filtered_too_short += 1
                continue
            if seq_len > self.max_len:
                filtered_too_long += 1
                continue

            # 3. Kiểm tra tỷ lệ ký tự không chuẩn
            if seq_len > 0:
                non_std_count = sum(1 for aa in rec.sequence if aa not in STANDARD_AMINO_ACIDS)
                ambiguous_ratio = non_std_count / seq_len
                if ambiguous_ratio > self.max_ambiguous_ratio:
                    filtered_ambiguous += 1
                    continue
            else:
                filtered_too_short += 1
                continue

            # Thỏa mãn mọi tiêu chí
            seen_ids.add(rec.id)
            seen_seqs.add(rec.sequence)
            passed_records.append(rec)

        passed_count = len(passed_records)
        pass_rate = (passed_count / total_input) if total_input > 0 else 0.0

        qc_stats: dict[str, int | float] = {
            "total_input": total_input,
            "passed_qc": passed_count,
            "filtered_too_short": filtered_too_short,
            "filtered_too_long": filtered_too_long,
            "filtered_ambiguous": filtered_ambiguous,
            "filtered_duplicates": filtered_duplicates,
            "pass_rate": round(pass_rate, 4),
        }

        return QualityFilterResult(cleaned_records=passed_records, qc_stats=qc_stats)


def filter_proteins(
    records: list[ProteinRecord],
    min_len: int = 30,
    max_len: int = 2000,
    max_ambiguous_ratio: float = 0.05,
    deduplicate: bool = True,
) -> tuple[list[ProteinRecord], dict[str, int | float]]:
    """Lọc bỏ các chuỗi rác, phân mảnh hoặc chứa quá nhiều ký tự lạ.

    Trả về: (Danh sách chuỗi sạch, Thống kê lọc QC).
    """
    filter_obj = QualityFilter(
        min_len=min_len,
        max_len=max_len,
        max_ambiguous_ratio=max_ambiguous_ratio,
        deduplicate=deduplicate,
    )
    result = filter_obj.filter_sequences(records)
    return result.cleaned_records, result.qc_stats
