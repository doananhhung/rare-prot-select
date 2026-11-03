"""Thực hiện Xuất Báo cáo Thực nghiệm trong Tài liệu 1 và Module 3.8 (exporter.py) trong Tài liệu 2."""

from __future__ import annotations

import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class NumpyJSONEncoder(json.JSONEncoder):
    """JSON Encoder hỗ trợ chuyển đổi các kiểu dữ liệu Numpy và Pandas."""

    def default(self, obj: object) -> object:
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        if isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, Path):
            return str(obj)
        return super().default(obj)


class ResultExporter:
    """Bộ công cụ xuất dữ liệu và báo cáo kết quả thực nghiệm đa định dạng (CSV, JSON, Markdown, LaTeX)."""

    @staticmethod
    def _ensure_dir(output_path: str | Path) -> Path:
        p = Path(output_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

    @classmethod
    def export_to_csv(cls, data: list[dict[str, object]] | pd.DataFrame, output_path: str | Path) -> None:
        """Xuất kết quả ra tệp CSV."""
        out_p = cls._ensure_dir(output_path)
        if isinstance(data, pd.DataFrame):
            df = data
        else:
            df = pd.DataFrame(data)
        df.to_csv(out_p, index=False, encoding="utf-8")
        logger.info(f"Exported CSV table: {out_p}")

    @classmethod
    def export_to_json(cls, data: dict[str, object] | list[object], output_path: str | Path, indent: int = 2) -> None:
        """Xuất kết quả ra tệp JSON."""
        out_p = cls._ensure_dir(output_path)
        with open(out_p, "w", encoding="utf-8") as f:
            json.dump(data, f, cls=NumpyJSONEncoder, indent=indent, ensure_ascii=False)
        logger.info(f"Exported JSON file: {out_p}")

    @classmethod
    def export_to_markdown(
        cls,
        df: pd.DataFrame,
        output_path: str | Path,
        title: str = "Experimental Results",
    ) -> None:
        """Xuất bảng kết quả ra tệp Markdown (.md) cho báo cáo khoa học."""
        out_p = cls._ensure_dir(output_path)
        md_content = f"# {title}\n\n"
        try:
            md_content += df.to_markdown(index=False)
        except Exception:
            # Fallback custom markdown table generator
            headers = [str(col) for col in df.columns]
            header_row = "| " + " | ".join(headers) + " |"
            sep_row = "| " + " | ".join(["---"] * len(headers)) + " |"
            rows = [header_row, sep_row]
            for _, row in df.iterrows():
                row_str = "| " + " | ".join(str(val) for val in row.values) + " |"
                rows.append(row_str)
            md_content += "\n".join(rows)
        md_content += "\n"
        with open(out_p, "w", encoding="utf-8") as f:
            f.write(md_content)
        logger.info(f"Exported Markdown report: {out_p}")

    @classmethod
    def export_summary_table(
        cls,
        results: list[dict[str, object]],
        output_base_path: str | Path,
        title: str = "Summary Table",
    ) -> None:
        """Xuất đồng thời ra CSV, JSON và Markdown."""
        base_p = Path(output_base_path)
        df = pd.DataFrame(results)

        csv_path = base_p.with_suffix(".csv")
        json_path = base_p.with_suffix(".json")
        md_path = base_p.with_suffix(".md")

        cls.export_to_csv(df, csv_path)
        cls.export_to_json(results, json_path)
        cls.export_to_markdown(df, md_path, title=title)

    @classmethod
    def export_dataframe(
        cls,
        df: pd.DataFrame,
        csv_path: str | Path,
        json_path: str | Path,
        markdown_path: str | Path,
        title: str = "Experimental Results",
    ) -> None:
        """Xuất đồng thời DataFrame ra cả 3 định dạng: CSV, JSON và Markdown."""
        cls.export_to_csv(df, csv_path)
        cls.export_to_json(df.to_dict(orient="records"), json_path)
        cls.export_to_markdown(df, markdown_path, title=title)


# Standalone function aliases matching Doc 2 specifications
def export_results_to_csv(data: list[dict] | pd.DataFrame, output_path: str) -> None:
    """Xuất kết quả ra tệp CSV."""
    ResultExporter.export_to_csv(data, output_path)


def export_results_to_json(data: dict | list, output_path: str) -> None:
    """Xuất kết quả ra tệp JSON."""
    ResultExporter.export_to_json(data, output_path)


def export_results_to_markdown(df: pd.DataFrame, output_path: str, title: str = "Experimental Results") -> None:
    """Xuất bảng kết quả ra Markdown."""
    ResultExporter.export_to_markdown(df, output_path, title)


def export_summary_table(results: list[dict], output_path: str, title: str = "Summary Table") -> None:
    """Xuất bảng tổng hợp kết quả."""
    ResultExporter.export_summary_table(results, output_path, title)
