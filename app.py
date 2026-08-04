from flask import Flask, render_template
from database.db import get_db_connection
from routes.auth import auth
from routes.pharmacy import pharmacy


# Create Flask application
app = Flask(__name__)

# Secret key (required later for sessions)
app.secret_key = "medconnect_secret_key"
app.register_blueprint(auth)
app.register_blueprint(pharmacy)

# Home Page
@app.route("/")
def home():
    conn = get_db_connection()

    conn.execute("SELECT 1")

    conn.close()

    return render_template("index.html")

# Run the application
if __name__ == "__main__":
    app.run(debug=True)