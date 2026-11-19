# Mathematical notation audit: direct dissertation follow-up

Source: E:/weixin/xwechat_files/wxid_ls2dlss34fj022_a7f4/msg/file/2026-10/Ph.D Dissertation.pdf. Directly inspected Chapter 3, printed pp52-55, Eq.3.1-3.7 and Algorithm3.1. Current English entry: main.tex. main(3).pdf not supplied. Text extraction is not visual layout verification.

A: confirmed mathematical conflict; B: notation/definition clarification; C: consistent meaning or justified dynamic extension; D: evidence required, no change. No confirmed A-class objective/constraint error was found.

| Object | Dissertation notation/source | English comparison / action | Class |
|---|---|---|---|
| i,j; O_ij | O_i,j (p52) | Same indices; commas are typographical | C |
| O^0; O^new(t); O(t) | O in Eq.3.1 (p53) | Retain English initial/admitted/new sets for arrivals | C |
| O^R; O^wait; O^int | Same union (p52) | Same meaning; table definitions added | B |
| K_ij | K_i,j (Eq.3.2) | Same eligible-machine set | C |
| S^0,S | Same (pp52-53) | Same baseline/execution distinction | C |
| B^0,B,E | Same; thesis also defines E^0 (p52) | Unused E^0 need not be introduced | C |
| X^0,X | Same (pp52-53) | No baseline invented for new orders | C |
| Cmax^0,Cmax; f1,f2 | Same (Eq.3.1) | Objectives agree | C |
| Y_iji'j' | Same (Eq.3.5 p54) | Y=1 means first operation precedes second | C |
| p; tilde p | pt; tilde pt (pp52-53) | English p follows requested notation; NOT a correction of thesis | B |
| epsilon_ij(t) | Same, greater than -1 (p52) | Same perturbation definition | C |
| r_i | Not explicit in inspected Chapter 3 model | Arrival release-time extension retained | C |
| t_k^ava(t) | Same (Eq.3.3) | Same availability notation | C |
| k^f; u^rec | Same (Eq.3.4) | Wait/reroute and full-duration restart agree | C |
| Ddev; lambda_B,lambda_X | Eq.3.1: denominator |O|Cmax^0 and 2|O| | English uses O^0 deliberately; weights and factors agree | C |
| Ddev/Dref | Not in directly inspected pp52-55 | English reward scaling distinct from objective normalization; thesis reward still needs targeted check | D |
| P^pro; P^asm | Same (Eq.3.3) | Separate sets retained; table definitions added | B |
| M | Large positive constant (Eq.3.5) | Same; table definition added | B |
| Xi; internal state; event operators | Xi,x_n,S^act,Q^evt,E^evt; Eq.3.6-3.7 | English abstract transition notation is a reformulation, not identical notation | C |
| x_n,D_n,n,t_n | x_n,D_n,n,t (Algorithm3.1 p55) | t_n makes physical-time correspondence explicit | B |
| pi,a_n,d_n | d_n <- pi(x_n,S^0,D_n), calling Algorithm3.2 | English explicitly separates rule selection and decoding; interface clarification, NOT a thesis error | B |
| Assembly synchronization / repair observability | Full restart and forced waiting explicit p53 | Detailed implementation remains unverified | D |
| Experiment deviation scale | Normalized objective Eq.3.1 | No numerical rescaling without logs | D |

## Actual previous edits retained
- sections/03_problem_formulation.tex:87-90: add existing waiting/interrupted sets, nominal duration, perturbation, predecessor sets and big-M to Table 1.
- Same file:151 and duration entries / Eq.(4): pt and tilde{pt} -> p and tilde p. This follows the requested English notation; thesis itself uses pt. No need to switch back and forth.
- Same file:364 onward: define event set, transition operators, decision index and physical-time correspondence.
- Same file:453-455: direct composite-policy call -> explicit rule selection and existing rule decoding. Original thesis composite-policy interface is valid; this is a B-class clarification.
- sections/04_methodology.tex:658-659: clarify terminal reward scaling versus Eq.(3) normalization.

## Invariants and verification
O^0 retained; new orders receive no invented baseline. Eq.(3) unchanged. Eight equation environments and their labels retain order and numbering 1-8; only processing-duration notation changes in Eq.(4). No HGNN/PPO core mechanism, rule pool, numerical experiment, or section structure changed.
Previous compilation generated 18 pages with all latexmk targets up to date and no undefined references, multiply defined labels or Overfull diagnostics. This follow-up changes only this report; no new compilation claimed.
Further evidence needed: original implementation of assembly matching/synchronization, repair observability, experiment deviation units, and targeted comparison of PPO reward normalization outside inspected pp52-55.

## Encoding-focus revision: Sections 4.1-4.3
Graph construction/update is an observation representation, not an independent algorithmic contribution. Contributions are the six scheduling-semantic paths with semantic attention and Role-aware Mean Pooling Fusion. Abstract, introduction contributions and conclusion received minimal naming alignment; no experimental conclusions changed.

New headings: 4.3 Meta-path Semantic Attention and Role-aware State Fusion; 4.3.1 Meta-path Semantic Attention-based Node Encoding; 4.3.2 Role-aware Mean Pooling Fusion. Attention and residual equations moved into the first conceptual block by moving the subheading, not equations. All Chapter 4 equation environments and the six-path table were checked verbatim unchanged. All labels retained; 4.4 remains in place.

Symbol clarification: internal state mathcal X_n, observed x_n, graph feature matrix boldsymbol X_n, observable global statistics z_n and decision type vartheta_n are distinguished explicitly; no global renaming. s_n remains the same tuple. Actor heads receive pooled/fused states and choose rules a_n; decoding produces d_n; environment enforces feasibility.

Implementation evidence: repository contains no runnable HGNN/PPO/simulator implementation. Existing mean-pooling formula defines role subsets and fusion, but exact role membership rules, neighborhood radius, role-slot order, MLP dimensions, and treatment of overlapping roles remain unverified. The manuscript's zero-vector/presence-indicator convention is retained as an explicit convention pending verification; the formula does not show where the indicator enters the MLP input. No indicator dimension or additional mechanism was invented. AGG_k and g internals, residual coefficient implementation and per-node versus global semantic weighting need code confirmation. Existing formulas preserved rather than silently redesigning them.

Figure 2 remains the legacy mixed-pool diagram (DCGP block and duplicated head label need eventual source editing); Figure 3 caption explicitly identifies schematic state evolution; Figure 4 caption aligns the two encoding stages with downstream rule selection, raster labels unchanged. Meta-path directions/instance extraction and figure glyph inconsistencies remain TODO; no directed paths were invented from undirected table notation. Planned simple/manual pools and screening/retraining remain pending, distinct from legacy experiments.
