import argparse
import os
import logging
import numpy as np
import pandas as pd
from utils.defects4j import D4JBug
from utils.javaparser import MethodRanges
from utils.git import get_commit_log

LOG_DIR = "/root/workspace/logs/search_BIC/"
if not os.path.exists(LOG_DIR):
  os.mkdir(LOG_DIR)

def search_BIC(bug, is_method_level=True):
  coverage_matrix = bug.get_coverage_matrix(test_types=['failings'])
  logging.info(f"Loaded {coverage_matrix}")
  logging.info(f"The number of total commits: {len(bug.commits)}")

  ranges_cache = {}
  visited = set()
  BIC_candidates = set()
  df = pd.DataFrame(columns=['src_path', 'method_name', 'line_range', 'rev_index', 'commit_hash', 'from_head'])
  for i, component in enumerate(coverage_matrix.components):
    assert coverage_matrix.is_covered_by_tests(component, only_failing=True)
    class_file, method_name, method_signature, lineno = component

    method_key = (class_file, method_name, method_signature)

    if is_method_level and method_key in visited:
      continue

    rel_src_path = os.path.join(bug.src_dir, class_file)
    abs_src_path = os.path.join(bug.project_root, rel_src_path)

    if is_method_level:
      if rel_src_path not in ranges_cache:
        ranges_cache[rel_src_path] = MethodRanges(abs_src_path)
      method_ranges = ranges_cache[rel_src_path]
      method_range = method_ranges.get_range(lineno)

    if is_method_level and method_range is not None:
      logging.debug(f"[line range] {class_file} {method_name} {method_range}")
      line_range = f"{method_range.begin_line},{method_range.end_line}"
      visited.add(method_key)
    else:
      logging.debug(f"[single line]   {class_file} {method_name} {lineno}")
      line_range = f"{lineno},{lineno}"

    commits_involved = get_commit_log(bug.project_root, rel_src_path, line_range)
    for i, commit_hash in enumerate(commits_involved):
      from_head = bug.commits.index(commit_hash)
      logging.debug(f"              - depth {i}, hash {commit_hash[:7]}, HEAD~{from_head}")
      BIC_candidates.add(commit_hash)
      df = df.append({'src_path': rel_src_path, 'method_name': method_name,
        'line_range': line_range, 'rev_index': i, 'commit_hash': commit_hash,
        'from_head': from_head}, ignore_index=True)

  logging.info(f"The number of BIC candidates: {len(BIC_candidates)}")
  return df

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('project_root', type=str)
  parser.add_argument('--method-level', '-m', action='store_true')
  parser.add_argument('--verbose', '-v', action='store_true')
  args = parser.parse_args()

  if not os.path.exists(args.project_root):
    exit(1)

  bug = D4JBug(args.project_root)

  # setup logging configuration
  logging.basicConfig(
    level=logging.DEBUG if args.verbose else logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    handlers=[
      logging.FileHandler(
        os.path.join(LOG_DIR, f"{bug.pid}-{bug.vid}b.log"), mode='w'),
      logging.StreamHandler()
  ])

  logging.info(f"Search BICs for {args.project_root}")
  df = search_BIC(bug, args.method_level)
  df.to_pickle(os.path.join(LOG_DIR, f"{bug.pid}-{bug.vid}b.pkl"))
