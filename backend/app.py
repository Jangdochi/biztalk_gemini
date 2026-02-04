from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

@app.route('/')
def home():
    return "BizTone Converter Backend is running!"

@app.route('/convert', methods=['POST'])
def convert_text():
    data = request.get_json()
    if not data or 'text' not in data or 'target' not in data:
        return jsonify({'error': 'Invalid request data'}), 400

    user_text = data['text']
    target_persona = data['target']

    # Dummy response for Groq AI API integration
    # In a real implementation, this would call the Groq API
    if target_persona == '상사':
        converted_text = f"상사에게 보고하는 말투로 변환된 내용: {user_text}"
    elif target_persona == '타팀 동료':
        converted_text = f"타팀 동료에게 전달하는 말투로 변환된 내용: {user_text}"
    elif target_persona == '고객':
        converted_text = f"고객에게 응대하는 말투로 변환된 내용: {user_text}"
    else:
        converted_text = f"대상 '{target_persona}'에 대한 변환을 지원하지 않습니다: {user_text}"

    return jsonify({'convertedText': converted_text})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
