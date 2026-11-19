# Problem-description refinement

Scope: only prose in Section 3.1 and Section 3.2 of sections/03_problem_formulation.tex. All eight equations, Table 1, and Section 3.3 verified byte-for-byte at text level unchanged.

Sources directly read: Ning et al., same-title revised manuscript/response PDF at E:/weixin/xwechat_files/wxid_ls2dlss34fj022_a7f4/msg/file/2026-04/FJSP_MAOs___IMA(1).pdf. This is a revised manuscript/response package, not a file literally named 师兄的论文.pdf. Existing publisher-text extract tmp/senior_paper_extracted.txt independently agrees, but is a secondary local extraction. Current main(3).pdf has been located in the 2026-10 WeChat folder; active editing remains the current main.tex source, not an older attachment snapshot. Dissertation pp52-55 and docs/math_notation_audit.md were consulted for the reactive scope.

Primary source anchors: Section 3.1 describes job styles, product component requirements, processing/assembly machine eligibility and joint assembly qualifications; Section 3.2 explains product assignment and qualified matching, non-overlap exceptions for joint assembly, same-machine/start-time synchronization and predecessor completion. In the response package, revised Section 3.2 excerpts for constraints (14)-(15) and (17)-(20) are explicit (text extraction around lines2255-2297). The publisher-text extract places Section 3.1 on article pp4-5 and constraint explanation on p6: (10)-(13) matching, (14)-(15) resource exception, (16) one product per job, (17)-(20) synchronization, (21)-(22) cross-job precedence. These mechanisms are inherited, not a new contribution. No additional matching freedom or commitment policy is inferred from the base paper; existing execution commitments remain the current reactive model's definition.

## Before: Section 3.1
This study extends the flexible job shop scheduling problem with multi-level assembly operations (FJSP-MAOs) of Ning et al.~\cite{ning2027fjspmaos} to dynamic production. Jobs follow prescribed routes,
operations use eligible processing or assembly machines, and compatible jobs can be matched flexibly to product requirements. Each assembly starts once its required components are ready, allowing processing and assembly to overlap.
The base model supplies technological, machine-capacity, product-assignment,
and assembly-matching constraints.

## After: Section 3.1
This study extends the flexible job shop scheduling problem with multi-level assembly operations
(FJSP-MAOs) of Ning et al.~\cite{ning2027fjspmaos} to dynamic production. Unlike conventional FJSP,
products require hierarchical assemblies whose components may be basic jobs or subassemblies.
Component requirements determine dependencies, allowing independent branches to progress in parallel.
Jobs follow prescribed operation sequences and use eligible processing or assembly machines.
Flexible matching associates jobs with products subject to job-style requirements and assembly
qualifications; each job belongs to one product, and components are not arbitrarily interchangeable.
Matched operations participating in one assembly share its machine and start time, and assembly
waits for the required predecessors. These records represent a joint assembly activity rather than
independent activities competing for machine capacity.

Reason: integrate hierarchy, constrained job-product matching and joint records into the existing citation paragraph; avoid a duplicate appended paragraph.

## Before: Section 3.2
Assembly predecessors follow
the selected feasible matching. Completed assemblies and committed component usage cannot be undone.

## After: Section 3.2
Assembly predecessors follow the selected feasible matching. The inherited component-matching
and joint-assembly synchronization requirements remain in force during reactive adjustments;
the constraints below do not reproduce the full base formulation. Completed assemblies and
committed component usage cannot be undone.

Reason: make inherited synchronization explicit without claiming the displayed reactive constraints are the complete base model. No new variable or PPO matching action introduced.
