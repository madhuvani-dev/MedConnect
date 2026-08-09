from flask import Blueprint, session, redirect, url_for, render_template
from database.db import get_db_connection

user = Blueprint("user", __name__)


@user.route("/user/dashboard")
def user_dashboard():

    # Check whether the user is logged in
    if "user_id" not in session:
        return redirect(url_for("auth.user_login_page"))

    # Get the logged-in user's information
    conn = get_db_connection()
    cursor = conn.cursor()

    user_data = cursor.execute(
        """
        SELECT id, full_name, email, phone
        FROM users
        WHERE id = ?
        """,
        (session["user_id"],)
    ).fetchone()

    conn.close()

    # If the user no longer exists in the database
    if user_data is None:
        session.pop("user_id", None)
        return redirect(url_for("auth.user_login_page"))

    return render_template(
        "user/dashboard.html",
        user=user_data
    )