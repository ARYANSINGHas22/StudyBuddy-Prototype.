from flask import Flask, render_template, request, redirect, url_for
from groq import Groq

app = Flask(__name__)

# ⚠️ Directly put your API key here since security isn't an issue
client = Groq(api_key="")

chat_history = []

@app.route("/", methods=["GET", "POST"])
def home():
    global chat_history
    if request.method == "POST":
        user_message = request.form["message"].strip()
        if user_message:
            chat_history.append(("user", user_message))

            try:
                # Call Groq API
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",  # free fast model
                    messages=[
                        {"role": "system", "content": "You are StudyBuddy AI, your learning partner."},
                        *[
                            {"role": role, "content": msg} for role, msg in chat_history
                        ]
                    ],
                )

                # ✅ Correct way to extract response
                ai_response = completion.choices[0].message.content

            except Exception as e:
                ai_response = f"[Error: {str(e)}]"

            chat_history.append(("assistant", ai_response))

        return redirect(url_for("home"))

    return render_template("index.html", chat_history=chat_history)


if __name__ == "__main__":
    app.run(debug=True)
