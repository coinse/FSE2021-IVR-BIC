import argparse
import json
import os
import csv
import re
import requests
import time
from urllib.parse import urlparse

# example
"""
{
  "Lang-1b": {
    "creationdate": "2011-08-23 12:50:00 +0000",
    "resolutiondate": "2013-10-15 02:33:00 +0000",
    "hash": "687b2e62b7c6e81cd9d5c872b7fa9cc8fd3f1509",
    "commitdate": "2013-07-26 01:03:52 +0000"
  }
}
"""

class NoDateTimeException(Exception):
  pass

class NotSupportedReportUrl(Exception):
  pass

def get_meta_data(pid):
  path_to_metadata = f"/root/workspace/resources/{pid}-meta.csv"
  if not os.path.exists(path_to_metadata):
    command = f'defects4j query -p {pid} -q "revision.id.fixed,revision.date.fixed,report.id,report.url" -o {path_to_metadata} -A'
    os.system(command)
  assert os.path.exists(path_to_metadata)

  metadata = {}
  with open(path_to_metadata, 'r') as f:
    for l in f:
      bid, revision_id_fixed, revision_date_fixed, report_id, report_url = tuple(l.strip().split(','))
      metadata[bid] = {
        'revision_id_fixed': revision_id_fixed,
        'revision_date_fixed': revision_date_fixed,
        'report_id': report_id,
        'report_url': report_url
      }
  return metadata

def get_json_from_url(url):
  res = requests.get(url, allow_redirects=True)
  res.raise_for_status()
  return res.json()

def ISO8601_to_YMDHMSZ(dt):
  if dt is None:
    raise NoDateTimeException()
  new_dt = re.sub("\.\d+", " ", dt)
  new_dt = new_dt.replace("T", " ")
  new_dt = new_dt.replace("Z", " +0000")
  new_dt = new_dt.strip()
  if "+" not in new_dt:
    new_dt += " +0000" # default: UTC
  return new_dt

def get_date_from_apache_issue(meta):
  issue_url = f'https://issues.apache.org/jira/rest/api/latest/issue/{meta["report_id"]}'
  issue_data = get_json_from_url(issue_url)
  creationdate = ISO8601_to_YMDHMSZ(issue_data['fields']['created'])
  resolutiondate = ISO8601_to_YMDHMSZ(issue_data['fields']['resolutiondate'])
  return creationdate, resolutiondate

def get_date_from_google_code(meta):
  issue_data = get_json_from_url(meta['report_url'])
  raise NoDateTimeException(meta['report_url'])

def get_date_from_github_issue(meta):
  # url:  https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}
  g = re.match("https://github.com/([^\/]+)/([^\/]+)/issues/(\d+)", meta['report_url'])
  owner, repo, issue_number = g.group(1), g.group(2), g.group(3)
  issue_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
  time.sleep(10)
  issue_data = get_json_from_url(issue_url)
  creationdate = ISO8601_to_YMDHMSZ(issue_data['created_at'])
  resolutiondate = ISO8601_to_YMDHMSZ(issue_data['closed_at'])
  return creationdate, resolutiondate

def get_date_from_github_pull_request(meta):
  # url:  https://api.github.com/repos/{owner}/{repo}/pulls/{issue_number}
  g = re.match("https://github.com/([^\/]+)/([^\/]+)/pull/(\d+)", meta['report_url'])
  owner, repo, issue_number = g.group(1), g.group(2), g.group(3)
  issue_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{issue_number}"
  time.sleep(10)
  issue_data = get_json_from_url(issue_url)
  creationdate = ISO8601_to_YMDHMSZ(issue_data['created_at'])
  resolutiondate = ISO8601_to_YMDHMSZ(issue_data['closed_at'])
  return creationdate, resolutiondate

def get_date_from_sourceforge(meta):
  # url: https://sourceforge.net/rest/p/{repo}/bugs/{issue_number}
  url_path = urlparse(meta['report_url']).path
  issue_url = "https://sourceforge.net/rest/" + url_path
  issue_data = get_json_from_url(issue_url)
  creationdate = ISO8601_to_YMDHMSZ(issue_data['ticket']['created_date'])
  resolutiondate = ISO8601_to_YMDHMSZ(issue_data['ticket']['mod_date']) # the last modified date is implicitly regarded as a resolution date
  return creationdate, resolutiondate

def create(pid, metadata, prev_issue_list=None):
  issue_list = {}
  errors = {}
  for bid in metadata:
    key = f"{pid}-{bid}b"
    print(key)
    if prev_issue_list is not None and key in prev_issue_list:
      # continue if it exists
      issue_list[key] = prev_issue_list[key]
      continue
    meta = metadata[bid]
    report_url = meta['report_url']
    try:
      print(f"Loading data from {report_url}")
      if report_url.startswith("https://issues.apache.org/jira"):
        # Apache Commons Issue (Jira)
        creationdate, resolutiondate = get_date_from_apache_issue(meta)
      elif report_url.startswith("https://storage.googleapis.com/google-code-archive/v2/code.google.com/"):
        # Google API
        creationdate, resolutiondate = get_date_from_google_code(meta)
      elif re.match("https://github.com/([^\/]+)/([^\/]+)/issues/(\d+)", report_url):
        # Github Issue
        creationdate, resolutiondate = get_date_from_github_issue(meta)
      elif re.match("https://github.com/([^\/]+)/([^\/]+)/pull/(\d+)", report_url):
        # Github Pull Request
        creationdate, resolutiondate = get_date_from_github_pull_request(meta)
      elif report_url.startswith("https://sourceforge.net/"):
        creationdate, resolutiondate = get_date_from_sourceforge(meta)
      else:
        raise NotSupportedReportUrl(report_url)
    except (NoDateTimeException, NotSupportedReportUrl, requests.exceptions.HTTPError) as e:
      # Log Errors
      print("Error", e.__class__.__name__, e)
      errors[key] = {
        'error_class': e.__class__.__name__,
        'error_message': str(e)
      }
      continue

    issue_list[key] = {
      "creationdate": creationdate,
      "resolutiondate": resolutiondate,
      "hash": meta['revision_id_fixed'],
      "commitdate": meta['revision_date_fixed']
    }
  return issue_list, errors

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('pid', type=str)
  parser.add_argument('--output', '-o', type=str, default=None)
  parser.add_argument('--makedir', '-d', action='store_true')
  args = parser.parse_args()

  metadata = get_meta_data(args.pid)

  if args.output is None:
    path_to_output = f"{args.pid}.json"
  path_to_error = os.path.splitext(path_to_output)[0] + '.error'

  # Load existing issue lists
  if os.path.exists(path_to_output):
    with open(path_to_output, 'r') as json_file:
      prev_issue_list = json.load(json_file)
  else:
    prev_issue_list = None

  issue_list, errors = create(args.pid, metadata, prev_issue_list)

  with open(path_to_output, 'w', encoding='utf-8') as f:
    json.dump(issue_list, f, indent=4)
  with open(path_to_error, 'w', encoding='utf-8') as f:
    json.dump(errors, f, indent=4)

  if args.makedir:
    savedir = args.pid
    if not os.path.exists(savedir):
      os.mkdir(savedir)
    for key in issue_list:
      with open(os.path.join(savedir, key + ".json"), 'w', encoding='utf-8') as f:
        json.dump({key: issue_list[key]}, f, indent=4)
