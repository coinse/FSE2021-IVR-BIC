# BIC and Dynamic Analysis

This repository implements a technique to reduce the search space of bug inducing commits (BICs) accompanying the paper:

*__Reducing the Search Space of Bug Inducing Commits Using Failure Coverage__* (FSE'21 IVR Track)

# Quick Navigation
- Section 3: [Detailed reason for subject exclusion](./resources/workspace/setup.error)
- Section 3.2.1: [Logs produced during the BIC search space reduction process](./resources/workspace/logs/search_BIC/)
- Section 3.2.2: [Manual Inspection results](./soundness_validation/README.md)
- Section 3.2.3: [SZZUnleashed results](./resources/workspace/szz_reults)
  - The files `./resources/workspace/issue_list/*.error` contain the reason why it is unable to collect the SZZ input data for some subjects.
- [All-in-one results](./resources/workspace/bic_expr.pkl) (One can reproduce the figures in the paper using [the analysis script](./bic_expr_analysis.ipynb).)

# A. A Guide to Replication
## A-1. Prerequisites
- Docker

## A-2. (On the host machine) Creating a Docker image & starting a container
```bash
docker build -t bic . # this will take a while
docker run -dt --name bic -v $(pwd)/resources/workspace:/root/workspace bic:latest
docker exec -it bic bash
```
Then, the directory `$(pwd)/resources/workspace` on the host machine will be mounted into a container (`/root/workspace/`).

## A-3. (On the container) Application on Defects4J

The result files are already provided. The following instructions just guide you through how to replicate it.

### A-3a. Initializing the environment
```bash
cd ~/workspace
sh initialize.sh
```

### A-3b. Reducing the BIC search space using failure coverage

```bash
cd ~/workspace
sh search_BIC.sh [pid] [start_vid] [end_vid]
# sh search_BIC.sh Lang 1 65
```

**See the log for each fault in `~/workspace/logs/search_BIC/{pid}-{vid}b.log`.** If there is some error while performing the reduction, the error message will be saved to `~/workspace/setup.error`.

### A-3c. Running SZZUnleashed using collected issue lists

- We have collected issue lists for Defects4J faults,
that are the input for [SZZUnleashed](https://github.com/wogscpar/SZZUnleashed), using `~/workspace/issue_list/create_issue_list.py`.
- The issue information for each fault, `{pid}-{vid}b`, is saved in the file `~/workspace/issue_list/{pid}/{pid}-{vid}b.json`.
  
  For example, the issue data for `Time-10b` is as follows:
  ```json
  {
      "Time-10b": {
          "creationdate": "2013-05-07 14:19:36 +0000",
          "resolutiondate": "2013-06-16 10:28:45 +0000",
          "hash": "3a413d7844c22dc6ddd50bf5d0d55ff3589e47ac",
          "commitdate": "2013-06-16 11:28:26 +0100"
      }
  }
  ```
    The `hash` corresponds to the fixed version commit provided by [Defects4J](https://github.com/rjust/defects4j). Find `revision.id.fixed` in their README to see more details.
- The file `~/workspace/issue_list/{pid}.error` contains the detailed reasons for the bugs whose data could not be properly collected.
- Using the issue list file, you can run SZZUnleashed with the following command:
    ```bash
    python3.6 run_szz.sh issue_list/{pid_1} ... issue_list/{pid_n}
    # python3.6 run_szz.sh issue_list/Lang issue_list/Time
    ```
    **The szz output will be collected in `~/workspace/szz_results`.**

### A-3d. Generating a file containing all experiment results in the log directory
```bash
python3.6 log_analyzer.py -d ./logs/search_BIC/ -o ~/workspace/bic_expr.pkl
```

`~/workspace/bic_expr.pkl` will contain the overall experimental results in the form of a Pandas Dataframe.

# B. Data analysis

## B-1. Prerequisites
- Python 3.9.1
- Installing dependencies:
    ```bash
    python -m pip install -r requirements.txt
    ```

## B-2. Plot drawing
On a host machine, use [./bic_expr_analysis.ipynb](./bic_expr_analysis.ipynb) to analyze the
experiment result file (`.pkl`) and draw plots.

Make sure that the result file (`./resources/workspace/bic_expr.pkl`) exists on the host machine.
Since we already provide the result file, you can just use the file without replicating the experiment (described in A).


## B-3. Manual Inspection (Section 3.2.3 in the paper)

Goto [Manual Inspection Results](./soundness_validation/README.md);


<img src="https://cdn140.picsart.com/264239141021202.jpg?type=webp&to=min&r=640)" width="400px">
