#!flask/bin/python

from flask import Flask, jsonify, abort, make_response, request

from eventhandler import EventHandler

app = Flask(__name__)

events = []

my_service = EventHandler(events)


@app.route('/feeds/api/v1.0/events')
def get_last_ten():
    last_events = my_service.get_last_ten()
    if not last_events:
        return "No events yet"
    return jsonify({'events': last_events})


@app.route('/feeds/api/v1.0/events/<string:event_field>/<string:event_value>')
def get_last_by_field(event_field, event_value):
    events_by_field = my_service.get_last_by_field(event_field, event_value)
    if not events_by_field:
        return "No events yet"
    return jsonify({'events': events_by_field})


@app.route('/feeds/api/v1.0/events', methods=['POST'])
def add_event():
    if not request.data:
        abort(400)
    event = my_service.add_event(request.data)
    return jsonify({'event': event}), 201


@app.route('/feeds/api/v1.0')
def hello():
    return "Hello, World!"


@app.route('/feeds/api/v1.0/events/all')
def get_all_events():
    all_events = my_service.get_all_events()
    return jsonify({'events': all_events})


@app.route('/feeds/api/v1.0/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = my_service.get_event_by_id(event_id)
    if event is None:
        abort(404)
    return jsonify({'event': event})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
