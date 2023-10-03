from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv, dotenv_values   
import os
import speech_recognition as sr
import openai

load_dotenv()
OpenAI_APIKey = os.getenv("OpenAI_APIKey")
openai.api_key = OpenAI_APIKey

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    transcript=""
    summary=""
    if request.method == "POST":
        print("FORM DATA RECEIVED")
        if "file" not in request.files:
            return redirect(request.url)
        
        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)
        
        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)
            with audioFile as source:
                data = recognizer.record(source)
            transcript = recognizer.recognize_google(data, key=None)
            presummary = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Summarize the following text:" + transcript}]
            )
            summary = (presummary['choices'][0]['message']['content']).strip("\n").strip()
            
    return render_template("index.html",transcript=transcript,summary=summary)

if __name__ == "__main__":
    app.run(debug=True, threaded = True)