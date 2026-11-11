# 第三章实验图数据清单

## 图3.7：DCGP-NCBE参数灵敏度

- 数据文件：`数据/mock_fig37_dcgp_fitness_sensitivity.csv`
- 绘图脚本：`mock_fig37_dcgp_fitness_sensitivity.py`
- 输出文件：`../../02_论文图片/03_反应式学习调度/mock_fig37_dcgp_fitness_sensitivity.png`、`.svg`
- 数据状态：**PLANNING DATA - replace before submission**
- 用途：在真实DCGP-NCBE参数实验完成前，验证四幅横排子图的论文版式及预期趋势。
- 预期趋势：进化代数和父代规模增加时适应度先改善后趋稳；父子代比例和结构趋同阈值在中间水平附近取得较低适应度，两端设置产生性能退化。
- 不确定性：CSV中的`fitness_sd`仅记录预期波动尺度，当前图按第二章参数设定图的样式仅绘制均值折线。
- 替换要求：提交论文前必须用真实重复实验所得的适应度均值和标准差替换该文件，并删除正文及图注中的规划模拟数据标记。

## 图3.14：候选规则选择比例

- 数据文件：`../../lyk数据/雷达图数据DCGP-NCBE规则选择比例数据.xlsx`
- 绘图脚本：`redraw_chapter3_experiment_figures.py`中的`draw_selection_radar()`。
- 输出文件：`../../02_论文图片/03_反应式学习调度/不同规模算例下各类规则的选择比例.png`、`.pdf`、`.svg`。
- 数据状态：**UNVERIFIED SUMMARY - replace or verify before submission**
- 当前边界：工作簿由单独整理的比例数据构成，未发现可追溯至HGNN-PPO训练过程的动作日志，且五类规则来源与第3.2节当前定义的DCGP-NCBE规则动作空间尚未统一。
- 使用要求：当前图仅保留行为统计接口，不参与性能结论。提交论文前应从真实动作日志重新统计，并使候选规则类别与第3.2节的动作空间定义一致。
