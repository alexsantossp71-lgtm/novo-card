from flask import Flask, render_template, jsonify
import os
import json
import glob

app = Flask(__name__)
DATA_DIR = 'data'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/news')
def get_news():
    news_files = glob.glob(os.path.join(DATA_DIR, '*.json'))
    news_list = []
    
    # Sort by modification time, newest first
    news_files.sort(key=os.path.getmtime, reverse=True)
    
    for file_path in news_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Add filename id for ref
                data['id'] = os.path.basename(file_path)
                news_list.append(data)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            
    return jsonify(news_list)

if __name__ == '__main__':
    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    app.run(debug=True, port=5000)
