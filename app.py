from flask import Flask, render_template, request, jsonify, redirect, send_file
import numpy as np
from numpy.linalg import norm
import pickle
import os
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from datetime import datetime

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

@app.route("/login", methods=["GET", "POST"])
def login_post():
    if request.method == "POST":
        admin_id = request.form.get("id")
        password = request.form.get("password")

        db = get_connection()
        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM admin WHERE admin_id=%s", (admin_id,))
            admin = cursor.fetchone()
        finally:
            db.close()

        if not admin:
            return "ID が存在しません"
        if not check_password_hash(admin['password'], password):
            return "パスワードが違います"

        # ログイン成功 - トップページへリダイレクト
        return redirect("/top")

    # GET の場合はログイン画面を表示
    return render_template("login.html")

@app.route("/register", methods=["POST"])
def register_post():
    # フォームから値を取得
    admin_id = request.form.get("id")
    password = request.form.get("password")
    password2 = request.form.get("password2")

    # 入力チェック
    if not admin_id or not password:
        return "ID またはパスワードが入力されていません"

    if password != password2:
        return "パスワードが一致しません"

    # パスワードをハッシュ化
    hashed = generate_password_hash(password)

    # DB登録
    db = get_connection()
    try:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO admin (admin_id, password, staff_name) VALUES (%s, %s, %s)",
            (admin_id, hashed, "未設定")
        )
        db.commit()
    except Exception as e:
        db.rollback()
        return f"登録エラー: {e}"
    finally:
        db.close()

    # 登録成功したらログイン画面へ
    return redirect("/login")

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
        case_emb = np.array(case["embedding"])
        sim = cosine_sim(input_emb, case_emb)
        results.append({
            "similarity": round(sim, 3),
            "visit_text": case["visit_text"],
            "support_plan": case["support_plan"]
        })

    results = sorted(results, key=lambda x: x["similarity"], reverse=True)
    return jsonify(results[:3])


# ================================
#  2.5 TF-IDF ベースのテキストマイニング
# ================================

def extract_keywords(text, top_n=10):
    """テキストからキーワードを抽出（TF-IDF上位語）"""
    if not text or not text.strip():
        return []
    
    words = re.findall(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]+', text)
    if not words:
        return []
    
    word_freq = {}
    for word in words:
        if len(word) >= 2:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [w[0] for w in sorted_words[:top_n]]


def get_visit_records_for_tfidf():
    """DBから訪問記録を取得してTF-IDF用のドキュメントを作成"""
    conn = get_connection()
    records = []
    
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    visit_record_id,
                    client_id,
                    COALESCE(reaction_understanding, '') as reaction,
                    COALESCE(cognitive_function, '') as cognitive,
                    COALESCE(psychiatric_symptoms, '') as psychiatric,
                    COALESCE(physical_condition, '') as physical,
                    COALESCE(living_situation, '') as living,
                    COALESCE(person_wishes, '') as person_wishes,
                    COALESCE(caregiver_wishes, '') as caregiver_wishes,
                    COALESCE(judgment_support, '') as judgment
                FROM visit_record
                WHERE reaction_understanding IS NOT NULL 
                   OR cognitive_function IS NOT NULL
                   OR psychiatric_symptoms IS NOT NULL
            """)
            rows = cur.fetchall()
            
            for row in rows:
                combined_text = " ".join([
                    str(row.get("reaction", "")),
                    str(row.get("cognitive", "")),
                    str(row.get("psychiatric", "")),
                    str(row.get("physical", "")),
                    str(row.get("living", "")),
                    str(row.get("person_wishes", "")),
                    str(row.get("caregiver_wishes", ""))
                ])
                
                if combined_text.strip():
                    records.append({
                        "id": row["visit_record_id"],
                        "client_id": row["client_id"],
                        "text": combined_text,
                        "policy": str(row.get("judgment", ""))
                    })
    
    return records


@app.route("/api/search_similar", methods=["POST"])
def search_similar():
    """TF-IDFベースの類似事例検索API"""
    data = request.json or {}
    
    input_parts = [
        data.get("know", ""),
        data.get("ninchi_kinou", ""),
        data.get("symptom", ""),
        data.get("body_con", ""),
        data.get("life_con", ""),
        data.get("honnin_will", ""),
        data.get("kangosha_will", "")
    ]
    input_text = " ".join(input_parts)
    
    if not input_text.strip():
        return jsonify({"results": [], "keywords": []})
    
    keywords = extract_keywords(input_text, top_n=8)
    
    records = get_visit_records_for_tfidf()
    
    if not records:
        return jsonify({
            "results": [],
            "keywords": keywords,
            "message": "事例データがありません。訪問記録を登録してください。"
        })
    
    corpus = [r["text"] for r in records]
    corpus.append(input_text)
    
    try:
        vectorizer = TfidfVectorizer(
            analyzer='char',
            ngram_range=(2, 4),
            max_features=1000
        )
        tfidf_matrix = vectorizer.fit_transform(corpus)
        
        input_vector = tfidf_matrix[-1]
        doc_vectors = tfidf_matrix[:-1]
        
        similarities = cosine_similarity(input_vector, doc_vectors)[0]
        
        results = []
        for i, sim in enumerate(similarities):
            if sim > 0.01:
                results.append({
                    "similarity": round(sim * 100, 1),
                    "text": records[i]["text"][:500],
                    "policy": records[i]["policy"][:500] if records[i]["policy"] else "支援方針未登録",
                    "client_id": records[i]["client_id"]
                })
        
        results = sorted(results, key=lambda x: x["similarity"], reverse=True)[:5]
        
    except Exception as e:
        return jsonify({
            "results": [],
            "keywords": keywords,
            "error": str(e)
        })
    
    return jsonify({
        "results": results,
        "keywords": keywords
    })


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


# ------- 対象者一覧取得API -------

@app.route("/api/get_clients")
def get_clients():
    """対象者一覧を取得"""
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT client_id, client_name, gender, consultation_date, current_status
                FROM client
                ORDER BY client_id DESC
            """)
            clients = cur.fetchall()

    return jsonify({"status": "ok", "clients": clients})


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
#  5. Excel出力API
# ================================

def create_excel_styles():
    """共通のExcelスタイルを作成"""
    header_font = Font(bold=True, size=12)
    header_fill = PatternFill(start_color="E8F4FC", end_color="E8F4FC", fill_type="solid")
    title_font = Font(bold=True, size=14)
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    center_align = Alignment(horizontal='center', vertical='center')
    left_align = Alignment(horizontal='left', vertical='center', wrap_text=True)
    return {
        'header_font': header_font,
        'header_fill': header_fill,
        'title_font': title_font,
        'thin_border': thin_border,
        'center_align': center_align,
        'left_align': left_align
    }


@app.route("/api/export_client", methods=["GET"])
def export_client():
    """利用者基本情報をExcelで出力"""
    client_id = request.args.get("client_id")
    if not client_id:
        return jsonify({"status": "error", "message": "client_id が必要です"}), 400

    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM client WHERE client_id = %s", (client_id,))
            data = cur.fetchone()

    if not data:
        return jsonify({"status": "error", "message": "データが見つかりません"}), 404

    wb = Workbook()
    ws = wb.active
    ws.title = "利用者基本情報"
    styles = create_excel_styles()

    ws.merge_cells('A1:D1')
    ws['A1'] = "利用者基本情報"
    ws['A1'].font = styles['title_font']
    ws['A1'].alignment = styles['center_align']

    fields = [
        ("氏名", data.get("name", "")),
        ("フリガナ", data.get("furigana", "")),
        ("生年月日", str(data.get("birth_date", "")) if data.get("birth_date") else ""),
        ("性別", data.get("gender", "")),
        ("住所", data.get("address", "")),
        ("電話番号", data.get("phone", "")),
        ("緊急連絡先", data.get("emergency_contact", "")),
        ("緊急連絡先電話", data.get("emergency_phone", "")),
        ("主治医・医療機関", data.get("medical_institution", "")),
        ("既往歴", data.get("medical_history", "")),
        ("現在の状態・経過", data.get("current_condition", "")),
        ("現在利用中の公的サービス", data.get("public_services", "")),
        ("現在利用中の非公的サービス", data.get("private_services", "")),
    ]

    for i, (label, value) in enumerate(fields, start=3):
        ws.cell(row=i, column=1, value=label).font = styles['header_font']
        ws.cell(row=i, column=1).fill = styles['header_fill']
        ws.cell(row=i, column=1).border = styles['thin_border']
        ws.cell(row=i, column=2, value=value).border = styles['thin_border']
        ws.cell(row=i, column=2).alignment = styles['left_align']

    ws.column_dimensions['A'].width = 25
    ws.column_dimensions['B'].width = 50

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    filename = f"client_{client_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     as_attachment=True, download_name=filename)


@app.route("/api/export_visit", methods=["GET"])
def export_visit():
    """訪問記録表をExcelで出力"""
    client_id = request.args.get("client_id")
    if not client_id:
        return jsonify({"status": "error", "message": "client_id が必要です"}), 400

    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM visit_record WHERE client_id = %s ORDER BY visit_datetime DESC LIMIT 1", (client_id,))
            data = cur.fetchone()

    if not data:
        return jsonify({"status": "error", "message": "データが見つかりません"}), 404

    wb = Workbook()
    ws = wb.active
    ws.title = "訪問記録表"
    styles = create_excel_styles()

    ws.merge_cells('A1:D1')
    ws['A1'] = "訪問記録表"
    ws['A1'].font = styles['title_font']
    ws['A1'].alignment = styles['center_align']

    fields = [
        ("訪問日時", str(data.get("visit_datetime", "")) if data.get("visit_datetime") else ""),
        ("訪問者氏名", data.get("visitor_name", "")),
        ("訪問目的", data.get("visit_purpose", "")),
        ("訪問に対する本人の反応・理解", data.get("vr_reaction", "")),
        ("認知機能", data.get("vr_cognition", "")),
        ("生活状況", data.get("vr_living", "")),
        ("身体状況", data.get("vr_physical", "")),
        ("精神状態", data.get("vr_mental", "")),
        ("服薬状況", data.get("vr_medication", "")),
        ("判断・支援内容", data.get("support_decision", "")),
        ("今後の方針・支援計画", data.get("future_plan", "")),
    ]

    for i, (label, value) in enumerate(fields, start=3):
        ws.cell(row=i, column=1, value=label).font = styles['header_font']
        ws.cell(row=i, column=1).fill = styles['header_fill']
        ws.cell(row=i, column=1).border = styles['thin_border']
        ws.cell(row=i, column=2, value=value).border = styles['thin_border']
        ws.cell(row=i, column=2).alignment = styles['left_align']

    ws.column_dimensions['A'].width = 30
    ws.column_dimensions['B'].width = 60

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    filename = f"visit_{client_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     as_attachment=True, download_name=filename)


@app.route("/api/export_physical", methods=["GET"])
def export_physical():
    """身体状況チェック表をExcelで出力"""
    client_id = request.args.get("client_id")
    if not client_id:
        return jsonify({"status": "error", "message": "client_id が必要です"}), 400

    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM physical_status WHERE client_id = %s ORDER BY physical_id DESC LIMIT 1", (client_id,))
            data = cur.fetchone()

    if not data:
        return jsonify({"status": "error", "message": "データが見つかりません"}), 404

    wb = Workbook()
    ws = wb.active
    ws.title = "身体状況チェック表"
    styles = create_excel_styles()

    ws.merge_cells('A1:D1')
    ws['A1'] = "身体状況チェック表"
    ws['A1'].font = styles['title_font']
    ws['A1'].alignment = styles['center_align']

    fields = [
        ("立ち上がり・運動機能", data.get("ps_mobility", "")),
        ("歩行状況・歩行レベル", data.get("ps_walking", "")),
        ("移動方法・範囲", data.get("ps_transport", "")),
        ("意思疎通", data.get("ps_communication", "")),
        ("視力", data.get("ps_vision", "")),
        ("聴力", data.get("ps_hearing", "")),
        ("食事", data.get("ps_eating", "")),
        ("排泄", data.get("ps_toilet", "")),
        ("入浴", data.get("ps_bathing", "")),
        ("睡眠", data.get("ps_sleep", "")),
        ("服薬管理", data.get("ps_medication", "")),
        ("金銭管理", data.get("ps_money", "")),
        ("家族の介護力", data.get("ps_family_care", "")),
        ("虐待の可能性", data.get("ps_abuse", "")),
        ("見守りの状況", data.get("ps_watch", "")),
        ("緊急時のSOS発信", data.get("ps_sos", "")),
    ]

    for i, (label, value) in enumerate(fields, start=3):
        ws.cell(row=i, column=1, value=label).font = styles['header_font']
        ws.cell(row=i, column=1).fill = styles['header_fill']
        ws.cell(row=i, column=1).border = styles['thin_border']
        ws.cell(row=i, column=2, value=value or "").border = styles['thin_border']
        ws.cell(row=i, column=2).alignment = styles['left_align']

    ws.column_dimensions['A'].width = 25
    ws.column_dimensions['B'].width = 60

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    filename = f"physical_{client_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     as_attachment=True, download_name=filename)


@app.route("/api/export_dasc21", methods=["GET"])
def export_dasc21():
    """DASC-21をExcelで出力"""
    client_id = request.args.get("client_id")
    if not client_id:
        return jsonify({"status": "error", "message": "client_id が必要です"}), 400

    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM dasc21 WHERE client_id = %s ORDER BY dasc_id DESC LIMIT 1", (client_id,))
            data = cur.fetchone()

    if not data:
        return jsonify({"status": "error", "message": "データが見つかりません"}), 404

    wb = Workbook()
    ws = wb.active
    ws.title = "DASC-21"
    styles = create_excel_styles()

    ws.merge_cells('A1:F1')
    ws['A1'] = "DASC-21 地域包括ケアシステムにおける認知症アセスメントシート"
    ws['A1'].font = styles['title_font']
    ws['A1'].alignment = styles['center_align']

    ws['A3'] = "情報提供者氏名"
    ws['B3'] = data.get("informant_name", "")
    ws['C3'] = "評価者氏名"
    ws['D3'] = data.get("evaluator_name", "")
    for col in ['A', 'B', 'C', 'D']:
        ws[f'{col}3'].border = styles['thin_border']

    ws['A5'] = "評価基準: 1=問題なくできる 2=だいたいできる 3=あまりできない 4=できない"
    ws['A5'].font = Font(italic=True, size=10)

    dasc_items = [
        ("A. 記憶", [
            ("1", "財布や鍵など、物を置いた場所がわからなくなることがありますか"),
            ("2", "5分前に聞いた話を思い出せないことがありますか"),
            ("3", "自分の生年月日がわからなくなることがありますか"),
        ]),
        ("B. 見当識", [
            ("4", "今日が何月何日かわからないときがありますか"),
            ("5", "自分のいる場所がどこだかわからなくなることがありますか"),
            ("6", "道に迷って家に帰ってこられなくなることがありますか"),
        ]),
        ("C. 問題解決・判断力", [
            ("7", "電気やガスや水道が止まってしまったときに、自分で適切に対処できますか"),
            ("8", "一日の計画を自分で立てることができますか"),
            ("9", "季節や状況に合った服を自分で選ぶことができますか"),
        ]),
        ("D. 家庭外のIADL", [
            ("10", "バスや電車、自家用車などを使って一人で外出できますか"),
            ("11", "貯金の出し入れや、家賃や公共料金の支払いは一人でできますか"),
        ]),
        ("E. 家庭内のIADL", [
            ("12", "薬を決まった時間に決まった分量のむことはできますか"),
            ("13", "電話をかけることができますか"),
            ("14", "自分で食事の準備はできますか"),
            ("15", "自分で、掃除機やほうきを使って掃除ができますか"),
            ("16", "自分で洗濯ができますか"),
        ]),
        ("F. 身体的ADL", [
            ("17", "自分で適切な量の食事をとることはできますか"),
            ("18", "入浴は一人でできますか"),
            ("19", "トイレは一人でできますか"),
            ("20", "身だしなみを整えることは一人でできますか"),
            ("21", "一人で外出できますか"),
        ]),
    ]

    row = 7
    headers = ["No.", "評価項目", "1", "2", "3", "4", "評価"]
    for col, header in enumerate(headers, start=1):
        cell = ws.cell(row=row, column=col, value=header)
        cell.font = styles['header_font']
        cell.fill = styles['header_fill']
        cell.border = styles['thin_border']
        cell.alignment = styles['center_align']
    row += 1

    for category, items in dasc_items:
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=7)
        cell = ws.cell(row=row, column=1, value=category)
        cell.font = Font(bold=True, color="2C5282")
        cell.fill = PatternFill(start_color="E8F4FC", end_color="E8F4FC", fill_type="solid")
        cell.border = styles['thin_border']
        row += 1

        for num, question in items:
            score = data.get(f"q{num}", "")
            ws.cell(row=row, column=1, value=num).border = styles['thin_border']
            ws.cell(row=row, column=1).alignment = styles['center_align']
            ws.cell(row=row, column=2, value=question).border = styles['thin_border']
            ws.cell(row=row, column=2).alignment = styles['left_align']
            for i, val in enumerate([1, 2, 3, 4], start=3):
                cell = ws.cell(row=row, column=i, value="○" if score == val else "")
                cell.border = styles['thin_border']
                cell.alignment = styles['center_align']
            ws.cell(row=row, column=7, value=score if score else "").border = styles['thin_border']
            ws.cell(row=row, column=7).alignment = styles['center_align']
            row += 1

    row += 1
    ws.cell(row=row, column=1, value="合計点").font = styles['header_font']
    ws.cell(row=row, column=2, value=data.get("total_score", ""))
    ws.cell(row=row, column=3, value="（21〜84点、31点以上で認知症の疑い）")

    row += 1
    ws.cell(row=row, column=1, value="備考").font = styles['header_font']
    ws.cell(row=row, column=2, value=data.get("remarks", ""))

    ws.column_dimensions['A'].width = 8
    ws.column_dimensions['B'].width = 55
    for col in ['C', 'D', 'E', 'F']:
        ws.column_dimensions[col].width = 6
    ws.column_dimensions['G'].width = 8

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    filename = f"dasc21_{client_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     as_attachment=True, download_name=filename)


@app.route("/api/export_dbd13", methods=["GET"])
def export_dbd13():
    """DBD-13をExcelで出力"""
    client_id = request.args.get("client_id")
    if not client_id:
        return jsonify({"status": "error", "message": "client_id が必要です"}), 400

    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM dbd13 WHERE client_id = %s ORDER BY dbd_id DESC LIMIT 1", (client_id,))
            data = cur.fetchone()

    if not data:
        return jsonify({"status": "error", "message": "データが見つかりません"}), 404

    wb = Workbook()
    ws = wb.active
    ws.title = "DBD-13"
    styles = create_excel_styles()

    ws.merge_cells('A1:G1')
    ws['A1'] = "DBD-13 認知症行動障害尺度（短縮版）"
    ws['A1'].font = styles['title_font']
    ws['A1'].alignment = styles['center_align']

    ws['A3'] = "回答者氏名"
    ws['B3'] = data.get("respondent_name", "")
    ws['C3'] = "評価者氏名"
    ws['D3'] = data.get("evaluator_name", "")
    ws['E3'] = "記入日"
    ws['F3'] = str(data.get("entry_date", "")) if data.get("entry_date") else ""
    for col in ['A', 'B', 'C', 'D', 'E', 'F']:
        ws[f'{col}3'].border = styles['thin_border']

    ws['A5'] = "評価基準: 0=全くない 1=ほとんどない 2=ときどきある 3=よくある 4=常にある"
    ws['A5'].font = Font(italic=True, size=10)

    dbd_items = [
        ("1", "同じことを何度も何度も聞く"),
        ("2", "よく物をなくしたり、置き場所を間違えたり、隠したりしている"),
        ("3", "日常的な物事に関心を示さない"),
        ("4", "夜中に起き出す"),
        ("5", "根拠のない事を言う（例：盗まれた、配偶者が浮気している等）"),
        ("6", "昼間、寝てばかりいる"),
        ("7", "やたらに歩き回る"),
        ("8", "同じ動作をいつまでも繰り返す"),
        ("9", "口汚くののしる"),
        ("10", "場違いあるいは季節に合わない不適切な服装をする"),
        ("11", "世話をされるのを拒否する"),
        ("12", "食べられないものを口に入れる"),
        ("13", "引き出しやタンスの中身を全部出してしまう"),
    ]

    row = 7
    headers = ["No.", "評価項目", "0", "1", "2", "3", "4", "評価"]
    for col, header in enumerate(headers, start=1):
        cell = ws.cell(row=row, column=col, value=header)
        cell.font = styles['header_font']
        cell.fill = styles['header_fill']
        cell.border = styles['thin_border']
        cell.alignment = styles['center_align']
    row += 1

    for num, question in dbd_items:
        score = data.get(f"d{num}", "")
        ws.cell(row=row, column=1, value=num).border = styles['thin_border']
        ws.cell(row=row, column=1).alignment = styles['center_align']
        ws.cell(row=row, column=2, value=question).border = styles['thin_border']
        ws.cell(row=row, column=2).alignment = styles['left_align']
        for i, val in enumerate([0, 1, 2, 3, 4], start=3):
            cell = ws.cell(row=row, column=i, value="○" if score == val else "")
            cell.border = styles['thin_border']
            cell.alignment = styles['center_align']
        ws.cell(row=row, column=8, value=score if score is not None else "").border = styles['thin_border']
        ws.cell(row=row, column=8).alignment = styles['center_align']
        row += 1

    row += 1
    ws.cell(row=row, column=1, value="合計点").font = styles['header_font']
    ws.cell(row=row, column=2, value=data.get("total_score", ""))
    ws.cell(row=row, column=3, value="（0〜52点、点数が高いほど行動障害が重い）")

    ws.column_dimensions['A'].width = 8
    ws.column_dimensions['B'].width = 55
    for col in ['C', 'D', 'E', 'F', 'G']:
        ws.column_dimensions[col].width = 6
    ws.column_dimensions['H'].width = 8

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    filename = f"dbd13_{client_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     as_attachment=True, download_name=filename)


# ================================
#  Flask 実行
# ================================
if __name__ == "__main__":
    app.run(debug=True)
