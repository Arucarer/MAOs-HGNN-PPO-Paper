#这个图是确定图里面的样式，所以不用修改这个图的文件
from __future__ import annotations

import importlib.util
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BASE_STYLE = (
    PROJECT_ROOT / "04_实验与绘图" / "公共绘图样式" / "原绘图样式"
    / "thesis_plot_style.py"
)

# 与第二、四章一致：基线在前，本文完整方法使用低饱和蓝并放在最后。
COLORS = {
    "light_gray": "#C9C9C9",
    "gray": "#A8A8A8",
    "dark_gray": "#707070",
    "orange": "#D9A15B",
    "purple": "#B39BC8",
    "teal": "#73A6A6",
    "blue": "#2F5D8C",
    "red": "#D32F2F",
}
LINE_COLORS = {
    COLORS["light_gray"]: "#8A8A8A",
    COLORS["gray"]: "#666666",
    COLORS["dark_gray"]: "#4F4F4F",
    COLORS["orange"]: "#A96F24",
    COLORS["purple"]: "#8F4FAF",
    COLORS["teal"]: "#1B8E82",
    COLORS["blue"]: "#154C79",
}

TIMES_PATH = Path(r"C:\Windows\Fonts\times.ttf")
SONGTI_PATH = Path(r"C:\Windows\Fonts\simsun.ttc")
ENGLISH_FONT = FontProperties(fname=TIMES_PATH)
SONGTI_FONT = FontProperties(fname=SONGTI_PATH)
MIXED_FONT = FontProperties(family=["Times New Roman", "SimSun"])

# 字典顺序就是图例和横轴顺序；不要按数据列出现顺序重新分配颜色。
METHOD_STYLES = {
    "dcgp_evolution": {
        "CGP": COLORS["gray"],
        "DCGP": COLORS["orange"],
        r"DCGP-$\alpha$": COLORS["purple"],
        r"DCGP-$\beta$": COLORS["teal"],
        "DCGP-NCBE": COLORS["blue"],
    },
    "dcgp_six_method": {
        "Baseline": COLORS["light_gray"],
        "CGP": COLORS["dark_gray"],
        "DCGP": COLORS["orange"],
        r"DCGP-$\alpha$": COLORS["purple"],
        r"DCGP-$\beta$": COLORS["teal"],
        "DCGP-NCBE": COLORS["blue"],
    },
    "rule_generalization": {
        "A6": COLORS["light_gray"],
        "A5": COLORS["dark_gray"],
        "A4": COLORS["orange"],
        "A3": COLORS["purple"],
        "A2": COLORS["teal"],
        "A1": COLORS["blue"],
    },
    "rl_generalization": {
        "L2D": COLORS["light_gray"],
        "MPGN–Multi-PPO": COLORS["dark_gray"],
        "HGNN-PPO": COLORS["orange"],
        "HGNNR-PPO": COLORS["purple"],
        "MHGNN–MA-PPO": COLORS["teal"],
        "SPRE-HGNN-PPO": COLORS["blue"],
    },
    "strategy_comparison": {
        "Fixed rule": COLORS["gray"],
        "Manual rule": COLORS["orange"],
        "Random selection": COLORS["purple"],
        "Fixed DCGP-NCBE": COLORS["teal"],
        "SPRE-HGNN-PPO": COLORS["blue"],
    },
    "attention_ablation": {
        "w/o attention": COLORS["gray"],
        "Full model": COLORS["blue"],
    },
}


def load_base_style():
    """复用第二、四章的字体、坐标轴和导出设置。"""
    if not BASE_STYLE.exists():
        #改动1
        return None
        #改动1
    spec = importlib.util.spec_from_file_location("thesis_plot_style", BASE_STYLE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def apply_style():
    """应用论文公共样式，并缩放到正文通栏图的字号。"""
    style = load_base_style()
    if style is not None:
        #改动1
        style.apply_thesis_style()
        #改动1
    # 显式注册Windows字体，避免独立Conda环境找不到中文字体。
    for font_path in (SONGTI_PATH, TIMES_PATH):
        font_manager.fontManager.addfont(font_path)
    plt.rcParams.update({
        # 西文先用Times New Roman；缺失的中文字形再回退到宋体。
        "font.family": ["Times New Roman", "SimSun"],
        "font.serif": ["Times New Roman", "SimSun"],
        "font.sans-serif": ["Times New Roman", "SimSun"],
        "mathtext.fontset": "custom",
        "mathtext.rm": "Times New Roman",
        "mathtext.it": "Times New Roman:italic",
        "mathtext.bf": "Times New Roman:bold",
        "mathtext.sf": "Times New Roman",
        "mathtext.tt": "Times New Roman",
        "mathtext.cal": "Times New Roman:italic",
        "font.size": 8.7,
        "axes.titlesize": 9.2,
        "axes.labelsize": 8.7,
        "xtick.labelsize": 8.2,
        "ytick.labelsize": 8.2,
        "legend.fontsize": 8.2,
    })
    return style


def validate_method_styles() -> None:
    """确保每组完整方法都位于末位且保持蓝色。"""
    expected_last = {
        "dcgp_evolution": "DCGP-NCBE",
        "dcgp_six_method": "DCGP-NCBE",
        "rule_generalization": "A1",
        "rl_generalization": "SPRE-HGNN-PPO",
        "strategy_comparison": "SPRE-HGNN-PPO",
        "attention_ablation": "Full model",
    }
    for group, method in expected_last.items():
        styles = METHOD_STYLES[group]
        assert list(styles)[-1] == method
        assert styles[method] == COLORS["blue"]


if __name__ == "__main__":
    validate_method_styles()
    print("第三章绘图配色与方法顺序校验通过。")
