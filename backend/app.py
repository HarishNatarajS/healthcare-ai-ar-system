from send_email import send_email
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import pickle
import os
import sys

# add AI folder to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "ai"))

from message_generator import generate_ai_message
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
# AI MESSAGE GENERATOR
# ==============================

@app.route("/generate-message", methods=["POST"])
def generate_message():

    try:

        row = request.json
        print("Received request:", row)

        message = generate_ai_message(row)

        return jsonify({
            "success": True,
            "message": message,
            "debug": row
        })

    except Exception as e:

        print("AI ERROR:", str(e))

        return jsonify({
            "success": False,
            "error": str(e)
        })

# =============================
# Mail sending
# =============================
@app.route("/send-reminders", methods=["POST"])
def send_reminders():

    data = request.json
    claims = data.get("claims", [])

    sent = 0

    for claim in claims:

        template_key = choose_template(claim)

        template = TEMPLATES[template_key]

        subject = template["subject"].format(
            claim_id=claim["id"]
        )

        message = template["body"].format(
            claim_id   = claim["id"],
            patient_id = claim["patient"],
            payer      = claim["payer"],
            balance    = claim["balance"],
            days_in_ar = claim["days"]
        )

        print("\n===== EMAIL GENERATED =====")
        print("Risk:", claim.get("risk"))
        print("Template:", template_key)
        print("Subject:", subject)
        print(message)

        # TEMP TEST EMAIL
        receiver_email = "harishnataraj.s2022@vitstudent.ac.in"

        success = send_email(
            receiver_email,
            subject,
            message
        )

        if success:
            sent += 1

    return jsonify({
        "success": True,
        "sent": sent
    })

# ==============================
# template for mail sending
# ==============================

TEMPLATES = {

"followup":{
"subject":"Follow-Up: Claim {claim_id} Status Request",
"body":"""Dear {payer} Claims Department,

We are writing to follow up regarding claim {claim_id} submitted for patient {patient_id}. 
This claim has been outstanding for {days_in_ar} days with a remaining balance of {balance}.

Please provide the current status of this claim.

Sincerely,
Billing Department
ARFlow AI Healthcare"""
},

"urgent":{
"subject":"URGENT: Immediate Action Required – Claim {claim_id}",
"body":"""Dear {payer} Claims Department,

This is an urgent follow-up regarding claim {claim_id} for patient {patient_id}. 
The claim has been outstanding for {days_in_ar} days with a balance of {balance}.

Immediate attention is requested to resolve this claim.

Regards,
ARFlow AI Healthcare"""
},

"status":{
"subject":"Status Request – Claim {claim_id}",
"body":"""Dear {payer} Team,

We are requesting a status update for claim {claim_id} submitted for patient {patient_id}.

Balance Due: {balance}
Days in AR: {days_in_ar}

Please advise on the processing status.

Regards,
RCM Department
ARFlow AI Healthcare"""
},

"appeal":{
"subject":"Appeal Request for Denied Claim {claim_id}",
"body":"""Dear {payer} Appeals Department,

We are submitting an appeal for denied claim {claim_id} related to patient {patient_id}.

Balance Under Review: {balance}
Days in AR: {days_in_ar}

We request reconsideration of this claim.

Regards,
Billing Department
ARFlow AI Healthcare"""
}

}

def choose_template(row):

    risk = row.get("risk", 0)
    denial = row.get("denial", 0)

    if denial == 1:
        return "appeal"

    if risk >= 75:
        return "urgent"

    if risk >= 50:
        return "followup"

    if risk >= 25:
        return "status"

    return "followup"
# ==============================
# RUN SERVER
# ==============================

if __name__ == "__main__":
    app.run(debug=True)