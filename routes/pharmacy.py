from flask import Blueprint, request, jsonify, session
from database.db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash


pharmacy = Blueprint("pharmacy", __name__)


# ==========================
# Pharmacy Registration
# ==========================

@pharmacy.route("/pharmacy/register", methods=["POST"])
def pharmacy_register():

    data = request.get_json()


    shop_name = data["shop_name"]
    owner_name = data["owner_name"]
    email = data["email"]
    password = data["password"]
    phone = data["phone"]
    dl_number = data["dl_number"]
    address = data["address"]


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