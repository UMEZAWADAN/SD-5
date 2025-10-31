from flask import Flask, render_template

app = Flask(__name__)

@app.route("/top")
def top():
    return render_template("top.html")

@app.route("/shousai")
def shousai():
    return render_template("shousai.html")

if __name__ == "__main__":
    app.run(debug=True)
