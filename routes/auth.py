from flask import Blueprint, request, jsonify, session , render_template
from database.db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint("auth", __name__)


# ==========================
# Patient Registration
# ==========================

@auth.route("/user/register", methods=["POST"])
def user_register():

    data = request.get_json()

    full_name = data["full_name"]
    email = data["email"]
    phone = data["phone"]
    password = data["password"]


    hashed_password = generate_password_hash(password)


    conn = get_db_connection()
    cursor = conn.cursor()


    try:

        cursor.execute("""
        INSERT INTO users
        (full_name, email, phone, password)

        VALUES (?, ?, ?, ?)

        """,
        (
            full_name,
            email,
            phone,
            hashed_password
        ))


        conn.commit()

        return jsonify({
            "message":"User registered successfully"
        }),201



    except Exception as e:

        return jsonify({
            "error":str(e)
        }),400


    finally:

        conn.close()



# ==========================
# Patient Login
# ==========================

@auth.route("/user/login", methods=["POST"])
def user_login():


    data = request.get_json()


    email = data["email"]
    password = data["password"]



    conn = get_db_connection()
    cursor = conn.cursor()


    user = cursor.execute(
        """
        SELECT * FROM users
        WHERE email=?
        """,
        (email,)
    ).fetchone()



    conn.close()



    if user and check_password_hash(
        user["password"],
        password
    ):


        


        session["user_id"] = user["id"]

        return jsonify({
            "message": "Login successful",
            "user": user["full_name"],
            "redirect": "/user/dashboard"
        }), 200
    return jsonify({

        "error":"Invalid email or password"

    }),401
@auth.route("/user/login", methods=["GET"])
def user_login_page():
    return render_template("user/login.html")