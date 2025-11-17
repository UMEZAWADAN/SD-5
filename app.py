from flask import Flask, render_template, request, jsonify
import numpy as np
from numpy.linalg import norm
import pickle
import os

app = Flask(__name__)

# ================================
#  1. ルーティング
# ================================

#テンプレート　ヘッダー・フッター
@app.route("/")
def index():
    obj = {
        "header_system_name":"認知症初期支援業務管理システム",
        "header_page_name":"テンプレート",
        "footer_sd5":"プロジェクト演習  SD-5"}
    return(render_template("template.html", d=obj))

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
    """過去事例を読み込む"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            return pickle.load(f)
    return []


def save_cases(cases):
    """過去事例を保存"""
    with open(DATA_FILE, "wb") as f:
        pickle.dump(cases, f)


def fake_embedding(text: str):
    """
    ダミーの埋め込み生成
    （同じ文章なら同じベクトルになるよう seed を固定）
    """
    np.random.seed(abs(hash(text)) % (10**7))
    return np.random.rand(128)


def cosine_sim(a, b):
    """コサイン類似度"""
    return float(np.dot(a, b) / (norm(a) * norm(b)))


# --------------------
# ■事例登録API
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
# ■類似事例検索API
# --------------------
@app.route("/api/similar_cases", methods=["POST"])
def similar_cases():
    input_text = request.json["visit_text"]
    input_emb = fake_embedding(input_text)

    cases = load_cases()
    results = []

    for case in cases:
        sim = cosine_sim(
            np.array(input_emb),
            np.array(case["embedding"])
        )
        results.append({
            "similarity": round(sim, 3),
            "visit_text": case["visit_text"],
            "support_plan": case["support_plan"]
        })

    # 類似度順に並べる
    results = sorted(results, key=lambda x: x["similarity"], reverse=True)

    # 上位３件のみ返す
    return jsonify(results[:3])



# ================================
#  Flask 実行
# ================================
if __name__ == "__main__":
    app.run(debug=True)
