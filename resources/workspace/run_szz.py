import argparse
import os
import shutil
import time

PATH_TO_JAR_FILE = "/root/SZZUnleashed/szz/build/libs/szz_find_bug_introducers-0.1.jar"
RESULT_DIR = "./szz_results"
SZZ_OUTPUT_DIR = "./results"

# Usage: python3.6 run_szz.py ./issue_list/Lang
if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('dirs', type=str, nargs='+')
  args = parser.parse_args()

  if not os.path.exists(RESULT_DIR):
    os.mkdir(RESULT_DIR)

  for issue_list_dir in args.dirs:
    for filename in os.listdir(issue_list_dir):
      bid = filename[:-5]
      pid, vid = tuple(bid.split('-'))
      path_to_issue_list = os.path.join(issue_list_dir, filename)
      path_to_repo = f"/tmp/{bid}"
      if not os.path.exists(path_to_repo):
        os.system(f"defects4j checkout -p {pid} -v {vid} -w {path_to_repo}")
      cmd = f"java -jar {PATH_TO_JAR_FILE} -i {path_to_issue_list} -r {path_to_repo}"
      os.system(cmd)

      if os.path.exists(SZZ_OUTPUT_DIR):
        if os.path.exists(os.path.join(RESULT_DIR, bid)):
          shutil.rmtree(os.path.join(RESULT_DIR, bid))
        shutil.move(SZZ_OUTPUT_DIR, os.path.join(RESULT_DIR, bid))

      if os.path.exists('./issues'):
        shutil.move('./issues', os.path.join(RESULT_DIR, bid, 'issues'))
      time.sleep(3)
