"""Thực hiện Công đoạn 1.3 trong Tài liệu 1 và Module 3.2 (annotation_mapper.py) trong Tài liệu 2."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass

from src.data.fasta_parser import ProteinRecord


@dataclass
class AnnotationMapping:
    """Đối tượng chứa thông tin ánh xạ nhãn phân họ và thống kê kích thước nhóm."""
    label_map: dict[str, str]  # seq_id -> subfamily_label
    subfamily_counts: dict[str, int]
    rare_subfamilies: list[str]
    major_subfamilies: list[str]
    medium_subfamilies: list[str]
    singleton_subfamilies: list[str]
    imbalance_ratio: float


class AnnotationMapper:
    """Bộ trích xuất và ánh xạ nhãn phân loại học / phân họ protein."""

    UNKNOWN_LABELS: frozenset[str] = frozenset(
        {"A01.Unknown", "F_Unknown", "TE_Unclassified", "UNKNOWN"}
    )

    @staticmethod
    def is_unknown_label(label: str) -> bool:
        """Kiểm tra xem nhãn phân họ có thuộc nhóm chưa định danh (Unknown / UPA) hay không."""
        return label in AnnotationMapper.UNKNOWN_LABELS

    @staticmethod
    def extract_merops_subfamily(header: str) -> str:
        """Trích xuất mã phân họ định danh [A01.xxx] từ header MEROPS A1A.

        Thu nhận đầy đủ cả 75 phân họ mã số ([A01.001]..[A01.971]) và 40 phân họ mã chữ-số
        ([A01.A02]..[A01.P02]) thành tổng cộng 115 phân họ định danh; gán nhãn 'A01.Unknown'
        cho khối chuỗi chưa định danh [A01.UPA].
        """
        match = re.search(r"\[([A-Z]\d{2}\.(?!UPA)[A-Z0-9]{3})\]", header)
        if match:
            return match.group(1)
        return "A01.Unknown"

    @staticmethod
    def extract_ce_subfamily(header: str) -> str:
        """Trích xuất mã nhóm phụ /Fxx/ từ header Carboxylesterase (ESTHER)."""
        match = re.search(r"/([Ff]\d+)/", header)
        if match:
            return match.group(1).upper()
        return "F_Unknown"

    @staticmethod
    def extract_thyme_family(header: str, seq_id: str, mapping_table: dict[str, str] | None = None) -> str:
        """Trích xuất họ Thioesterase (TE1-TE27) từ bảng ánh xạ hoặc header."""
        if mapping_table is not None:
            if seq_id in mapping_table:
                return mapping_table[seq_id]
            # Try searching by header substring
            for k, v in mapping_table.items():
                if k in header:
                    return v

        # Try finding explicit TE pattern in header, e.g., TE1, TE14, TE-2, TE_1, Thioesterase Family 1
        te_match = re.search(
            r"\b(?:TE|Thioesterase[-_ ]?Family[-_ ]?|Thioesterase[-_ ]?Fam[-_ ]?|Family[-_ ]?|Fam[-_ ]?)(\d+)\b",
            header,
            re.IGNORECASE,
        )
        if te_match:
            return f"TE{te_match.group(1)}"

        # Try finding gene name GN=...
        gn_match = re.search(r"\bGN=([A-Za-z0-9_-]+)", header)
        if gn_match:
            return f"GN_{gn_match.group(1)}"

        # Try finding organism OS=...
        os_match = re.search(r"\bOS=([A-Za-z0-9_ ]+?)(?:\s+OX=|\s+GN=|\s+PE=|\s+SV=|$)", header)
        if os_match:
            org = os_match.group(1).strip().replace(" ", "_")
            return f"OS_{org[:25]}"

        return "TE_Unclassified"

    @classmethod
    def extract_merops_subfamilies(cls, records: list[ProteinRecord]) -> dict[str, str]:
        """Trích xuất toàn bộ nhãn phân họ cho tập bản ghi MEROPS."""
        return {rec.id: cls.extract_merops_subfamily(rec.header) for rec in records}

    @classmethod
    def extract_ce_subgroups(cls, records: list[ProteinRecord]) -> dict[str, str]:
        """Trích xuất toàn bộ nhãn nhóm phụ cho tập bản ghi Carboxylesterase."""
        return {rec.id: cls.extract_ce_subfamily(rec.header) for rec in records}

    @classmethod
    def extract_thyme_families(
        cls, records: list[ProteinRecord], mapping_table: dict[str, str] | None = None
    ) -> dict[str, str]:
        """Trích xuất toàn bộ nhãn họ cho tập bản ghi Thioesterase."""
        return {rec.id: cls.extract_thyme_family(rec.header, rec.id, mapping_table) for rec in records}

    @staticmethod
    def compute_family_statistics(label_map: dict[str, str]) -> dict[str, int]:
        """Đếm số lượng thành viên n_g của từng phân họ."""
        counts = Counter(label_map.values())
        return dict(counts)

    @staticmethod
    def identify_rare_families(subfamily_counts: dict[str, int], threshold: int = 5) -> list[str]:
        """Xác định danh sách các phân họ hiếm (n_g <= threshold)."""
        return [fam for fam, count in subfamily_counts.items() if count <= threshold]

    @classmethod
    def get_subfamily_statistics(
        cls, label_map: dict[str, str], rare_threshold: int = 5
    ) -> dict[str, object]:
        """Tính toán thống kê chi tiết cấu trúc phân họ và độ mất cân bằng."""
        if not label_map:
            return {
                "subfamily_counts": {},
                "total_subfamilies": 0,
                "major_groups": [],
                "medium_groups": [],
                "rare_groups": [],
                "singleton_groups": [],
                "imbalance_ratio": 1.0,
            }

        counts = Counter(label_map.values())
        subfamily_counts = dict(counts.most_common())

        major_groups = [fam for fam, cnt in subfamily_counts.items() if cnt >= 20]
        medium_groups = [fam for fam, cnt in subfamily_counts.items() if 5 < cnt < 20]
        rare_groups = [fam for fam, cnt in subfamily_counts.items() if cnt <= rare_threshold]
        singleton_groups = [fam for fam, cnt in subfamily_counts.items() if cnt == 1]

        max_c = max(subfamily_counts.values()) if subfamily_counts else 1
        min_c = min(subfamily_counts.values()) if subfamily_counts else 1
        imbalance_ratio = round(max_c / min_c, 2) if min_c > 0 else float("inf")

        return {
            "subfamily_counts": subfamily_counts,
            "total_subfamilies": len(subfamily_counts),
            "major_groups": major_groups,
            "medium_groups": medium_groups,
            "rare_groups": rare_groups,
            "singleton_groups": singleton_groups,
            "imbalance_ratio": imbalance_ratio,
        }

    @classmethod
    def map_annotations(
        cls,
        records: list[ProteinRecord],
        dataset_name: str,
        mapping_table: dict[str, str] | None = None,
        rare_threshold: int = 5,
    ) -> AnnotationMapping:
        """Ánh xạ nhãn tự động dựa trên tên tập dữ liệu."""
        dname_lower = dataset_name.lower().strip()
        if (
            "thyme" in dname_lower
            or "thioesterase" in dname_lower
            or dname_lower == "te"
            or "te_" in dname_lower
            or "_te" in dname_lower
        ):
            label_map = cls.extract_thyme_families(records, mapping_table=mapping_table)
        elif "merops" in dname_lower or "a1a" in dname_lower or "peptidase" in dname_lower:
            label_map = cls.extract_merops_subfamilies(records)
        elif (
            "carboxylesterase" in dname_lower
            or "esther" in dname_lower
            or dname_lower == "ce"
            or "ce_" in dname_lower
            or "_ce" in dname_lower
            or "esterase" in dname_lower
        ):
            label_map = cls.extract_ce_subgroups(records)
        else:
            # Fallback auto-detection from first few headers
            first_headers = [r.header for r in records[:10]]
            if any("[" in h and "]" in h for h in first_headers):
                label_map = cls.extract_merops_subfamilies(records)
            elif any("/F" in h or "/f" in h for h in first_headers):
                label_map = cls.extract_ce_subgroups(records)
            else:
                label_map = cls.extract_thyme_families(records, mapping_table=mapping_table)

        stats = cls.get_subfamily_statistics(label_map, rare_threshold=rare_threshold)
        return AnnotationMapping(
            label_map=label_map,
            subfamily_counts=stats["subfamily_counts"],
            rare_subfamilies=stats["rare_groups"],
            major_subfamilies=stats["major_groups"],
            medium_subfamilies=stats["medium_groups"],
            singleton_subfamilies=stats["singleton_groups"],
            imbalance_ratio=stats["imbalance_ratio"],
        )


# Standalone function aliases matching Doc 2 specifications
def extract_merops_subfamilies(records: list[ProteinRecord]) -> dict[str, str]:
    """Trích xuất mã phân họ [A01.xxx] từ header MEROPS A1A."""
    return AnnotationMapper.extract_merops_subfamilies(records)


def extract_ce_subgroups(records: list[ProteinRecord]) -> dict[str, str]:
    """Trích xuất mã nhóm /Fxx/ từ header Carboxylesterase."""
    return AnnotationMapper.extract_ce_subgroups(records)


def extract_thyme_families(
    records: list[ProteinRecord], mapping_table: dict[str, str] | None = None
) -> dict[str, str]:
    """Trích xuất họ TE từ header hoặc bảng ánh xạ."""
    return AnnotationMapper.extract_thyme_families(records, mapping_table)


def get_subfamily_statistics(label_map: dict[str, str], rare_threshold: int = 5) -> dict[str, object]:
    """Đếm số lượng thành viên n_g của từng phân họ và xác định nhóm hiếm."""
    return AnnotationMapper.get_subfamily_statistics(label_map, rare_threshold)
