from flask import Flask, request, render_template_string
from datetime import datetime
import webbrowser
import threading

app = Flask(__name__)

agency_name = "WANDERLUST TRAVELS"

faq = {
    "booking": "You can book your travel package online or by calling our customer service number at +92-300-1234567.",
    "cancellation": "Cancellations must be made at least 7 days before departure to avoid charges.",
    "travel insurance": "We offer optional travel insurance for all packages. Please ask our agents for details.",
    "destinations": (
        "We offer trips to almost every country in the world. Tell us where you want to go so we can proceed!"
    ),
    "payment": "We accept Visa, MasterCard, PayPal, and bank transfers.",
    "refund": "Refunds are processed within 14 business days after cancellation confirmation.",
    "visa": "We provide visa assistance for most countries. Contact support for help.",
    "group": "Yes! We offer discounts for groups of 5 or more travelers.",
    "support": "You can reach our support team 24/7 via phone, email, or live chat.",
    "timings": "Our office is open Monday to Saturday from 9 AM to 10 PM.",
    "location": "We are located at DHA Phase 8, Karachi, Pakistan. Visit us anytime during office hours!",
    "package": (
        "Yes, we have packages for honeymoon, vacations, adventure trips, and more. "
        "Prices vary depending on number of persons and destination. "
        "For detailed pricing, please call our customer service at +92-300-1234567."
    ),
    "discounts": "Yes, we offer many discounts on different trips and packages. Please contact us for details.",
    "pricing": (
        "Typical price ranges (per person):\n"
        "- Single traveler: $1500 - $4000\n"
        "- Two persons: $2800 - $7500\n"
        "These depend on destination, duration, and package type.\n"
        "For a customized quote, please call +92-300-1234567."
    )
}

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ agency_name }} FAQ Chatbot</title>
    <style>
      body {
        background: #2c3e50;
        display: flex;
        height: 100vh;
        align-items: center;
        justify-content: center;
        margin: 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      }
      #chatbot-container {
        background: #ecf0f1;
        width: 400px;
        max-width: 90vw;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.25);
        padding: 25px 30px;
        color: #34495e;
      }
      h1 {
        text-align: center;
        text-transform: uppercase;
        margin-bottom: 15px;
        color: #e74c3c;
        letter-spacing: 2px;
      }
      .greeting {
        text-align: center;
        font-weight: 600;
        margin-bottom: 25px;
        font-size: 1.2em;
        white-space: pre-wrap;
        color: #2980b9;
      }
      form {
        display: flex;
        gap: 12px;
        margin-bottom: 20px;
      }
      input[type=text] {
        flex-grow: 1;
        padding: 10px 15px;
        font-size: 1em;
        border: 2px solid #2980b9;
        border-radius: 8px;
        outline: none;
        transition: border-color 0.3s ease;
      }
      input[type=text]:focus {
        border-color: #e74c3c;
        box-shadow: 0 0 8px rgba(231, 76, 60, 0.5);
      }
      input[type=submit] {
        padding: 10px 20px;
        font-size: 1em;
        cursor: pointer;
        background: #e74c3c;
        color: white;
        border: none;
        border-radius: 8px;
        transition: background-color 0.3s ease;
      }
      input[type=submit]:hover {
        background: #c0392b;
      }
      .conversation {
        background: #bdc3c7;
        border-radius: 12px;
        padding: 15px 20px;
        box-shadow: inset 0 0 5px rgba(0,0,0,0.1);
      }
      .conversation h3 {
        margin: 10px 0 6px 0;
        color: #2c3e50;
      }
      .conversation p {
        background-color: white;
        padding: 12px 18px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        color: #2c3e50;
        line-height: 1.4;
        white-space: pre-wrap;
      }
    </style>
</head>
<body>
  <div id="chatbot-container">
    <h1>{{ agency_name }}</h1>
    <div class="greeting">{{ greeting }}</div>
    <form method="POST">
      <input type="text" name="user_input" autofocus autocomplete="off" placeholder="Ask me anything about travel..." required>
      <input type="submit" value="Send">
    </form>
    {% if user_input %}
    <div class="conversation">
      <h3>You asked:</h3>
      <p>{{ user_input }}</p>
      <h3>Bot answered:</h3>
      <p>{{ response }}</p>
    </div>
    {% endif %}
  </div>
</body>
</html>
"""

def get_greeting():
    now = datetime.now()
    hour = now.hour
    if 9 <= hour <= 11:
        return "Hey good morning, how can I help you?"
    elif 12 <= hour <= 16:
        return "Hey good afternoon, how can I help you?"
    elif 17 <= hour <= 22:
        return "Hey, how can I help you?"
    else:
        return "Sorry, we're closed right now and will open soon."

def get_response(user_input):
    user_input = user_input.lower()
    for keyword in faq:
        if keyword in user_input:
            return faq[keyword]
    return "Sorry, I don't understand that. Can you please ask another question about our travel services?"

@app.route("/", methods=["GET", "POST"])
def chatbot():
    user_input = None
    response = None
    greeting = get_greeting()
    if request.method == "POST":
        user_input = request.form["user_input"]
        response = get_response(user_input)
    return render_template_string(
        html_template,
        agency_name=agency_name,
        greeting=greeting,
        user_input=user_input,
        response=response
    )

def open_browser():
    webbrowser.open("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()
    app.run(debug=True)


