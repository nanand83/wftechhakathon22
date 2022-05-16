from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from extract_cage_company_profile import extract_company_profile_single
import json

project_id = "theinclusiveteam"
subscription_id = "cage-report-push"
results_topic = "company-results"
# Number of seconds the subscriber should listen for messages
timeout = 20.0

subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()
# `projects/{project_id}/subscriptions/{subscription_id}`

subscription_path = subscriber.subscription_path(project_id, subscription_id)
result_topic_path = publisher.topic_path(project_id, results_topic)

def publish_cage_results(results):
    # `projects/{project_id}/topics/{topic_id}`
    if not results:
        res_map = { 'connector': 'cage', 'results': None }
    else:
        res_map = { 'connector': 'cage', 'results': results.__dict__ }

    future = publisher.publish(result_topic_path, json.dumps(res_map).encode('utf-8'))
    print(future.result())
    print(f"Published messages to {result_topic_path}.")


def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    #print(f"Received {message}.")
    incoming_message = json.loads(message.data.decode('utf-8'))
    #print ("Cage Message recd")
    company_profile = extract_company_profile_single(str(incoming_message['dunsNum']))
    #print ("COmpany Profile is : ", str(company_profile))
    publish_cage_results(company_profile)
    message.ack()
    print ("Cage connector processed for ", str(incoming_message['dunsNum']))

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

with subscriber:
    try:
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()  
        streaming_pull_future.result()  
