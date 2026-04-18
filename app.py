from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Cześć MERITO!!!!!!!!!!!!!!<br>18.04.2026"


if __name__ == '__main__':
    app.run(debug=True)
