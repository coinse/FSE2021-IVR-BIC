# Manual Inspection

[Prior work](https://github.com/justinwm/InduceBenchmark/blob/master/Defects4J.csv) (Wen et al. 2019) identified the BICs for the faults in Defects4J.
We found that 14 commits among the identified BICs are not contained in the reduced BIC search space obtained using failure coverage.
The following table gives the list of the commits. Please click the *details* to see the detailed inspection results.


| Fault                                                        | Omission fault   | Commit identified as a BIC                 | Inspection results                   |
|:-------------------------------------------------------------|:----------------:|:-------------------------------------------|:-------------------------------------|
| Lang-65b                                                     | O                | `fe70395` [[diff](./commits/fe70395.diff)] | Modifies no source code [[details](./inspection/fe70395.md)] |
| Closure-12b                                                  | O                | `df223ef` [[diff](./commits/df223ef.diff)] | Modifies comments only  [[details](./inspection/df223ef.md)] |
| Closure-90b<br>Closure-125b                                  | O<br>X           | `4c6e103` [[diff](./commits/4c6e103.diff)] | Modifies comments only  [[details](./inspection/4c6e103.md)] |
| Closure-127b                                                 | X                | `a0a3968` [[diff](./commits/a0a3968.diff)] | Not exist in the commit log [[details](./inspection/a0a3968.md)] |
| Math-13b                                                     | O                | `2885ba1` [[diff](./commits/2885ba1.diff)] | Not a failure starting point [[details](./inspection/2885ba1.md)] |
| Closure-19b                                                  | O                | `6700b61` [[diff](./commits/6700b61.diff)] | Not a failure starting point [[details](./inspection/6700b61.md)] |
| Closure-75b                                                  | X                | `70f817a` [[diff](./commits/70f817a.diff)] | Not a failure starting point [[details](./inspection/70f817a.md)] |
| Math-12b                                                     | X                | `c1de4ed` [[diff](./commits/c1de4ed.diff)] | Modified lines are not executed by the failing tests [[details](./inspection/c1de4ed.md)] |
| Math-74b                                                     | X                | `c95eb0b` [[diff](./commits/c95eb0b.diff)] | Modified lines are not executed by the failing tests [[details](./inspection/c95eb0b.md)] |
| Closure-107b<br>Closure-114b<br>Closure-118b<br>Closure-130b | O<br>X<br>O<br>X | `f322be0` [[diff](./commits/f322be0.diff)] | Modified lines are not executed by the failing tests [[details](./inspection/f322be0.md)] |