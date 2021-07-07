# c1de4ed

[`c1de4ed`](../commits/c1de4ed.diff) was identified as the BIC of `Math-12b`.
The commit modifies a single file: `src/main/java/org/apache/commons/math3/random/EmpiricalDistribution.java` (**file A**)

We measure the coverage of the following three bug-revealing test cases of `Math-12b` on the buggy snapshot of `Math-12b` (`67fc870`).

- `org.apache.commons.math3.distribution.GammaDistributionTest::testDistributionClone`
- `org.apache.commons.math3.distribution.LogNormalDistributionTest::testDistributionClone`
- `org.apache.commons.math3.distribution.NormalDistributionTest::testDistributionClone`

(Tip) You can measure the coverage in the docker container:
```bash
cd ~/workspace
REL=false sh setup_project.sh Math 12
cd /tmp/Math-12b/coverage_xmls/failings/
grep -ri "EmpiricalDistribution" ./ # nothing found
```

File A exists in the buggy snapshot but not covered by the failing test cases. Since the file is not the cause of the failures, the commit `c1de4ed` that only modified the file cannot be a BIC.