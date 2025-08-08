# CHTC Summer Research Facilitation Project

**Fellow**: Kashika Mahajan  
**Mentors**: Andrew Owen, Ian Ross  
**Fellowship Dates**: May 19 – August 8, 2025

________


## 📚 Background

Researchers using HTCondor often struggle to quickly understand how their computational workloads (clusters of jobs) are performing. Current interfaces expose too much raw data, making it difficult, especially for less experienced users—to diagnose issues like  jobs on hold, poor resource utilization, or unexpected failures.

This project aimed to build tools that simplify job monitoring, flag issues, and offer meaningful insights into workload behavior using accessible metrics and clear visual feedback.

________


## 📁 Repository Structure

  - hold_classifer.py # Diagnoses held jobs and groups by hold reasons
  - runtime_histogram.py # Plots job runtime distribution using ASCII histograms
  - resource_usage_summary.py # Summarizes requested vs actual CPU, memory, disk
  - cluster_status_dashboard.py # Prints status distribution of jobs in a cluster
  - README.md # This file

________


## ⚙️ Setup and Installation
1. Clone this repository:
2. Install all the packages in the requirements.txt
3. You must have access to:
  - HTCondor Python bindings
  - Elasticsearch (if querying historical job data)
  ⚠️ Note: Some tools require authentication to the CHTC Elasticsearch instance, which is currently not available to general users.

________

## 🚀 Usage Instructions

Each tool is meant to be run as a standalone Python script with a cluster ID as input.

Example command: `python dashboard.py <ClusterId>`

________


## Features and Deliverables
1. Cluster Status Dashboard
    Purpose: Quickly visualize job statuses (Idle, Running, Held, Completed)
    Features:
      - Combines data from both queue and history
      - Highlights abnormal patterns using ASCII charts
  
### Example: Cluster Status Dashboard Output
```
Cluster 123 Status Dashboard

             Status | Bar                                                | Count |      %
-----------------------------------------------------------------------------------------
               Idle | █████████████                                      |  8686 |  27.0%
            Running |                                                    |   433 |   1.3%
           Removing |                                                    |     0 |   0.0%
          Completed |                                                    |     0 |   0.0%
               Held | ███████████████████████████████████                | 23067 |  71.7%
Transferring Output |                                                    |     0 |   0.0%
          Suspended |                                                    |     0 |   0.0%

```

  
3. Cluster Runtime Histogram
    Purpose: Understand runtime variance across jobs
    Features:
      - Binned by percentiles
      - Flags jobs with runtime < 10 min
      - Can print list of affected job IDs
  
 
### Example: Cluster Runtime Histogram Output
``` 
Histogram of Job Runtimes by Percentiles:

ClusterId: 4421577

First Submitted : 2023-12-21
Last Completed  : 1 week ago

Percentile Time Range                    | Histogram             # Jobs
-----------------------------------------------------------------------
00–10%                    6s -         7s | ██████                    32
10–20%                    7s -         8s | ████████████████████     104
20–30%                    8s -     1m 45s | ████████████████          88
30–40%                1m 45s -     3m 33s | ██████████████            75
40–50%                3m 33s -    12m 14s | ██████████████            75
50–60%               12m 14s -    20m 57s | ██████████████            74
60–70%               20m 57s -     33m 8s | ██████████████            75
70–80%                33m 8s -   1h 4m 1s | ██████████████            75
80–90%              1h 4m 1s - 2h 32m 17s | ██████████████            75
90–100%          2h 32m 17s - 14h 10m 28s | ██████████████            75

Note: Bars in red represent bins with median runtime < 10 minutes.
Info: Total number of jobs in such bins: 374


```


4. Hold Classifier
    Purpose: Explain why jobs were held
    Features:
      - Clusters jobs by HoldReasonCode + HoldReasonSubCode
      - Displays percentage and example reasons
      - Includes human-readable legend of hold codes

5. Resource Utilization Report
    Purpose: Compare requested vs actual usage
    Features:
      - Summarizes CPU, memory, and disk usage
      - Adds flags for under (<15%) or over (>80%) utilization
      - Includes bar chart and percentiles


