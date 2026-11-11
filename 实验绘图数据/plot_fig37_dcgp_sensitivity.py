from __future__ import annotations

import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
from matplotlib.offsetbox import AnchoredOffsetbox, HPacker, TextArea

from chapter3_plot_style import ENGLISH_FONT, SONGTI_FONT, apply_style


PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIGURE_DIR = PROJECT_ROOT / "02_论文图片" / "03_反应式学习调度"
TEXT_WIDTH_IN = 443.86319 / 72.27
X_LABEL_FONT = FontProperties(fname=Path(r"C:\Windows\Fonts\timesbi.ttf"), size=10.0)
Y_LABEL_FONT = FontProperties(fname=Path(r"C:\Windows\Fonts\timesbd.ttf"), size=9.2)


# 原始工作簿未随项目提供，以下数值按现有图3.7中的12个数据点录入。
SENSITIVITY_DATA = (
    ("Generation", ("10", "25", "50", "100"), (13.4, 9.7, 5.7, 6.3), (5.0, 15.0), 1.0),
    ("Parent size", ("2", "10", "20", "50"), (16.2, 7.8, 6.8, 6.7), (6.0, 17.0), 1.0),
    ("parent/offspring", ("0.2", "0.5", "1", "2"), (7.2, 5.6, 6.2, 9.3), (5.0, 10.0), 0.5),
)
PANEL_TITLES = ("进化代数", "父代规模", "父子代比例")


def style_axis(axis: plt.Axes) -> None:
    """保留原图的网格、四边框和Times New Roman刻度。"""
    axis.set_axisbelow(True)
    axis.grid(True, linestyle="--", linewidth=0.45, color="#D0D0D0", alpha=0.8)
    for spine in axis.spines.values():
        spine.set_visible(True)
        spine.set_color("#000000")
        spine.set_linewidth(0.75)
    axis.tick_params(width=0.7, length=3.0, labelrotation=0)
    for label in (*axis.get_xticklabels(), *axis.get_yticklabels()):
        font = ENGLISH_FONT.copy()
        font.set_size(label.get_fontsize())
        label.set_fontproperties(font)


def save_figure(figure: plt.Figure) -> None:
    """保留旧PNG，并导出可编辑矢量图和论文使用的PNG。"""
    stem = FIGURE_DIR / "dcgp_rpd_sensitivity_combined"
    original = FIGURE_DIR / "dcgp_rpd_sensitivity_combined_原图.png"
    if not original.exists():
        shutil.copy2(stem.with_suffix(".png"), original)
    figure.savefig(stem.with_suffix(".png"), dpi=600, bbox_inches="tight", pad_inches=0.03)
    figure.savefig(stem.with_suffix(".pdf"), bbox_inches="tight", pad_inches=0.03)
    figure.savefig(stem.with_suffix(".svg"), bbox_inches="tight", pad_inches=0.03)
    plt.close(figure)


def draw_figure() -> None:
    """保持正文通栏宽度，仅压缩纵向布局重画图3.7。"""
    apply_style()
    figure, axes = plt.subplots(1, 3, figsize=(TEXT_WIDTH_IN, 2.05))

    for panel_index, (axis, (xlabel, tick_labels, values, limits, tick_step), panel_title) in enumerate(
        zip(axes, SENSITIVITY_DATA, PANEL_TITLES)
    ):
        positions = np.arange(len(values))
        axis.plot(
            positions,
            values,
            color="#000000",
            linewidth=1.15,
            marker="o",
            markersize=4.8,
            markerfacecolor="#000000",
            markeredgewidth=0.8,
        )
        axis.set_xticks(positions, tick_labels)
        axis.set_ylim(*limits)
        axis.set_yticks(np.arange(limits[0], limits[1] + tick_step / 2, tick_step))
        axis.set_xlabel(xlabel, fontproperties=X_LABEL_FONT, labelpad=2.5)
        axis.set_ylabel("RPD (%)", fontproperties=Y_LABEL_FONT, labelpad=2.5)
        title = HPacker(
            children=(
                TextArea(
                    f"({chr(97 + panel_index)})",
                    textprops={"fontproperties": ENGLISH_FONT, "fontsize": 10.0},
                ),
                TextArea(
                    panel_title,
                    textprops={"fontproperties": SONGTI_FONT, "fontsize": 10.0},
                ),
            ),
            align="center",
            pad=0,
            sep=3,
        )
        axis.add_artist(AnchoredOffsetbox(
            loc="lower center",
            child=title,
            frameon=False,
            pad=0,
            borderpad=0,
            bbox_to_anchor=(0.5, 1.035),
            bbox_transform=axis.transAxes,
        ))
        style_axis(axis)

    # 缩短坐标轴高度和上下留白，文字与标记保持正常比例。
    figure.subplots_adjust(left=0.075, right=0.995, top=0.91, bottom=0.25, wspace=0.31)
    save_figure(figure)


if __name__ == "__main__":
    assert all(len(labels) == len(values) == 4 for _, labels, values, _, _ in SENSITIVITY_DATA)
    draw_figure()
