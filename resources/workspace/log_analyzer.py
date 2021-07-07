import os
import logging
import argparse
import json
import numpy as np
import pandas as pd

FIND_TOTAL_COMMIT = "grep 'INFO' {} | grep 'The number of total commits'"
LOG = "{}-{}b.log"
PKL = "{}-{}b.pkl"
SZZ_RESULT = "/root/workspace/szz_results/{}-{}b/fix_and_introducers_pairs.json"

def get_final_word_of_output(command):
  return os.popen(command).read().strip().split()[-1]

subjects = {
  'Cli': 40,
  'Closure': 176,
  'Codec': 18,
  'Collections': 28,
  'Compress': 47,
  'Csv': 16,
  'Gson': 18,
  'JacksonCore': 26,
  'JacksonDatabind': 112,
  'JacksonXml': 6,
  'Jsoup': 93,
  'JxPath': 22,
  'Lang': 65,
  'Math': 106,
  'Mockito': 38,
  'Time': 27, # Time 21-27: no src dir when reverting back to the buggy version
}

bic_ground_truth = {}
with open('/root/workspace/resources/wen19-defects4j-bug-inducing-commits.csv', 'r') as f:
  f.readline()
  for l in f:
    pid, vid, bic = l.strip().split(',')
    bic_ground_truth[(pid, vid)] = bic

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--dir', '-d', type=str, default="./logs/search_BIC/")
  parser.add_argument('--verbose', '-v', action='store_true')
  parser.add_argument('--output', '-o', type=str, default="./output.pkl")
  args = parser.parse_args()

  logging.basicConfig(
    level=logging.DEBUG if args.verbose else logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    handlers=[
      logging.StreamHandler(),
      logging.FileHandler('log_analyzer.log', mode='w')
  ])

  df = pd.DataFrame()
  reduction = {}
  for pid in subjects:
    reduction[pid] = []
    for i in range(1, subjects[pid] + 1):
      vid = str(i)

      df_row = {'pid': pid, 'vid': vid}

      log_file = os.path.join(args.dir, LOG.format(pid, vid))
      pkl_file = os.path.join(args.dir, PKL.format(pid, vid))

      if not os.path.exists(log_file):
        logging.debug(f"{log_file} does not exist. Skipped.")
        continue
      if not os.path.exists(pkl_file):
        logging.debug(f"{pkl_file} does not exist. Skipped.")
        continue

      num_total_commits = int(get_final_word_of_output(FIND_TOTAL_COMMIT.format(log_file)))
      dyn_df = pd.read_pickle(pkl_file)
      dyn_bic = dyn_df['commit_hash'].unique().tolist()
      reduction_ratio = len(dyn_bic)/num_total_commits
      error = reduction_ratio == 0.0
      reduction[pid].append(reduction_ratio)
      logging.info(f"{pid}-{vid}b:")
      logging.info(f"- <DBIC> {len(dyn_bic)}/{num_total_commits}={round(reduction_ratio*100, 2)}% {'(error)' if error else ''}")

      df_row["num_total_commits"] = num_total_commits
      df_row["num_dyn"] = len(dyn_bic)
      df_row["dyn"] = dyn_bic

      df_row["has_wen_bic"] = (pid, vid) in bic_ground_truth

      # Load MING ground truth
      if (pid, vid) in bic_ground_truth:
        wen19_bic = bic_ground_truth[(pid, vid)]
        logging.info(f"- <WEN19> {wen19_bic}")
        logging.info(f"- WEN19 in DBIC({len(dyn_bic)}): {wen19_bic in dyn_bic} {'' if wen19_bic in dyn_bic else '!'}")
        df_row["is_wen_in_dyn"] = wen19_bic in dyn_bic
        df_row["wen"] = wen19_bic
      else:
        wen19_bic = None

      # Load SZZ results
      szz_file = SZZ_RESULT.format(pid, vid)
      df_row["has_szz_results"] = os.path.exists(szz_file)
      if os.path.exists(szz_file):
        with open(szz_file, 'r') as f:
          szz_bic = list(set([pair[1] for pair in json.load(f)]))
        df_row["num_szz"] = len(szz_bic)
        df_row["szz"] = szz_bic
        if wen19_bic is not None:
          logging.info(f"- MING in SZZ({len(szz_bic)}): {wen19_bic in szz_bic} {'' if wen19_bic in szz_bic else '!'}")
          df_row["is_wen_in_szz"] = wen19_bic in szz_bic
        reduction_ratio = len(szz_bic)/num_total_commits
        error = reduction_ratio == 0.0
        logging.info(f"- <SZZ> {len(szz_bic)}/{num_total_commits}={round(reduction_ratio*100, 2)}% {'(error)' if error else ''}")

        # DBIC vs SZZ
        in_dyn_szz = [ commit_hash for commit_hash in szz_bic if commit_hash in dyn_bic]
        logging.info(f"- DBIC <-> SZZ: only dyn {len(dyn_bic) - len(in_dyn_szz)} | both {len(in_dyn_szz)} | only szz {len(szz_bic) - len(in_dyn_szz)}")
        df_row["num_only_dyn"] = len(dyn_bic) - len(in_dyn_szz)
        df_row["num_both"] = len(in_dyn_szz)
        df_row["num_only_szz"] = len(szz_bic) - len(in_dyn_szz)
      df = df.append(df_row, ignore_index=True)

      logging.info("=================")
    logging.info(f"Avg. Reduction Ratio of {pid} ({len(reduction[pid])} data points): {round(np.mean(reduction[pid]) * 100, 2)}%")
  total_reduction = sum(reduction.values(), [])
  logging.info(f"Avg. Reduction Ratio of All ({len(total_reduction)} data points): {round(np.mean(total_reduction) * 100, 2)}%")

  df.to_pickle(args.output)
