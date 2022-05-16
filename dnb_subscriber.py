from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from extract_dnb_company_profile import extract_company_profile_row
import json, time, traceback

project_id = "theinclusiveteam"
subscription_id = "dnb-push"
results_topic = "company-results"
# Number of seconds the subscriber should listen for messages
timeout = 20.0

subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()
# `projects/{project_id}/subscriptions/{subscription_id}`

subscriber_path = subscriber.subscription_path(project_id, subscription_id)
result_topic_path = publisher.topic_path(project_id, results_topic)

def publish_dnb_results(results):
    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_id}`
    if not results:
        res_map = { 'connector': 'dnb', 'results': None }
    else:
        res_map = { 'connector': 'dnb', 'results': results.__dict__ }

    future = publisher.publish(result_topic_path, json.dumps(res_map).encode('utf-8'))
    print(future.result())
    print(f"Published messages to {result_topic_path}.")

imeout = 20.0


def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    #print(f"Received {message}.")
    incoming_message = json.loads(message.data.decode('utf-8'))
    #print ("DNB Message recd")
    company_profile = extract_company_profile_row(incoming_message)
    publish_dnb_results(company_profile)
    message.ack()

# Single threaded to avoid overhitting DnB Url
print("Listening for messages on ", subscriber_path)
while True:
    try:
        response = subscriber.pull(subscription=subscriber_path, max_messages=1)
        if len(response.received_messages) > 0:
            this_message = response.received_messages[0]
            #subscriber.modify_ack_deadline(subscription=subscriber_path, ack_ids=[this_message.ack_id], ack_deadline_seconds=30)      ##30s Ack Deadline
            incoming_message = json.loads(this_message.message.data.decode('utf-8'))
            #print ("DNB Message recd")
            company_profile = extract_company_profile_row(incoming_message)
            publish_dnb_results(company_profile)
            subscriber.acknowledge(subscription=subscriber_path, ack_ids=[this_message.ack_id])
            print ("DNB connector processed")
    except Exception as ex:
        traceback.print_exc()
        print ("Error occurred while consuming dnb topic: ", ex)

    time.sleep(2)


#subscriber = pubsub_v1.SubscriberClient()
# `projects/{project_id}/subscriptions/{subscription_id}`
#subscription_path = subscriber.subscription_path(project_id, subscription_id)
#streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
#print(f"Listening for messages on {subscription_path}..\n")

#with subscriber:
#    try:
#        streaming_pull_future.result(timeout=timeout)
#    except TimeoutError:
#        streaming_pull_future.cancel()  
#        streaming_pull_future.result()  
