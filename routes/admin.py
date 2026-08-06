from flask import Blueprint, request, jsonify, session
from database.db import get_db_connection
from werkzeug.security import generate_password_hash

admin = Blueprint("admin", __name__)
from database.db import get_db_connection
from werkzeug.security import generate_password_hash


conn = get_db_connection()
cursor = conn.cursor()


hashed_password = generate_password_hash("admin123")


cursor.execute("""
UPDATE admin
SET password = ?
WHERE username = ?
""",
(
    hashed_password,
    "admin"
))


conn.commit()
conn.close()


print("Admin password updated with hash successfully!")


# ==========================
# Admin Login
# ==========================

@admin.route("/admin/login", methods=["POST"])
def admin_login():

    data = request.get_json()

    username = data["username"]
    password = data["password"]


    conn = get_db_connection()
    cursor = conn.cursor()


    admin_data = cursor.execute(

        """
        SELECT * FROM admin
        WHERE username = ?
        """,

        (username,)

    ).fetchone()


    conn.close()


    if admin_data:

        if admin_data["password"] == password:

            session["admin_id"] = admin_data["id"]

            return jsonify({

                "message": "Admin login successful"

            })


    return jsonify({

        "error": "Invalid username or password"

    }), 401
# ==========================
# View Pending Pharmacies
# ==========================

@admin.route("/admin/pharmacies/pending", methods=["GET"])
def pending_pharmacies():

    conn = get_db_connection()
    cursor = conn.cursor()


    pharmacies = cursor.execute(
        """
        SELECT 
        id,
        shop_name,
        owner_name,
        email,
        phone,
        dl_number,
        address,
        status

        FROM pharmacies

        WHERE status='Pending'
        """
    ).fetchall()


    conn.close()


    pharmacy_list = []


    for pharmacy in pharmacies:

        pharmacy_list.append({

            "id": pharmacy["id"],
            "shop_name": pharmacy["shop_name"],
            "owner_name": pharmacy["owner_name"],
            "email": pharmacy["email"],
            "phone": pharmacy["phone"],
            "dl_number": pharmacy["dl_number"],
            "address": pharmacy["address"],
            "status": pharmacy["status"]

        })


    return jsonify(pharmacy_list)
# ==========================
# Approve Pharmacy
# ==========================

@admin.route("/admin/pharmacy/approve/<int:id>", methods=["PUT"])
def approve_pharmacy(id):

    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE pharmacies
        SET status = 'Approved'
        WHERE id = ?
        """,
        (id,)
    )


    conn.commit()
    conn.close()


    return jsonify({

        "message": "Pharmacy approved successfully"

    })
# ==========================
# Reject Pharmacy
# ==========================

@admin.route("/admin/pharmacy/reject/<int:id>", methods=["PUT"])
def reject_pharmacy(id):

    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE pharmacies
        SET status = 'Rejected'
        WHERE id = ?
        """,
        (id,)
    )


    conn.commit()
    conn.close()


    return jsonify({

        "message": "Pharmacy rejected"

    })