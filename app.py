from flask import Flask, render_template, request, jsonify
import pymysql
from datetime import datetime

app = Flask(__name__)

# ================================
# ✅ DB接続設定（あなたの環境に合わせ済み）
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
# ✅ ページ表示ルーティング
# ================================
@app.route("/")
def index():
    return render_template("top.html")

@app.route("/shousai")
def shousai():
    return render_template("shousai.html")


# =====================================================
# ✅ 1) 利用者基本情報（client）保存 API
# =====================================================
@app.route("/api/save_client", methods=["POST"])
def save_client():
    data = request.json

    sql = """
        INSERT INTO client (
            writer_name, consultation_date, current_status,
            resident_name, gender, phone_number
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """

    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute(sql, (
                data["writer_name"],
                data["consultation_date"],
                data["current_status"],
                data["resident_name"],
                data["gender"],
                data["phone_number"]
            ))
        conn.commit()

    return jsonify({"status": "saved"})


# =====================================================
# ✅ 2) 訪問記録（visit_record）保存 API
# =====================================================
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


# =====================================================
# ✅ 3) 身体状況チェック（physical_status）保存 API
# =====================================================
@app.route("/api/save_physical_status", methods=["POST"])
def save_physical_status():
    data = request.json

    sql = """
        INSERT INTO physical_status (
            client_id, check_item
        ) VALUES (%s, %s)
    """

    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute(sql, (
                data["client_id"],
                data["check_item"]
            ))
        conn.commit()

    return jsonify({"status": "saved"})


# =====================================================
# ✅ 4) DASC-21 保存 API
# =====================================================
@app.route("/api/save_dasc21", methods=["POST"])
def save_dasc21():
    data = request.json

    sql = """
        INSERT INTO dasc21 (
            client_id, respondent_name, evaluator_name,
            assessment_date, total_score
        ) VALUES (%s, %s, %s, %s, %s)
    """

    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute(sql, (
                data["client_id"],
                data["respondent_name"],
                data["evaluator_name"],
                data["assessment_date"],
                data["total_score"]
            ))
        conn.commit()

    return jsonify({"status": "saved"})


# =====================================================
# ✅ 5) DBD-13 保存 API
# =====================================================
@app.route("/api/save_dbd13", methods=["POST"])
def save_dbd13():
    data = request.json

    sql = """
        INSERT INTO dbd13 (
            client_id, respondent_name, evaluator_name,
            assessment_date, total_score
        ) VALUES (%s, %s, %s, %s, %s)
    """

    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute(sql, (
                data["client_id"],
                data["respondent_name"],
                data["evaluator_name"],
                data["assessment_date"],
                data["total_score"]
            ))
        conn.commit()

    return jsonify({"status": "saved"})


# ================================
# ✅ Flask 実行
# ================================
if __name__ == "__main__":
    app.run(debug=True)
