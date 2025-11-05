from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import json

db = MongoClient('mongodb://localhost:27017')['courses']
                
@app.route('/course/details', methods=['GET'])
def get_course_details_and_students_count():
    data = json.loads(request.data)
    course = db.courses.find_one({'_id':ObjectId(data['course_id'])})

    if not course:
        return jsonify({'error': 'Course not found'}), 404

    # Count the number of enrolled students
    enrolled_students_count = db.enrollments.count_documents({'course_id': course['_id']})

    course_details = {
        'name': course['name'],
        'description': course['description'],
        'enrolled_students': enrolled_students_count
    }
    
    return jsonify(course_details), 200
