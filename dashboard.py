import htcondor
import classad
import sys
import math

"""
This program provides an ASCII dashboard for the status of jobs in a cluster
"""

# get data from the schedd
def fetch_counts(clusterId, job_states):
    schedd = htcondor.Schedd()
    counts = { state: 0 for state in job_states }
    # history (finished jobs)
    for ad in schedd.history(
            constraint = f"ClusterId == {clusterId}",
            projection = ["JobStatus"],
            match = -1
        ):
        counts[job_states[ad.eval("JobStatus")]] += 1
    # queue (running / pending jobs)
    for ad in schedd.query(
            constraint = f"ClusterId == {clusterId}",
            projection = ["JobStatus"],
            limit = -1
        ):
        counts[job_states[ad.eval("JobStatus")-1]] += 1
    return counts

#print the dashboard
def draw_bars(counts, job_states, bar_width=50):
    # compute column widths
    max_label_len = max(len(s) for s in job_states)
    max_count     = max(counts.values()) or 1
    count_width   = len(str(max_count))
    per_width     = len("100.0%")
    total_count   = sum(counts.values())

    # header
    header = (
        f"{'Status'.rjust(max_label_len)} | "
        f"{'Bar'.ljust(bar_width)} | "
        f"{'Count'.rjust(count_width)} | "
        f"{'%'.rjust(per_width)}"
    )
    print(header)
    print("-" * len(header))

    # rows
    for state in job_states:
        cnt    = counts[state]
        length = math.ceil( int(cnt / total_count * bar_width ) )
        bar    = "█" * length
        per    = cnt * 100 / total_count

        state_str = state.rjust(max_label_len)
        bar_str   = bar.ljust(bar_width)
        cnt_str   = str(cnt).rjust(count_width)
        per_str   = f"{per:5.1f}%".rjust(per_width)

        print(f"{state_str} | {bar_str} | {cnt_str} | {per_str}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python dashboard_once.py <ClusterId>")
        sys.exit(1)

    clusterId  = sys.argv[1]
    job_states = [
        "Idle", "Running", "Removing", "Completed",
        "Held", "Transferring Output", "Suspended"
    ]

    counts = fetch_counts(clusterId, job_states)
    print(f"\nCluster {clusterId} Status Dashboard\n")
    draw_bars(counts, job_states)

