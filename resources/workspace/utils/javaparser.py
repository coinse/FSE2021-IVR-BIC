import os

METHOD_RANGE_ANALYZER = "/root/workspace/java_analyzer/target/java-analyzer-1.0-SNAPSHOT-shaded.jar"

class MethodRange:
  def __init__(self, begin_line, end_line):
    self.begin_line = begin_line
    self.end_line = end_line

  def __str__(self):
    return f"{self.begin_line}:{self.end_line}"

class MethodRanges:
  def __init__(self, path_to_source, separator='|'):
    self.ranges = []
    source_root = os.path.dirname(path_to_source)
    file_name = os.path.basename(path_to_source)

    max_lineno = -1
    with os.popen(f"java -jar {METHOD_RANGE_ANALYZER} {source_root} {file_name}") as f:
      for l in f:
        if l.startswith("[method]") or l.startswith("[constructor]") or l.startswith("[field]"):
          signature, begin_line, end_line = tuple(l.strip().split(separator)[1:])
          begin_line, end_line = int(begin_line), int(end_line)
          self.ranges.append(MethodRange(begin_line, end_line))
          if end_line > max_lineno:
            max_lineno = end_line


    self.lookup_helper = [None] * (max_lineno + 1)
    for method_index, method_range in enumerate(self.ranges):
      for lineno in range(method_range.begin_line, method_range.end_line + 1):
        self.lookup_helper[lineno] = method_index

  def get_range(self, lineno):
    if lineno < len(self.lookup_helper):
      method_index = self.lookup_helper[lineno]
      if method_index is not None:
        return self.ranges[method_index]
    return None
