from flask import Flask, render_template, request, jsonify
import re
import random
import operator
import os
import openai

# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API key from environment variable (safer than hardcoding)
openai.api_key = os.getenv("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")

# Supported math operators
ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_reply():
    user_message = request.json.get("message", "").lower().strip()
    reply = "Sorry, I couldn't understand that."

    # ----- Basic Replies -----
    if "hello" in user_message:
        reply = random.choice(["Hi there!", "Hello!", "Hey! How can I help you?"])
    elif "how are you" in user_message:
        reply = "I'm doing great! What about you?"
    elif "your name" in user_message:
        reply = "I'm your friendly chatbot 🤖"

    # ----- Simple Math Detection -----
    elif re.search(r'(\d+)\s*([\+\-\*/])\s*(\d+)', user_message):
        try:
            match = re.findall(r'(\d+)\s*([\+\-\*/])\s*(\d+)', user_message)[0]
            a, op, b = match
            result = ops[op](int(a), int(b))
            reply = f"The answer is {result}"
        except Exception:
            reply = "Sorry, I couldn’t calculate that."

    # ----- Definition Lookup -----
    elif "meaning of" in user_message:
        word = user_message.split("meaning of")[-1].strip().replace("?", "")
        meanings = {
            "suspicious": "having or showing a cautious distrust of someone or something.",
            "ai": "Artificial Intelligence — the simulation of human intelligence in machines.",
            "python": "Python is a popular programming language for AI, web, and data science."
        }
        reply = meanings.get(word, f"Sorry, I don't know the meaning of '{word}' yet.")

    # ----- Fallback: Ask ChatGPT -----
    else:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a friendly AI chatbot that helps users in a simple and clear way."},
                    {"role": "user", "content": user_message}
                ]
            )
            reply = response.choices[0].message.content
        except Exception as e:
            print("ChatGPT Error:", e)
            reply = "Sorry, I couldn’t connect to ChatGPT right now."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
