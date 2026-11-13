from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from functools import wraps
from datetime import datetime, date
import os
from data_manager import db

app = Flask(__name__)
app.secret_key = "zone_sport_center_basketball_secret_key_2026"

# Context processor for templates
@app.context_processor
def inject_globals():
    return {
        "current_user": g.user if hasattr(g, 'user') else None,
        "now": datetime.now(),
        "today_str": datetime.now().strftime("%Y-%m-%d")
    }

@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = db.get_user_by_id(user_id)
        if not g.user:
            session.clear()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash("Please sign in to access this feature!", "warning")
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash("Please sign in to proceed!", "warning")
            return redirect(url_for("login"))
        if g.user.get("role") != "admin":
            flash("You do not have Administrator permissions to perform this action!", "danger")
            return redirect(url_for("dashboard"))
        return f(*args, **kwargs)
    return decorated_function

# ========================================================
# 1. USER AUTHENTICATION & PROFILE MANAGEMENT
# ========================================================

@app.route("/login", methods=["GET", "POST"])
def login():
    if g.user:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        user = db.get_user_by_username(username)
        if user and user.get("password") == password:
            session.clear()
            session["user_id"] = user["id"]
            flash(f"Welcome back, {user['full_name']}! Signed in successfully.", "success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("dashboard"))
        else:
            flash("Invalid username or password!", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out successfully.", "success")
    return redirect(url_for("login"))

@app.route("/profile", methods=["GET", "POST"])
@login_required
def user_profile():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        bio = request.form.get("bio", "").strip()

        if not full_name or not email or not phone:
            flash("Please fill in all required fields!", "danger")
        else:
            db.update_user_profile(g.user["id"], full_name, email, phone, bio)
            flash("Profile updated successfully!", "success")
            return redirect(url_for("user_profile"))

    return render_template("profile.html", active_page="profile")

@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        old_pwd = request.form.get("old_password", "").strip()
        new_pwd = request.form.get("new_password", "").strip()
        confirm_pwd = request.form.get("confirm_password", "").strip()

        if not old_pwd or not new_pwd:
            flash("Please enter all required password fields!", "danger")
        elif new_pwd != confirm_pwd:
            flash("New password and confirmation password do not match!", "danger")
        elif len(new_pwd) < 6:
            flash("New password must be at least 6 characters long!", "warning")
        else:
            success, msg = db.change_user_password(g.user["id"], old_pwd, new_pwd)
            if success:
                flash(msg, "success")
                return redirect(url_for("user_profile"))
            else:
                flash(msg, "danger")

    return render_template("change_password.html", active_page="change_password")

@app.route("/reset-demo-data", methods=["POST"])
@admin_required
def reset_demo_data():
    db.reset_to_seed()
    flash("All demo data for Zone Sport Center has been reset to defaults successfully!", "success")
    return redirect(url_for("dashboard"))

# ========================================================
# 2. DASHBOARD
# ========================================================

@app.route("/")
@app.route("/dashboard")
@login_required
def dashboard():
    stats = db.get_dashboard_summary()
    return render_template("dashboard.html", stats=stats, active_page="dashboard")

# ========================================================
# 3. STUDENT MANAGEMENT
# ========================================================

@app.route("/students")
@login_required
def student_list():
    query = request.args.get("q", "").strip()
    students = db.get_all_students(query=query)
    return render_template("students/index.html", students=students, query=query, active_page="students")

@app.route("/students/new", methods=["GET", "POST"])
@admin_required
def student_new():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        dob = request.form.get("dob", "").strip()
        gender = request.form.get("gender", "Male")
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        note = request.form.get("note", "").strip()

        if not name or not phone or not dob:
            flash("Full Name, Date of Birth, and Phone Number are required!", "danger")
        else:
            new_st = db.add_student(name, dob, gender, phone, address, note)
            flash(f"Student '{new_st['name']}' (ID: {new_st['id']}) registered successfully!", "success")
            return redirect(url_for("student_detail", student_id=new_st["id"]))

    return render_template("students/form.html", is_edit=False, student=None, active_page="students")

@app.route("/students/<student_id>")
@login_required
def student_detail(student_id):
    student = db.get_student_by_id(student_id)
    if not student:
        flash("Student not found!", "danger")
        return redirect(url_for("student_list"))
    return render_template("students/detail.html", student=student, active_page="students")

@app.route("/students/<student_id>/edit", methods=["GET", "POST"])
@admin_required
def student_edit(student_id):
    student = db.get_student_by_id(student_id)
    if not student:
        flash("Student does not exist!", "danger")
        return redirect(url_for("student_list"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        dob = request.form.get("dob", "").strip()
        gender = request.form.get("gender", "Male")
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        status = request.form.get("status", "Active")
        note = request.form.get("note", "").strip()

        if not name or not phone:
            flash("Full Name and Phone Number are required!", "danger")
        else:
            db.update_student(student_id, name, dob, gender, phone, address, status, note)
            flash("Student profile updated successfully!", "success")
            return redirect(url_for("student_detail", student_id=student_id))

    return render_template("students/form.html", is_edit=True, student=student, active_page="students")

@app.route("/students/<student_id>/delete", methods=["POST"])
@admin_required
def student_delete(student_id):
    db.delete_student(student_id)
    flash(f"Student {student_id} deleted successfully!", "success")
    return redirect(url_for("student_list"))

# ========================================================
# 4. COACH MANAGEMENT
# ========================================================

@app.route("/coaches")
@login_required
def coach_list():
    query = request.args.get("q", "").strip()
    coaches = db.get_all_coaches(query=query)
    return render_template("coaches/index.html", coaches=coaches, query=query, active_page="coaches")

@app.route("/coaches/new", methods=["GET", "POST"])
@admin_required
def coach_new():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        experience = request.form.get("experience", "").strip()
        specialty = request.form.get("specialty", "").strip()
        bio = request.form.get("bio", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not name or not phone or not email:
            flash("Full Name, Phone Number, and Email Address are required!", "danger")
        else:
            new_coach = db.add_coach(name, phone, email, experience, specialty, bio,
                                     create_user_account=True, username=username, password=password)
            flash(f"Coach '{new_coach['name']}' (ID: {new_coach['id']}) added successfully with system login credentials created!", "success")
            return redirect(url_for("coach_detail", coach_id=new_coach["id"]))

    return render_template("coaches/form.html", is_edit=False, coach=None, active_page="coaches")

@app.route("/coaches/<coach_id>")
@login_required
def coach_detail(coach_id):
    coach = db.get_coach_by_id(coach_id)
    if not coach:
        flash("Coach not found!", "danger")
        return redirect(url_for("coach_list"))
    return render_template("coaches/detail.html", coach=coach, active_page="coaches")

@app.route("/coaches/<coach_id>/edit", methods=["GET", "POST"])
@admin_required
def coach_edit(coach_id):
    coach = db.get_coach_by_id(coach_id)
    if not coach:
        flash("Coach does not exist!", "danger")
        return redirect(url_for("coach_list"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        experience = request.form.get("experience", "").strip()
        specialty = request.form.get("specialty", "").strip()
        bio = request.form.get("bio", "").strip()
        status = request.form.get("status", "Active")

        if not name or not phone or not email:
            flash("Full Name, Phone Number, and Email Address are required!", "danger")
        else:
            db.update_coach(coach_id, name, phone, email, experience, specialty, bio, status)
            flash("Coach profile updated successfully!", "success")
            return redirect(url_for("coach_detail", coach_id=coach_id))

    return render_template("coaches/form.html", is_edit=True, coach=coach, active_page="coaches")

@app.route("/coaches/<coach_id>/delete", methods=["POST"])
@admin_required
def coach_delete(coach_id):
    db.delete_coach(coach_id)
    flash(f"Coach {coach_id} deleted successfully!", "success")
    return redirect(url_for("coach_list"))

# ========================================================
# 5. CLASS MANAGEMENT
# ========================================================

@app.route("/classes")
@login_required
def class_list():
    query = request.args.get("q", "").strip()
    level = request.args.get("level", "").strip()
    status = request.args.get("status", "").strip()

    classes = db.get_all_classes(level=level or None, status=status or None, query=query or None)
    return render_template("classes/index.html", classes=classes, query=query,
                           selected_level=level, selected_status=status, active_page="classes")

@app.route("/classes/new", methods=["GET", "POST"])
@admin_required
def class_new():
    coaches = db.get_all_coaches()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        level = request.form.get("level", "Beginner")
        coach_id = request.form.get("coach_id", "").strip()
        max_students = request.form.get("max_students", "15")
        tuition_fee = request.form.get("tuition_fee", "1500000")
        status = request.form.get("status", "Đang học")
        schedule = request.form.get("schedule", "").strip()
        location = request.form.get("location", "Zone Arena Court 1").strip()
        description = request.form.get("description", "").strip()

        if not name or not schedule:
            flash("Class Name and Schedule are required!", "danger")
        else:
            new_cl = db.add_class(name, level, coach_id, max_students, tuition_fee, status, schedule, location, description)
            flash(f"Class '{new_cl['name']}' (ID: {new_cl['id']}) created successfully!", "success")
            return redirect(url_for("class_detail", class_id=new_cl["id"]))

    return render_template("classes/form.html", is_edit=False, cl=None, coaches=coaches, active_page="classes")

@app.route("/classes/<class_id>")
@login_required
def class_detail(class_id):
    cl = db.get_class_by_id(class_id)
    if not cl:
        flash("Class not found!", "danger")
        return redirect(url_for("class_list"))
    return render_template("classes/detail.html", cl=cl, active_page="classes")

@app.route("/classes/<class_id>/edit", methods=["GET", "POST"])
@admin_required
def class_edit(class_id):
    cl = db.get_class_by_id(class_id)
    if not cl:
        flash("Class does not exist!", "danger")
        return redirect(url_for("class_list"))

    coaches = db.get_all_coaches()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        level = request.form.get("level", "Beginner")
        coach_id = request.form.get("coach_id", "").strip()
        max_students = request.form.get("max_students", "15")
        tuition_fee = request.form.get("tuition_fee", "1500000")
        status = request.form.get("status", "Đang học")
        schedule = request.form.get("schedule", "").strip()
        location = request.form.get("location", "").strip()
        description = request.form.get("description", "").strip()

        if not name or not schedule:
            flash("Class Name and Schedule are required!", "danger")
        else:
            db.update_class(class_id, name, level, coach_id, max_students, tuition_fee, status, schedule, location, description)
            flash("Class information updated successfully!", "success")
            return redirect(url_for("class_detail", class_id=class_id))

    return render_template("classes/form.html", is_edit=True, cl=cl, coaches=coaches, active_page="classes")

@app.route("/classes/<class_id>/delete", methods=["POST"])
@admin_required
def class_delete(class_id):
    db.delete_class(class_id)
    flash(f"Class {class_id} deleted successfully!", "success")
    return redirect(url_for("class_list"))

# ========================================================
# 6. ENROLLMENT MANAGEMENT
# ========================================================

@app.route("/enrollments")
@login_required
def enrollment_list():
    class_id = request.args.get("class_id", "").strip()
    status = request.args.get("status", "").strip()
    enrollments = db.get_all_enrollments(class_id=class_id or None, status=status or None)
    classes = db.get_all_classes()
    return render_template("enrollments/index.html", enrollments=enrollments, classes=classes,
                           selected_class_id=class_id, selected_status=status, active_page="enrollments")

@app.route("/enrollments/register", methods=["GET", "POST"])
@admin_required
def enrollment_register():
    if request.method == "POST":
        student_id = request.form.get("student_id", "").strip()
        class_id = request.form.get("class_id", "").strip()
        enroll_date = request.form.get("enroll_date", "").strip()
        auto_payment = request.form.get("auto_payment") == "yes"

        if not student_id or not class_id:
            flash("Please select both a student and a basketball class!", "danger")
        else:
            success, msg = db.enroll_student(student_id, class_id, enroll_date=enroll_date or None, auto_create_payment=auto_payment)
            if success:
                flash(msg, "success")
                return redirect(url_for("class_detail", class_id=class_id))
            else:
                flash(msg, "danger")

    students = db.get_all_students()
    classes = db.get_all_classes()
    selected_student_id = request.args.get("student_id", "")
    selected_class_id = request.args.get("class_id", "")

    return render_template("enrollments/register.html", students=students, classes=classes,
                           selected_student_id=selected_student_id, selected_class_id=selected_class_id,
                           active_page="enrollments")

@app.route("/enrollments/<enrollment_id>/cancel", methods=["POST"])
@admin_required
def enrollment_cancel(enrollment_id):
    success, msg = db.cancel_enrollment(enrollment_id)
    if success:
        flash(msg, "success")
    else:
        flash(msg, "danger")

    redirect_back = request.args.get("redirect_back")
    if redirect_back == "class":
        return redirect(url_for("class_detail", class_id=request.args.get("class_id")))
    return redirect(url_for("enrollment_list"))

# ========================================================
# 10. TUITION & PAYMENT MANAGEMENT
# ========================================================

@app.route("/payments")
@admin_required
def payment_list():
    status = request.args.get("status", "").strip()
    query = request.args.get("q", "").strip()

    payments = db.get_all_payments(status=status or None, query=query or None)
    all_payments = db.get_all_payments()

    total_collected = sum(p.get("paid_amount", 0) for p in all_payments)
    total_receivable = sum(p.get("amount", 0) for p in all_payments)
    total_debt = max(0, total_receivable - total_collected)
    paid_count = sum(1 for p in all_payments if p.get("status") in ["Đã thanh toán", "Paid"])
    unpaid_count = sum(1 for p in all_payments if p.get("status") not in ["Đã thanh toán", "Paid"])
    collection_rate = round((total_collected / total_receivable * 100), 1) if total_receivable > 0 else 0

    return render_template("payments/index.html", payments=payments, query=query, selected_status=status,
                           total_collected=total_collected, total_debt=total_debt, total_receivable=total_receivable,
                           paid_count=paid_count, unpaid_count=unpaid_count, collection_rate=collection_rate,
                           active_page="payments")

@app.route("/payments/record", methods=["GET", "POST"])
@admin_required
def payment_record():
    if request.method == "POST":
        student_id = request.form.get("student_id", "").strip()
        class_id = request.form.get("class_id", "").strip()
        amount = request.form.get("amount", 0)
        paid_amount = request.form.get("paid_amount", 0)
        status = request.form.get("status", "Đã thanh toán")
        payment_date = request.form.get("payment_date", "").strip()
        payment_method = request.form.get("payment_method", "Tiền mặt")
        note = request.form.get("note", "").strip()

        if not student_id or not class_id:
            flash("Please select both a student and a class!", "danger")
        else:
            db.record_payment(student_id, class_id, amount, paid_amount, status, payment_date or None, payment_method, note)
            flash("Tuition payment invoice recorded successfully!", "success")
            return redirect(url_for("payment_list"))

    students = db.get_all_students()
    classes = db.get_all_classes()
    selected_student_id = request.args.get("student_id", "")

    return render_template("payments/record.html", students=students, classes=classes,
                           selected_student_id=selected_student_id, active_page="payments")

@app.route("/payments/<payment_id>/update", methods=["POST"])
@admin_required
def payment_update(payment_id):
    paid_amount = request.form.get("paid_amount", 0)
    status = request.form.get("status", "Đã thanh toán")
    payment_method = request.form.get("payment_method", "Chuyển khoản QR")
    note = request.form.get("note", "").strip()

    db.update_payment(payment_id, paid_amount, status, payment_method, note=note)
    flash(f"Payment invoice {payment_id} updated successfully!", "success")
    return redirect(url_for("payment_list"))

# ========================================================
# ATTENDANCE & PRACTICE TRACKING
# ========================================================

@app.route("/attendance", methods=["GET", "POST"])
@login_required
def attendance_view():
    classes = db.get_all_classes()
    # If user is coach, default to their first class
    if g.user.get("role") == "coach" and g.user.get("coach_id"):
        coach_classes = [c for c in classes if c.get("coach_id") == g.user.get("coach_id")]
        if coach_classes:
            classes = coach_classes

    selected_class_id = request.args.get("class_id") or (classes[0]["id"] if classes else None)
    selected_date = request.args.get("date") or datetime.now().strftime("%Y-%m-%d")

    if request.method == "POST":
        target_class_id = request.form.get("class_id")
        target_date = request.form.get("date")
        target_class = db.get_class_by_id(target_class_id)
        if target_class:
            att_list = []
            for s in target_class["students"]:
                status = request.form.get(f"status_{s['id']}", "Present")
                att_list.append({"student_id": s["id"], "status": status})
            db.record_attendance(target_class_id, att_list, target_date)
            flash(f"Attendance for date {target_date} in class '{target_class['name']}' saved successfully!", "success")
            return redirect(url_for("attendance_view", class_id=target_class_id, date=target_date))

    selected_class = db.get_class_by_id(selected_class_id) if selected_class_id else None
    students_in_class = []

    if selected_class:
        existing_att = {
            a["student_id"]: a["status"]
            for a in db.data.get("attendances", [])
            if a["class_id"] == selected_class_id and a["date"] == selected_date
        }
        for s in selected_class["students"]:
            s_copy = dict(s)
            s_copy["attendance_status"] = existing_att.get(s["id"], "Present")
            students_in_class.append(s_copy)

    return render_template("attendance/index.html", classes=classes, selected_class=selected_class,
                           selected_date=selected_date, students_in_class=students_in_class,
                           active_page="attendance")

# ========================================================
# 11. REPORTS & STATISTICS
# ========================================================

@app.route("/reports")
@admin_required
def reports_view():
    summary = db.get_dashboard_summary()
    monthly_data = db.get_monthly_reports(target_year=2026)
    return render_template("reports/index.html", summary=summary, monthly_data=monthly_data, active_page="reports")

if __name__ == "__main__":
    print("=" * 60)
    print("ZONE SPORT CENTER - Basketball Training Center Management System")
    print("Running server at: http://127.0.0.1:5000")
    print("Admin Account: username 'admin' / password 'admin123'")
    print("Coach Account: username 'coach_nam' / password 'coach123'")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=True)