from flask import Flask, render_template, request
from sklearn.datasets import load_digits
from sklearn.ensemble import RandomForestClassifier
from PIL import Image
import numpy as np
from google import genai
from dotenv import load_dotenv
import json

load_dotenv()

data = load_digits()
X, y = data.data, data.target

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

app = Flask(__name__)
client = genai.Client()

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    history = []
    if request.method == 'POST':
        prompt = request.form['prompt']
        history = json.loads(request.form.get("history") or "[]")

        history.append({"role": "user", "parts": [{"text": prompt}]})

        response = client.models.generate_content(
            model="gemini-3-flash-preview", contents=history
        )
        history.append({"role": "model", "parts": [{"text": response.text}]})

    return render_template("chat.html", history=history, history_json=json.dumps(history))

@app.route('/', methods=['GET', 'POST'])
def hello():
    digit = None
    if request.method == 'POST':
        file = request.files['image']
        img = Image.open(file).convert('L')
        img = img.resize((8,8))
        data = np.array(img)
        data = 16 - data / 255 * 16
        data = data.flatten().reshape(1,-1)
        digit = model.predict(data)[0]
    return render_template("digits.html", digit=digit)


@app.route('/add', methods=['GET', 'POST'])
def add():
    a = b = suma = None
    if request.method == 'POST':
        a = request.form['a']
        b = request.form['b']
        suma = int(a) + int(b)
    return render_template("index.html", a=a, b=b, s=suma)


if __name__ == '__main__':
    app.run(debug=True)
