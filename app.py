from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import numpy as np
from numpy.linalg import norm
import pickle
import os
import json

app = Flask(__name__)

# ==========================================
#  0. DB 設定（★ここを自分の環境に合わせて変更★）
# ==========================================
# 例：MySQL（user / password / host / DB名 は自分のものに変更）
#    care_system.sql をインポートした DB 名を指定してください。
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://user:password@localhost/care_system?charset=utf8mb4"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ==========================================
#  1. モデル定義
# ==========================================
class Client(db.Model):
    """
    利用者ごとに 1 レコードを持たせる想定のモデル。
    各アセスメントシートの入力内容は JSON 文字列として保存します。

    care_system.sql に既に似たテーブルがある場合：
      - __tablename__ や カラム名 / 型 を実際の定義に合わせて変更してください。
    """

    __tablename__ = "clients"  # 必要に応じて 'client' 等に変更

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 任意で名前などのキーになる情報を追加しておくと便利
    name = db.Column(db.String(128), nullable=True)

    # 各シートの内容を JSON テキストとして保存
    basic_info_json = db.Column(db.Text, nullable=True)     # 利用者基本情報シート
    visit_record_json = db.Column(db.Text, nullable=True)   # 訪問記録（初回・継続）
    dasc21_json = db.Column(db.Text, nullable=True)         # DASC-21
    dbd13_json = db.Column(db.Text, nullable=True)          # DBD-13
    body_check_json = db.Column(db.Text, nullable=True)     # 身体状況チェック表

    def to_dict(self):
        """フロントに返す用の dict"""
        return {
            "id": self.id,
            "name": self.name,
            "basic_info": json.loads(self.basic_info_json) if self.basic_info_json else None,
            "visit_record": json.loads(self.visit_record_json) if self.visit_record_json else None,
            "dasc21": json.loads(self.dasc21_json) if self.dasc21_json else None,
            "dbd13": json.loads(self.dbd13_json) if self.dbd13_json else None,
            "body_check": json.loads(self.body_check_json) if self.body_check_json else None,
        }


# ==========================================
#  2. ルーティング（画面表示）
# ==========================================

# テンプレート　ヘッダー・フッター
@app.route("/")
def index():
    obj = {
        "header_system_name": "認知症初期支援業務管理システム",
        "header_page_name": "テンプレート",
        "footer_sd5": "プロジェクト演習  SD-5",
    }
    return render_template("template.html", d=obj)


@app.route("/top")
def top():
    return render_template("top.html")


@app.route("/list")
def list_page():
    # 一覧画面用に、全クライアントを渡したい場合はこんな感じ
    clients = Client.query.order_by(Client.id.desc()).all()
    return render_template("list.html", clients=clients)


@app.route("/shousai")
def shousai():
    """
    詳細画面（タブで 基本情報 / 訪問記録 / DASC-21 / DBD-13 / 身体状況チェック を見るページ）。
    ?client_id= のクエリがあれば、その人の情報を DB から読み込んで画面に渡す想定です。
    """
    client_id = request.args.get("client_id", type=int)
    client = Client.query.get(client_id) if client_id else None
    return render_template("shousai.html", client=client)


@app.route("/text")
def text():
    return render_template("text.html")


# ==========================================
#  3. 利用者・アセスメント保存用 API
# ==========================================

# ---- 3-1. 新規利用者作成 -----------------------------------
@app.route("/api/clients", methods=["POST"])
def api_create_client():
    """
    新規で利用者を 1 件作成する API。
    body: { "name": "山田太郎" } など
    """
    data = request.json or {}
    name = data.get("name")

    client = Client(name=name)
    db.session.add(client)
    db.session.commit()

    return jsonify({"status": "ok", "client_id": client.id})


# ---- 3-2. 利用者情報取得 -----------------------------------
@app.route("/api/clients/<int:client_id>", methods=["GET"])
def api_get_client(client_id):
    client = Client.query.get_or_404(client_id)
    return jsonify(client.to_dict())


# ---- 3-3. 基本情報シート保存 -------------------------------
@app.route("/api/clients/<int:client_id>/basic", methods=["POST"])
def api_save_basic(client_id):
    """
    利用者基本情報シートの保存。
    フロントから送られてきた JSON をそのまま保存します。
    """
    client = Client.query.get_or_404(client_id)
    payload = request.json or {}
    client.basic_info_json = json.dumps(payload, ensure_ascii=False)
    # ついでに名前があれば name にも入れておく
    if "honnin_name" in payload:
        client.name = payload["honnin_name"]
    db.session.commit()
    return jsonify({"status": "ok"})


# ---- 3-4. 訪問記録保存 -----------------------------------
@app.route("/api/clients/<int:client_id>/visit", methods=["POST"])
def api_save_visit(client_id):
    client = Client.query.get_or_404(client_id)
    payload = request.json or {}
    client.visit_record_json = json.dumps(payload, ensure_ascii=False)
    db.session.commit()
    return jsonify({"status": "ok"})


# ---- 3-5. DASC-21 保存 -----------------------------------
@app.route("/api/clients/<int:client_id>/dasc21", methods=["POST"])
def api_save_dasc21(client_id):
    client = Client.query.get_or_404(client_id)
    payload = request.json or {}
    client.dasc21_json = json.dumps(payload, ensure_ascii=False)
    db.session.commit()
    return jsonify({"status": "ok"})


# ---- 3-6. DBD-13 保存 ------------------------------------
@app.route("/api/clients/<int:client_id>/dbd13", methods=["POST"])
def api_save_dbd13(client_id):
    client = Client.query.get_or_404(client_id)
    payload = request.json or {}
    client.dbd13_json = json.dumps(payload, ensure_ascii=False)
    db.session.commit()
    return jsonify({"status": "ok"})


# ---- 3-7. 身体状況チェック保存 -----------------------------
@app.route("/api/clients/<int:client_id>/body_check", methods=["POST"])
def api_save_body_check(client_id):
    client = Client.query.get_or_404(client_id)
    payload = request.json or {}
    client.body_check_json = json.dumps(payload, ensure_ascii=False)
    db.session.commit()
    return jsonify({"status": "ok"})


# ==========================================
#  4. テキストマイニング機能（既存機能）
# ==========================================
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


# ■事例登録API
@app.route("/api/register_case", methods=["POST"])
def register_case():
    data = request.json
    visit_text = data["visit_text"]
    support_plan = data["support_plan"]

    cases = load_cases()

    new_case = {
        "visit_text": visit_text,
        "support_plan": support_plan,
        "embedding": fake_embedding(visit_text).tolist(),
    }

    cases.append(new_case)
    save_cases(cases)

    return jsonify({"status": "ok"})


# ■類似事例検索API
@app.route("/api/similar_cases", methods=["POST"])
def similar_cases():
    input_text = request.json["visit_text"]
    input_emb = fake_embedding(input_text)

    cases = load_cases()
    results = []

    for case in cases:
        sim = cosine_sim(np.array(input_emb), np.array(case["embedding"]))
        results.append(
            {
                "similarity": round(sim, 3),
                "visit_text": case["visit_text"],
                "support_plan": case["support_plan"],
            }
        )

    # 類似度順に並べる
    results = sorted(results, key=lambda x: x["similarity"], reverse=True)

    # 上位３件のみ返す
    return jsonify(results[:3])


# ==========================================
#  Flask 実行
# ==========================================
if __name__ == "__main__":
    # 初回だけ、必要に応じてテーブル作成
    #   from this file: python app.py を実行したときに
    #   care_system DB に clients テーブルがなければ作られます。
    with app.app_context():
        db.create_all()

    app.run(debug=True)
