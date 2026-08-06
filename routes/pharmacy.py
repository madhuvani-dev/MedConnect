from flask import Blueprint, request, jsonify, session, render_template
from database.db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash


pharmacy = Blueprint("pharmacy", __name__)


# ==========================
# Pharmacy Registration
# ==========================

@pharmacy.route("/pharmacy/register", methods=["GET"])
def pharmacy_register_page():
    return render_template("pharmacy/register.html")
@pharmacy.route("/pharmacy/register", methods=["POST"])
def pharmacy_register():

    shop_name = request.form["shop_name"]
    owner_name = request.form["owner_name"]
    email = request.form["email"]
    password = request.form["password"]
    phone = request.form["phone"]
    dl_number = request.form["dl_number"]
    address = request.form["address"]


    hashed_password = generate_password_hash(password)


    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
        INSERT INTO pharmacies
        (
        shop_name,
        owner_name,
        email,
        password,
        phone,
        dl_number,
        address
        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

        """,
        (
            shop_name,
            owner_name,
            email,
            hashed_password,
            phone,
            dl_number,
            address
        ))


        conn.commit()


        return jsonify({

            "message":"Pharmacy registered successfully. Waiting for admin approval."

        }),201



    except Exception as e:


        return jsonify({

            "error":str(e)

        }),400



    finally:

        conn.close()



# ==========================
# Pharmacy Login
# ==========================

@pharmacy.route("/pharmacy/login", methods=["POST"])
def pharmacy_login():


    data = request.get_json()


    email = data["email"]
    password = data["password"]



    conn = get_db_connection()
    cursor = conn.cursor()



    pharmacy_data = cursor.execute(

        """
        SELECT * FROM pharmacies
        WHERE email=?
        """,

        (email,)

    ).fetchone()



    conn.close()



    if pharmacy_data and check_password_hash(
        pharmacy_data["password"],
        password
    ):


        if pharmacy_data["status"] != "Approved":

            return jsonify({

                "error":"Your pharmacy account is waiting for admin approval"

            }),403



        session["pharmacy_id"] = pharmacy_data["id"]


        return jsonify({

            "message":"Pharmacy login successful",
            "pharmacy":pharmacy_data["shop_name"]

        })



    return jsonify({

        "error":"Invalid email or password"

    }),401