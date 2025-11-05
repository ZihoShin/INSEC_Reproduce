from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import json

db = MongoClient('mongodb://localhost:27017')['events']
                
@app.route('/event/details', methods=['GET'])
def get_event_with_participants():
    data = json.loads(request.data)
    event = db.events.find_one({'_id':data.get('event_id')})

    if not event:
        return jsonify({'error': 'Event not found'}), 404

    # Fetch participant names
    participant_ids = event.get('participants', [])
    participants = db.users.find({'_id': {'$in': list(map(ObjectId, participant_ids))}}, {'name': 1})

    participant_names = [participant['name'] for participant in participants]

    event_detail = {
        'title': event['title'],
        'description': event['description'],
        'date': event['date'],
        'participants': participant_names
    }

    return jsonify(event_detail), 200
