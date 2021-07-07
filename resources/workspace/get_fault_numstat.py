import os
import sys
import re
import json

iregex = re.compile(' (\d+) insertion')
dregex = re.compile(' (\d+) deletion')
root_dir = "/root/defects4j/framework/projects/"
active = "active-bugs.csv"

results = {}
try:
  for name in os.listdir(root_dir):
    path = os.path.join(root_dir, name)
    if os.path.isdir(path):
      bug_file = os.path.join(path, active)
      if not os.path.exists(bug_file):
        continue
      pid = name
      with open(bug_file, 'r') as f:
        f.readline()
        bugs = [l.split(',')[0] for l in f]
      for bid in bugs:
        print(pid, bid)
        command = f"sh get_fault_numstat.sh {pid} {bid}"
        with os.popen(command) as pipe:
          stat = pipe.readlines()[-1]
        print(stat)
        im = iregex.search(stat)
        dm = dregex.search(stat)

        results[(pid, bid)] = {
          'insertions': int(im.group(1)) if im else 0,
          'deletions': int(dm.group(1)) if dm else 0
        }
finally:
  with open("./resources/fault_numstat.csv", 'w') as f:
    f.write("pid,vid,insertions,deletions\n")
    for key in sorted(results):
      pid, bid = key
      f.write(f"{pid},{bid},{results[key]['insertions']},{results[key]['deletions']}\n")
