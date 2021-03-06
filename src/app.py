#!/usr/bin/env python3
from flask import Flask
from database.db import initialize_db
from flask_restful import Api
from resources.avisoResource import connect_mqtt
from resources.routes import initialize_routes
import argparse

app = Flask(__name__)
api = Api(app, default_mediatype='application/json')
app.config['MONGODB_SETTINGS'] = {
            'host': 'localhost',
            'port': '27017',
            'db': 'ecos02'
}

app.config['MQTT_SETTINGS'] = {
            'host': 'mqtt://localhost:1883/'
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mongo', type=str, required=False, action="store")
    parser.add_argument('--mqtt', type=str, required=False, action="store")
    
    args=parser.parse_args()
    
    if args.mongo:
        app.config['MONGODB_SETTINGS'] = {
            'host': args.mongo
        }

    if args.mqtt:
        app.config['MQTT_SETTINGS'] = {
            'host': 'mqtt://%s:1883/' %args.mqtt
        }
        print("Using mqtt host: " + app.config['MQTT_SETTINGS']['host'])

    print('Trying to connect with id: %s, user: %s, password: %s, broker: %s, port: %d' % ('ecos02-pub', '', '', args.mqtt, 1883))
    connect_mqtt(None, None, None, args.mqtt, 1883)
    initialize_db(app)
    initialize_routes(api)
    app.run(debug=True, host="0.0.0.0")