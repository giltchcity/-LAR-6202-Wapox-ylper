

主文件：[main.tex](main.tex)。它是独立的 LaTeX 回复文档，包含逐条回复、实验表格及矢量示意图。所需 PDF 图件存放在仓库的 `figures/` 目录，无需外部参考文献数据库。

## 当前范围

- 已起草 62 条回复：Editor 4 条、Reviewer 1 6 条、Reviewer 2 52 条。
- R1-3(a) 已包含 matched multi-keyframe pose-transport 的十例配对结果、Stage 1 观测关联与 Stage 2 位移构造的关系，并关联到 R1-3(c) 的完整关联门限消融；Editor 对应回复已补齐。
- R1-3(b) 使用五条多回环序列的干净版数据：15 次纠正、15 个纠正后检查点和 10 个继续融合后检查点。表中保留 F-score 差值与四项原有体积指标。
- R1-4 用文字说明主实验的均值和逐事件 F@25 差值范围。另包含参数敏感性、ElasticFusion 对比、Chamfer distance 和计时说明。
- 审稿意见使用黑色，作者回复使用蓝色。英文回复按《The Elements of Style》的简洁、明确与具体表达原则润色；保留原始审稿意见、实验结果、评测范围、位姿来源、计时口径和体积误差说明。
- Figure R1 位于 R1-3(b)，展示重复纠正与继续融合的检查点；Figure R2 位于 R2-G2，包含三个机制示意面板。[图源与导出文件](figures/mechanisms/)包括绘图脚本、TikZ、SVG 和 PNG 预览。`main.tex` 引用仓库中的 PDF 矢量图件。

这是供合作者讨论的初稿。正文里的修改描述需与最终修订论文同步。

## 在 Overleaf 使用

将本仓库导入一个独立的 Overleaf 项目，以 `main.tex` 为主文件，使用 pdfLaTeX 编译。论文正文继续保留在 [论文仓库](https://github.com/giltchcity/-LAR-6202-Wapox)，两个项目分别维护。

源文件声明了所需宏包，包括 geometry、fontenc、amsmath、amssymb、booktabs、xcolor、enumitem、longtable、tikz、float、graphicx、hyperref 和 pdfpages。

## 编译与校验状态

已核对 62 条回复；本次文字修改未改动审稿意见、表格、插图内容、LaTeX 标签或交叉引用。此前 Codex 编译环境初始化时报 `Unable to find standard directories for platform`；完整 PDF 编译与排版仍需在 Overleaf 中验证。

## 版本协作

以仓库根目录的 `main.tex` 为回复稿的同步文件。每轮先同步合作者的修改，再提交一批正文与回复的对应改动。最终交付前同步全文位置、表图编号和对应的论文修改。
