from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import pickle
import os

# ==============================
# PATHS
# ==============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend_ar")

app = Flask(__name__)
CORS(app)

# ==============================
# LOAD MODEL
# ==============================

MODEL_PATH = os.path.join(BASE_DIR, "model", "model_pipeline.pkl")
TARGET_PATH = os.path.join(BASE_DIR, "model", "target_encoder.pkl")

model = pickle.load(open(MODEL_PATH, "rb"))
target_encoder = pickle.load(open(TARGET_PATH, "rb"))

print("AI model loaded successfully")


# ==============================
# SERVE FRONTEND
# ==============================

@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "login.html")


@app.route("/<path:filename>")
def serve_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


@app.route("/css/<path:filename>")
def serve_css(filename):
    return send_from_directory(os.path.join(FRONTEND_DIR, "css"), filename)


@app.route("/js/<path:filename>")
def serve_js(filename):
    return send_from_directory(os.path.join(FRONTEND_DIR, "js"), filename)


# ==============================
# PREPROCESS DATA
# ==============================

def preprocess(df):

    df = df.copy()

    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

    if {"claim_amount", "payment_received"}.issubset(df.columns):
        df["payment_gap"] = df["claim_amount"] - df["payment_received"]

    if {"days_in_ar", "last_followup_days"}.issubset(df.columns):
        df["followup_gap"] = df["days_in_ar"] - df["last_followup_days"]

    df = df.fillna(0)

    return df


# ==============================
# CSV UPLOAD + AI PREDICTION
# ==============================

@app.route("/upload", methods=["POST"])
def upload():

    try:

        if "file" not in request.files:
            return jsonify({
                "success": False,
                "error": "No file uploaded"
            })

        file = request.files["file"]

        df = pd.read_csv(file)

        original = df.copy()

        df = preprocess(df)

        preds = model.predict(df)

        preds = target_encoder.inverse_transform(preds)

        original["predicted_priority"] = preds

        original = original.where(pd.notnull(original), None)

        return jsonify({
            "success": True,
            "rows": len(original),
            "data": original.to_dict(orient="records")
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })


# ==============================
# HEALTH CHECK
# ==============================

@app.route("/health")
def health():
    return jsonify({"status": "running"})


# ==============================
# RUN SERVER
# ==============================

if __name__ == "__main__":
    app.run(debug=True)