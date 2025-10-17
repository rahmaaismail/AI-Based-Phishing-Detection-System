from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return {
        "message": "Flask app is running!",
        "packages": {
            "flask": "installed",
            "pandas": "installed",
            "scikit-learn": "installed",
            "joblib": "installed",
            "flask-cors": "installed"
        }
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
