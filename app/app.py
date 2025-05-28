from flask import Flask, request, redirect, url_for, render_template_string
import mysql.connector, time

app = Flask(__name__)

# ------------------------------------------------------------------ #
# Helper: connect with retries so Flask starts even if MySQL is booting
# ------------------------------------------------------------------ #
def get_db_connection(retries: int = 10, delay: int = 3):
    for attempt in range(1, retries + 1):
        try:
            return mysql.connector.connect(
                host="mysql_db",           # container name of MySQL
                user="root",
                password="rootpassword",
                database="flask_db"
            )
        except mysql.connector.Error as err:
            print(f"[{attempt}/{retries}]  MySQL not ready → {err}")
            time.sleep(delay)
    raise RuntimeError("MySQL connection failed after several retries.")

# ------------------------------------------------------------------ #
# SQL: ensure `users` table exists
# ------------------------------------------------------------------ #
def create_users_table_if_needed(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id   INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            dob  DATE NOT NULL
        )
        """
    )
    conn.commit()
    cursor.close()

# ------------------------------------------------------------------ #
# Routes
# ------------------------------------------------------------------ #
FORM_HTML = """<!doctype html>
<title>Register User</title>
<h2>Enter your details</h2>
<form method="post" action="/">
  <label>Name: <input name="name" required></label><br><br>
  <label>Date of Birth (YYYY-MM-DD):
         <input name="dob" type="date" required></label><br><br>
  <button type="submit">Submit</button>
</form>
<p><a href="{{ url_for('list_users') }}">View all users</a></p>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"].strip()
        dob  = request.form["dob"]        # HTML5 date already YYYY-MM-DD
        if not name:
            return "Name cannot be empty", 400

        conn = get_db_connection()
        create_users_table_if_needed(conn)

        cur = conn.cursor(prepared=True)
        cur.execute("INSERT INTO users (name, dob) VALUES (%s, %s)", (name, dob))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("list_users"))

    # GET → show form
    return render_template_string(FORM_HTML)

@app.route("/users")
def list_users():
    conn = get_db_connection()
    create_users_table_if_needed(conn)
    cur = conn.cursor()
    cur.execute("SELECT id, name, dob FROM users ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # quick inline template
    table_rows = "".join(
        f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>" for r in rows
    )
    return f"""
    <!doctype html>
    <title>All Users</title>
    <h2>Registered Users</h2>
    <table border="1" cellpadding="6">
      <tr><th>ID</th><th>Name</th><th>DOB</th></tr>
      {table_rows or '<tr><td colspan="3">No data yet</td></tr>'}
    </table>
    <p><a href="{url_for('index')}">Back to form</a></p>
    """

if __name__ == "__main__":
    # listen on all interfaces so we can map the port
    app.run(host="0.0.0.0", port=5000, debug=False)
