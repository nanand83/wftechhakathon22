#!/usr/bin/bash

echo "Starting Company data publisher"
nohup python3 publisher.py 2>&1> company_data_publisher.log &

echo "Starting Cage, DnB, Website suscribers"
nohup python3 cage_subscriber.py 2>&1> cage_subscriber.log &
nohup python3 dnb_subscriber.py 2>&1> dnb_subscriber.log &
#nohup python3 website_subscriber.py 2>&1> cage_subscriber.log &

