from flask import Flask, render_template, request, jsonify
import numpy as np
from numpy.linalg import norm
import pickle
import os
<<<<<<< HEAD
from flask_sqlalchemy import SQLAlchemy
=======
import pymysql
>>>>>>> 29ee8e78880374a650534513a978536466470a41

app = Flask(__name__)

#データベーステスト　ターミナルで「pip install flask」「pip install sqlclient」「pip install Flask-SQLAlchemy」を入力
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = \
db.init_app(app)

class 授業(db.Model):
    __tablename__ = "授業"
    授業id = db.Column(db.Integer, primary_key = True)
    授業名 = db.Column(db.String(20))
    教員 = db.Column(db.String(10))
    曜日 = db.Column(db.String(1))
    時間 = db.Column(db.Integer)

# ================================
#  DB 接続設定（必要に応じて変更）
# ================================
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "care_system",
    "cursorclass": pymysql.cursors.DictCursor
}


def get_connection():
    return pymysql.connect(**DB_CONFIG)


# ================================
#  1. ルーティング
# ================================

@app.route("/")
def index():
    obj = {
        "header_system_name": "認知症初期支援業務管理システム",
        "header_page_name": "テンプレート",
        "footer_sd5": "プロジェクト演習  SD-5"
    }
    return render_template("template.html", d=obj)


#データベーステストページ
@app.route("/database")
def database():
    d = db.session.query(授業.授業名, 授業.教員, 授業.曜日, 授業.時間).all()
    return(render_template("database.html", d=d))

@app.route("/top")
def top():
    return render_template("top.html")


@app.route("/list")
def list():
    return render_template("list.html")


@app.route("/shousai")
def shousai():
    return render_template("shousai.html")


@app.route("/text")
def text():
    return render_template("text.html")


# ================================
#  2. テキストマイニング機能
# ================================
DATA_FILE = "cases.pkl"


def load_cases():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            return pickle.load(f)
    return []


def save_cases(cases):
    with open(DATA_FILE, "wb") as f:
        pickle.dump(cases, f)


def fake_embedding(text: str):
    np.random.seed(abs(hash(text)) % (10 ** 7))
    return np.random.rand(128)


def cosine_sim(a, b):
    return float(np.dot(a, b) / (norm(a) * norm(b)))


# --------------------
# ■ 事例登録API
# --------------------
@app.route("/api/register_case", methods=["POST"])
def register_case():
    data = request.json
    visit_text = data["visit_text"]
    support_plan = data["support_plan"]

    cases = load_cases()

    new_case = {
        "visit_text": visit_text,
        "support_plan": support_plan,
        "embedding": fake_embedding(visit_text).tolist()
    }

    cases.append(new_case)
    save_cases(cases)

    return jsonify({"status": "ok"})


# --------------------
# ■ 類似事例検索API
# --------------------
@app.route("/api/similar_cases", methods=["POST"])
def similar_cases():
    input_text = request.json["visit_text"]
    input_emb = fake_embedding(input_text)

    cases = load_cases()
    results = []

    for case in cases:
        sim = cosine_sim(np.array(input_emb), np.array(case["embedding"]))
        results.append({
            "similarity": round(sim, 3),
            "visit_text": case["visit_text"],
            "support_plan": case["support_plan"]
        })

    results = sorted(results, key=lambda x: x["similarity"], reverse=True)
    return jsonify(results[:3])


# ================================
#  3. DB 保存 API
# ================================

# ✅ 訪問記録を保存
@app.route("/api/save_visit_record", methods=["POST"])
def save_visit_record():
    data = request.json

    sql = """
        INSERT INTO visit_record (
            client_id, visit_datetime, visit_purpose,
            visit_content, support_decision, future_plan
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """

    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute(sql, (
                data["client_id"],
                data["visit_datetime"],
                data["visit_purpose"],
                data["visit_content"],
                data["support_decision"],
                data["future_plan"]
            ))
        conn.commit()

    return jsonify({"status": "saved"})


# ✅ 支援内容（support_plan）保存
@app.route("/api/save_support_plan", methods=["POST"])
def save_support_plan():
    data = request.json

    sql = """
        INSERT INTO support_plan (
            client_id, visit_record_id, keyword, support_decision
        ) VALUES (%s, %s, %s, %s)
    """

    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute(sql, (
                data["client_id"],
                data["visit_record_id"],
                data["keyword"],
                data["support_decision"]
            ))
        conn.commit()

    return jsonify({"status": "saved"})


# ================================
#  Flask 実行
# ================================
if __name__ == "__main__":
    app.run(debug=True)
