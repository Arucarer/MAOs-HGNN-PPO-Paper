#绘图部分的内容

from __future__ import annotations

import logging
import re
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.lines import Line2D
from matplotlib.offsetbox import AnchoredOffsetbox, HPacker, TextArea
from matplotlib.patches import ConnectionPatch, Rectangle
from matplotlib.ticker import MaxNLocator

from chapter3_plot_style import (
    COLORS,
    ENGLISH_FONT,
    LINE_COLORS,
    METHOD_STYLES,
    SONGTI_FONT,
    apply_style,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR / "数据"
LYK_DATA_DIR = PROJECT_ROOT / "lyk数据"
DCGP_DATA_DIR = DATA_DIR / "DCGP补充数据"
EXTERNAL_DCGP_DIR = PROJECT_ROOT.parent / "图和表(1)" / "DCGPoutputs"
FIGURE_DIR = SCRIPT_DIR.parent / "figures" / "03_反应式学习调度"
#改动1
TEXT_WIDTH_IN = 443.86319 / 72.27
ZOOM_COLOR = "#D64B3C"
METHODS = list(METHOD_STYLES["rl_generalization"])
# 图例使用最终名称；每个元组分别指向工作簿中的Cmax列和Dt列。
SOURCE_METHODS = {
    "L2D": ("L2D", "L2D"),
    "MPGN–Multi-PPO": ("MPGN-MPPO", "MPGN-MPPO"),
    "HGNN-PPO": ("GNN-DRL", "GNN-DRL"),
    "HGNNR-PPO": ("HGNNR-DRL", "HGNNR-DRL"),
    "MHGNN–MA-PPO": ("MHGNN-SAC", "MHGNN-SAC"),
    #改动1
    "SPRE-HGNN-PPO": ("本文算法", "本文算法"),
}
MARKERS = ("o", "v", "^", "D", "s", "*")

RULE_METHODS = (
    ("固定规则", "A6", COLORS["light_gray"], "o"),
    ("人工组合规则", "A5", COLORS["dark_gray"], "v"),
    ("GP规则", "A4", COLORS["orange"], "D"),
    ("文献规则B", "A3", COLORS["purple"], "^"),
    ("文献规则A", "A2", COLORS["teal"], "s"),
    ("本文规则", "A1", COLORS["blue"], "*"),
)


def save_figure(figure: plt.Figure, name: str) -> None:
    """按论文现有文件名导出PNG，并保留可编辑PDF和SVG。"""
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    stem = FIGURE_DIR / name
    original = FIGURE_DIR / f"{name}_原图.png"
    if stem.with_suffix(".png").exists() and not original.exists():
        shutil.copy2(stem.with_suffix(".png"), original)
    figure.savefig(stem.with_suffix(".png"), dpi=600, bbox_inches="tight", pad_inches=0.03)
    figure.savefig(stem.with_suffix(".pdf"), bbox_inches="tight", pad_inches=0.03)
    figure.savefig(stem.with_suffix(".svg"), bbox_inches="tight", pad_inches=0.03)
    figure.savefig(
        FIGURE_DIR / f"{name}_新版候选.png",
        dpi=600,
        bbox_inches="tight",
        pad_inches=0.03,
    )
    plt.close(figure)


def style_axis(axis: plt.Axes) -> None:
    """沿用第二、四章的开放坐标轴：无网格，仅保留左、下边框。"""
    axis.grid(False)
    axis.spines[["top", "right"]].set_visible(False)
    axis.spines[["left", "bottom"]].set_color("#333333")
    axis.spines[["left", "bottom"]].set_linewidth(0.8)
    axis.tick_params(axis="y", labelrotation=90)
    # 逐项指定字体，避免Conda环境把数字刻度回退为非Times字体。
    for label in (*axis.get_xticklabels(), *axis.get_yticklabels()):
        font = (SONGTI_FONT if re.search(r"[\u4e00-\u9fff]", label.get_text()) else ENGLISH_FONT).copy()
        font.set_size(label.get_fontsize())
        label.set_fontproperties(font)
    axis.xaxis.get_offset_text().set_fontproperties(ENGLISH_FONT)
    axis.yaxis.get_offset_text().set_fontproperties(ENGLISH_FONT)


def rolling(values: pd.Series, window: int = 20) -> pd.Series:
    return values.rolling(window, min_periods=1, center=True).mean()


def plot_raw_and_trend(
    axis: plt.Axes,
    x: pd.Series,
    values: pd.Series,
    color: str,
    *,
    linestyle: str = "-",
    label: str | None = None,
) -> None:
    """同时保留逐回合波动和短窗口趋势，避免过度平滑掩盖训练过程。"""
    axis.plot(x, values, color=color, linewidth=0.40, alpha=0.42, linestyle=linestyle)
    axis.plot(
        x,
        rolling(values),
        color=LINE_COLORS.get(color, color),
        linewidth=1.15,
        linestyle=linestyle,
        label=label,
    )


def set_panel_title(
    axis: plt.Axes,
    panel: str,
    chinese: str,
    english: str = "",
    *,
    pad: float = 4,
    title_x: float = 0.5,
    prefix_x: float = 0.0,
    prefix_y: float = 1.015,
) -> None:
    """拆分英文面板编号与中文标题，保证两类文字分别使用指定字体。"""
    axis.set_title(chinese, x=title_x, pad=pad, fontproperties=SONGTI_FONT)
    prefix = f"({panel})" + (f" {english}" if english else "")
    prefix_artist = axis.text(
        prefix_x, prefix_y, prefix, transform=axis.transAxes,
        ha="left", va="bottom", fontproperties=ENGLISH_FONT,
        clip_on=False,
    )
    prefix_artist.set_math_fontfamily("custom")


def set_compact_panel_title(
    axis: plt.Axes,
    panel: str,
    chinese: str,
    english: str = "",
    *,
    font_size: float | None = None,
    anchor_y: float = 1.015,
) -> None:
    """把英文编号、英文术语和中文标题紧凑居中为一个整体。"""
    font_size = font_size or plt.rcParams["axes.titlesize"]
    prefix = f"({panel})" + (f" {english}" if english else "")
    title = HPacker(
        children=(
            TextArea(prefix, textprops={
                "fontproperties": ENGLISH_FONT,
                "fontsize": font_size,
                "math_fontfamily": "custom",
            }),
            TextArea(chinese, textprops={
                "fontproperties": SONGTI_FONT,
                "fontsize": font_size,
                "math_fontfamily": "custom",
            }),
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
        bbox_to_anchor=(0.5, anchor_y),
        bbox_transform=axis.transAxes,
    ))


def set_legend_fonts(legend) -> None:
    """纯中文标签用宋体，纯英文标签用Times New Roman。"""
    for text in legend.get_texts():
        font = (SONGTI_FONT if re.search(r"[\u4e00-\u9fff]", text.get_text()) else ENGLISH_FONT).copy()
        font.set_size(text.get_fontsize())
        text.set_fontproperties(font)


def sync_dcgp_data() -> None:
    """把已确认的补充工作簿复制进项目，避免绘图依赖外部临时目录。"""
    sources = {
        "典型场景训练数据.xlsx": EXTERNAL_DCGP_DIR / "DCGP训练曲线数据" / "典型场景训练数据_S01，M02，L05.xlsx",
        "DCGP消融退化率.xlsx": EXTERNAL_DCGP_DIR / "DCGP消融实验数据" / "工作站2_消融退化率_DR.xlsx",
        "DCGP六算法泛化数据.xlsx": EXTERNAL_DCGP_DIR / "DCGP对比泛化实验数据" / "测试集规则实验_合并_六算法抽样_滑窗.xlsx",
    }
    DCGP_DATA_DIR.mkdir(parents=True, exist_ok=True)
    for name, source in sources.items():
        target = DCGP_DATA_DIR / name
        if source.exists() and (not target.exists() or source.stat().st_mtime > target.stat().st_mtime):
            shutil.copy2(source, target)

    # 对已有成图保留上游原版，便于在同一PDF中直观看前后差异。
    original_figures = {
        "典型场景训练曲线_NCBE触发及局部放大_原图.png": EXTERNAL_DCGP_DIR / "DCGP训练曲线数据" / "典型场景训练曲线_NCBE触发及局部放大.png",
        "DCGP消融退化率热力图_原图.png": EXTERNAL_DCGP_DIR / "DCGP消融实验数据" / "工作站2_消融退化率_热力图_小中大规模.png",
        "六算法_S03_M04_L05_Cmax_Dt_箱线图_2列3行_原图.png": EXTERNAL_DCGP_DIR / "DCGP对比泛化实验数据" / "箱线图_六算法_S03_M04_L05" / "六算法_S03_M04_L05_Cmax_Dt_箱线图_2列3行.png",
    }
    for name, source in original_figures.items():
        if source.exists():
            shutil.copy2(source, FIGURE_DIR / name)


def load_attention_data() -> dict[str, pd.DataFrame]:
    folder = DATA_DIR / "注意力消融与训练曲线"
    #改动1
    files = {
        "小规模": folder / "小规模算例_1280轮_绘图数据.xlsx",
        "中规模": folder / "中规模算例_1280轮_绘图数据.xlsx",
        "大规模": folder / "大规模算例_1280轮_绘图数据.xlsx",
    }
    data = {scale: pd.read_excel(path, sheet_name="绘图数据") for scale, path in files.items()}
    assert all(len(frame) == 1280 for frame in data.values())
    return data


def draw_attention_ablation(data: dict[str, pd.DataFrame]) -> None:
    """用三份Excel重画完整模型与无注意力模型的2×3曲线。"""
    figure_font_size = 10.1
    secondary_font_size = 9.0
    figure, axes = plt.subplots(2, 3, figsize=(TEXT_WIDTH_IN, 3.35), sharex="col")
    metrics = (
        ("raw_makespan", r"$C_{\max}$"),
        ("plan_deviation_rate", r"$D$"),
    )
    for column, (scale, frame) in enumerate(data.items()):
        for row, (metric, ylabel) in enumerate(metrics):
            axis = axes[row, column]
            for prefix, label, color in (
                ("without_attention", "Without attention", COLORS["gray"]),
                ("full_model", "Full model", COLORS["blue"]),
            ):
                values = frame[f"{prefix}_{metric}"]
                plot_raw_and_trend(axis, frame["episode"], values, color, label=label)
            if row == 0:
                set_compact_panel_title(
                    axis, chr(97 + column), "",
                    #改动1
                    {"小规模": "Small-scale instances", "中规模": "Medium-scale instances", "大规模": "Large-scale instances"}[scale],
                    #改动1
                    font_size=figure_font_size,
                )
            axis.set_ylabel(
                ylabel if column == 0 else "",
                fontsize=figure_font_size,
            )
            if row == 1:
                axis.set_xlabel(
                    "Training episodes", fontsize=figure_font_size,
                    fontproperties=ENGLISH_FONT,
                    #改动1
                )
            axis.tick_params(axis="both", labelsize=secondary_font_size)
            style_axis(axis)
            if row == 0:
                legend = axis.legend(
                    loc="upper right", bbox_to_anchor=(1.03, 1.0), frameon=False,
                    #改动1
                    fontsize=6.8, handlelength=1.25,
                    #改动1
                    handletextpad=0.35, labelspacing=0.25, borderaxespad=0.35,
                    #改动1
                )
                set_legend_fonts(legend)
    figure.tight_layout(h_pad=0.22, w_pad=0.70)
    save_figure(figure, "lyk大中小有无注意力机制")
    #改动1


def draw_training_curves(data: dict[str, pd.DataFrame]) -> None:
    """从同一Excel的完整模型列重画HGNN-PPO训练曲线。"""
    figure_font_size = 10.1
    secondary_font_size = 9.0
    figure, axes = plt.subplots(2, 3, figsize=(TEXT_WIDTH_IN, 3.35), sharex="col")
    metrics = (
        ("full_model_raw_makespan", r"$C_{\max}$"),
        ("full_model_plan_deviation_rate", r"$D$"),
    )
    for column, (scale, frame) in enumerate(data.items()):
        for row, (metric, ylabel) in enumerate(metrics):
            axis = axes[row, column]
            values = frame[metric]
            axis.plot(
                frame["episode"], values, color=COLORS["gray"],
                linewidth=0.42, alpha=0.55, label="Per-episode value",
                #改动1
            )
            axis.plot(
                frame["episode"], rolling(values), color=COLORS["blue"],
                linewidth=1.20, label="20-episode moving average",
                #改动1
            )
            if row == 0:
                set_compact_panel_title(
                    axis, chr(97 + column), "",
                    #改动1
                    {"小规模": "Small-scale instances", "中规模": "Medium-scale instances", "大规模": "Large-scale instances"}[scale],
                    #改动1
                    font_size=figure_font_size,
                )
            axis.set_ylabel(
                ylabel if column == 0 else "",
                fontsize=figure_font_size,
            )
            if row == 1:
                axis.set_xlabel(
                    "Training episodes", fontsize=figure_font_size,
                    #改动1
                    fontproperties=ENGLISH_FONT,
                    #改动1
                )
            axis.tick_params(axis="both", labelsize=secondary_font_size)
            style_axis(axis)
            if row == 0:
                legend = axis.legend(
                    loc="upper right", frameon=False,
                    fontsize=6.8, handlelength=1.25,
                    #改动1
                    handletextpad=0.35, labelspacing=0.25, borderaxespad=0.35,
                    #改动1
                )
                set_legend_fonts(legend)
    figure.tight_layout(h_pad=0.22, w_pad=0.70)
    save_figure(figure, "lyk强化学习训练曲线1")
    #改动1


def load_sensitivity_sheet(path: Path, sheet: str) -> tuple[pd.Series, list[tuple[str, pd.Series, pd.Series]]]:
    raw = pd.read_excel(path, sheet_name=sheet, header=None)
    frame = raw.iloc[4:2404].apply(pd.to_numeric, errors="coerce")
    episode = frame.iloc[:, 0]
    series = []
    for column in range(1, 9, 2):
        label = raw.iloc[2, column]
        if pd.isna(label) or frame.iloc[:, column].isna().all():
            continue
        display = str(label).replace("（基准）", "")
        series.append((display, frame.iloc[:, column], frame.iloc[:, column + 1], "基准" in str(label)))
    ordered = [item for item in series if not item[3]] + [item for item in series if item[3]]
    return episode, [(label, makespan, deviation) for label, makespan, deviation, _ in ordered]


def draw_sensitivity() -> None:
    """用参数敏感性工作簿重画2×4定量网格。"""
    path = LYK_DATA_DIR / "3.3.1敏感性实验数据" / "HGNN_PPO_自然敏感性数据_蓝线不变.xlsx"
    sheets = ("轨迹采样步数", "HGNN层数", "学习率", "PPO裁剪参数")
    title_parts = (
        ("轨迹采样步数", ""),
        ("层数", "HGNN"),
        ("学习率", ""),
        ("裁剪参数", "PPO"),
    )
    legend_titles = ("N_step", "L", "α", "ε")
    figure, axes = plt.subplots(
        2, 4, figsize=(TEXT_WIDTH_IN, 3.15),
        sharex="col", sharey="row",
    )
    top_legends = []
    for column, sheet in enumerate(sheets):
        episode, series = load_sensitivity_sheet(path, sheet)
        palette = ([COLORS["gray"], COLORS["orange"], COLORS["blue"]]
                   if len(series) == 3 else [COLORS["light_gray"], COLORS["orange"], COLORS["purple"], COLORS["blue"]])
        for row, ylabel in enumerate((r"$C_{\max}$", r"$D$")):
            axis = axes[row, column]
            for (label, makespan, deviation), color in zip(series, palette):
                values = makespan if row == 0 else deviation
                plot_raw_and_trend(
                    axis, episode, values, color,
                    label=label.split("=", 1)[-1].strip(),
                )
            if row == 0:
                chinese, english = title_parts[column]
                set_compact_panel_title(
                    axis, chr(101 + column), chinese, english, anchor_y=1.040
                )
            axis.set_ylabel(ylabel if column == 0 else "")
            if row == 1:
                axis.set_xlabel("训练回合", fontproperties=SONGTI_FONT)
            style_axis(axis)
            if column > 0:
                # 各子图保留纵轴线和刻度线，仅最左列显示纵轴数值。
                axis.tick_params(axis="y", labelleft=False, left=True)
            if row == 0:
                legend = axis.legend(
                    loc="upper right", frameon=False, fontsize=6.5,
                )
                set_legend_fonts(legend)
                top_legends.append((axis, legend, legend_titles[column]))
    figure.subplots_adjust(left=0.09, right=0.995, top=0.94, bottom=0.16, hspace=0.08, wspace=0.035)
    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    for axis, legend, title in top_legends:
        # 参数名紧贴第一条图例线左侧，并统一保留5磅间距。
        handle_box = legend.legend_handles[0].get_window_extent(renderer)
        title_position = axis.transAxes.inverted().transform((
            handle_box.x0 - 5 * figure.dpi / 72,
            (handle_box.y0 + handle_box.y1) / 2,
        ))
        axis.text(
            *title_position, title, transform=axis.transAxes,
            ha="right", va="center", fontproperties=ENGLISH_FONT, fontsize=10,
        )
    save_figure(figure, "敏感性参数实验图")


def draw_degradation_heatmap() -> None:
    """直接读取补充工作簿中的30个场景消融退化率。"""
    frame = pd.read_excel(DCGP_DATA_DIR / "DCGP消融退化率.xlsx").iloc[:30]
    short_method_names = (
        "CGP", "DCGP", r"DCGP-$\alpha$", r"DCGP-$\beta$",
    )
    metric_columns = {
        0: [
            "CGP_Cmax退化率(%)", "DCGP_Cmax退化率(%)",
            "DCGP-w/o SA_Cmax退化率(%)", "DCGP-w/o NC_Cmax退化率(%)",
        ],
        1: [
            "CGP_Dt退化率(%)", "DCGP_Dt退化率(%)",
            "DCGP-w/o SA_Dt退化率(%)", "DCGP-w/o NC_Dt退化率(%)",
        ],
    }
    matrices = {}
    for scale, start in zip("SML", (0, 10, 20)):
        subset = frame.iloc[start:start + 10]
        matrices[scale] = np.stack(
            [subset[metric_columns[metric]].to_numpy(dtype=float) for metric in (0, 1)],
            axis=2,
        )

    # 用独立中列承载共享方法名，避免手工偏移破坏两侧热力图比例。
    figure = plt.figure(figsize=(TEXT_WIDTH_IN, 4.45))
    grid = figure.add_gridspec(
        3, 3,
        width_ratios=(10, 2.2, 10),
        left=0.015, right=0.995, top=0.975, bottom=0.19,
        hspace=0.24, wspace=0.035,
    )
    axes = np.empty((3, 2), dtype=object)
    cmap = LinearSegmentedColormap.from_list("chapter3_diverging", [COLORS["blue"], "#F5F5F5", COLORS["orange"]])
    limits = [max(abs(matrices[s][:, :, metric]).max() for s in "SML") for metric in (0, 1)]
    for row, scale in enumerate("SML"):
        method_axis = figure.add_subplot(grid[row, 1])
        method_axis.set_axis_off()
        for method_index, method_name in enumerate(short_method_names):
            method_axis.text(
                0.5, 1 - (method_index + 0.5) / 4, method_name,
                transform=method_axis.transAxes,
                ha="center", va="center", fontsize=8.8,
                fontproperties=ENGLISH_FONT,
            )
        for column, metric_name in enumerate((r"$C_{\max}$", r"$D$")):
            axis = figure.add_subplot(grid[row, column * 2])
            axes[row, column] = axis
            matrix = matrices[scale][:, :, column].T
            image = axis.imshow(matrix, cmap=cmap, norm=TwoSlopeNorm(vmin=-limits[column], vcenter=0, vmax=limits[column]), aspect="auto")
            axis.set_xticks(range(10))
            if row == 2:
                axis.set_xticklabels([f"{index:02d}" for index in range(1, 11)])
                axis.tick_params(axis="x", labelsize=8.2)
                for label in axis.get_xticklabels():
                    label.set_fontproperties(ENGLISH_FONT)
            else:
                axis.tick_params(labelbottom=False)
            axis.set_yticks([])
            set_compact_panel_title(
                axis, chr(97 + row * 2 + column),
                f"{'小中大'[row]}规模 {metric_name} 退化率",
                font_size=9.5,
            )
            for i in range(4):
                for j in range(10):
                    value = matrix[i, j]
                    axis.text(
                        j, i, f"{value:.1f}", ha="center", va="center",
                        fontsize=8.0, fontproperties=ENGLISH_FONT,
                        color="white" if abs(value) > limits[column] * 0.55 else "#333333",
                    )
            axis.tick_params(length=0)
            for spine in axis.spines.values():
                spine.set_visible(False)
    figure.supxlabel("算例编号", y=0.118, fontsize=9.5, fontproperties=SONGTI_FONT)
    for column in range(2):
        # 每个指标共用一条水平色标，避免重复色标压缩矩阵。
        axis_box = axes[0, column].get_position()
        colorbar_width = axis_box.width * 0.78
        x_position = axis_box.x0 + (axis_box.width - colorbar_width) / 2
        colorbar_axis = figure.add_axes([x_position, 0.082, colorbar_width, 0.014])
        colorbar = figure.colorbar(axes[0, column].images[0], cax=colorbar_axis, orientation="horizontal")
        colorbar.ax.tick_params(labelsize=8.2, pad=2)
        for label in colorbar.ax.get_xticklabels():
            label.set_fontproperties(ENGLISH_FONT)
    figure.text(
        0.5, 0.018, "退化率  (%)",
        ha="center", va="bottom", fontsize=9.5, fontproperties=SONGTI_FONT,
    )
    save_figure(figure, "DCGP消融退化率热力图")


def load_dcgp_training_data() -> dict[str, pd.DataFrame]:
    """读取S01、M02、L05三个典型场景的五算法逐代结果。"""
    workbook = DCGP_DATA_DIR / "典型场景训练数据.xlsx"
    sheets = {
        "S01（小规模）": "small_low_01",
        "M02（中规模）": "medium_low_02",
        "L05（大规模）": "large_insert_high_01",
    }
    return {
        title: pd.read_excel(workbook, sheet_name=sheet, header=[0, 1])
        for title, sheet in sheets.items()
    }


def mark_zoom_region(
    axis: plt.Axes,
    zoom_axis: plt.Axes,
    x_bounds: tuple[float, float],
    y_bounds: tuple[float, float],
) -> None:
    """沿用图2.10的红框、浅色选区和虚线连接方式。"""
    x_min, x_max = x_bounds
    y_min, y_max = y_bounds
    region = (x_min, y_min), x_max - x_min, y_max - y_min
    axis.add_patch(Rectangle(
        *region, facecolor=ZOOM_COLOR, alpha=0.10,
        edgecolor="none", zorder=0.5,
    ))
    axis.add_patch(Rectangle(
        *region, fill=False, edgecolor=ZOOM_COLOR,
        linewidth=1.35, linestyle=(0, (3, 2)), zorder=7,
    ))
    axis.figure.add_artist(ConnectionPatch(
        xyA=(x_max, y_max), coordsA=axis.transData,
        xyB=(0, 0), coordsB=zoom_axis.transAxes,
        color=ZOOM_COLOR, linewidth=1.2,
        linestyle=(0, (3, 2)), clip_on=False, zorder=7,
    ))
    for spine in zoom_axis.spines.values():
        spine.set_visible(True)
        spine.set_color(ZOOM_COLOR)
        spine.set_linewidth(1.35)


def add_trigger_inset(
    axis: plt.Axes,
    generation: pd.Series,
    curves: list[tuple[pd.Series, str, str, str]],
    x_bounds: tuple[int, int],
) -> None:
    """按各面板的真实变化区间放大五条曲线，并标出NCBE跳变点。"""
    x_min, x_max = x_bounds
    zoom_mask = generation.between(x_min, x_max)
    inset = axis.inset_axes([0.42, 0.48, 0.55, 0.46])
    for index, (values, color, linestyle, marker) in enumerate(curves):
        is_ncbe = index == len(curves) - 1
        inset.plot(
            generation, values, color=LINE_COLORS.get(color, color),
            linewidth=1.5 if is_ncbe else 0.95,
            linestyle=linestyle, marker=marker,
            markersize=2.8 if is_ncbe else 2.3,
            markerfacecolor="white", markevery=2,
            zorder=4 if is_ncbe else 2,
        )
    ncbe = curves[-1][0]
    change_mask = ncbe.diff().abs().gt(1e-12) & zoom_mask
    inset.scatter(
        generation[change_mask], ncbe[change_mask],
        marker="*", s=28, facecolor=COLORS["red"],
        edgecolor="white", linewidth=0.3, zorder=5,
    )
    visible = np.concatenate([
        values[zoom_mask].to_numpy(dtype=float) for values, _, _, _ in curves
    ])
    padding = max(np.ptp(visible) * 0.04, abs(np.mean(visible)) * 0.001, 1e-4)
    inset.set_xlim(x_min, x_max)
    inset.set_ylim(visible.min() - padding, visible.max() + padding)
    inset.set_xticks(np.linspace(x_min, x_max, 3, dtype=int))
    decimals = 3 if np.max(np.abs(visible)) < 1 else 1
    inset.set_yticks(
        (visible.min(), visible.max()),
        labels=(f"{visible.min():.{decimals}f}", f"{visible.max():.{decimals}f}"),
    )
    inset.tick_params(labelsize=9.2, pad=1, width=0.6, length=2)
    style_axis(inset)
    mark_zoom_region(
        axis, inset, (x_min, x_max),
        (visible.min() - padding, visible.max() + padding),
    )


def draw_dcgp_training_curves() -> None:
    """重画DCGP五个版本在三个典型场景上的逐代Cmax和Dt曲线。"""
    methods = (
        ("CGP", "CGP", COLORS["gray"], "o", "--"),
        ("普通DCGP", "DCGP", COLORS["orange"], "D", ":"),
        ("DCGP-NCBE-w/o SA", r"DCGP-$\alpha$", COLORS["purple"], "^", "-."),
        ("DCGP-NCBE-w/o NC", r"DCGP-$\beta$", COLORS["teal"], "v", "-."),
        ("DCGP-NCBE", "DCGP-NCBE", COLORS["blue"], "s", "-"),
    )
    # 六个面板分别围绕其真实数据特征放大，不能按场景共用同一触发窗口。
    zoom_windows = (
        ((14, 30), (24, 42)),
        ((21, 33), (22, 49)),
        ((24, 41), (31, 41)),
    )
    # 保留图2.10的双栏结构，同时压缩三行组合图的总高度。
    figure, axes = plt.subplots(3, 2, figsize=(TEXT_WIDTH_IN, 6.35), sharex="col")
    for row, (title, frame) in enumerate(load_dcgp_training_data().items()):
        generation = frame.iloc[:, 0]
        for column, metric in enumerate(("Cmax", "Dt")):
            axis = axes[row, column]
            # 数学变量用Times New Roman斜体，描述性下标max保持正体。
            metric_label = r"$C_{\max}$" if column == 0 else r"$D$"
            curves = []
            for source, method, color, marker, linestyle in methods:
                values = frame[(source, metric)]
                curves.append((values, color, linestyle, marker))
                is_ncbe = method == "DCGP-NCBE"
                axis.plot(
                    generation, values, color=LINE_COLORS.get(color, color),
                    linewidth=1.45 if is_ncbe else 0.95,
                    linestyle=linestyle, marker=marker,
                    markersize=3.4 if is_ncbe else 2.8,
                    markerfacecolor="white", markevery=7,
                    zorder=4 if is_ncbe else 2, label=method,
                )
            ncbe = frame[("DCGP-NCBE", metric)]
            change_mask = ncbe.diff().abs().gt(1e-12)
            axis.scatter(
                generation[change_mask], ncbe[change_mask], marker="*", s=21,
                facecolor=COLORS["red"], edgecolor="white", linewidth=0.3,
                zorder=5,
            )
            add_trigger_inset(axis, generation, curves, zoom_windows[row][column])
            panel = chr(97 + row * 2 + column)
            scene, scale = re.fullmatch(r"([^（]+)（([^）]+)）", title).groups()
            set_compact_panel_title(
                axis, panel, f"{scale} {metric_label} 演化", scene,
                font_size=10.0, anchor_y=1.035,
            )
            if row == 2:
                axis.set_xlabel("训练代数", fontproperties=SONGTI_FONT)
            style_axis(axis)
            axis.tick_params(labelsize=9.2)
            axis.xaxis.label.set_fontsize(9.6)
            axis.yaxis.set_major_locator(MaxNLocator(nbins=4))
    handles, labels = axes[0, 0].get_legend_handles_labels()
    legend = figure.legend(
        handles, labels, loc="lower center",
        bbox_to_anchor=(0.5, 0.012), ncol=5,
        frameon=False, fontsize=9.2,
        columnspacing=1.35, handlelength=1.5, handletextpad=0.30,
    )
    set_legend_fonts(legend)
    for label in legend.get_texts():
        if label.get_text() == "DCGP-NCBE":
            label.set_fontweight("bold")
    figure.subplots_adjust(
        left=0.075, right=0.995, bottom=0.145, top=0.985,
        hspace=0.27, wspace=0.13,
    )
    save_figure(figure, "典型场景训练曲线_NCBE触发及局部放大")


def load_rule_generalization(sheet: str) -> dict[str, np.ndarray]:
    """读取一个DCGP泛化场景中的六类规则Cmax和Dt结果。"""
    frame = pd.read_excel(DCGP_DATA_DIR / "DCGP六算法泛化数据.xlsx", sheet_name=sheet, header=[0, 1])
    data = {}
    for source, method, _, _ in RULE_METHODS:
        data[method] = frame.loc[:, [(source, "Cmax"), (source, "Dt")]].to_numpy(dtype=float)
    assert all(values.shape == (60, 2) for values in data.values())
    return data


def draw_dcgp_generalization_boxplot() -> None:
    """沿用第二、四章雨云结构重画三个典型场景的六算法分布。"""
    panels = (
        ("S_03", "S03", "小规模"),
        ("M_04", "M04", "中规模"),
        ("L_05", "L05", "大规模"),
    )
    figure, axes = plt.subplots(3, 2, figsize=(TEXT_WIDTH_IN, 5.9))
    method_names = tuple(method for _, method, _, _ in RULE_METHODS)
    method_colors = {method: color for _, method, color, _ in RULE_METHODS}
    for row, (sheet, scene, scale) in enumerate(panels):
        data = load_rule_generalization(sheet)
        for column, metric in enumerate((0, 1)):
            axis = axes[row, column]
            metric_label = r"$C_{\max}$" if column == 0 else r"$D$"
            draw_distribution(
                axis,
                [data[method][:, metric] for method in method_names],
                method_names,
                method_colors,
                proposed_method="A1",
            )
            set_compact_panel_title(
                axis, chr(97 + row * 2 + column),
                f"{scale} {metric_label} 分布", scene,
            )
            axis.set_xticks(range(1, 7), [method for _, method, _, _ in RULE_METHODS] if row == 2 else [])
            if row == 2:
                plt.setp(axis.get_xticklabels(), rotation=20, ha="right")
            style_axis(axis)
    figure.tight_layout(h_pad=0.65, w_pad=0.55)
    save_figure(figure, "六算法_S03_M04_L05_Cmax_Dt_箱线图_2列3行")


def draw_dcgp_generalization_pareto() -> None:
    """按确认口径只画各算法自身非支配点，并突出本文规则的全局前沿贡献。"""
    panels = (("S_03", "S03（小规模）"), ("M_04", "M04（中规模）"), ("L_05", "L05（大规模）"))
    figure_font_size = 10.1
    figure, axes = plt.subplots(1, 3, figsize=(TEXT_WIDTH_IN, 2.75))
    for panel, (axis, (sheet, title)) in enumerate(zip(axes, panels)):
        data = load_rule_generalization(sheet)
        pooled = np.vstack(list(data.values()))
        pooled_mask = nondominated(pooled)
        global_front = pooled[pooled_mask]
        global_front = global_front[np.argsort(global_front[:, 0])]
        start = 0
        proposed_global = np.empty((0, 2))
        for _, method, color, marker in RULE_METHODS:
            points = data[method]
            front = points[nondominated(points)]
            axis.scatter(
                front[:, 0], front[:, 1], marker=marker,
                s=40 if method == "A1" else 28, color=color,
                alpha=0.92 if method == "A1" else 0.33,
                edgecolors="none", zorder=4 if method == "A1" else 2,
                label=method,
            )
            if method == "A1":
                proposed_global = points[pooled_mask[start:start + len(points)]]
            start += len(points)
        axis.plot(global_front[:, 0], global_front[:, 1], color="#777777", linewidth=1.05, alpha=0.72, label="全局前沿")
        axis.scatter(proposed_global[:, 0], proposed_global[:, 1], s=58, facecolors="none", edgecolors=COLORS["red"], linewidths=1.2, zorder=6, label="本文前沿点")
        scene, scale = re.fullmatch(r"([^（]+)（([^）]+)）", title).groups()
        set_compact_panel_title(axis, chr(97 + panel), scale, scene, font_size=figure_font_size)
        axis.set_xlabel(r"$C_{\max}$", fontsize=figure_font_size)
        if panel == 0:
            axis.set_ylabel(r"$D$", fontsize=figure_font_size)
        axis.tick_params(axis="both", labelsize=figure_font_size)
        axis.margins(y=0.10)
        axis.yaxis.set_major_locator(MaxNLocator(nbins=4, steps=[1, 2, 2.5, 5, 10]))
        style_axis(axis)
    handles, labels = axes[0].get_legend_handles_labels()
    legend = figure.legend(
        handles, labels, loc="lower center", bbox_to_anchor=(0.5, 0.01),
        ncol=8, frameon=False, fontsize=figure_font_size,
        columnspacing=0.90, handlelength=1.0, handletextpad=0.35,
    )
    set_legend_fonts(legend)
    figure.tight_layout(rect=(0, 0.11, 1, 1), w_pad=0.65)
    save_figure(figure, "DCGP六算法典型场景Pareto前沿")


def load_selection_ratios() -> dict[str, np.ndarray]:
    workbook = LYK_DATA_DIR / "雷达图数据DCGP-NCBE规则选择比例数据.xlsx"
    frame = pd.read_excel(workbook, sheet_name="全部数据", header=1)
    source_columns = ("DCGP-NCBE", "DCGP", "CGP", "Simple rules", "Manual rules")
    data = {}
    for scale in "SML":
        rows = frame[frame["算例"].astype(str).str.startswith(f"TR_{scale}")]
        data[scale] = rows.loc[:, source_columns].to_numpy(dtype=int)
    assert all(values.shape == (10, 5) for values in data.values())
    assert all(np.all(values.sum(axis=1) == 100) for values in data.values())
    return data


def draw_selection_radar() -> None:
    """用lyk数据中的Excel比例数据重画三尺度雷达图。"""
    data = load_selection_ratios()
    figure_font_size = 10.1
    angles = np.linspace(0, 2 * np.pi, 10, endpoint=False)
    closed_angles = np.r_[angles, angles[0]]
    order = (4, 3, 2, 1, 0)
    labels = ("人工规则", "简单规则", "CGP", "DCGP", "DCGP-NCBE")
    colors = (COLORS["light_gray"], COLORS["dark_gray"], COLORS["orange"], COLORS["teal"], COLORS["blue"])
    figure, axes = plt.subplots(1, 3, figsize=(TEXT_WIDTH_IN, 2.55), subplot_kw={"projection": "polar"})
    for panel, (axis, scale) in enumerate(zip(axes, "SML")):
        axis.set_theta_offset(np.pi / 2)
        axis.set_theta_direction(-1)
        axis.set_xticks(angles, [f"{scale}{index:02d}" for index in range(1, 11)], fontproperties=ENGLISH_FONT)
        axis.set_ylim(0, 50)
        # 保留等距网格，不在小尺寸雷达图内堆叠径向数字。
        axis.set_yticks((10, 20, 30, 40, 50), ("", "", "", "", ""))
        axis.set_rlabel_position(92)
        axis.tick_params(axis="x", labelsize=8.8, pad=2)
        axis.grid(color="#D6D6D6", linewidth=0.55)
        axis.spines["polar"].set_color("#A0A0A0")
        for source_column, label, color, marker in zip(order, labels, colors, MARKERS):
            values = data[scale][:, source_column]
            axis.plot(
                closed_angles, np.r_[values, values[0]],
                color=LINE_COLORS.get(color, color), linewidth=1.15,
                marker=marker, markersize=3.3, markerfacecolor="white",
                markeredgewidth=0.75, label=label,
            )
            if label == "DCGP-NCBE":
                axis.fill(closed_angles, np.r_[values, values[0]], color=color, alpha=0.12)
        set_compact_panel_title(
            axis, chr(97 + panel), f"{'小中大'[panel]}规模算例",
            font_size=figure_font_size, anchor_y=1.20,
        )
    handles, legend_labels = axes[0].get_legend_handles_labels()
    legend = figure.legend(
        handles, legend_labels, loc="lower center", bbox_to_anchor=(0.5, 0.01),
        ncol=5, frameon=False, fontsize=figure_font_size,
        columnspacing=1.25, handlelength=1.35, handletextpad=0.35,
    )
    set_legend_fonts(legend)
    figure.subplots_adjust(left=0.035, right=0.965, top=0.82, bottom=0.18, wspace=0.40)
    save_figure(figure, "不同规模算例下各类规则的选择比例")


def load_rl_sheet(workbook: Path, sheet: str) -> dict[str, np.ndarray]:
    frame = pd.read_excel(workbook, sheet_name=sheet, header=[0, 1])
    data = {}
    for method in METHODS:
        source_cmax, source_dt = SOURCE_METHODS[method]
        data[method] = frame.loc[:, [(source_cmax, "Cmax"), (source_dt, "Dt")]].to_numpy(dtype=float)
    assert all(values.shape == (50, 2) for values in data.values())
    return data


def nondominated(points: np.ndarray) -> np.ndarray:
    """返回双目标最小化问题中的非支配点。"""
    return np.asarray([
        not np.any(np.all(points <= point, axis=1) & np.any(points < point, axis=1))
        for point in points
    ])


def draw_rl_pareto() -> None:
    workbook = DATA_DIR / "强化学习泛化实验" / "六算法_每算例300组Pareto分配数据_分布强化版.xlsx"
    #改动1
    panels = (
        ("small_insert_high_03", "S_03（小规模）"),
        ("medium_repair_long_03", "M_04（中规模）"),
        ("large_combined_high_03", "L_05（大规模）"),
    )
    figure, axes = plt.subplots(1, 3, figsize=(TEXT_WIDTH_IN, 2.85))
    for panel, (axis, (sheet, title)) in enumerate(zip(axes, panels)):
        data = load_rl_sheet(workbook, sheet)
        pooled = np.vstack(list(data.values()))
        pooled_mask = nondominated(pooled)
        front = pooled[pooled_mask]
        front = front[np.argsort(front[:, 0])]
        start = 0
        proposed_global = np.empty((0, 2))
        for method, marker in zip(METHODS, MARKERS):
            color = METHOD_STYLES["rl_generalization"][method]
            points = data[method]
            method_front = points[nondominated(points)]
            axis.scatter(
                method_front[:, 0], method_front[:, 1],
                s=22 if method == "SPRE-HGNN-PPO" else 15,
                marker=marker, color=color,
                edgecolors="none", alpha=0.90 if method == "SPRE-HGNN-PPO" else 0.34,
                zorder=4 if method == "SPRE-HGNN-PPO" else 2, label=method,
            )
            if method == "SPRE-HGNN-PPO":
                proposed_global = points[pooled_mask[start:start + len(points)]]
            start += len(points)
        axis.plot(
            front[:, 0], front[:, 1], color="#777777",
            linewidth=0.95, alpha=0.72, zorder=3, label="全局前沿",
        )
        axis.scatter(
            proposed_global[:, 0], proposed_global[:, 1], s=34,
            facecolors="none", edgecolors=COLORS["red"], linewidths=1.0,
            zorder=6, label="本文前沿点",
        )
        scene, scale = re.fullmatch(r"([^（]+)（([^）]+)）", title).groups()
        set_panel_title(axis, chr(97 + panel), scale, scene)
        axis.set_xlabel(r"$C_{\max}$")
        if panel == 0:
            axis.set_ylabel(r"$D$")
        style_axis(axis)
    handles, labels = axes[0].get_legend_handles_labels()
    labels = (
        "L2D", "MPGN-MPPO", "GNN-DRL", "HGNNR-DRL", "MHGNN-SAC",
        "本文算法", "全局前沿", "本文前沿点",
    )
    figure.subplots_adjust(left=0.075, right=0.99, top=0.90, bottom=0.34, wspace=0.22)
    legend = figure.legend(
        handles, labels, loc="lower center", bbox_to_anchor=(0.5, 0.01),
        ncol=4, frameon=False, fontsize=10.1,
        columnspacing=0.90, handlelength=1.0, handletextpad=0.35,
    )
    set_legend_fonts(legend)
    save_figure(figure, "强化学习泛化实验帕累托前沿图")


def draw_distribution(
    axis: plt.Axes,
    series: list[np.ndarray],
    methods: tuple[str, ...] = tuple(METHODS),
    method_colors: dict[str, str] | None = None,
    *,
    proposed_method: str = "SPRE-HGNN-PPO",
) -> None:
    """沿用第二、四章的半小提琴、左侧散点和中央箱线雨云结构。"""
    method_colors = method_colors or METHOD_STYLES["rl_generalization"]
    rng = np.random.default_rng(20260812)
    for position, (method, values) in enumerate(zip(methods, series), start=1):
        color = method_colors[method]
        violin = axis.violinplot([values], positions=[position], widths=0.82, showextrema=False)
        body = violin["bodies"][0]
        vertices = body.get_paths()[0].vertices
        vertices[:, 0] = np.maximum(vertices[:, 0], position)
        body.set_facecolor(color)
        body.set_edgecolor(LINE_COLORS[color])
        body.set_linewidth(0.65)
        body.set_alpha(0.28)
        axis.scatter(
            position - rng.uniform(0.08, 0.32, len(values)), values,
            s=4.8, color=color, alpha=0.30, edgecolors="none", zorder=2,
        )
        edge_color = COLORS["red"] if method == proposed_method else "#444444"
        box = axis.boxplot(
            [values], positions=[position], widths=0.18,
            patch_artist=True, showfliers=False, notch=True,
            medianprops={"color": "#222222", "linewidth": 1.1},
            whiskerprops={"color": edge_color, "linewidth": 0.85},
            capprops={"color": edge_color, "linewidth": 0.85},
        )
        box["boxes"][0].set(
            facecolor=color, edgecolor=edge_color,
            linewidth=1.15 if method == proposed_method else 0.9,
            alpha=0.70,
        )


def draw_rl_raincloud() -> None:
    workbook = DATA_DIR / "强化学习泛化实验" / "六算法_每算例300组Pareto分配数据_分布强化版.xlsx"
    #改动1
    panels = (
        ("small_insert_high_03", "S_03（Small-scale）"),
        #改动1
        ("medium_repair_long_03", "M_04（Medium-scale）"),
        #改动1
        ("large_failure_high_03", "L_02（Large-scale）"),
        #改动1
    )
    legend_labels = (
        "L2D", "MPGN-MPPO", "GNN-DRL", "HGNNR-DRL", "MHGNN-SAC", "Proposed method",
        #改动1
    )
    figure, axes = plt.subplots(2, 3, figsize=(TEXT_WIDTH_IN, 4.55))
    for column, (sheet, title) in enumerate(panels):
        data = load_rl_sheet(workbook, sheet)
        for row, metric in enumerate((0, 1)):
            axis = axes[row, column]
            draw_distribution(axis, [data[method][:, metric] for method in METHODS])
            scene, scale = re.fullmatch(r"([^（]+)（([^）]+)）", title).groups()
            set_compact_panel_title(
                axis, chr(97 + row * 3 + column), "",
                f"{scale} ({scene.replace('_', '')})", font_size=8.0, anchor_y=1.025,
            )
            #改动1
            axis.set_ylabel((r"$C_{\max}$" if row == 0 else r"$D$") if column == 0 else "")
            axis.set_xticks(range(1, 7), [])
            axis.tick_params(axis="x", labelsize=7.2, pad=2)
            style_axis(axis)
    handles = [
        Line2D([], [], color=METHOD_STYLES["rl_generalization"][method], marker="s",
               linestyle="none", markersize=5, label=label)
        for method, label in zip(METHODS, legend_labels)
    ]
    legend = figure.legend(
        handles=handles, loc="lower center", bbox_to_anchor=(0.5, 0.01),
        ncol=6, frameon=False, fontsize=8.2,
        #改动1
        columnspacing=0.85, handlelength=0.75, handletextpad=0.20,
        #改动1
    )
    set_legend_fonts(legend)
    figure.tight_layout(rect=(0, 0.085, 1, 1), h_pad=0.80, w_pad=0.75)
    #改动1
    save_figure(figure, "lyk泛化实验云雨图")
    #改动1


def main() -> None:
    """只重画当前已有数值来源的第三章实验图。"""
    # fontTools会把无害的字体子集提示写入标准错误流，统一降噪便于自动校验退出状态。
    logging.getLogger("fontTools").setLevel(logging.ERROR)
    apply_style()
    plt.rcParams.update({"svg.fonttype": "none", "pdf.fonttype": 42})
    sync_dcgp_data()
    data = load_attention_data()
    draw_dcgp_training_curves()
    draw_dcgp_generalization_boxplot()
    draw_dcgp_generalization_pareto()
    draw_training_curves(data)
    draw_attention_ablation(data)
    draw_sensitivity()
    draw_degradation_heatmap()
    draw_selection_radar()
    draw_rl_pareto()
    draw_rl_raincloud()
    print("第三章可复现实验图已统一重画。")


if __name__ == "__main__":
    main()
