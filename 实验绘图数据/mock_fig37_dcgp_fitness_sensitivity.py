from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
from matplotlib import font_manager
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.font_manager import FontProperties
from matplotlib.offsetbox import AnchoredOffsetbox, HPacker, TextArea

from chapter3_plot_style import ENGLISH_FONT, SONGTI_FONT, apply_style


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = Path(__file__).resolve().parent / "数据" / "mock_fig37_dcgp_fitness_sensitivity.csv"
FIGURE_DIR = PROJECT_ROOT / "02_论文图片" / "03_反应式学习调度"
OUTPUT_STEM = FIGURE_DIR / "mock_fig37_dcgp_fitness_sensitivity"
TEXT_WIDTH_IN = 443.86319 / 72.27
FIGURE_RATIO = 3.05  # 在第二章参数图基础上适度增加纵向尺寸。
X_LABEL_FONT = FontProperties(fname=Path(r"C:\Windows\Fonts\timesbi.ttf"), size=8.8)
X_SUBSCRIPT_FONT = FontProperties(fname=Path(r"C:\Windows\Fonts\timesbi.ttf"), size=6.4)
Y_LABEL_FONT = FontProperties(fname=Path(r"C:\Windows\Fonts\times.ttf"), size=8.8)
TIMES_ITALIC_PATH = Path(r"C:\Windows\Fonts\timesi.ttf")


def style_axis(axis: plt.Axes) -> None:
    axis.set_axisbelow(True)
    axis.grid(True, linestyle="--", linewidth=0.42, color="#D0D0D0", alpha=0.78)
    for spine in axis.spines.values():
        spine.set_visible(True)
        spine.set_color("#000000")
        spine.set_linewidth(0.72)
    axis.tick_params(axis="x", width=0.68, length=2.8, pad=1.8, labelrotation=0)
    axis.tick_params(axis="y", width=0.68, length=2.8, pad=4.0, labelrotation=90)
    for label in axis.get_xticklabels():
        font = ENGLISH_FONT.copy()
        font.set_size(7.6)
        label.set_fontproperties(font)
    for label in axis.get_yticklabels():
        font = ENGLISH_FONT.copy()
        font.set_size(7.6)
        label.set_fontproperties(font)
        label.set_rotation(90)
        label.set_rotation_mode("anchor")
        label.set_horizontalalignment("center")
        label.set_verticalalignment("center")


def add_panel_title(axis: plt.Axes, panel_index: int, chinese_title: str) -> None:
    title = HPacker(
        children=(
            TextArea(
                f"({chr(97 + panel_index)})",
                textprops={"fontproperties": ENGLISH_FONT, "fontsize": 8.8},
            ),
            TextArea(
                chinese_title,
                textprops={"fontproperties": SONGTI_FONT, "fontsize": 8.8},
            ),
        ),
        align="center",
        pad=0,
        sep=2.0,
    )
    axis.add_artist(
        AnchoredOffsetbox(
            loc="lower center",
            child=title,
            frameon=False,
            pad=0,
            borderpad=0,
            bbox_to_anchor=(0.5, 1.040),
            bbox_transform=axis.transAxes,
        )
    )


def format_levels(parameter: str, values: pd.Series) -> list[str]:
    numeric_values = values.to_numpy(dtype=float)
    if parameter in {"Generation", "Parent size"}:
        return [f"{value:.0f}" for value in numeric_values]
    if parameter == "parent/offspring":
        return [f"{value:g}" for value in numeric_values]
    return [f"{value:.2f}" for value in numeric_values]


def set_parameter_label(axis: plt.Axes, parameter: str) -> None:
    if parameter != r"$\tau_D$":
        axis.set_xlabel(parameter, fontproperties=X_LABEL_FONT, labelpad=2.0)
        return

    # 直接使用Times New Roman字形组合希腊字母和下标，避免mathtext字体回退。
    axis.set_xlabel("")
    axis.text(
        0.495,
        -0.145,
        "τ",
        transform=axis.transAxes,
        ha="right",
        va="center",
        fontproperties=X_LABEL_FONT,
        clip_on=False,
    )
    axis.text(
        0.505,
        -0.170,
        "D",
        transform=axis.transAxes,
        ha="left",
        va="center",
        fontproperties=X_SUBSCRIPT_FONT,
        clip_on=False,
    )


def draw_figure() -> None:
    """绘制图3.7上半部分；数据仅用于实验规划和版式预览。"""
    apply_style()
    font_manager.fontManager.addfont(TIMES_ITALIC_PATH)
    plt.rcParams.update(
        {
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "mathtext.fontset": "custom",
            "mathtext.rm": "Times New Roman",
            "mathtext.it": "Times New Roman:style=italic",
        }
    )
    frame = pd.read_csv(DATA_PATH)
    expected_status = "PLANNING DATA - replace before submission"
    if set(frame["data_status"]) != {expected_status}:
        raise ValueError("Mock data status marker is missing or inconsistent.")

    parameter_order = list(dict.fromkeys(frame["parameter"]))
    figure, axes = plt.subplots(
        1,
        4,
        figsize=(TEXT_WIDTH_IN, TEXT_WIDTH_IN / FIGURE_RATIO),
    )

    for panel_index, (axis, parameter) in enumerate(zip(axes, parameter_order)):
        subset = frame.loc[frame["parameter"] == parameter].sort_values("level_order")
        positions = np.arange(len(subset))
        values = subset["fitness_mean"].to_numpy(dtype=float)
        axis.plot(
            positions,
            values,
            color="#000000",
            linewidth=1.05,
            marker="o",
            markersize=4.1,
            markerfacecolor="#000000",
            markeredgecolor="#000000",
            markeredgewidth=0.65,
        )
        axis.set_xticks(positions, format_levels(parameter, subset["level"]))
        axis.set_ylim(0.19, 0.25)
        axis.set_yticks((0.19, 0.21, 0.23, 0.25))
        set_parameter_label(axis, parameter)
        if panel_index == 0:
            axis.set_ylabel(
                r"Fitness $\mathit{f}$",
                fontproperties=Y_LABEL_FONT,
                math_fontfamily="custom",
                labelpad=2.0,
            )
        else:
            axis.set_ylabel("")
        add_panel_title(axis, panel_index, str(subset["panel_title"].iloc[0]))
        style_axis(axis)

    # 延续第二章参数设定图的横排结构，并适度增加坐标框的纵向尺寸。
    figure.subplots_adjust(left=0.064, right=0.995, top=0.895, bottom=0.175, wspace=0.31)
    figure.savefig(OUTPUT_STEM.with_suffix(".png"), dpi=600, facecolor="white")
    figure.savefig(OUTPUT_STEM.with_suffix(".svg"), facecolor="white")
    plt.close(figure)


if __name__ == "__main__":
    draw_figure()
