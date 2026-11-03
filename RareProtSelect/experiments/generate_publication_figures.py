#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate publication-quality Figure 3 for RareProtSelect Report
- Panel A: Budget Trajectory of Rare Sensitivity (k = 1 to 115)
- Panel B: Pareto Trade-off at Full Budget (k = 115)
Uses Vietnamese decimal commas, large clear typography, and clean un-overlapping layout.
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def main():
    csv_path = Path("RareProtSelect/outputs/tables/exp2_rare_weighted_a1a.csv")
    if not csv_path.exists():
        raise FileNotFoundError(f"Cannot find CSV at {csv_path}")

    df = pd.read_csv(csv_path)

    # Set font styling
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["font.size"] = 11

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.2, 5.8))

    # ==========================================
    # PANEL A: Trajectory vs k (1 to 115)
    # ==========================================
    df_00 = df[df["alpha"] == 0.0].sort_values("budget_k")
    df_05 = df[df["alpha"] == 0.5].sort_values("budget_k")
    df_10 = df[df["alpha"] == 1.0].sort_values("budget_k")

    # Plot lines
    ax1.plot(df_00["budget_k"], df_00["rare_sensitivity_blast_pct"],
             color="#7f7f7f", linestyle="--", linewidth=2.4, marker="o", markersize=6,
             label=r"Mô hình cơ sở ($\alpha = 0,00$)")
    ax1.plot(df_05["budget_k"], df_05["rare_sensitivity_blast_pct"],
             color="#d95f02", linestyle="-", linewidth=3.0, marker="s", markersize=7,
             label=r"RareProtSelect cân bằng ($\alpha = 0,50$)")
    ax1.plot(df_10["budget_k"], df_10["rare_sensitivity_blast_pct"],
             color="#1b9e77", linestyle="-.", linewidth=2.4, marker="^", markersize=6.5,
             label=r"RareProtSelect ưu tiên tối đa ($\alpha = 1,00$)")

    # Key annotations on Panel A
    # Point at k=115 for alpha=0.5
    ax1.annotate(r"$\mathbf{\alpha = 0,50}$" + " (59,11%)",
                 xy=(115, 59.11), xytext=(-125, -6), textcoords="offset points",
                 fontsize=11.5, fontweight="bold", color="#d95f02",
                 arrowprops=dict(arrowstyle="->", color="#d95f02", lw=1.5),
                 bbox=dict(boxstyle="round,pad=0.25", facecolor="#fff2e6", edgecolor="#d95f02", lw=1.2))

    # Point at k=115 for alpha=1.0
    ax1.annotate(r"$\mathbf{\alpha = 1,00}$" + " (91,11%)",
                 xy=(115, 91.11), xytext=(-125, -18), textcoords="offset points",
                 fontsize=11.5, fontweight="bold", color="#1b9e77",
                 arrowprops=dict(arrowstyle="->", color="#1b9e77", lw=1.5),
                 bbox=dict(boxstyle="round,pad=0.25", facecolor="#e6f7f2", edgecolor="#1b9e77", lw=1.2))

    # Point at k=115 for alpha=0.0
    ax1.annotate(r"$\mathbf{\alpha = 0,00}$" + " (2,22%)",
                 xy=(115, 2.22), xytext=(-125, 16), textcoords="offset points",
                 fontsize=11, fontweight="bold", color="#555555",
                 arrowprops=dict(arrowstyle="->", color="#555555", lw=1.2),
                 bbox=dict(boxstyle="round,pad=0.2", facecolor="#f0f0f0", edgecolor="#888888", lw=1.0))

    # Highlight region k=1..50
    ax1.annotate(r"Dải ngân sách $k = 1 - 50$:" + "\n" + r"$\alpha = 0,00$ duy trì mức $0,00\%$",
                 xy=(25, 0.0), xytext=(15, 24), textcoords="offset points",
                 fontsize=10.5, color="#555555",
                 arrowprops=dict(arrowstyle="->", color="#888888", lw=1.0),
                 bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#aaaaaa", lw=0.8, alpha=0.9))

    # Annotation at inflection point k=20
    ax1.annotate(r"Điểm uốn bứt phá từ $k = 20$" + "\n" + r"($\alpha = 0,50$ bắt đầu tăng tốc)",
                 xy=(20, 2.22), xytext=(0, 44), textcoords="offset points",
                 fontsize=10.5, color="#d95f02", ha="center",
                 arrowprops=dict(arrowstyle="->", color="#d95f02", lw=1.2),
                 bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#d95f02", lw=0.8, alpha=0.9))

    ax1.set_title("A. Tiến trình tăng trưởng Rare Sensitivity theo ngân sách $k$", fontsize=12.5, fontweight="bold", pad=10)
    ax1.set_xlabel(r"Ngân sách chuỗi đại diện $k$ ($1 \dots 115$)", fontsize=11.5, fontweight="bold")
    ax1.set_ylabel(r"Rare Sensitivity (%) (45 nhóm hiếm $\leq$ 5 chuỗi)", fontsize=11.5, fontweight="bold")
    ax1.set_xlim(-2, 122)
    ax1.set_ylim(-5, 105)
    ax1.grid(True, linestyle="--", alpha=0.55)
    ax1.legend(loc="upper left", frameon=True, fontsize=10.5, framealpha=0.95, edgecolor="#cccccc")

    # ==========================================
    # PANEL B: Pareto Trade-off at k = 115
    # ==========================================
    df_115 = df[df["budget_k"] == 115].sort_values("alpha")
    overall = df_115["overall_sensitivity_blast_pct"].tolist()
    worst = df_115["worst_group_sensitivity_blast_pct"].tolist()
    rare = df_115["rare_sensitivity_blast_pct"].tolist()
    macro = df_115["macro_sensitivity_blast_pct"].tolist()

    # Lines connecting the 3 alpha points
    ax2.plot(overall, worst, marker="o", color="#e41a1c", linewidth=2.6, markersize=8.5, label="Worst-Group Sensitivity (0,00%)")
    ax2.plot(overall, rare, marker="s", color="#1f77b4", linewidth=2.8, linestyle="--", markersize=9, label=r"Rare Sensitivity (45 nhóm $\leq$ 5)")
    ax2.plot(overall, macro, marker="^", color="#2ca02c", linewidth=2.4, linestyle=":", markersize=8.5, label="Macro Sensitivity (115 nhóm)")

    # Annotations on Panel B
    # Point alpha = 1.00 (overall=79.08, rare=91.11, macro=83.44)
    ax2.annotate(r"$\mathbf{\alpha = 1,00}$" + " (91,11%)",
                 xy=(overall[2], rare[2]), xytext=(12, -4), textcoords="offset points",
                 fontsize=11.5, fontweight="bold", color="#1f77b4",
                 bbox=dict(boxstyle="round,pad=0.2", facecolor="#edf4fb", edgecolor="#1f77b4", lw=1.0))
    ax2.annotate(r"$\alpha = 1,00$" + " (83,44%)",
                 xy=(overall[2], macro[2]), xytext=(12, -14), textcoords="offset points",
                 fontsize=10.5, fontweight="bold", color="#2ca02c",
                 bbox=dict(boxstyle="round,pad=0.15", facecolor="#eef8ee", edgecolor="#2ca02c", lw=0.8))

    # Point alpha = 0.50 (overall=94.13, rare=59.11, macro=78.87) - BEST SURVEYED TRADEOFF
    ax2.annotate(r"$\mathbf{\alpha = 0,50}$" + " (59,11%)\n[Điểm cân bằng tốt nhất khảo sát]",
                 xy=(overall[1], rare[1]), xytext=(-16, 8), textcoords="offset points", ha="right",
                 fontsize=11.5, fontweight="bold", color="#1f77b4",
                 arrowprops=dict(arrowstyle="->", color="#1f77b4", lw=1.5),
                 bbox=dict(boxstyle="round,pad=0.25", facecolor="#e6f2ff", edgecolor="#1f77b4", lw=1.2))

    ax2.annotate(r"$\alpha = 0,50$" + " (78,87%)",
                 xy=(overall[1], macro[1]), xytext=(-16, -2), textcoords="offset points", ha="right",
                 fontsize=10.5, fontweight="bold", color="#2ca02c",
                 bbox=dict(boxstyle="round,pad=0.15", facecolor="#eef8ee", edgecolor="#2ca02c", lw=0.8))

    # Point alpha = 0.00 (overall=93.57, rare=2.22, macro=49.28)
    ax2.annotate(r"$\mathbf{\alpha = 0,00}$" + " (2,22%)",
                 xy=(overall[0], rare[0]), xytext=(-14, 10), textcoords="offset points", ha="right",
                 fontsize=11, fontweight="bold", color="#1f77b4",
                 bbox=dict(boxstyle="round,pad=0.15", facecolor="#edf4fb", edgecolor="#1f77b4", lw=0.8))
    ax2.annotate(r"$\alpha = 0,00$" + " (49,28%)",
                 xy=(overall[0], macro[0]), xytext=(-14, -8), textcoords="offset points", ha="right",
                 fontsize=10.5, fontweight="bold", color="#2ca02c",
                 bbox=dict(boxstyle="round,pad=0.15", facecolor="#eef8ee", edgecolor="#2ca02c", lw=0.8))

    ax2.set_title(r"B. Đánh đổi Pareto giữa Overall Sens. và Rare Sens. tại $k = 115$", fontsize=12.5, fontweight="bold", pad=10)
    ax2.set_xlabel("Overall Within-Subfamily Sensitivity BLAST (%)", fontsize=11.5, fontweight="bold")
    ax2.set_ylabel("Subfamily Sensitivity (%)", fontsize=11.5, fontweight="bold")
    ax2.set_xlim(75.5, 98.0)
    ax2.set_ylim(-5, 105)
    ax2.grid(True, linestyle="--", alpha=0.55)
    ax2.legend(loc="upper right", frameon=True, fontsize=10.5, framealpha=0.95, edgecolor="#cccccc")

    plt.suptitle("Đánh giá định lượng hiệu năng tái cân bằng của RareProtSelect trên tập MEROPS A1A",
                 fontsize=13.5, fontweight="bold", y=0.98)
    plt.tight_layout()

    # Save to outputs and latex directory
    out_png1 = Path("RareProtSelect/outputs/figures/exp2_pareto_tradeoff.png")
    out_svg1 = Path("RareProtSelect/outputs/figures/exp2_pareto_tradeoff.svg")
    out_png2 = Path("report_latex/Images/figures/exp2_pareto_tradeoff.png")
    out_svg2 = Path("report_latex/Images/figures/exp2_pareto_tradeoff.svg")

    fig.savefig(out_png1, dpi=300, bbox_inches="tight")
    fig.savefig(out_svg1, bbox_inches="tight")
    fig.savefig(out_png2, dpi=300, bbox_inches="tight")
    fig.savefig(out_svg2, bbox_inches="tight")
    plt.close(fig)

    print(f"Successfully generated new Figure 3 to:\n  - {out_png1}\n  - {out_png2}")

if __name__ == "__main__":
    main()
