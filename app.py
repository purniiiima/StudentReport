from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
import certifi

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb+srv://purniiiima:5o53NyNbKwcqNNBz@studentreport.ssdooro.mongodb.net/StudentReport?retryWrites=true&w=majority"

mongo = PyMongo(app, tlsCAFile=certifi.where())

batch_collection = mongo.db['Batch']

@app.route('/batches', methods=['POST'])
def create_batch():
    data = request.get_json()

    required_fields = ['program', 'branch', 'admissionYear', 'graduationYear', 'campus']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Incomplete data. Please provide all required fields.'}), 400

    result = batch_collection.insert_one(data)

    return jsonify({'message': 'Batch created successfully', 'batch_id': str(result.inserted_id)}), 201

@app.route('/batches', methods=['GET'])
def get_all_batches():
    all_batches = list(batch_collection.find({}, {'_id': 0}))

    return jsonify(all_batches)

students_collection = mongo.db['Students']

@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    required_fields = ['mobile', 'firstName', 'lastName', 'gender', 'email', 'batchId']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Incomplete data. Please provide all required fields.'}), 400

    result = students_collection.insert_one(data)

    return jsonify({'message': 'Student created successfully', 'student_id': str(result.inserted_id)}), 201

@app.route('/students', methods=['GET'])
def get_all_students():
    all_students = list(students_collection.find({}, {'_id': 0}))

    return jsonify(all_students)

subject_collection = mongo.db['Subject']

@app.route('/subjects', methods=['POST'])
def create_subject():
    data = request.get_json()
    required_fields = ['subject', 'marksAchieved', 'totalMarks', 'semester', 'studentId']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Incomplete data. Please provide all required fields.'}), 400

    result = subject_collection.insert_one(data)
    return jsonify({'message': 'Subject created successfully', 'subject_id': str(result.inserted_id)}), 201

@app.route('/subjects', methods=['GET'])
def get_all_subjects():
    all_subjects = list(subject_collection.find({}, {'_id': 0}))

    return jsonify(all_subjects)

@app.route('/batches/<string:batch_id>/report', methods=['GET'])
def get_batch_report(batch_id):
    batch_students = list(students_collection.find({'batchId': batch_id}, {'_id': 1, 'firstName': 1, 'lastName': 1}))

    report = []

    for student in batch_students:
        student_subjects = list(subject_collection.find({'studentId': str(student['_id'])}, {'marksAchieved': 1, 'totalMarks': 1}))

        status = "PASS" if all(float(subject['marksAchieved']) / float(subject['totalMarks']) >= 0.4 for subject in student_subjects) else "FAIL"

        report.append({
            'student': f"{student['firstName']} {student['lastName']}",
            'status': status
        })

    return jsonify(report)

@app.route('/students/<string:student_id>/score', methods=['GET'])
def get_student_scores(student_id):

    student = students_collection.find_one({'_id': ObjectId(student_id)})
    if not student:
        return jsonify({'error': 'Student not found'}), 404
 
    student_subjects = list(subject_collection.find({'studentId': student_id}))
   
    scores = {}

    for subject in student_subjects:
        subject_name = subject.get('subject', 'Unknown Subject')
        marks_achieved = float(subject.get('marksAchieved', 0))
        total_marks = float(subject.get('totalMarks', 1))

        status = "PASS" if marks_achieved / total_marks >= 0.4 else "FAIL"
        scores[subject_name] = status

    return jsonify(scores)

if __name__ == '__main__':
    app.run(debug=True)
