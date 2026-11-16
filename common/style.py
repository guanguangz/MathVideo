"""所有视频共用的样式：颜色、字号、字体、常用组件。

在 videos/<名>/scenes.py 开头这样引入：

    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
    from common.style import *
"""
from manim import *

# ---------- 字体 ----------
CJK_FONT = "Noto Sans SC"

# ---------- 颜色 ----------
VAR_COLOR = BLUE        # 变量
EMPH_COLOR = YELLOW     # 强调
RESULT_COLOR = GREEN    # 结果
TEXT_COLOR = WHITE

# ---------- 字号 ----------
TITLE_SIZE = 48
BODY_SIZE = 36
MATH_SIZE = 40

# ---------- 节奏 ----------
RUN_TIME = 1.5
PAUSE = 1.5

# ---------- 中文 LaTeX 模板 ----------
CTEX = TexTemplateLibrary.ctex


def Title(text: str, **kw) -> Text:
    """顶部标题（中文）。"""
    return Text(text, font=CJK_FONT, font_size=TITLE_SIZE, color=TEXT_COLOR, **kw).to_edge(UP, buff=0.6)


def Body(text: str, **kw) -> Text:
    """正文（中文）。"""
    kw.setdefault("color", TEXT_COLOR)
    return Text(text, font=CJK_FONT, font_size=BODY_SIZE, **kw)


def Formula(*tex: str, **kw) -> MathTex:
    """纯公式。"""
    kw.setdefault("font_size", MATH_SIZE)
    return MathTex(*tex, **kw)


def CnTex(*tex: str, **kw) -> Tex:
    """中文与公式混排，例如 CnTex(r"当 $x\\to 0$ 时")。"""
    kw.setdefault("font_size", BODY_SIZE)
    kw.setdefault("tex_template", CTEX)
    return Tex(*tex, **kw)


def highlight_box(mob: Mobject, color=EMPH_COLOR) -> SurroundingRectangle:
    """给重要结论加框。"""
    return SurroundingRectangle(mob, color=color, buff=0.2, corner_radius=0.1)


def use_vertical():
    """切换为竖屏 9:16（短视频）。在 scenes.py 顶部调用。"""
    config.pixel_width = 1080
    config.pixel_height = 1920
    config.frame_width = 8.0
    config.frame_height = 8.0 * 16 / 9
