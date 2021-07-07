import os

COMMIT_LOG_CMD = 'git log -M -C -L {0}:{1} | grep -E "^commit [0-9a-z]*"'

def get_commit_log(project_root, path_to_source, line_range):
  commit_log_cmd = COMMIT_LOG_CMD.format(line_range, path_to_source)
  with os.popen(f"cd {project_root}; {commit_log_cmd}") as f:
    commits = [l.strip().split()[1] for l in f]
  return commits
