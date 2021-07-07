# Getting Started
```
sh initialize.sh
```

# [DBIC] Reduce BIC Search Space using Dynamic Analysis
```
sh search_BIC.sh {pid} {start_vid} {end_vid}
# sh search_BIC.sh Lang 1 65
# this will produce log files in [./logs/search_BIC/]
```

# [SZZ] Run SZZ using Issue List
```
python3.6 run_szz.py {path_to_issue_list_dir}
# python3.6 run_szz.py ./results/issue_list/Lang/
```

# Analyze DBIC and SZZ results (with Ming GT)
```
python log_analyzer.py -d ./logs/search_BIC/
```
