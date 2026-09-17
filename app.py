from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    session
)
import sqlite3
import os
import re

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "student-management-secret-key")
app.config["SESSION_COOKIE_HTTPONLY"] = True

DATABASE = "students.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            department TEXT NOT NULL,
            year INTEGER NOT NULL,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def is_valid_email(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None


def validate_student_form(form):
    name = form.get("name", "").strip()
    email = form.get("email", "").strip()
    phone = form.get("phone", "").strip()
    department = form.get("department", "").strip()
    year = form.get("year", "").strip()
    address = form.get("address", "").strip()

    errors = []

    if not name:
        errors.append("Name is required.")

    if not email:
        errors.append("Email is required.")
    elif not is_valid_email(email):
        errors.append("Enter a valid email address.")

    if not phone:
        errors.append("Phone number is required.")
    elif not phone.isdigit() or len(phone) != 10:
        errors.append("Phone number must contain exactly 10 digits.")

    if not department:
        errors.append("Department is required.")

    if not year:
        errors.append("Year is required.")
    else:
        try:
            year_number = int(year)
            if year_number not in [1, 2, 3, 4]:
                errors.append("Year must be between 1 and 4.")
        except ValueError:
            errors.append("Year must be a number.")

    student = {
        "name": name,
        "email": email,
        "phone": phone,
        "department": department,
        "year": year,
        "address": address
    }

    return student, errors


@app.route("/")
def index():
     if user_is_logged_in():
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))

@app.route("/add", methods=["POST"])
def add_student():
    
    if not user_is_logged_in():
        return redirect(url_for("login"))
    student, errors = validate_student_form(request.form)

    if errors:
        for error in errors:
            flash(error, "danger")
        return redirect(url_for("index"))

    connection = get_db_connection()

    try:
        connection.execute("""
            INSERT INTO students
            (name, email, phone, department, year, address)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            student["name"],
            student["email"],
            student["phone"],
            student["department"],
            student["year"],
            student["address"]
        ))

        connection.commit()
        flash("Student added successfully.", "success")

    except sqlite3.IntegrityError:
        flash("This email address already exists.", "danger")

    finally:
        connection.close()

    return redirect(url_for("index"))


@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
     if not user_is_logged_in():
        return redirect(url_for("login"))

    connection = get_db_connection()

    student = connection.execute("""
        SELECT * FROM students WHERE id = ?
    """, (student_id,)).fetchone()

    if student is None:
        connection.close()
        flash("Student not found.", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        updated_student, errors = validate_student_form(request.form)

        if errors:
            connection.close()

            for error in errors:
                flash(error, "danger")

            return render_template(
                "edit.html",
                student=updated_student,
                student_id=student_id
            )

        try:
            connection.execute("""
                UPDATE students
                SET name = ?,
                    email = ?,
                    phone = ?,
                    department = ?,
                    year = ?,
                    address = ?
                WHERE id = ?
            """, (
                updated_student["name"],
                updated_student["email"],
                updated_student["phone"],
                updated_student["department"],
                updated_student["year"],
                updated_student["address"],
                student_id
            ))

            connection.commit()
            flash("Student updated successfully.", "success")
            connection.close()

            return redirect(url_for("index"))

        except sqlite3.IntegrityError:
            connection.close()
            flash("This email address already belongs to another student.", "danger")

            return render_template(
                "edit.html",
                student=updated_student,
                student_id=student_id
            )

    connection.close()

    return render_template(
        "edit.html",
        student=student,
        student_id=student_id
    )


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    if not user_is_logged_in():
        return redirect(url_for("login"))
    connection = get_db_connection()

    student = connection.execute("""
        SELECT * FROM students WHERE id = ?
    """, (student_id,)).fetchone()

    if student:
        connection.execute("""
            DELETE FROM students WHERE id = ?
        """, (student_id,))

        connection.commit()
        flash("Student deleted successfully.", "success")
    else:
        flash("Student not found.", "danger")

    connection.close()

    return redirect(url_for("index"))


@app.route("/api/students", methods=["GET"])
def api_get_students():
    connection = get_db_connection()

    students = connection.execute("""
        SELECT * FROM students ORDER BY id DESC
    """).fetchall()

    connection.close()

    return jsonify([dict(student) for student in students])


@app.route("/api/students", methods=["POST"])
def api_add_student():
    data = request.get_json()

    required_fields = [
        "name",
        "email",
        "phone",
        "department",
        "year"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "error": f"{field} is required"
            }), 400

    if not is_valid_email(data["email"]):
        return jsonify({
            "error": "Invalid email address"
        }), 400

    connection = get_db_connection()

    try:
        cursor = connection.execute("""
            INSERT INTO students
            (name, email, phone, department, year, address)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data["name"],
            data["email"],
            data["phone"],
            data["department"],
            data["year"],
            data.get("address", "")
        ))

        connection.commit()
        student_id = cursor.lastrowid

        student = connection.execute("""
            SELECT * FROM students WHERE id = ?
        """, (student_id,)).fetchone()

        connection.close()

        return jsonify(dict(student)), 201

    except sqlite3.IntegrityError:
        connection.close()

        return jsonify({
            "error": "Email already exists"
        }), 409


@app.route("/api/students/<int:student_id>", methods=["GET"])
def api_get_student(student_id):
    connection = get_db_connection()

    student = connection.execute("""
        SELECT * FROM students WHERE id = ?
    """, (student_id,)).fetchone()

    connection.close()

    if student is None:
        return jsonify({
            "error": "Student not found"
        }), 404

    return jsonify(dict(student))


@app.route("/api/students/<int:student_id>", methods=["PUT"])
def api_update_student(student_id):
    data = request.get_json()

    connection = get_db_connection()

    existing_student = connection.execute("""
        SELECT * FROM students WHERE id = ?
    """, (student_id,)).fetchone()

    if existing_student is None:
        connection.close()

        return jsonify({
            "error": "Student not found"
        }), 404

    try:
        connection.execute("""
            UPDATE students
            SET name = ?,
                email = ?,
                phone = ?,
                department = ?,
                year = ?,
                address = ?
            WHERE id = ?
        """, (
            data.get("name"),
            data.get("email"),
            data.get("phone"),
            data.get("department"),
            data.get("year"),
            data.get("address", ""),
            student_id
        ))

        connection.commit()

        updated_student = connection.execute("""
            SELECT * FROM students WHERE id = ?
        """, (student_id,)).fetchone()

        connection.close()

        return jsonify(dict(updated_student))

    except sqlite3.IntegrityError:
        connection.close()

        return jsonify({
            "error": "Email already exists"
        }), 409


@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def api_delete_student(student_id):
    connection = get_db_connection()

    cursor = connection.execute("""
        DELETE FROM students WHERE id = ?
    """, (student_id,))

    connection.commit()
    connection.close()

    if cursor.rowcount == 0:
        return jsonify({
            "error": "Student not found"
        }), 404

    return jsonify({
        "message": "Student deleted successfully"
    })


initialize_database()
def user_is_logged_in():
    return session.get("logged_in") is True


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == "admin" and password == "admin123":
            session["logged_in"] = True
            session["username"] = username

            flash("Login successful.", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid username or password.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    if not user_is_logged_in():
        return redirect(url_for("login"))

    connection = get_db_connection()

    total_students = connection.execute("""
        SELECT COUNT(*) AS count
        FROM students
    """).fetchone()["count"]

    department_count = connection.execute("""
        SELECT COUNT(DISTINCT department) AS count
        FROM students
    """).fetchone()["count"]

    first_year_count = connection.execute("""
        SELECT COUNT(*) AS count
        FROM students
        WHERE year = 1
    """).fetchone()["count"]

    final_year_count = connection.execute("""
        SELECT COUNT(*) AS count
        FROM students
        WHERE year = 4
    """).fetchone()["count"]

    connection.close()

    return render_template(
        "dashboard.html",
        total_students=total_students,
        department_count=department_count,
        first_year_count=first_year_count,
        final_year_count=final_year_count
    )


@app.route("/students")
def students_page():
    if not user_is_logged_in():
        return redirect(url_for("login"))

    search = request.args.get("search", "").strip()

    connection = get_db_connection()

    if search:
        students = connection.execute("""
            SELECT * FROM students
            WHERE name LIKE ?
               OR email LIKE ?
               OR department LIKE ?
               OR phone LIKE ?
            ORDER BY id DESC
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        )).fetchall()
    else:
        students = connection.execute("""
            SELECT * FROM students
            ORDER BY id DESC
        """).fetchall()

    connection.close()

    return render_template(
        "students.html",
        students=students,
        search=search
    )



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
