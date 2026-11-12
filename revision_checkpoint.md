# Revision checkpoint

日期：2026-11-13。续接当前工作区，未重置Git，未重跑tmp/restructure_ch4.py。

## 已完成与修改文件
- sections/00_frontmatter.tex：替换其他课题摘要，修正标题、关键词与highlights。摘要不补造性能数值。
- sections/01_introduction.tex：贡献聚焦异构图与注意力编码，PPO作为执行接口。
- sections/03_problem_formulation.tex：3.3标题统一，增加环境到策略过渡，区分完工事件和外部扰动。
- sections/04_methodology.tex：保留上次完成的结构与MDP前移；增加计划规则池的边界说明。17个原公式保留。
- sections/05_experiments.tex：保留现有数值与图；弱化精简/混合规则库优越性比较；在实验设置增加空白规则评价模板；明确编码消融控制变量。
- sections/07_conclusion.tex：补写与真实研究主线一致且明确证据边界的结论。
- 本文件：交接记录。

## 最终章节结构
3.1 Problem Description
3.2 Reactive Scheduling Model
3.3 Event-driven Simulation Environment
4.1 Overall Framework and MDP Formulation
4.2 Dynamic Heterogeneous Graph Representation
4.3 Meta-path Semantic Attention-based State Encoding
4.3.1 Heterogeneous Relation and Meta-path Aggregation
4.3.2 Semantic Attention and Decision-specific Readout
4.4 Multi-head PPO-based Adaptive Rule Selection

## 上次第四章审计
四个二级节和4.3两个三级节已经完成；MDP与转移在4.1，规则解码与训练在4.4。未发现重复标签。所有公式逐字保留，相对编号因MDP前移自动更新，引用仍采用标签。图2/3/4与元路径表保留。元路径表实际是Table 2，Table 1为第三章符号表，不硬编码表号。
六类路径涵盖前序、资源竞争、工序机器关联、资源调整、装配分支耦合与层级依赖。邻居权重alpha、语义权重beta和残差eta明确分开；语义归一化限于有效模式。g仅定义为可学习标量映射，AGG、g内部结构、角色选择半径、空角色处理与残差参数仍缺实现证据，不能声称代码已核实。
MDP沿用决策索引n与物理时间t_n；是否具备充分Markov状态仍须核实完整特征、事件信息及可观测性。

## 动作空间与实验事实边界
当前材料描述旧混合池：简单、人工和演化复合规则（包含DCGP-NCBE）。规则比例图支持这一来源，但未发现可核验的训练实现或模型检查点，不能据此确认三个头的真实逐条名称与数量。
新方案仅为计划：Offline-screened dispatching rule pools，从简单与人工规则筛选，不包含将DCGP演化包装为本论文创新。每头5–8条只是设计范围，正文不写成事实。新池尚待实现、验证、重训；旧数值一律不归属新池。
规则评价表是明确标注未完成的模板，无虚构规则或数值。训练/验证集筛选，固定其他决策类别，兼顾双目标及多样性，禁止测试集泄漏。

## 图表处理建议
保留Figure 1问题图、Figure 2总体框架、Figure 3动态图、Figure 4编码图及真实比较/消融图。规则选择比例图保留为旧混合池的辅助行为证据，不作为新池结果或因果贡献证明。原始图文件均未修改或删除。
Figure 2含离线DCGP生成模块、重复Decision Head 2标签及Hyper-edge字样，与当前HGNN定位需统一；Figure 4部分机器形状、角色标签及不等号表述需核实。原图问题尚未修图，不能宣称图文完全一致。

## 待完成与下一步
1. 获取逐头规则清单、评分方向、平局处理、适用性掩码及故障恢复解码实现。
2. 实现独立验证筛选并记录规则双目标评价、选择依据、规则多样性及最终配置；重新训练并保存模型来源。
3. 在相同PPO/规则/奖励/预算下完成异构信息、语义注意力和其他实际模块的受控消融；现有比较不能独立证明所有模块贡献。
4. 核实紧急插单数据标签到算例/模型的对应、跨扰动泛化、运行时间、种子与重复试验；不改原数值。
5. 需要原大论文和实现重新核对；本次项目未提供原大论文PDF，已有docs中的旧核查只作为交接材料，不冒充本次直接核对。
6. 替换原图中的旧范围与标注，补充未完成参考文献、作者及单位信息。引言已有准确段落和相关工作结尾保留。
7. 检查tmp/continuation-build.log与build/main.log；最新PDF为build/main.pdf，根目录main.pdf可能是旧版。

## 验证
续接脚本确认所有原equation环境逐字不变，所有章节标签无重复。编译状态见下方追加记录。备份在tmp/continuation-before；脚本tmp/continue_revision.py不是可重复运行的维护接口，勿直接重跑。
编译补记：latexmk日志确认16页PDF已写出且All targets up-to-date；PowerShell进程报告exit 1（存在外部命令stderr警告），不等同于LaTeX排版错误。build/main.log未检出undefined、multiply defined或Overfull。尚未完成本轮PDF逐页视觉审查；保留Underfull与hyperref书签警告。

## 离线筛选对应关系续修
- 4.1精简筛选定义并指向5.2.2及筛选表；4.4明确各头调用相应固定集合、输出维度与集合大小对应。
- 5.2.2改为Offline Rule Evaluation and Action-space Configuration，模板从5.1实际移入5.2.2，按三类决策头分组，不虚构候选名称与Selected结果。
- 增加同实例/扰动、相同预算、其他两类决策固定、统计量与变异记录要求；固定背景下排名仅为条件评价，不能声称全局最优。
- 最终保留行必须映射到三个规则集合并报告数量，然后冻结、重训、再进行编码器对照。旧混合池数据仍保留原归属。
- Figure 2保留原图，在图注明确其为旧混合池框架、离线生成模块不代表新筛选机制。尚未重画，最终新配置定稿仍需替换该图；不以改图掩盖实验未完成。
- 本次仅修改sections/04_methodology.tex、sections/05_experiments.tex及本记录。编译日志tmp/screening-build.log。
候选设计预览：5.2.2新增18条用户建议规则设计表及18行待评价表；用带波浪号的集合区分初始候选与最终规则集合，未修改现有MDP或PPO公式。明确BAS-O不是Ddev的直接最小化；装配评分、缺失基准、未知维修时间、规则冗余与完整工时重启均需实现核实。未添加规则代码或实验数值。编译日志tmp/candidate-build.log。
按作者要求暂时注释F7注意力训练对照图与F8旧混合规则比例图，连同图内附带解释及直接交叉引用；保留原图文件和注释源码。摘要与结论同步取消对已隐藏图的展示性表述。F7原图实际为有无注意力对照，并非复合规则优越性图；此处执行暂隐藏，不据此改变其原有实验含义。
恢复F7及其直接说明，F8继续隐藏。第五章按五组补充实验安排位置：5.2.2规则、5.3编码器与模块读出消融、5.5扰动/跨规模/独立测试、5.6计时及甘特案例；Discussion顺延5.7。新增experiment_audit.md、experiment_progress.md，因缺训练仿真实现未运行实验。

## 文件清理与实验版式占位
新增编码器对照表/图框、扰动趋势图框、在线计时表/图框、甘特图框及案例目标表；原规则评价表复用。占位均标注results pending，无虚构数据。
删除本轮一次性修改脚本、临时预览和旧日志；保留历史备份、原始图与数据。根目录部分旧编译文件被其他进程占用，未强制关闭进程或删除。
最新论文路径build/main.pdf。临时文件和build已经由.gitignore排除；本地编辑器设置不加入论文提交。
