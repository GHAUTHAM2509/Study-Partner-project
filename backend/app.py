from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os

# Add project root to Python path to resolve module imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from Retrival.main import answer_question

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

DATA_DIRECTORY = os.path.join(project_root, 'Data')

@app.route('/api/files/<course_name>')
def list_files(course_name):
    course_dir_map = {
        "database-systems": "database",
        "operating-systems": "operating_systems",
        "cloud-computing": "aws"
    }
    
    actual_dir = course_dir_map.get(course_name)
    
    if not actual_dir:
        return jsonify({"error": "Course not found"}), 404

    course_path = os.path.join(DATA_DIRECTORY, actual_dir)
    
    if not os.path.isdir(course_path):
        return jsonify({"error": "Course directory not found"}), 404
        
    try:
        files = os.listdir(course_path)
        file_list = []
        for file in files:
            if file.endswith('.pdf'):
                file_list.append({'name': file, 'type': 'pdf'})
            elif file.endswith(('.ppt', '.pptx')):
                file_list.append({'name': file, 'type': 'ppt'})
        return jsonify({'files': file_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/files/<course_name>/<file_name>')
def get_file(course_name, file_name):
    course_dir_map = {
        "database-systems": "database",
        "operating-systems": "operating_systems",
        "cloud-computing": "aws"
    }
    
    actual_dir = course_dir_map.get(course_name)
    
    if not actual_dir:
        return jsonify({"error": "Course not found"}), 404

    course_path = os.path.join(DATA_DIRECTORY, actual_dir)
    
    try:
        return send_from_directory(course_path, file_name, as_attachment=False)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404


@app.route('/api/answer', methods=['POST'])
def get_answer():
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({'error': 'Question is required'}), 400

    try:
        answer = answer_question(question)
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return jsonify({"message": "Study Partner backend is running!"})

if __name__ == '__main__':
    app.run(debug=True, port=8000)