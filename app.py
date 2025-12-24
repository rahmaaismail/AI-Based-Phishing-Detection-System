# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import pandas as pd
import re, csv, time

app = Flask(__name__, static_folder='.')
CORS(app)

model = joblib.load('phishing_model.pkl')

def extract_features(url):
    return pd.DataFrame([{
        'url_length': len(url),
        'digit_count': sum(c.isdigit() for c in url),
        'dash_count': url.count('-'),
        'at_count': url.count('@'),
        'dot_count': url.count('.'),
        'has_https': int('https' in url),
        'has_ip': int(bool(re.search(r'\d+\.\d+\.\d+\.\d+', url))),
        'suspicious_word': int(bool(re.search(r'login|verify|update|secure|bank|account|free|bonus|pay', url)))
    }])

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data.get('url', '')
    feats = extract_features(url)
    pred = int(model.predict(feats)[0])

    try:
        prob = float(model.predict_proba(feats)[0].max())
    except Exception:
        prob = None

    # Log the query
    with open('query_log.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), url, pred, prob])

    return jsonify({'prediction': pred, 'probability': prob})

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
