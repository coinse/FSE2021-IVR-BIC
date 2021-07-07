PID=$1
VID=$2
BIC=$3
defects4j checkout -p ${PID} -v ${VID}b -w /tmp/${PID}-${VID}b-check
cd /tmp/${PID}-${VID}b-check
defects4j export -p classes.relevant -o classes.relevant
defects4j export -p tests.trigger -o tests.trigger.expected
defects4j export -p dir.src.classes -o dir.src.classes
defects4j test
mv failing_tests failing_tests.original
git format-patch ${BIC} --stdout > d4j.patch
git checkout ${BIC}
git apply d4j.patch
git checkout -- $(cat dir.src.classes)
#cat tests.trigger.expected
