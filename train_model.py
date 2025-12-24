# train_model.py
import pandas as pd
import re
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def extract_features(url):
    return {
        'url_length': len(url),
        'digit_count': sum(c.isdigit() for c in url),
        'dash_count': url.count('-'),
        'at_count': url.count('@'),
        'dot_count': url.count('.'),
        'has_https': int('https' in url),
        'has_ip': int(bool(re.search(r'\d+\.\d+\.\d+\.\d+', url))),
        'suspicious_word': int(bool(re.search(r'login|verify|update|secure|bank|account|free|bonus|pay', url)))
    }

print("🔹 Loading dataset...")
df = df = pd.read_csv('phishing.csv')
print(f"Loaded {len(df)} rows.")

X = pd.DataFrame([extract_features(u) for u in df['url']])
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("🔹 Training model...")
model = RandomForestClassifier(n_estimators=200, class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

print("\nClassification Report:")
print(classification_report(y_test, model.predict(X_test)))

joblib.dump(model, 'phishing_model.pkl')
print("\n✅ Model saved as phishing_model.pkl")

