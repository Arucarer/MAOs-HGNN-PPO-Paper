# 论文源码审阅导航

本文件只说明源码位置和标记，不参与论文编译。

| 正文编号 | 文件 |
|---|---|
| 第1章：引言 | [01_introduction.tex](../sections/01_introduction.tex) |
| 第2章：文献综述 | [02_literature_review.tex](../sections/02_literature_review.tex) |
| 第3章：问题描述与数学建模 | [03_problem_formulation.tex](../sections/03_problem_formulation.tex) |
| 第4章：方法 | [04_methodology.tex](../sections/04_methodology.tex) |
| 第5章：实验 | [05_experiments.tex](../sections/05_experiments.tex) |
| 第6章：结论与未来工作 | [07_conclusion.tex](../sections/07_conclusion.tex) |

`06_discussion.tex` 未启用；实际第六章是 `07_conclusion.tex`。

## 标记用法

- `完整中文译文｜4.3.1-P02`：紧跟该英文编辑块的完整中文翻译，区别于原有段意说明。
- 正文115个编辑块均已补译；贡献条目的译文包含条目开头，不能只对照编号后的半句。
- 章节标题、图注、表题、主要表格文字和两段伪代码也有对应中文注释。
- 摘要按当前英文忠实补译，但保留“旧研究主题，与正文不同”的提醒，未替换英文摘要。
- `第 4.3.1 节｜第 02 段｜4.3.1-P02`：可直接搜索、定位并反馈的正文编辑块。
- `E`、`F`、`T`、`A`：分别标识公式、图块、表格、算法；标签保留不变。
- `待补实验`、`待补文献`、原有 `TODO`：提醒尚未核验或完成的内容。
- 编号不进入PDF；正文遇到公式或代码边界时可能分为多个编辑块。
- 英文正文与中文译文均按整段排版：行长围绕固定宽度适度浮动，优先在自然停顿处换行。
- 短句、短分句接在同一段内，不逐个标点另起一行；英文不拆单词，中文尽量不拆语义分句。
- 数学表达式、引用和表格代码保持原结构。VS Code 的显示换行不改变论文版面。

## 本次译文的主要术语

| English | 中文 |
|---|---|
| processing--assembly | 加工—装配 |
| baseline schedule | 基准计划 |
| schedule deviation | 计划偏离度 |
| meta-path semantic attention | 元路径语义注意力 |
| decision-specific role readout | 面向决策的角色读出 |
| rule selection / concrete scheduling decision | 规则选择／具体调度决策 |
| role-wise mean pooling | 按角色均值池化 |
| potential shaping | 势函数奖励塑形 |

## 章节索引

- **1** Introduction — `01_introduction.tex`
- **2** Literature Review — `02_literature_review.tex`
- **2.1** Dynamic Processing--Assembly Scheduling — `02_literature_review.tex`
- **2.2** Reinforcement Learning and Graph-based State Representation — `02_literature_review.tex`
- **2.3** Research Gaps and Motivation — `02_literature_review.tex`
- **3** Problem Description and Mathematical Formulation — `03_problem_formulation.tex`
- **3.1** Problem Description — `03_problem_formulation.tex`
- **3.2** Reactive Scheduling Model — `03_problem_formulation.tex`
- **3.3** Event-driven Discrete-event Simulation Environment — `03_problem_formulation.tex`
- **4** Dynamic Heterogeneous Graph-based Rule Selection — `04_methodology.tex`
- **4.1** Overall Framework — `04_methodology.tex`
- **4.2** Dynamic Heterogeneous Graph Construction and Update — `04_methodology.tex`
- **4.2.1** Typed Graph and Observable Features — `04_methodology.tex`
- **4.2.2** Event-driven Graph Update — `04_methodology.tex`
- **4.3** Meta-path Semantic Attention-based State Encoding — `04_methodology.tex`
- **4.3.1** Heterogeneous Relation Aggregation — `04_methodology.tex`
- **4.3.2** Processing--Assembly Meta-path Semantics — `04_methodology.tex`
- **4.3.3** Semantic Attention and Residual Enhancement — `04_methodology.tex`
- **4.3.4** Decision-specific Role Readout — `04_methodology.tex`
- **4.4** Multi-head PPO-based Adaptive Rule Selection — `04_methodology.tex`
- **4.4.1** Rule Actions and Scheduling Decisions — `04_methodology.tex`
- **4.4.2** Three Actor Heads and Dual-objective Reward — `04_methodology.tex`
- **4.4.3** PPO Optimization and Online Execution — `04_methodology.tex`
- **5** Experimental Results and Discussion — `05_experiments.tex`
- **5.1** Experimental Setup — `05_experiments.tex`
- **5.2** Hyperparameter and Rule-set Configuration — `05_experiments.tex`
- **5.2.1** Hyperparameter Sensitivity — `05_experiments.tex`
- **5.2.2** Candidate Rule-set Configuration — `05_experiments.tex`
- **5.3** Ablation Experiments — `05_experiments.tex`
- **5.4** Comparative Experiments — `05_experiments.tex`
- **5.4.1** Comparison across Training Instance Sizes — `05_experiments.tex`
- **5.5** Generalization Experiments — `05_experiments.tex`
- **5.5.1** Performance on Independent Instances — `05_experiments.tex`
- **5.5.2** Transfer across Disturbance Conditions and Decision Time — `05_experiments.tex`
- **5.6** Discussion — `05_experiments.tex`
- **6** Conclusion and Future Work — `07_conclusion.tex`

## 审阅时特别留意

- 第二章的引用和逐篇研究内容仍有占位符。
- 第四章有关实现、规则库和训练设置的核验提示仍保留。
- 第五章新增实验尚未完成的内容仍明确标为待补结果。
- 第六章结论正文尚未写入；现有提示不会显示在PDF中。
- 摘要仍保留其他研究主题的旧稿，需要另行修改；本次未改写摘要。
