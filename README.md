# CHTC Summer Research Facilitation Project

**Fellow**: Kashika Mahajan  
**Mentors**: Andrew Owen, Ian Ross  
**Fellowship Dates**: May 19 – August 8, 2025

________


## 📚 Background

Researchers using HTCondor often struggle to quickly understand how their computational workloads (clusters of jobs) are performing. Current interfaces expose too much raw data, making it difficult, especially for less experienced users—to diagnose issues like stuck jobs, poor resource utilization, or unexpected failures.

This project aimed to build tools that simplify job monitoring, flag issues, and offer meaningful insights into workload behavior using accessible metrics and clear visual feedback.

________


## 📁 Repository Structure

├── hold_classifer.py # Diagnoses held jobs and groups by hold reasons
├── runtime_histogram.py # Plots job runtime distribution using ASCII histograms
├── resource_usage_summary.py # Summarizes requested vs actual CPU, memory, disk
├── cluster_status_dashboard.py # Prints status distribution of jobs in a cluster
└── README.md # This file

________


## ⚙️ Setup and Installation
1. Clone this repository:
2. You must have access to:
  - HTCondor Python bindings
  - Elasticsearch (if querying historical job data)
  ⚠️ Note: Some tools require authentication to the CHTC Elasticsearch instance, which is currently not available to general users.

________

## 🚀 Usage Instructions

Each tool is meant to be run as a standalone Python script with a cluster ID as input.

Example command: python dashboard.py <ClusterId>

________


## Features and Deliverables
1. Cluster Status Dashboard
    Purpose: Quickly visualize job statuses (Idle, Running, Held, Completed)
    Features:
      - Combines data from both queue and history
      - Highlights abnormal patterns using ASCII charts

2. Cluster Runtime Histogram
    Purpose: Understand runtime variance across jobs
    Features:
      - Binned by percentiles
      - Flags jobs with runtime < 10 min
      - Can print list of affected job IDs


3. Hold Classifier
    Purpose: Explain why jobs were held
    Features:
      - Clusters jobs by HoldReasonCode + HoldReasonSubCode
      - Displays percentage and example reasons
      - Includes human-readable legend of hold codes

4. Resource Utilization Report
    Purpose: Compare requested vs actual usage
    Features:
      - Summarizes CPU, memory, and disk usage
      - Adds flags for under (<15%) or over (>80%) utilization
      - Includes bar chart and percentiles


