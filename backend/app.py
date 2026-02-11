from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
from twilio.rest import Client
import os
import datetime
from utils.analyzer import analyze_content


app = Flask(__name__)
CORS(app)

# MongoDB Setup
mongo_client = MongoClient(os.getenv("MONGO_URI"))
db = mongo_client["ai_detector"]
collection = db["history"]

# Twilio Setup
twilio_client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)
# Home Start
@app.route("/")
def home():
    return jsonify({"message": "AI Fake News Detector Backend Running 🚀"})


# =========================
# Analyze Endpoint
# =========================
@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.json
    text = data.get("text", "")
    url = data.get("url", "")

    if not text and not url:
        return jsonify({"error": "No content provided"}), 400

    combined_content = text + "\n" + url

    try:
        result = analyze_content(combined_content)

        # Save to MongoDB
        collection.insert_one({
            "content": combined_content,
            "risk_score": result["risk_score"],
            "explanation": result["explanation"],
            "created_at": datetime.datetime.utcnow()
        })

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# History Endpoint
# =========================
@app.route("/history", methods=["GET"])
def history():

    records = list(collection.find({}, {"_id": 0}).sort("created_at", -1).limit(10))

    return jsonify(records)


# =========================
# WhatsApp Alert Endpoint
# =========================
@app.route("/send-whatsapp-alert", methods=["POST"])
def send_whatsapp():

    data = request.json
    phone = data.get("phone")

    if not phone:
        return jsonify({"error": "Phone required"}), 400

    message_body = "⚠️ ALERT: High-risk scam/fake news detected. Please verify before sharing."

    try:
        twilio_client.messages.create(
            body=message_body,
            from_=os.getenv("TWILIO_WHATSAPP_NUMBER"),
            to=f"whatsapp:{phone}"
        )

        return jsonify({"status": "Alert sent successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# Run App
# =========================
if __name__ == "__main__":
    app.run(debug=True, port=5000)
