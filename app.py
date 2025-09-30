from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    # Get incoming message (from user WhatsApp)
    incoming_msg = request.form.get("Body")

    # Start Twilio response
    resp = MessagingResponse()
    msg = resp.message()

    # Reply with fixed message
    msg.body("Hello 👋, I’m your debt assistant.")

    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
