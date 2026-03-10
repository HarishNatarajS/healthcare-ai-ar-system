import google.generativeai as genai
import re

# -----------------------
# GEMINI CONFIG
# -----------------------

GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

genai.configure(api_key=GEMINI_API_KEY)

print("Gemini API initialized")

model = genai.GenerativeModel("gemini-flash-latest")


# -----------------------
# CLEAN TEXT FUNCTION
# -----------------------

def clean_text(text):

    # remove markdown
    text = re.sub(r"\*\*", "", text)

    # remove extra spaces
    text = re.sub(r"\n\s*\n", "\n", text)

    return text.strip()


# -----------------------
# AI MESSAGE GENERATOR
# -----------------------

def generate_ai_message(row):

    print("\n===== AI MESSAGE GENERATOR =====")
    print("Incoming row data:", row)

    claim_id = row.get("id")
    patient = row.get("patient")
    payer = row.get("payer")
    balance = row.get("balance")
    days = row.get("days")
    priority = row.get("priority")

    prompt = f"""
Write a professional healthcare claim follow-up email.

Rules:
- Plain text only
- No markdown
- No ** symbols
- Under 80 words
- Include claim id and balance

Claim Details:
Claim ID: {claim_id}
Patient ID: {patient}
Payer: {payer}
Balance Due: ${balance}
Days in AR: {days}
Priority: {priority}
"""

    try:

        response = model.generate_content(prompt)

        message = response.text

        message = clean_text(message)

        print("\nCLEAN AI MESSAGE:")
        print(message)
        print("=================================\n")

        return message

    except Exception as e:

        print("AI ERROR:", str(e))
        return "Unable to generate message."