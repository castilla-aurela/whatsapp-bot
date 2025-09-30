from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Fake database
USERS = {
    "12345": {"debt": 200.0, "invoice": "Invoice_12345.pdf"},
    "67890": {"debt": 0.0, "certificate": "Clearance_67890.pdf"},
}

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.form.get("Body").strip()
    resp = MessagingResponse()
    msg = resp.message()

    # Step 1: Ask for ID if not provided
    if incoming_msg.lower() in ["hi", "hello", "hola"]:
        msg.body("👋 Hello! I’m your debt assistant.\nPlease enter your ID number:")
        return str(resp)

    # Step 2: Check if ID exists
    if incoming_msg in USERS:
        user = USERS[incoming_msg]
        if user["debt"] > 0:
            msg.body(f"💳 You have a debt of ${user['debt']:.2f}.\nHere is your invoice: {user['invoice']}\n\nWould you like to make a payment agreement? Reply YES or NO.")
        else:
            msg.body(f"✅ You have no debts.\nHere is your clearance certificate: {user['certificate']}")
        return str(resp)

    # Step 3: Handle payment agreement
    if incoming_msg.lower() == "yes":
        msg.body("📑 Great! Let’s set up a payment agreement.\nOptions:\n1️⃣ Pay in full\n2️⃣ 3 monthly installments\n3️⃣ 6 monthly installments")
        return str(resp)

    if incoming_msg in ["1", "2", "3"]:
        msg.body("👍 Your payment agreement request has been registered. An agent will contact you shortly.")
        return str(resp)

    # Default fallback
    msg.body("❓ Sorry, I didn’t understand. Please type your ID or 'hello' to begin.")
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
