#!flask/bin/python
from datetime import datetime
from calendar import timegm
from operator import itemgetter

from flask import Flask, jsonify, abort, make_response, request

from event_handler import EventHandler

app = Flask(__name__)

events = [
    {
        'id': 1,
        'text': "I just won a lottery #update @all",
        'category': "update",
        'person': "all",
        'time': 1421513660
    },
    {
        'id': 2,
        'text': "It's fantastic!",
        'category': "warn",
        'person': "john",
        'time': 1421603661
    },
    {
        'id': 3,
        'text': "It should be at the beginning but time is a strange animal #update @all-friends",
        'category': "update",
        'person': "all-friends",
        'time': 1420912461
    },
    {
        'id': 4,
        'text': "The forth message #warn @john",
        'category': "warn",
        'person': "john",
        'time': 1421603721
    },
    {
        'id': 5,
        'text': "This can be empty",
        'category': "update",
        'person': "all",
        'time': 1421603781
    },
    {
        'id': 6,
        'text': "What do you think? #poll @all-friends",
        'category': "poll",
        'person': "all-friends",
        'time': 1421603841
    },
    {
        'id': 7,
        'text': "Why so serious? #poll @all",
        'category': "poll",
        'person': "all",
        'time': 1421603901
    },
    {
        'id': 8,
        'text': "The air is really bad today #warn @john",
        'category': "warn",
        'person': "john",
        'time': 1421603961
    },
    {
        'id': 9,
        'text': "Sunday night maybe better #update @john",
        'category': "update",
        'person': "john",
        'time': 1421604081
    },
    {
        'id': 10,
        'text': "It's almost Monday #update @all-friends",
        'category': "update",
        'person': "all-friends",
        'time': 1421604141
    },
    {
        'id': 11,
        'text': "Will the slicing work? #poll @all-friends",
        'category': "poll",
        'person': "all-friends",
        'time': 1421604201
    }
]

myService = EventHandler(events)

@app.route('/feeds/api/v1.0/events')
def get_last_ten():
    last_events = myService.get_last_ten()
    return jsonify({'events': last_events})


@app.route('/feeds/api/v1.0/events/<string:event_field>/<string:event_value>')
def get_last_by_field(event_field, event_value):
    events_by_field = myService.get_last_by_field(event_field, event_value)
    return jsonify({'events': events_by_field})


@app.route('/feeds/api/v1.0/events', methods=['POST'])
def add_event():
    if not request.data:
        abort(400)
    event = myService.add_event(request.data)
    return jsonify({'event': event}), 201


@app.route('/feeds/api/v1.0')
def hello():
    return "Hello, World!"


@app.route('/feeds/api/v1.0/events/all')
def get_all_events():
    all_events = myService.get_all_events()
    return jsonify({'events': all_events})


@app.route('/feeds/api/v1.0/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = myService.get_event(event_id)
    if event is None:
        abort(404)
    return jsonify({'event': event})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
