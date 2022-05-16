from google.cloud import pubsub_v1
import pandas as pd
import json


project_id = "theinclusiveteam"
topic_ids = ['cage-report-topic', 'dnb-topic', 'website-topic']

publisher = pubsub_v1.PublisherClient()
# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_id}`
topic_paths = [publisher.topic_path(project_id, x) for x in topic_ids]


df = pd.read_excel('data/Original_Data.xlsx')
df['dunsNum'] = df['dunsNum'].apply(str)

# Data must be a bytestring
# data = data_str.encode("utf-8")
# When you publish a message, the client returns a future.
for idx, row in df[0:10].iterrows():
    for t in topic_paths:
        future = publisher.publish(t, row.to_json().encode('utf-8'))
        print(future.result())

print(f"Published messages to {topic_paths}.")
