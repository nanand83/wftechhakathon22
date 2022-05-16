from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
import json, time, traceback
import redis

project_id = "theinclusiveteam"
subscription_id = "company-results"
# Number of seconds the subscriber should listen for messages
timeout = 60.0

r = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscriber_path = subscriber.subscription_path(project_id, subscription_id)

known_connectors = ['dnb','cage', 'website']

def triangulate(message):
    result_source = message['connector']

    if message['results']:
        print ("Got results from [{0}] connector for Company: {1}".format(result_source, message['results']['name']))
        r.hset(message['results']['dunsNum'], result_source, json.dumps(message['results']))
        
        r_hkeys = r.hkeys(message['results']['dunsNum'])
        print (r_hkeys)
        if set(r_hkeys) == set(known_connectors):
            print ("Triangulating for ", message['results']['dunsNum'])
    
    else:
        print ("Got empty results from ", result_source)

    

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    #print(f"Received {message}.")
    incoming_message = json.loads(message.data.decode('utf-8'))
    triangulate(incoming_message)
    message.ack()


print("Listening for messages on ", subscriber_path)

while True:
    try:
        response = subscriber.pull(request={'subscription': subscriber_path, 'max_messages' : 1})
            #subscriber.modify_ack_deadline(request={         ##30s Ack Deadline
            #    'subscription':subscriber_path, 
            #    'ack_ids':[x.ack_id for x in response.received_messages], 
            #    'ack_deadline_seconds':30
            #})
        
        for this_message in response.received_messages:
            incoming_message = json.loads(this_message.message.data.decode('utf-8'))
            triangulate(incoming_message)
            #print ("Acking for Message Id: ",this_message.ack_id)
            subscriber.acknowledge(request={'subscription': subscriber_path, 'ack_ids':[this_message.ack_id]})

    except KeyboardInterrupt as ex:
        #traceback.print_exc()
        print ("Interrupted... Breaking")
        break

    except Exception as other_ex:
        traceback.print_exc()

    print ("Sleeping and retrying..")
    time.sleep(2)

print ("Done!")
