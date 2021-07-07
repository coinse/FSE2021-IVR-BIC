project=$1
version=$2

tmpdir=/tmp/temporal

[ -d $tmpdir ] && rm -rf $tmpdir
defects4j checkout -p $project -v ${version}b -w ${tmpdir}
[ -d $tmpdir ] || exit 1

cd ${tmpdir}
git diff HEAD HEAD^ --stat -- . ':(exclude).defects4j.config'
