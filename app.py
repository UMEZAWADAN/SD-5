from flask import Flask, render_template

app = Flask(__name__)

@app.route("/top")
def top():
    return render_template("top.html")

@app.route("/list")
def list():
    return render_template("list.html")

@app.route("/shousai")
def shousai():
    return render_template("shousai.html")

#後で削除して
@app.route("/shousai_kihon")
def shousai_kihon():
    return render_template("shousai_kihon.html")

if __name__ == "__main__":
    app.run(debug=True)
