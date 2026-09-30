

主文件：[main.tex](main.tex)。它是独立 LaTeX 文档，包含正文、TikZ 示意图以及完整事件表，无外部图片或参考文献文件依赖。

## 当前范围

- 已起草 62 条回复：Editor 4 条、Reviewer 1 6 条、Reviewer 2 52 条。
- R1-3(a) 已包含 matched multi-keyframe pose-transport 的十例配对结果、Stage 1 观测关联与 Stage 2 位移构造的关系，并关联到 R1-3(c) 的完整关联门限消融；Editor 对应回复已补齐。
- 包含连续纠正与融合的 51 个检查点、原主实验及高分辨率子集的 62 个事件、参数敏感性、ElasticFusion 对比、Chamfer distance 和计时说明。
- 采用黑色审稿意见、蓝色作者回复。文字经过 anti-defensive-writing 审校，保留评测范围、不同系统位姿来源、时间口径和体积误差等必要限制。

这是供合作者讨论的初稿。正文里的修改描述需与最终修订论文同步。

## 在 Overleaf 使用

将本仓库导入一个独立的 Overleaf 项目，以 `main.tex` 为主文件，使用 pdfLaTeX 编译。论文正文继续保留在 [论文仓库](https://github.com/giltchcity/-LAR-6202-Wapox)，两个项目分别维护。

需要的宏包均在源文件中声明：geometry、fontenc、amsmath、amssymb、booktabs、xcolor、enumitem、longtable、tikz、hyperref。

## 编译与校验状态

62 条回复、LaTeX 环境配对和内部交叉引用已通过源码检查。Codex 内置编译器在初始化阶段报 `Unable to find standard directories for platform`，PDF 编译及排版尚未验证。

## 版本协作

以仓库根目录的 `main.tex` 为回复稿的同步文件。每轮先同步合作者的修改，再提交一批正文与回复的对应改动。最终交付前同步全文位置、表图编号和对应的论文修改。
