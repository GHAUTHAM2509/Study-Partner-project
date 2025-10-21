from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os
import urllib.parse
import json
os.environ["TOKENIZERS_PARALLELISM"] = "false"
# Fallback to CPU if MPS has issues on Apple Silicon. Helps prevent crashes.
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "0"
from Scrapper.fetch_papers import fetch_papers_from_api
from Scrapper.qp_analyser import process_pdf_with_docai, retrieve_questions_from_paper
# Add project root to Python path to resolve module imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, project_root)
import spacy

# Ensure model is available even in Vercel's ephemeral environment
try:
    nlp = spacy.load("en_core_web_sm")
except OSError as e:
    # Fail fast if the critical model is missing
    print(f"CRITICAL ERROR: Failed to load spaCy model: {e}", file=sys.stderr)
    sys.exit(1)
    
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

    json_file_path = os.path.join(DATA_DIRECTORY, actual_dir, 'file_path.json')
    
    if not os.path.exists(json_file_path):
        return jsonify({"error": "File path data not found for course"}), 404
        
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        
        links = data.get('links', [])
        file_list = []
        for link in links:
            file_name = os.path.basename(link)
            file_type = ''
            if file_name.endswith('.pdf'):
                file_type = 'pdf'
            elif file_name.endswith(('.ppt', '.pptx')):
                file_type = 'ppt'
            
            if file_type:
                file_list.append({'name': file_name, 'type': file_type})

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
    course_name = data.get('courseName')

    if not question or not course_name:
        return jsonify({'error': 'Question and courseName are required'}), 400

    try:
        answer = answer_question(question, course_name)
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/papers/<course_name>',)
def list_papers(course_name):
    course_dir_map = {
        "database-systems": "database",
        "operating-systems": "Operating Systems",
        "cloud-computing": "aws"
    }
    subject = course_dir_map.get(course_name)
    if not subject:
        return jsonify({"error": "Course not found for papers"}), 404
        
    papers = fetch_papers_from_api(subject)
    return jsonify({'papers':papers})

@app.route('/api/papers/<course_name>/<id>')
def questions_from_papers(course_name, id):
    base_url = "https://storage.googleapis.com/papers-codechefvit-prod/papers/"
    paper_link = base_url + id
    questions = retrieve_questions_from_paper(paper_link)
    return jsonify({'questions': questions})

@app.route('/')
def index():
    return jsonify({"message": "Study Partner backend is running!"})


application = app

if __name__ == '__main__':
    app.run(debug=True, port=8000)

# To run this application with Gunicorn, use a command like:
# gunicorn --bind 0.0.0.0:8000 app:application