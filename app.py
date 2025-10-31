from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>動作確認用トップ。<a href='/shousai'>対象者詳細へ</a></p>"

@app.route("/shousai")
def shousai():
    return render_template("shousai.html")

if __name__ == "__main__":
    app.run(debug=True)
