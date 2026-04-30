"""Generate architecture.png for README embedding (no external diagram tools required)."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    out_path = root / "architecture.png"

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.axis("off")

    def box(x, y, w, h, text):
        patch = FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.03,rounding_size=0.12",
            linewidth=1.6,
            edgecolor="#1f3a5f",
            facecolor="#eef5ff",
        )
        ax.add_patch(patch)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=11, wrap=True)

    box(0.3, 2.0, 2.2, 1.2, "Input\nInvoice PDF/Image")
    box(2.9, 2.0, 2.6, 1.2, "Azure AI\nDocument Intelligence\n(OCR + layout)")
    box(6.0, 2.0, 2.4, 1.2, "Agent brain\nAzure OpenAI\n(ReAct)")
    box(8.9, 2.0, 2.2, 1.2, "Tools\nValidate totals\nPolicy RAG")
    box(4.4, 0.35, 3.6, 1.05, "Output\nStructured invoice report")

    def arrow(x1, y1, x2, y2):
        ax.add_patch(
            FancyArrowPatch(
                (x1, y1),
                (x2, y2),
                arrowstyle="-|>",
                mutation_scale=14,
                linewidth=1.4,
                color="#1f3a5f",
            )
        )

    arrow(2.55, 2.6, 2.85, 2.6)
    arrow(5.55, 2.6, 5.95, 2.6)
    arrow(8.45, 2.6, 8.85, 2.6)
    arrow(10.0, 2.0, 6.2, 1.45)
    arrow(6.2, 2.0, 6.2, 1.45)

    ax.text(
        6.0,
        4.55,
        "Invoice Analysis Agent — Single-agent pipeline (final implementation)",
        ha="center",
        va="center",
        fontsize=13,
        fontweight="bold",
        color="#102542",
    )

    fig.tight_layout()
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
