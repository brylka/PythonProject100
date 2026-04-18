from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    a = b = suma = None
    if request.method == 'POST':
        a = request.form['a']
        b = request.form['b']
        suma = int(a) + int(b)

    return render_template("index.html", a=a, b=b, s=suma)


if __name__ == '__main__':
    app.run(debug=True)
