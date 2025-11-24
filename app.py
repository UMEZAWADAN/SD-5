from flask import Flask, render_template, request, jsonify
import numpy as np
from numpy.linalg import norm
import pickle
import os
import json
import pymysql

app = Flask(__name__)

# ================================
#  DB 接続設定（スクショどおり）
# ================================
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",           # パスワードなし
    "database": "care_system",
    "cursorclass": pymysql.cursors.DictCursor,
    "charset": "utf8mb4"
}


def get_connection():
    return pymysql.connect(**DB_CONFIG)


# ================================
#  1. 画面ルーティング
# ================================
@app.route("/")
def index():
    obj = {
        "header_system_name": "認知症初期集中支援 業務支援システム",
        "header_page_name": "トップ",
        "footer_sd5": "プロジェクト演習 SD-5",
    }
    # ここはお好きなトップテンプレートに合わせて変えてOK
    return render_template("top.html", d=obj)


@app.route("/top")
def top():
    return render_template("top.html")


@app.route("/list")
def list_page():
    # 利用者一覧などを出したい場合はここで SELECT
    return render_template("list.html")


@app.route("/shousai")
def shousai():
    """
    5つのアセスメントシート（client / visit_record / physical_status / DASC21 / DBD13）
    をタブ切り替えで表示する詳細画面。
    """
    return render_template("shousai.html")


@app.route("/text")
def text():
    # 類似ケース検索用の画面など
    return render_template("text.html")


# ================================
#  2. テキストマイニング機能
# ================================
DATA_FILE = "cases.pkl"


def load_cases():
    """過去事例を読み込む（pickle）"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            return pickle.load(f)
    return []


def save_cases(cases):
    """過去事例を保存（pickle）"""
    with open(DATA_FILE, "wb") as f:
        pickle.dump(cases, f)


def fake_embedding(text: str):
    """ダミーの埋め込みベクトル（同じテキスト→同じベクトル）"""
    np.random.seed(abs(hash(text)) % (10**7))
    return np.random.rand(128)


def cosine_sim(a, b):
    """コサイン類似度"""
    return float(np.dot(a, b) / (norm(a) * norm(b)))


@app.route("/api/register_case", methods=["POST"])
def register_case():
    """
    （既存）事例登録 API
    body: { "visit_text": "...", "support_plan": "..." }
    """
    data = request.json
    visit_text = data.get("visit_text", "")
    support_plan = data.get("support_plan", "")

    cases = load_cases()
    new_case = {
        "visit_text": visit_text,
        "support_plan": support_plan,
        "embedding": fake_embedding(visit_text).tolist()
    }
    cases.append(new_case)
    save_cases(cases)
    return jsonify({"status": "ok"})


@app.route("/api/similar_cases", methods=["POST"])
def similar_cases():
    """
    （既存）類似事例検索 API
    body: { "visit_text": "..." }
    """
    input_text = request.json.get("visit_text", "")
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

    results = sorted(results, key=lambda x: x["similarity"], reverse=True)
    return jsonify(results[:3])


# ================================
#  3. アセスメントシート DB 保存用 API
# ================================
# 仕様：
# ・すべて「上書き保存」
# ・client_id 単位で 5テーブルとも 1レコードを持つ想定
# ・レコードが無ければ INSERT / あれば UPDATE（＝実質上書き）


# ------ 3-1. 利用者基本情報（client） ------
CLIENT_COLUMNS = [
    # client_id は別扱い（主キーではないがキーとして扱う）
    "writer_name",
    "consultation_date",
    "current_status",
    "client_name",
    "gender",
    "birth_date",
    "address",
    "phone_number",
    "disability_adl_level",
    "dementia_adl_level",
    "certification_info",
    "disability_certification",
    "living_environment",
    "economic_status",
    "visitor_name",
    "visitor_contact",
    "relation_to_client",
    "family_composition",
    "emergency_contact_name",
    "emergency_relation",
    "emergency_contact_info",
    "life_history",
    "daily_life_pattern",
    "time_of_day",
    "person_content",
    "caregiver_content",
    "hobbies",
    "social_connections",
    "disease_onset_date",
    "disease_name",
    "medical_institution",
    "medical_history",
    "current_condition",
    "public_services",
    "private_services",
]


@app.route("/api/save_client", methods=["POST"])
def save_client():
    """
    利用者基本情報を保存（client テーブル）
    body: {
       "client_id": "ABC001",
       "writer_name": "...",
       "consultation_date": "...",
       ...
       "private_services": "..."
    }
    """
    data = request.json or {}
    client_id = data.get("client_id")
    if not client_id:
        return jsonify({"status": "error", "message": "client_id がありません"}), 400

    # カラム順に値を並べる（存在しないキーは None）
    values = [data.get(col) for col in CLIENT_COLUMNS]

    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            # すでにその client_id のレコードがあるか確認
            cur.execute("SELECT client_id FROM client WHERE client_id = %s", (client_id,))
            row = cur.fetchone()

            if row:
                # UPDATE（上書き）
                set_clause = ", ".join([f"{col}=%s" for col in CLIENT_COLUMNS])
                sql = f"""
                    UPDATE client
                    SET {set_clause}
                    WHERE client_id = %s
                """
                cur.execute(sql, values + [client_id])
            else:
                # INSERT（新規）
                cols = ", ".join(["client_id"] + CLIENT_COLUMNS)
                placeholders = ", ".join(["%s"] * (1 + len(CLIENT_COLUMNS)))
                sql = f"""
                    INSERT INTO client ({cols})
                    VALUES ({placeholders})
                """
                cur.execute(sql, [client_id] + values)

        conn.commit()

    return jsonify({"status": "ok", "message": "保存しました"})


# ------ 3-2. 訪問記録表（visit_record） ------
VISIT_COLUMNS = [
    # visit_record_id は自動採番想定（あれば使ってもOK）
    # "visit_record_id",
    "client_id",
    "physical_status_id",   # 身体状況チェック表への FK（今は None でもOK）
    "visit_datetime",
    "visitor_name",
    "visit_purpose",
    "visit_condition",
    "support_decision",
    "future_plan",
]


@app.route("/api/save_visit_record", methods=["POST"])
def save_visit_record():
    """
    訪問記録を保存（visit_record テーブル）
    body: {
       "client_id": "ABC001",
       "physical_status_id": 1 or null,
       "visit_datetime": "2025-11-24 14:00",
       "visitor_name": "...",
       "visit_purpose": "...",
       "visit_condition": "...",
       "support_decision": "...",
       "future_plan": "..."
    }
    ・client_id で 1レコードを管理（既存あれば UPDATE）
    """
    data = request.json or {}
    client_id = data.get("client_id")
    if not client_id:
        return jsonify({"status": "error", "message": "client_id がありません"}), 400

    # 既存レコードを取得（client_id で 1件想定）
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT visit_record_id
                  FROM visit_record
                 WHERE client_id = %s
                 ORDER BY visit_record_id ASC
                 LIMIT 1
            """, (client_id,))
            row = cur.fetchone()

            values = [data.get(col) for col in VISIT_COLUMNS]  # client_id も含む

            if row:
                # UPDATE
                visit_record_id = row["visit_record_id"]
                set_clause = ", ".join([f"{col}=%s" for col in VISIT_COLUMNS])
                sql = f"""
                    UPDATE visit_record
                       SET {set_clause}
                     WHERE visit_record_id = %s
                """
                cur.execute(sql, values + [visit_record_id])
            else:
                # INSERT
                cols = ", ".join(VISIT_COLUMNS)
                placeholders = ", ".join(["%s"] * len(VISIT_COLUMNS))
                sql = f"""
                    INSERT INTO visit_record ({cols})
                    VALUES ({placeholders})
                """
                cur.execute(sql, values)

        conn.commit()

    return jsonify({"status": "ok", "message": "保存しました"})


# ------ 3-3. 身体状況チェック表（physical_status） ------
PHYSICAL_COLUMNS = [
    "client_id",
    "check_item",   # JSON 文字列でフォーム全部突っ込む想定
]


@app.route("/api/save_physical_status", methods=["POST"])
def save_physical_status():
    """
    身体状況チェック表を保存（physical_status）
    body: {
       "client_id": "ABC001",
       "check_item": {... 画面上の入力全部を入れたオブジェクト ...}
    }
    check_item は JSON 文字列として保存
    """
    data = request.json or {}
    client_id = data.get("client_id")
    if not client_id:
        return jsonify({"status": "error", "message": "client_id がありません"}), 400

    raw_check = data.get("check_item", {})
    # dict や list が来た場合は JSON 文字列にする
    if isinstance(raw_check, (dict, list)):
        check_item_str = json.dumps(raw_check, ensure_ascii=False)
    else:
        check_item_str = str(raw_check) if raw_check is not None else None

    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT physical_status_id
                  FROM physical_status
                 WHERE client_id = %s
                 ORDER BY physical_status_id ASC
                 LIMIT 1
            """, (client_id,))
            row = cur.fetchone()

            if row:
                # UPDATE
                physical_status_id = row["physical_status_id"]
                sql = """
                    UPDATE physical_status
                       SET check_item = %s
                     WHERE physical_status_id = %s
                """
                cur.execute(sql, (check_item_str, physical_status_id))
            else:
                # INSERT
                sql = """
                    INSERT INTO physical_status (client_id, check_item)
                    VALUES (%s, %s)
                """
                cur.execute(sql, (client_id, check_item_str))

        conn.commit()

    return jsonify({"status": "ok", "message": "保存しました"})


# ------ 3-4. DASC-21（dasc21） ------
DASC_COLUMNS = [
    "client_id",
    "informant_name",
    "evaluator_name",
    "assessment_item",  # 質問ごとの回答を JSON で保存
    "remarks",          # 備考も JSON で保存
    "total_score",
]


@app.route("/api/save_dasc21", methods=["POST"])
def save_dasc21():
    """
    DASC-21 を保存
    body: {
      "client_id": "ABC001",
      "informant_name": "...",
      "evaluator_name": "...",
      "assessment_item": { "q1": 2, "q2": 3, ... },
      "remarks": { "q1": "メモ", ... },
      "total_score": 42
    }
    """
    data = request.json or {}
    client_id = data.get("client_id")
    if not client_id:
        return jsonify({"status": "error", "message": "client_id がありません"}), 400

    def to_json_str(v):
        if isinstance(v, (dict, list)):
            return json.dumps(v, ensure_ascii=False)
        return str(v) if v is not None else None

    assessment_str = to_json_str(data.get("assessment_item"))
    remarks_str = to_json_str(data.get("remarks"))
    total_score = data.get("total_score")

    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT dasc_id
                  FROM dasc21
                 WHERE client_id = %s
                 ORDER BY dasc_id ASC
                 LIMIT 1
            """, (client_id,))
            row = cur.fetchone()

            if row:
                # UPDATE
                dasc_id = row["dasc_id"]
                sql = """
                    UPDATE dasc21
                       SET informant_name = %s,
                           evaluator_name = %s,
                           assessment_item = %s,
                           remarks = %s,
                           total_score = %s
                     WHERE dasc_id = %s
                """
                cur.execute(sql, (
                    data.get("informant_name"),
                    data.get("evaluator_name"),
                    assessment_str,
                    remarks_str,
                    total_score,
                    dasc_id
                ))
            else:
                # INSERT
                sql = """
                    INSERT INTO dasc21 (
                        client_id, informant_name, evaluator_name,
                        assessment_item, remarks, total_score
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """
                cur.execute(sql, (
                    client_id,
                    data.get("informant_name"),
                    data.get("evaluator_name"),
                    assessment_str,
                    remarks_str,
                    total_score
                ))

        conn.commit()

    return jsonify({"status": "ok", "message": "保存しました"})


# ------ 3-5. DBD-13（dbd13） ------
DBD_COLUMNS = [
    "client_id",
    "respondent_name",
    "evaluator_name",
    "entry_date",
    "assessment_item",    # JSON
    "remarks",            # JSON
    "subtotal_score",
    "total_score",
]


@app.route("/api/save_dbd13", methods=["POST"])
def save_dbd13():
    """
    DBD-13 を保存
    body: {
      "client_id": "ABC001",
      "respondent_name": "...",
      "evaluator_name": "...",
      "entry_date": "2025-11-24",
      "assessment_item": { "q1": 3, ... },
      "remarks": { "q1": "メモ", ... },
      "subtotal_score": 20,
      "total_score": 45
    }
    """
    data = request.json or {}
    client_id = data.get("client_id")
    if not client_id:
        return jsonify({"status": "error", "message": "client_id がありません"}), 400

    def to_json_str(v):
        if isinstance(v, (dict, list)):
            return json.dumps(v, ensure_ascii=False)
        return str(v) if v is not None else None

    assessment_str = to_json_str(data.get("assessment_item"))
    remarks_str = to_json_str(data.get("remarks"))

    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT dbd_id
                  FROM dbd13
                 WHERE client_id = %s
                 ORDER BY dbd_id ASC
                 LIMIT 1
            """, (client_id,))
            row = cur.fetchone()

            if row:
                # UPDATE
                dbd_id = row["dbd_id"]
                sql = """
                    UPDATE dbd13
                       SET respondent_name = %s,
                           evaluator_name = %s,
                           entry_date = %s,
                           assessment_item = %s,
                           remarks = %s,
                           subtotal_score = %s,
                           total_score = %s
                     WHERE dbd_id = %s
                """
                cur.execute(sql, (
                    data.get("respondent_name"),
                    data.get("evaluator_name"),
                    data.get("entry_date"),
                    assessment_str,
                    remarks_str,
                    data.get("subtotal_score"),
                    data.get("total_score"),
                    dbd_id
                ))
            else:
                # INSERT
                sql = """
                    INSERT INTO dbd13 (
                        client_id, respondent_name, evaluator_name,
                        entry_date, assessment_item, remarks,
                        subtotal_score, total_score
                    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """
                cur.execute(sql, (
                    client_id,
                    data.get("respondent_name"),
                    data.get("evaluator_name"),
                    data.get("entry_date"),
                    assessment_str,
                    remarks_str,
                    data.get("subtotal_score"),
                    data.get("total_score"),
                ))

        conn.commit()

    return jsonify({"status": "ok", "message": "保存しました"})


# ================================
#  4. 全シート一括取得 API（B-2 用）
# ================================
@app.route("/api/get_all_data")
def get_all_data():
    """
    クライアントID で 5つのシートのデータをまとめて取得
    GET /api/get_all_data?client_id=ABC001
    戻り値:
    {
      "client": {...} or null,
      "visit_record": {...} or null,
      "physical_status": {...} or null,
      "dasc21": {...} or null,
      "dbd13": {...} or null
    }
    """
    client_id = request.args.get("client_id")
    if not client_id:
        return jsonify({"status": "error", "message": "client_id がありません"}), 400

    result = {
        "client": None,
        "visit_record": None,
        "physical_status": None,
        "dasc21": None,
        "dbd13": None,
    }

    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            # client
            cur.execute("SELECT * FROM client WHERE client_id = %s LIMIT 1", (client_id,))
            result["client"] = cur.fetchone()

            # visit_record
            cur.execute("""
                SELECT * FROM visit_record
                 WHERE client_id = %s
                 ORDER BY visit_record_id ASC
                 LIMIT 1
            """, (client_id,))
            result["visit_record"] = cur.fetchone()

            # physical_status
            cur.execute("""
                SELECT * FROM physical_status
                 WHERE client_id = %s
                 ORDER BY physical_status_id ASC
                 LIMIT 1
            """, (client_id,))
            row = cur.fetchone()
            if row and row.get("check_item"):
                # JSON を dict に戻して渡す
                try:
                    row["check_item"] = json.loads(row["check_item"])
                except Exception:
                    pass
            result["physical_status"] = row

            # dasc21
            cur.execute("""
                SELECT * FROM dasc21
                 WHERE client_id = %s
                 ORDER BY dasc_id ASC
                 LIMIT 1
            """, (client_id,))
            row = cur.fetchone()
            if row:
                for key in ("assessment_item", "remarks"):
                    if row.get(key):
                        try:
                            row[key] = json.loads(row[key])
                        except Exception:
                            pass
            result["dasc21"] = row

            # dbd13
            cur.execute("""
                SELECT * FROM dbd13
                 WHERE client_id = %s
                 ORDER BY dbd_id ASC
                 LIMIT 1
            """, (client_id,))
            row = cur.fetchone()
            if row:
                for key in ("assessment_item", "remarks"):
                    if row.get(key):
                        try:
                            row[key] = json.loads(row[key])
                        except Exception:
                            pass
            result["dbd13"] = row

    return jsonify(result)


# ================================
#  実行
# ================================
if __name__ == "__main__":
    app.run(debug=True)
