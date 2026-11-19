# Fourth-chapter refinement report

## Audit and changes
4.1 previously had no framework/MDP subheadings and introduced pool-screening details before its MDP. It now contains 4.1.1 Overall Framework and 4.1.2 MDP Formulation. The framework ends with offline/online interaction and introduces the MDP. Pool provenance/pending validation is retained with the action discussion, without claiming screening is complete.
4.2 retains the graph and update equations, defines V/E explicitly, separates stable structural context from dynamic state, and explains the graph relation families underlying the six patterns. No new edge operator or directed path is implemented.
4.3.1 retains projection, relation aggregation, six patterns, semantic aggregation, attention and residual equations in the same order. Added the local-to-multi-hop motivation and explicitly flags reduction, duplicate counting, sharing and scoring/granularity details as unverified.
4.3.2 retains role sets, mean pooling and fusion; explains role-specific summaries and confirms that overlap/context extent are unspecified. Existing presence indicator is not promoted to a verified implementation: its input position is missing from the displayed formula and requires confirmation.
4.4 renamed Multi-head PPO-based Decision Policy, kept compact without artificial extra headings. Actor, decoding, reward, GAE, PPO loss and training remain in their original order. Reduced repeated novelty/disclaimer language.

## Structure
4.1 Overall Framework and MDP Formulation
4.1.1 Overall Framework
4.1.2 MDP Formulation
4.2 Dynamic Heterogeneous Graph Representation
4.3 Meta-path Semantic Attention and Role-aware State Fusion
4.3.1 Meta-path Semantic Attention-based Node Encoding
4.3.2 Role-aware Mean Pooling Fusion
4.4 Multi-head PPO-based Decision Policy

## Invariants
All 17 numbered equation environments retained verbatim and in order. No mathematical operator, loss, normalization, residual, path definition or rule pool changed. Existing labels retained; only two new subheading labels added. All figures and the path table retained. Navigation comment numbers reflect actual sections; new technical prose has Chinese review comments. Existing older full translations remain review material and may need a later sentence-by-sentence translation pass after English finalization.

## Graph/path support
1: operation precedence; 2: operation-machine plus reverse relation; 3: machine-operation; 4: machine-operation-machine; 5: operation-junction incidence; 6: junction-assembly incidence. All are supported at the manuscript semantic-definition level. Actual directed edge construction, path instance enumeration and duplicate handling cannot be certified without source code. No runnable encoder/simulator is present in this repository.

## Source and figure checks
Dissertation direct extraction: Chapter3.2.1-3.2.2 and Figure3.2, printed pp56-59, supports role selection, mean pooling, fusion and rule-to-decision transitions. It does not supply the missing implementation contracts above.
Figure2 still depicts DCGP/offline generation, duplicate Decision Head2 and hyper-edge labels; it needs editable-source revision. Caption identification of the legacy pool does not resolve this discrepancy. Figure3 is a state-evolution schematic. Figure4 has the correct broad path/role/pooling/Actor flow, but machine glyph inconsistency, role labels, strict unequal-set shorthand, residual alpha versus manuscript eta, and absent explicit applicability mask require source-figure review. Raster files were not edited.

## Remaining verification
Full potential function, penalties, rule masks/fallbacks, GAE implementation and repair observability need implementation evidence. New simple/manual pools remain planned, with screening and retraining pending; old mixed-pool results remain distinct. No final rule counts or new results asserted.
Compilation log: build/methodology-final-build.txt. Check final log and generated build/main.pdf; no claim of complete implementation reproducibility or visual correction of original raster diagrams.
