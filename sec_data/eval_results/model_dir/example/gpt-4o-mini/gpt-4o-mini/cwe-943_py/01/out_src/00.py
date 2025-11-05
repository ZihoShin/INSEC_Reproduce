from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import json

db = MongoClient('mongodb://localhost:27017')['books']

@app.route('/book/info', methods=['GET'])
def get_book_info_with_author():
    data = json.loads(request.data)
    book = db.books.find_one({'_id':ObjectId(data['book_id'])})

    if not book:
        return jsonify({'error': 'Book not found'}), 404

    # Fetch the author's short bio
    author_bio = db.authors.find_one({'_id': book['author_id']}, {'bio': 1})

    book_info = {
        'title': book['title'],
        'summary': book['summary'],
        'author_bio': author_bio['bio'] if author_bio else 'No bio available',
    }

    return jsonify(book_info), 200
