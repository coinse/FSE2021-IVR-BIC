# c95eb0b

[`c95eb0b`](../commits/c95eb0b.diff) was identified as the BIC of `Math-74b`.

The change introduced by the commit is as follows:

```diff
--- a/src/java/org/apache/commons/math/ode/nonstiff/AdaptiveStepsizeIntegrator.java
+++ b/src/java/org/apache/commons/math/ode/nonstiff/AdaptiveStepsizeIntegrator.java
@@ -108,8 +108,8 @@ public abstract class AdaptiveStepsizeIntegrator
 
     this.scalAbsoluteTolerance = 0;
     this.scalRelativeTolerance = 0;
-    this.vecAbsoluteTolerance  = vecAbsoluteTolerance;
-    this.vecRelativeTolerance  = vecRelativeTolerance;
+    this.vecAbsoluteTolerance  = vecAbsoluteTolerance.clone();
+    this.vecRelativeTolerance  = vecRelativeTolerance.clone();
```

It modifies two lines in the `AdaptiveStepsizeIntegrator` class.

However, if we run the bug-revealing test case 
`org.apache.commons.math.ode.nonstiff.AdamsMoultonIntegratorTest:polynomial` on the buggy version, `034b4d6`,
then the test fails but does not execute the newly introduced lines.
The coverage results of the file `src/main/java/org/apache/commons/math/ode/nonstiff/AdaptiveStepsizeIntegrator.java` (moved from `src/java/` to `src/main/java`) are as follows:

```xml
<method name="&lt;init&gt;" signature="(Ljava/lang/String;DD[D[D)V" line-rate="0.0" branch-rate="1.0">
        <lines>
                <line number="123" hits="0" branch="false"/>
                <line number="125" hits="0" branch="false"/>
                <line number="126" hits="0" branch="false"/>
                <line number="127" hits="0" branch="false"/>
                <line number="129" hits="0" branch="false"/> 
                <line number="130" hits="0" branch="false"/> 
                <line number="131" hits="0" branch="false"/> (this.vecAbsoluteTolerance  = vecAbsoluteTolerance.clone();)
                <line number="132" hits="0" branch="false"/> (this.vecRelativeTolerance  = vecRelativeTolerance.clone();)
                <line number="134" hits="0" branch="false"/>
                <line number="136" hits="0" branch="false"/>
        </lines>
</method>
```

It suggests that the change contained in commit `c95eb0b` is not the cause of the failure.
