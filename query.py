import time
import elasticsearch
import csv
import sys
import os


# Connect to Elasticsearch
es = elasticsearch.Elasticsearch(
    "https://elastic.osg.chtc.io/q",
    http_auth=("*****", "************")
)

# Get ClusterId from user input
if len(sys.argv) != 2:
    print("Usage: python script.py <ClusterId>")
    sys.exit(1)

try:
    cluster_id = int(sys.argv[1])
except ValueError:
    print("ClusterId must be an integer.")
    sys.exit(1)

# Define query
query = {
    "query": {
        "bool": {
            "should": [
                {"match": {"Owner": "yren86"}}
            ]
        }
    }
}

# Initial scroll
response = es.search(
    index="adstash-ospool-job-history-*",
    body=query,
    scroll='5m'
)

scroll_id = response['_scroll_id']
hits = response['hits']['hits']

MAX_RESULTS = 1000000
all_hits = []
fieldnames = set()

# Scroll loop
while hits and len(all_hits) < MAX_RESULTS:
    remaining = MAX_RESULTS - len(all_hits)
    to_add = hits[:remaining]

    all_hits.extend(to_add)
    for hit in to_add:
        fieldnames.update(hit['_source'].keys())

    if len(all_hits) >= MAX_RESULTS:
        break

    response = es.scroll(scroll_id=scroll_id, scroll='5m')
    scroll_id = response['_scroll_id']
    hits = response['hits']['hits']


output_dir = os.path.join(os.getcwd(), "cluster_data")
os.makedirs(output_dir, exist_ok=True)

print(output_dir)

# Write to CSV
csv_filename = os.path.join(output_dir, f"cluster_{cluster_id}_jobs.csv")
print(csv_filename)

with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=sorted(fieldnames))
    writer.writeheader()
    for hit in all_hits:
        writer.writerow(hit['_source'])

print(f"Dumped {len(all_hits)} jobs for ClusterId {cluster_id} to {csv_filename}")

# Cleanup
es.clear_scroll(scroll_id=scroll_id)
