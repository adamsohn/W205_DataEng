#!/usr/bin/env python
import json
from kafka import KafkaProducer
from flask import Flask, request

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='kafka:29092')

def log_to_kafka(topic, event):
    event.update(request.headers)
    producer.send(topic, json.dumps(event).encode())

@app.route("/")
def default_response():
    event = {'event_type': 'default', 'metadata_characteristic': ''}
    log_to_kafka('events', event)
    return "This is the default response!\n"

@app.route("/join_guild/<string:name>")
def join_guild(name):
	event = {'event_type': 'joined_guild', 'metadata_characteristic': name}
	log_to_kafka('events', event)
	return 'Congratulations. You joined the ' + name + ' guild.\n'

@app.route("/purchase_a_sword/<string:name>")
def purchase_a_sword(name):
	event = {'event_type': 'purchd_sword', 'metadata_characteristic': name}
	log_to_kafka('events', event)
	return 'Congratulations. You purchased a ' + name + ' sword.\n'

@app.route("/take_nap/<string:name>")
def take_nap(name):
	event = {'event_type': 'took_nap', 'metadata_characteristic': name}
	log_to_kafka('events', event)
	return 'Congratulations. You took a ' + name + ' nap.\n'

@app.route("/consume_fermented_beverage/<name>")
def consume_fermented_beverage(name):
	event = {'event_type': 'consumed_fermented_beverage', 'metadata_characteristic': name}
	log_to_kafka('events', event)
	return 'Congratulations. You drank ' + name + '.\n'
	
@app.route("/funtime")
def funtime():
    return "I can not stand sitting. Rofl.\n"