# 数学视频项目 — Agent 指南

这个项目用来制作数学讲解视频（3Blue1Brown 风格的动画）。任务：根据给定的题目或知识点，写出讲解脚本、做成动画、渲染成 mp4。

## 技术栈
- **Manim Community Edition**（`manim`），不要用 3b1b 的 manimgl
- **LaTeX**（公式渲染）+ 中文支持 `ctex`
- **ffmpeg**：Manim 渲染和视频拼接都需要
- 可选配音：`manim-voiceover`（带 TTS，自动让动画和旁白对齐）

### 本机环境（Windows 11）
- Python 虚拟环境：`.venv`（Python 3.13，由 uv 创建）。所有命令用 `.venv\Scripts\manim.exe` / `.venv\Scripts\python.exe`，或先 `.venv\Scripts\activate`。
  装新包：`uv pip install --python .venv\Scripts\python.exe <包名>`
- LaTeX：MiKTeX（用户级安装，已开启缺包自动安装）。如果 LaTeX 报缺包，用 `mpm --install=<包名>` 补装。
- ffmpeg：winget 安装的 Gyan.FFmpeg。
- `fc-list` 在 Windows 上不可用，查中文字体用：
  `.venv\Scripts\python.exe -c "import manimpango; print(manimpango.list_fonts())"`
  本机可用中文字体：`Noto Sans SC`（默认）、`Noto Serif SC`、`Microsoft YaHei`、`SimHei`、`DengXian`。

## 项目结构
```
MathVideo/
├── CLAUDE.md
├── videos/
│   └── <视频名>/            # 每个视频一个文件夹，例如 videos/chain-rule/
│       ├── script.md         # 讲解脚本 + 分镜
│       ├── scenes.py         # 这个视频的所有 Scene
│       └── assets/           # 图片、音频等素材
├── common/
│   └── style.py              # 共用的颜色、字体、常用组件
├── output/                   # 最终成片
└── media/                    # Manim 自动生成的渲染缓存（不要手动改）
```
`scenes.py` 里用 `from common.style import *` 引入共用样式（`common/style.py` 会自动把项目根目录加进 `sys.path` 的写法见下方模板）。

## 工作流程（每个视频都按这个顺序）
1. **写脚本**：在 `script.md` 里写出讲解思路，分成若干段（每段对应一个 Scene）。每段写清楚：要讲什么、屏幕上出现什么、旁白说什么。**先把脚本给用户看，确认后再写代码。**
2. **写动画**：在 `scenes.py` 里每段一个 Scene 类，命名清楚（如 `Intro`、`DefineDerivative`、`Example1`）。
3. **低画质预览**：`manim -pql videos/<名>/scenes.py <SceneName>`，快速检查。
4. **检查画面**：用 `manim -s` 导出关键帧截图，自己看一遍：文字有没有出界、重叠、公式有没有渲染错、中文有没有变成方框。有问题先自己改。
5. **高画质成片**：确认后用 `-qh`（1080p60）渲染，用 ffmpeg 把所有 Scene 按顺序拼起来，放到 `output/<名>.mp4`。

## 数学内容要求
- 数学必须正确。每个公式、每一步推导写进动画前先核对一遍；有数值例子就用 Python 算一下验证。
- 讲解逻辑：先直觉/图像，再公式，最后例题。不要一上来就堆公式。
- 一个画面只讲一件事，信息量不要太大。
- 推导过程用 `TransformMatchingTex` 让公式一步步变形，而不是直接替换。

## 中文与公式
- 纯中文文字：`Text("...", font=CJK_FONT)`（`CJK_FONT` 在 `common/style.py`，默认 `Noto Sans SC`）。
- 纯公式：`MathTex(r"...")`。
- 中文和公式混排：`Tex`，并设置 `tex_template=TexTemplateLibrary.ctex`（style.py 里有 `CnTex` 封装）。
- 如果中文显示成方框或报错，优先检查字体和 ctex 是否安装。

## 风格规范（`common/style.py`，所有视频共用）
- 深色背景（Manim 默认），主色统一：变量 `BLUE`，强调 `YELLOW`，结果 `GREEN`
- 字号统一：标题 48、正文 36、公式 40 左右
- 动画节奏：每个动作 `run_time` 约 1–2 秒，重要结论后 `self.wait(1–2)`
- 画面留边距，元素不要贴边；用 `.to_edge()`、`.next_to()` 排版，不要硬写坐标
- 视频比例默认 16:9；短视频（抖音/小红书/Shorts）改竖屏 9:16：`config.pixel_width=1080, config.pixel_height=1920`（同时 `config.frame_width=8, config.frame_height=8*16/9`）

## 配音（用户要求时再做）
- 用 `manim-voiceover`，旁白文字来自 `script.md`
- 中文 TTS 优先用 gTTS（`lang="zh-CN"`）或用户指定的服务
- 用 `with self.voiceover(text=...) as tracker:` 让动画时长跟着旁白走

## 注意事项
- 每次改完代码都要重新渲染并检查，不要只改代码就说"好了"
- 渲染报错时先读完整报错，最常见的是 LaTeX 语法错误和缺字体
- 不要删除 `output/` 里已经做好的成片
- 完成后告诉用户：成片位置、时长、包含哪几个 Scene
