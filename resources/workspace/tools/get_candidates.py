import argparse
import pandas as pd

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('pkl', type=str)
  parser.add_argument('output', type=str)
  parser.add_argument('--depth', '-d', type=int, default=None)
  args = parser.parse_args()

  dyn_df = pd.read_pickle(args.pkl)
  if args.depth is not None:
    dyn_df = dyn_df[dyn_df.rev_index < args.depth]
  candidates = dyn_df[["commit_hash", "from_head"]].sort_values(by="from_head").drop_duplicates().commit_hash.values
  with open(args.output, 'w') as f:
    f.write("\n".join(candidates))
