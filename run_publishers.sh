#!/usr/bin/bash

echo "Starting Company data publisher"
python3 publisher.py > company_data_publisher.log 2>&1 &

echo "Starting Cage, DnB, Website suscribers"
python3 cage_subscriber.py > cage_subscriber.log 2>&1 &
python3 dnb_subscriber.py > dnb_subscriber.log 2>&1 &
#python3 website_subscriber.py > cage_subscriber.log 2>&1 &

#python3 results_aggregator.py > results_aggregator.log 2>&1 &

tail -f cage_subscriber.log dnb_subscriber.log results_aggregator.log | egrep -iv "warning|tensorflow|fork"
