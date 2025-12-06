from flask import Flask, render_template, request, jsonify
import numpy as np
from numpy.linalg import norm
import pickle
import os
import pymysql

app = Flask(__name__)

# ================================
#  DB 接続設定
# ================================
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",           # 必要に応じて変更
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
    # ここは自由に変えてOK（トップ or テンプレートなど）
    obj = {
        "header_system_name": "認知症初期支援業務管理システム",
        "header_page_name": "テンプレート",
        "footer_sd5": "プロジェクト演習  SD-5"
    }
    return render_template("template.html", d=obj)


@app.route("/top")
def top():
    return render_template("top.html")


@app.route("/list")
def list_page():
    return render_template("list.html")

@app.route("/touroku")
def touroku():
    return render_template("touroku.html")

@app.route("/shousai")
def shousai():
    # ?client_id=1 などのクエリは JS 側で拾って使う
    return render_template("shousai.html")

@app.route("/text")
def text():
    return render_template("text.html")

@app.route("/login")
def login():
    return render_template("login.html")

# 1. 画面ルーティング（ここまで）
# login() の下までが画面ルート

@app.route("/login")
def login():
    return render_template("login.html")

# >>> ここから登録処理を追加する <<<
@app.route("/register", methods=["POST"])
def register_post():
    admin_id = request.form["id"]
    password = request.form["password"]
    staff_name = request.form["staff_name"]

    hashed = generate_password_hash(password)

    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO admin (admin_id, password, staff_name) VALUES (%s, %s, %s)",
        (admin_id, hashed, staff_name)
    )
    db.commit()

    return redirect("/login")
# >>> ここまで追加 <<<

# ================================
#  2. テキストマイニング機能（既存）
# ================================
DATA_FILE = "cases.pkl"


def load_cases():
    """過去事例を読み込む（ローカル pickle）"""
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
    np.random.seed(abs(hash(text)) % (10 ** 7))
    return np.random.rand(128)


def cosine_sim(a, b):
    """コサイン類似度"""
    return float(np.dot(a, b) / (norm(a) * norm(b)))


@app.route("/api/register_case", methods=["POST"])
def register_case():
    """事例登録API（ローカル pickle 保存）"""
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
    """類似事例検索API"""
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
#  3. アセスメントシート DB API
# ================================

# ------- 共通ユーティリティ -------

def to_int_or_none(value):
    try:
        if value is None or value == "":
            return None
        return int(value)
    except (ValueError, TypeError):
        return None


def to_date_or_none(value):
    """
    <input type="date"> は 'YYYY-MM-DD' または '' が来る想定。
    空なら None を返す（NOT NULL の項目はフロント側で入力を必須にする想定）
    """
    if not value:
        return None
    return value  # そのまま渡す（MySQLが解釈できる形式前提）


def to_datetime_or_none(value):
    """
    datetime-local -> 'YYYY-MM-DDTHH:MM'
    MySQL DATETIME 用に 'YYYY-MM-DD HH:MM:00' に変換
    """
    if not value:
        return None
    v = value.replace("T", " ")
    if len(v) == 16:
        v = v + ":00"
    return v


# ------- client：利用者基本情報 -------

@app.route("/api/save_client", methods=["POST"])
def save_client():
    data = request.json or {}

    client_id = to_int_or_none(data.get("client_id"))

    writer_name = data.get("writer_name", "")
    consultation_date = to_date_or_none(data.get("consultation_date"))
    current_status = data.get("current_status", "")
    client_name = data.get("client_name", "")
    gender = data.get("gender", "")
    birth_date = to_date_or_none(data.get("birth_date"))
    address = data.get("address", "")
    phone_number = data.get("phone_number", "")
    disability_adl_level = data.get("disability_adl_level", "")
    dementia_adl_level = data.get("dementia_adl_level", "")
    certification_info = data.get("certification_info", "")
    disability_certification = data.get("disability_certification", "")
    living_environment = data.get("living_environment", "")
    economic_status = data.get("economic_status", "")
    visitor_name = data.get("visitor_name", "")
    visitor_contact = data.get("visitor_contact", "")
    relation_to_client = data.get("relation_to_client", "")
    family_composition = data.get("family_composition", "")
    emergency_contact_name = data.get("emergency_contact_name", "")
    emergency_relation = data.get("emergency_relation", "")
    emergency_contact_info = data.get("emergency_contact_info", "")
    life_history = data.get("life_history", "")
    daily_life_pattern = data.get("daily_life_pattern", "")
    time_of_day = data.get("time_of_day", "")
    person_content = data.get("person_content", "")
    caregiver_content = data.get("caregiver_content", "")
    hobbies = data.get("hobbies", "")
    social_connections = data.get("social_connections", "")
    disease_onset_date = to_date_or_none(data.get("disease_onset_date"))
    disease_name = data.get("disease_name", "")
    medical_institution = data.get("medical_institution", "")
    medical_history = data.get("medical_history", "")
    current_condition = data.get("current_condition", "")
    public_services = data.get("public_services", "")
    private_services = data.get("private_services", "")

    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            if client_id is not None:
                # 既存かチェック
                cur.execute(
                    "SELECT client_id FROM client WHERE client_id = %s",
                    (client_id,)
                )
                row = cur.fetchone()
            else:
                row = None

            if row:
                # UPDATE
                sql = """
                    UPDATE client
                       SET writer_name=%s,
                           consultation_date=%s,
                           current_status=%s,
                           client_name=%s,
                           gender=%s,
                           birth_date=%s,
                           address=%s,
                           phone_number=%s,
                           disability_adl_level=%s,
                           dementia_adl_level=%s,
                           certification_info=%s,
                           disability_certification=%s,
                           living_environment=%s,
                           economic_status=%s,
                           visitor_name=%s,
                           visitor_contact=%s,
                           relation_to_client=%s,
                           family_composition=%s,
                           emergency_contact_name=%s,
                           emergency_relation=%s,
                           emergency_contact_info=%s,
                           life_history=%s,
                           daily_life_pattern=%s,
                           time_of_day=%s,
                           person_content=%s,
                           caregiver_content=%s,
                           hobbies=%s,
                           social_connections=%s,
                           disease_onset_date=%s,
                           disease_name=%s,
                           medical_institution=%s,
                           medical_history=%s,
                           current_condition=%s,
                           public_services=%s,
                           private_services=%s
                     WHERE client_id=%s
                """
                cur.execute(sql, (
                    writer_name, consultation_date, current_status,
                    client_name, gender, birth_date, address, phone_number,
                    disability_adl_level, dementia_adl_level,
                    certification_info, disability_certification,
                    living_environment, economic_status,
                    visitor_name, visitor_contact, relation_to_client,
                    family_composition, emergency_contact_name,
                    emergency_relation, emergency_contact_info,
                    life_history, daily_life_pattern, time_of_day,
                    person_content, caregiver_content, hobbies,
                    social_connections, disease_onset_date, disease_name,
                    medical_institution, medical_history,
                    current_condition, public_services, private_services,
                    client_id
                ))
            else:
                # INSERT
                sql = """
                    INSERT INTO client (
                        writer_name, consultation_date, current_status,
                        client_name, gender, birth_date, address, phone_number,
                        disability_adl_level, dementia_adl_level,
                        certification_info, disability_certification,
                        living_environment, economic_status,
                        visitor_name, visitor_contact, relation_to_client,
                        family_composition, emergency_contact_name,
                        emergency_relation, emergency_contact_info,
                        life_history, daily_life_pattern, time_of_day,
                        person_content, caregiver_content, hobbies,
                        social_connections, disease_onset_date, disease_name,
                        medical_institution, medical_history,
                        current_condition, public_services, private_services
                    )
                    VALUES (
                        %s,%s,%s,
                        %s,%s,%s,%s,%s,
                        %s,%s,
                        %s,%s,
                        %s,%s,
                        %s,%s,%s,
                        %s,%s,
                        %s,%s,
                        %s,%s,%s,
                        %s,%s,%s,
                        %s,%s,%s,
                        %s,%s,
                        %s,%s,%s
                    )
                """
                cur.execute(sql, (
                    writer_name, consultation_date, current_status,
                    client_name, gender, birth_date, address, phone_number,
                    disability_adl_level, dementia_adl_level,
                    certification_info, disability_certification,
                    living_environment, economic_status,
                    visitor_name, visitor_contact, relation_to_client,
                    family_composition, emergency_contact_name,
                    emergency_relation, emergency_contact_info,
                    life_history, daily_life_pattern, time_of_day,
                    person_content, caregiver_content, hobbies,
                    social_connections, disease_onset_date, disease_name,
                    medical_institution, medical_history,
                    current_condition, public_services, private_services
                ))
                client_id = cur.lastrowid

        conn.commit()

    return jsonify({"status": "saved", "client_id": client_id})


# ------- visit_record：訪問記録（1クライアント1件を上書き） -------

@app.route("/api/save_visit_record", methods=["POST"])
def save_visit_record():
    data = request.json
    cid = data.get("client_id")

    if not cid:
        return jsonify({"status": "error", "message": "client_id がありません"}), 400

    conn = get_connection()
    with conn:
        with conn.cursor() as cur:

            # 既存レコードがあるか？
            cur.execute("SELECT visit_record_id FROM visit_record WHERE client_id=%s", (cid,))
            row = cur.fetchone()

            if row:
                # 既存 → UPDATE
                sql = """
                    UPDATE visit_record SET
                        visit_datetime=%s,
                        visitor_name=%s,
                        visit_purpose=%s,
                        visit_condition=%s,
                        support_decision=%s,
                        future_plan=%s
                    WHERE client_id=%s
                """
                cur.execute(sql, (
                    data.get("visit_datetime"),
                    data.get("visitor_name"),
                    data.get("visit_purpose"),
                    data.get("visit_condition"),
                    data.get("support_decision"),
                    data.get("future_plan"),
                    cid
                ))
            else:
                # 新規 → INSERT
                sql = """
                    INSERT INTO visit_record (
                        client_id, visit_datetime, visitor_name,
                        visit_purpose, visit_condition,
                        support_decision, future_plan
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cur.execute(sql, (
                    cid,
                    data.get("visit_datetime"),
                    data.get("visitor_name"),
                    data.get("visit_purpose"),
                    data.get("visit_condition"),
                    data.get("support_decision"),
                    data.get("future_plan")
                ))

        conn.commit()

    return jsonify({"status": "saved"})


# ------- physical_status：身体状況チェック（1クライアント1件上書き） -------

@app.route("/api/save_physical_status", methods=["POST"])
def save_physical_status():
    data = request.json
    cid = data.get("client_id")

    if not cid:
        return jsonify({"status": "error", "message": "client_id がありません"}), 400

    conn = get_connection()
    with conn:
        with conn.cursor() as cur:

            # 既存レコードを確認
            cur.execute("SELECT physical_status_id FROM physical_status WHERE client_id=%s", (cid,))
            row = cur.fetchone()

            if row:
                # UPDATE
                sql = """
                    UPDATE physical_status SET
                        check_item=%s
                    WHERE client_id=%s
                """
                cur.execute(sql, (data.get("check_item"), cid))
            else:
                # INSERT
                sql = """
                    INSERT INTO physical_status (client_id, check_item)
                    VALUES (%s, %s)
                """
                cur.execute(sql, (cid, data.get("check_item")))

        conn.commit()

    return jsonify({"status": "saved"})


# ------- dasc21：DASC-21（B：毎回追加） -------

@app.route("/api/save_dasc21", methods=["POST"])
def save_dasc21():
    data = request.json or {}

    client_id = to_int_or_none(data.get("client_id"))
    if client_id is None:
        return jsonify({"status": "error", "message": "client_id がありません"}), 400

    informant_name = data.get("informant_name", "")
    evaluator_name = data.get("evaluator_name", "")
    assessment_item = data.get("assessment_item", "")
    remarks = data.get("remarks", "")
    total_score = to_int_or_none(data.get("total_score")) or 0

    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            sql = """
                INSERT INTO dasc21 (
                    client_id, informant_name, evaluator_name,
                    assessment_item, remarks, total_score
                )
                VALUES (%s,%s,%s,%s,%s,%s)
            """
            cur.execute(sql, (
                client_id, informant_name, evaluator_name,
                assessment_item, remarks, total_score
            ))
            dasc_id = cur.lastrowid
        conn.commit()

    return jsonify({"status": "saved", "dasc_id": dasc_id})


# ------- dbd13：DBD-13（B：毎回追加） -------

@app.route("/api/save_dbd13", methods=["POST"])
def save_dbd13():
    data = request.json or {}

    client_id = to_int_or_none(data.get("client_id"))
    if client_id is None:
        return jsonify({"status": "error", "message": "client_id がありません"}), 400

    respondent_name = data.get("respondent_name", "")
    evaluator_name = data.get("evaluator_name", "")
    entry_date = to_date_or_none(data.get("entry_date"))
    assessment_item = data.get("assessment_item", "")
    remarks = data.get("remarks", "")
    subtotal_score = to_int_or_none(data.get("subtotal_score")) or 0
    total_score = to_int_or_none(data.get("total_score")) or 0

    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            sql = """
                INSERT INTO dbd13 (
                    client_id, respondent_name, evaluator_name, entry_date,
                    assessment_item, remarks, subtotal_score, total_score
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """
            cur.execute(sql, (
                client_id, respondent_name, evaluator_name, entry_date,
                assessment_item, remarks, subtotal_score, total_score
            ))
            dbd_id = cur.lastrowid
        conn.commit()

    return jsonify({"status": "saved", "dbd_id": dbd_id})


# ------- shousai 画面用：一括取得API -------

@app.route("/api/get_all_data")
def get_all_data():
    client_id = to_int_or_none(request.args.get("client_id"))
    if client_id is None:
        return jsonify({"status": "error", "message": "client_id がありません"}), 400

    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            # client
            cur.execute("SELECT * FROM client WHERE client_id=%s", (client_id,))
            client = cur.fetchone()

            # visit_record（最新1件）
            cur.execute(
                "SELECT * FROM visit_record WHERE client_id=%s ORDER BY visit_record_id DESC LIMIT 1",
                (client_id,)
            )
            visit_record = cur.fetchone()

            # physical_status（1件）
            cur.execute(
                "SELECT * FROM physical_status WHERE client_id=%s ORDER BY physical_status_id DESC LIMIT 1",
                (client_id,)
            )
            physical_status = cur.fetchone()

            # dasc21（最新1件）
            cur.execute(
                "SELECT * FROM dasc21 WHERE client_id=%s ORDER BY dasc_id DESC LIMIT 1",
                (client_id,)
            )
            dasc21_row = cur.fetchone()

            # dbd13（最新1件）
            cur.execute(
                "SELECT * FROM dbd13 WHERE client_id=%s ORDER BY dbd_id DESC LIMIT 1",
                (client_id,)
            )
            dbd13_row = cur.fetchone()

    return jsonify({
        "status": "ok",
        "client": client,
        "visit_record": visit_record,
        "physical_status": physical_status,
        "dasc21": dasc21_row,
        "dbd13": dbd13_row
    })

# ================================
#  4. 共有フォルダ（ファイル管理）
# ================================

from flask import send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# フォルダなければ作成
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -------------------------
# ⑥ ファイルアップロード
# -------------------------
@app.route("/api/upload_file", methods=["POST"])
def upload_file():
    client_id = request.form.get("client_id")
    file = request.files.get("file")

    if not client_id:
        return jsonify({"status": "error", "message": "client_id がありません"}), 400
    if not file:
        return jsonify({"status": "error", "message": "ファイルがありません"}), 400

    # 保存先：/uploads/<client_id>/
    client_folder = os.path.join(app.config["UPLOAD_FOLDER"], str(client_id))
    os.makedirs(client_folder, exist_ok=True)

    filename = secure_filename(file.filename)
    save_path = os.path.join(client_folder, filename)
    file.save(save_path)

    # DB 登録
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            sql = """
                INSERT INTO shared_folder (client_id, file_path)
                VALUES (%s, %s)
            """
            cur.execute(sql, (client_id, f"{client_id}/{filename}"))
        conn.commit()

    return jsonify({"status": "saved"})


# -------------------------
# ⑦ ファイル一覧取得
# -------------------------
@app.route("/api/files", methods=["GET"])
def get_files():
    client_id = request.args.get("client_id")

    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT folder_id, file_path, uploaded_at FROM shared_folder WHERE client_id=%s",
                (client_id,)
            )
            files = cur.fetchall()

    return jsonify({"status": "ok", "files": files})


# -------------------------
# ⑧ ファイル削除
# -------------------------
@app.route("/api/delete_file", methods=["POST"])
def delete_file():
    folder_id = request.json.get("folder_id")

    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT file_path FROM shared_folder WHERE folder_id=%s", (folder_id,))
            row = cur.fetchone()

            if not row:
                return jsonify({"status": "error", "message": "ファイルが存在しません"}), 404

            file_path = row["file_path"]

            # DB から削除
            cur.execute("DELETE FROM shared_folder WHERE folder_id=%s", (folder_id,))
        conn.commit()

    # 実ファイルも削除
    actual = os.path.join(app.config["UPLOAD_FOLDER"], file_path)
    if os.path.exists(actual):
        os.remove(actual)

    return jsonify({"status": "deleted"})


# -------------------------
# ⑨ ファイルダウンロード
# -------------------------
@app.route("/uploads/<path:filepath>")
def uploaded_file(filepath):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filepath, as_attachment=True)

# ================================
#  Flask 実行
# ================================
if __name__ == "__main__":
    app.run(debug=True)
