PROJECT=$1
BEGIN=$2
END=$3
for i in $(seq $BEGIN $END); do
  REL=false sh setup_project.sh $PROJECT $i
  if [ $? -eq 0 ]; then
    python3.6 search_BIC.py /tmp/${PROJECT}-${i}b/ -m -v
  fi
  rm -rf /tmp/${PROJECT}-${i}b/
done
