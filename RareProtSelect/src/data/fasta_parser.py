"""Thực hiện Công đoạn 1.1 trong Tài liệu 1 và Module 3.2 (fasta_parser.py) trong Tài liệu 2."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProteinRecord:
    """Đối tượng biểu diễn một bản ghi protein chuẩn hóa từ tệp FASTA."""
    id: str
    sequence: str
    header: str
    length: int

    def __repr__(self) -> str:
        return f"ProteinRecord(id='{self.id}', length={self.length}, header='{self.header[:40]}...')"


class FastaParser:
    """Bộ phân tích cú pháp tệp FASTA sinh học."""

    @staticmethod
    def parse_header(header_line: str) -> tuple[str, str]:
        """Bóc tách định danh duy nhất (id) và phần mô tả từ dòng header FASTA.

        Hỗ trợ các định dạng:
        - MEROPS: >MER0000885 - pepsin A ... -> id = 'MER0000885'
        - UniProt/SwissProt: >sp|G8JVR4| Ethanol ... -> id = 'G8JVR4'
        - ESTHER/CE: >9acar-l7m799 /F12/ ... -> id = '9acar-l7m799'
        - Thông thường: >ID Description -> id = 'ID'
        """
        clean_header = header_line.strip()
        if clean_header.startswith(">"):
            clean_header = clean_header[1:].strip()

        if not clean_header:
            return "", ""

        # Check for UniProt format: sp|ACCESSION| or tr|ACCESSION|
        uniprot_match = re.match(r"^(?:sp|tr)\|([A-Za-z0-9_-]+)\|?(.*)$", clean_header)
        if uniprot_match:
            seq_id = uniprot_match.group(1).strip()
            desc = uniprot_match.group(2).strip()
            return seq_id, desc

        # Check for first token (before space or tab or -)
        parts = clean_header.split(maxsplit=1)
        seq_id = parts[0].strip()
        # Clean potential trailing hyphen or separator
        if seq_id.endswith("-"):
            seq_id = seq_id[:-1].strip()

        desc = parts[1].strip() if len(parts) > 1 else ""
        return seq_id, desc

    @staticmethod
    def remove_gaps(sequence: str) -> str:
        """Loại bỏ ký tự khoảng trắng, dấu gạch ngang alignment (-), dấu chấm (.)."""
        return re.sub(r"[\s\-\.]", "", sequence)

    @classmethod
    def dewrap(cls, sequence: str) -> str:
        """Nối các dòng chuỗi bị ngắt, khử khoảng trắng và chuẩn hóa thành chữ hoa."""
        clean_seq = cls.remove_gaps(sequence)
        return clean_seq.upper()

    @classmethod
    def read_fasta(cls, file_path: str | Path) -> list[ProteinRecord]:
        """Đọc tệp FASTA thô và chuyển đổi thành danh sách ProteinRecord chuẩn hóa."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Không tìm thấy tệp FASTA: {path}")

        records: list[ProteinRecord] = []
        current_header: str | None = None
        current_id: str | None = None
        current_seq_fragments: list[str] = []

        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line_str = line.strip()
                if not line_str:
                    continue

                if line_str.startswith(">"):
                    if current_header is not None and current_id is not None:
                        seq_str = cls.dewrap("".join(current_seq_fragments))
                        records.append(
                            ProteinRecord(
                                id=current_id,
                                sequence=seq_str,
                                header=current_header,
                                length=len(seq_str),
                            )
                        )
                    current_header = line_str
                    current_id, _ = cls.parse_header(line_str)
                    current_seq_fragments = []
                else:
                    current_seq_fragments.append(line_str)

            # Process last record
            if current_header is not None and current_id is not None:
                seq_str = cls.dewrap("".join(current_seq_fragments))
                records.append(
                    ProteinRecord(
                        id=current_id,
                        sequence=seq_str,
                        header=current_header,
                        length=len(seq_str),
                    )
                )

        return records

    @staticmethod
    def write_fasta(records: list[ProteinRecord], output_path: str | Path, line_wrap: int = 60) -> None:
        """Ghi danh sách ProteinRecord ra tệp FASTA chuẩn."""
        out_p = Path(output_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)

        with open(out_p, "w", encoding="utf-8") as f:
            for rec in records:
                header = rec.header if rec.header.startswith(">") else f">{rec.header}"
                f.write(f"{header}\n")
                seq = rec.sequence
                if line_wrap > 0:
                    for i in range(0, len(seq), line_wrap):
                        f.write(f"{seq[i:i+line_wrap]}\n")
                else:
                    f.write(f"{seq}\n")


def parse_fasta(file_path: str | Path) -> list[ProteinRecord]:
    """Đọc tệp FASTA thô và chuyển đổi thành danh sách ProteinRecord chuẩn hóa."""
    return FastaParser.read_fasta(file_path)
