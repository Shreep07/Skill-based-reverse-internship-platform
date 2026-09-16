from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from database import init_db, get_db
from werkzeug.security import generate_password_hash, check_password_hash

import tempfile
import os
import subprocess
import io
from datetime import datetime, timedelta
import random
import string
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ─── EMAIL CONFIG ────────────────────────────────────────────────────────────
# Set enabled=True and fill in your Gmail credentials to activate emails.
EMAIL_CONFIG = {
    "enabled": False,                        # <-- Change to True to enable
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "your_email@gmail.com",      # <-- Your Gmail
    "sender_password": "your_app_password_here", # <-- Gmail App Password
}

def send_email(to_email, to_name, subject, body_html):
    """Send an HTML email. Silently skips if email is disabled or fails."""
    if not EMAIL_CONFIG.get("enabled"):
        print(f"[Email Skipped] To: {to_email} | {subject}")
        return
    try:
        wrapper = f"""<!DOCTYPE html><html><body style="margin:0;padding:0;background:#0f172a;font-family:Arial,sans-serif;">
        <div style="max-width:560px;margin:40px auto;background:#1e293b;border-radius:16px;overflow:hidden;border:1px solid #334155;">
          <div style="background:linear-gradient(135deg,#6366f1,#8b5cf6);padding:24px 32px;">
            <h1 style="margin:0;color:#fff;font-size:20px;font-weight:800;">&#9889; SkillHire</h1>
          </div>
          <div style="padding:32px;">{body_html}</div>
          <div style="padding:14px 32px;border-top:1px solid #334155;text-align:center;">
            <p style="color:#475569;font-size:12px;margin:0;">&copy; 2026 SkillHire Platform</p>
          </div>
        </div></body></html>"""
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"SkillHire <{EMAIL_CONFIG['sender_email']}>"
        msg["To"] = f"{to_name} <{to_email}>"
        msg.attach(MIMEText(wrapper, "html"))
        with smtplib.SMTP(EMAIL_CONFIG["smtp_host"], EMAIL_CONFIG["smtp_port"]) as srv:
            srv.ehlo()
            srv.starttls()
            srv.login(EMAIL_CONFIG["sender_email"], EMAIL_CONFIG["sender_password"])
            srv.sendmail(EMAIL_CONFIG["sender_email"], to_email, msg.as_string())
        print(f"[Email Sent] To: {to_email} | {subject}")
    except Exception as e:
        print(f"[Email Error] {e}")

app = Flask(__name__)
app.secret_key = "skillhire_secret_premium"

# Initialize Database on startup
with app.app_context():
    init_db()

# Helper function to generate unique random task codes
def generate_task_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def parse_deadline(deadline_str):
    """Safely parse a SQLite TIMESTAMP string to a Python datetime."""
    if not deadline_str:
        return None
    s = str(deadline_str)
    for fmt in ('%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S'):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None

def format_deadline_iso(deadline_str):
    dt = parse_deadline(deadline_str)
    return dt.isoformat() if dt else ""

def is_deadline_passed(deadline_str):
    dt = parse_deadline(deadline_str)
    return dt < datetime.now() if dt else False

def format_pretty_date(date_str):
    """Convert YYYY-MM-DD HH:MM:SS to '15 May, 09:00 PM'"""
    if not date_str:
        return None
    dt = parse_deadline(date_str)
    if not dt:
        return date_str
    return dt.strftime("%d %b, %I:%M %p")


# ─── AUTHENTICATION ROUTES ─────────────────────────────
@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/student/login", methods=["GET", "POST"])

def student_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ? AND role = 'student'", (email,)).fetchone()
        db.close()
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            session["user_name"] = user["name"]
            return redirect(url_for("student_dashboard"))
        flash("Invalid student credentials!", "error")
    return render_template("student_login.html")

@app.route("/company/login", methods=["GET", "POST"])
def company_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ? AND role = 'company'", (email,)).fetchone()
        db.close()
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            session["user_name"] = user["name"]
            return redirect(url_for("company_dashboard"))
        flash("Invalid company credentials!", "error")
    return render_template("company_login.html")

@app.route("/student/register", methods=["GET", "POST"])
def student_register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        db = get_db()
        try:
            db.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, 'student')", (name, email, password))
            db.commit()
            flash("Student account created! Please login.", "success")
            return redirect(url_for("student_login"))
        except:
            flash("Email already exists!", "error")
        finally:
            db.close()
    return render_template("student_register.html")

@app.route("/company/register", methods=["GET", "POST"])
def company_register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        website = request.form["website"]
        contact = request.form["contact"]
        tax_id = request.form["tax_id"]
        password = generate_password_hash(request.form["password"])
        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (name, email, password, role, website, contact, tax_id, verification_status) VALUES (?, ?, ?, 'company', ?, ?, ?, 'Pending')", 
                (name, email, password, website, contact, tax_id)
            )
            db.commit()
            flash("Company account created! Our team will verify your details soon.", "success")
            return redirect(url_for("company_login"))

        except:
            flash("Email already exists!", "error")
            return redirect(url_for("company_register"))

        finally:
            db.close()
    return render_template("company_register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        db.close()
        
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            session["user_name"] = user["name"]
            
            if user["role"] == "admin":
                return redirect(url_for("admin_dashboard"))
            elif user["role"] == "company":
                return redirect(url_for("company_dashboard"))
            else:
                return redirect(url_for("student_dashboard"))
        
        flash("Invalid email or password!", "error")
    
    return render_template("login.html")

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        db.close()
        
        if user:
            # In a real app, you would send an actual email here.
            flash("A password reset link has been sent to your email.", "success")
        else:
            flash("That email address is not registered.", "error")
        return redirect(url_for("forgot_password"))
    return render_template("forgot_password.html")


@app.route("/register", methods=["GET", "POST"])



def register():
    return redirect(url_for("student_register"))

@app.route("/student/logout")
def student_logout():
    session.clear()
    return redirect(url_for("student_login"))

@app.route("/company/logout")
def company_logout():
    session.clear()
    return redirect(url_for("company_login"))

@app.route("/logout")
def logout():
    role = session.get("role")
    session.clear()
    if role == "company":
        return redirect(url_for("company_login"))
    return redirect(url_for("student_login"))


# ─── STUDENT ROUTES ─────────────────────────────────────
@app.route("/student/dashboard")
def student_dashboard():
    if "user_id" not in session or session["role"] != "student":
        return redirect(url_for("login"))

    db = get_db()

    available_tasks = db.execute(
        "SELECT COUNT(*) as count FROM tasks WHERE status = 'Active'"
    ).fetchone()

    submitted_tasks = db.execute(
        "SELECT COUNT(*) as count FROM assignments WHERE student_id = ?",
        (session["user_id"],)
    ).fetchone()

    evaluated = db.execute(
        """SELECT COUNT(*) as count FROM evaluations e
           JOIN submissions s ON e.submission_id = s.id
           JOIN assignments a ON s.assignment_id = a.id
           WHERE a.student_id = ?""",
        (session["user_id"],)
    ).fetchone()

    deadlines = db.execute(
        """SELECT t.title, a.deadline FROM assignments a
           JOIN tasks t ON a.task_id = t.id
           WHERE a.student_id = ? AND a.deadline IS NOT NULL
           ORDER BY a.deadline ASC LIMIT 3""",
        (session["user_id"],)
    ).fetchall()

    hiring_alerts = db.execute(
        """SELECT t.title, u.name as company_name, e.id as eval_id
           FROM evaluations e
           JOIN submissions s ON e.submission_id = s.id
           JOIN assignments a ON s.assignment_id = a.id
           JOIN tasks t ON a.task_id = t.id
           JOIN users u ON t.company_id = u.id
           WHERE a.student_id = ? AND e.status = 'Selected'""",
        (session["user_id"],)
    ).fetchall()

    db.close()

    return render_template("student_dashboard.html",
        user_name=session["user_name"],
        available=available_tasks["count"],
        submitted=submitted_tasks["count"],
        evaluated=evaluated["count"],
        deadlines=deadlines,
        hiring_alerts=hiring_alerts
    )



@app.route("/student/tasks")
def task_list():
    if "user_id" not in session or session["role"] != "student":
        return redirect(url_for("login"))

    filter_applied = request.args.get("filter_applied") == "true"
    db = get_db()
    
    # Get student email
    user = db.execute("SELECT email FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    student_email = user["email"] if user else ""

    # Check for invitations
    invitations = db.execute("SELECT task_id FROM task_invitations WHERE email = ?", (student_email,)).fetchall()
    invited_task_ids = [i["task_id"] for i in invitations]

    query = """
        SELECT t.*, u.name as company_name, datetime('now') as current_time 
        FROM tasks t
        JOIN users u ON t.company_id = u.id
        WHERE t.status = 'Active'
    """
    params = []

    # ── LOGIC: If invited, show ONLY invited tasks ──
    if invited_task_ids:
        placeholders = ', '.join(['?'] * len(invited_task_ids))
        query += f" AND t.id IN ({placeholders})"
        params.extend(invited_task_ids)
        is_invited_view = True
    else:
        is_invited_view = False
        # Fallback to the regular application filter if the button was clicked
        if filter_applied:
            query += """ AND t.company_id IN (
                SELECT jp.company_id 
                FROM job_applications ja
                JOIN job_postings jp ON ja.job_id = jp.id
                WHERE ja.student_id = ?
            )"""
            params.append(session["user_id"])
        
    query += " ORDER BY t.id DESC"
    
    tasks = db.execute(query, params).fetchall()

    assigned = db.execute(
        "SELECT task_id FROM assignments WHERE student_id = ?",
        (session["user_id"],)
    ).fetchall()
    
    assigned_ids = [a["task_id"] for a in assigned]
    db.close()

    tasks_list = []
    for t in tasks:
        task_dict = dict(t)
        raw_langs = task_dict.get("languages") or "Python,C,C++,Java,JavaScript"
        task_dict["languages_list"] = [l.strip() for l in raw_langs.split(",") if l.strip()]
        
        # Format dates for UI
        task_dict["start_time_pretty"] = format_pretty_date(task_dict.get("start_time"))
        task_dict["end_time_pretty"] = format_pretty_date(task_dict.get("end_time"))
        
        # Calculate precise status in Python
        now = datetime.now()
        start_dt = parse_deadline(task_dict.get("start_time"))
        end_dt = parse_deadline(task_dict.get("end_time"))
        
        task_dict["is_upcoming"] = start_dt > now if start_dt else False
        task_dict["is_ended"] = end_dt < now if end_dt else False
        task_dict["is_live"] = not task_dict["is_upcoming"] and not task_dict["is_ended"]
        
        tasks_list.append(task_dict)

    return render_template("task_list.html",
        user_name=session["user_name"],
        tasks=tasks_list,
        assigned_ids=assigned_ids,
        filter_applied=filter_applied,
        is_invited_view=is_invited_view
    )

@app.route("/student/tasks/start/<int:task_id>")
def start_task(task_id):
    if "user_id" not in session or session["role"] != "student":
        return redirect(url_for("login"))

    db = get_db()
    
    existing = db.execute(
        "SELECT id FROM assignments WHERE student_id = ? AND task_id = ?",
        (session["user_id"], task_id)
    ).fetchone()
    
    if existing:
        db.close()
        return redirect(url_for("solve_task", assignment_id=existing["id"]))

    import random
    v_easy = db.execute("SELECT id FROM task_variants WHERE task_id = ? AND level = 'Easy'", (task_id,)).fetchall()
    v_med  = db.execute("SELECT id FROM task_variants WHERE task_id = ? AND level = 'Medium'", (task_id,)).fetchall()
    v_hard = db.execute("SELECT id FROM task_variants WHERE task_id = ? AND level = 'Hard'", (task_id,)).fetchall()
    
    ve_id = random.choice(v_easy)["id"] if v_easy else None
    vm_id = random.choice(v_med)["id"] if v_med else None
    vh_id = random.choice(v_hard)["id"] if v_hard else None
    
    task = db.execute(
        "SELECT * FROM tasks WHERE id = ?", 
        (task_id,)
    ).fetchone()
    
    if not task:
        db.close()
        flash("Task not found!", "error")
        return redirect(url_for("task_list"))

    # Security: Window Check using Local Time
    now = datetime.now()
    start_dt = parse_deadline(task["start_time"])
    end_dt = parse_deadline(task["end_time"])

    if start_dt and now < start_dt:
        db.close()
        flash(f"This assessment has not started yet. Starts at {format_pretty_date(task['start_time'])}", "error")
        return redirect(url_for("task_list"))
        
    if end_dt and now > end_dt:
        db.close()
        flash("This assessment window has closed.", "error")
        return redirect(url_for("task_list"))

    time_limit = task["time_limit"] if task else 60
    deadline = datetime.now() + timedelta(minutes=time_limit)

    
    task_code = generate_task_code()
    
    db.execute(
        """INSERT INTO assignments (task_id, student_id, variant_easy_id, variant_medium_id, variant_hard_id, task_code, deadline, language)
           VALUES (?, ?, ?, ?, ?, ?, ?, 'Python')""",
        (task_id, session["user_id"], ve_id, vm_id, vh_id, task_code, deadline)
    )
    
    assignment_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    db.commit()
    db.close()
    
    return redirect(url_for("solve_task", assignment_id=assignment_id))

@app.route("/student/solve/<int:assignment_id>", methods=["GET", "POST"])
def solve_task(assignment_id):
    if "user_id" not in session or session["role"] != "student":
        return redirect(url_for("login"))

    db = get_db()

    assignment = db.execute(
        """SELECT a.id as assignment_id, a.*, t.title, t.description, t.time_limit, a.task_code, u.name as company_name
           FROM assignments a
           JOIN tasks t ON a.task_id = t.id
           JOIN users u ON t.company_id = u.id
           WHERE a.id = ? AND a.student_id = ?""",
        (assignment_id, session["user_id"])
    ).fetchone()



    if not assignment:
        flash("Assignment not found!", "error")
        db.close()
        return redirect(url_for("task_list"))

    # ── Fetch All 3 Levels ──
    v_easy = db.execute("SELECT * FROM task_variants WHERE id = ?", (assignment["variant_easy_id"],)).fetchone()
    v_med  = db.execute("SELECT * FROM task_variants WHERE id = ?", (assignment["variant_medium_id"],)).fetchone()
    v_hard = db.execute("SELECT * FROM task_variants WHERE id = ?", (assignment["variant_hard_id"],)).fetchone()

    existing_submission = db.execute(
        "SELECT * FROM submissions WHERE assignment_id = ?",
        (assignment_id,)
    ).fetchone()

    # ── Strict One-Attempt Policy ─────────────────────────────
    if existing_submission and (existing_submission["solution_easy"] or existing_submission["solution"]):
        eval_done = db.execute("SELECT id FROM evaluations WHERE submission_id = ?", (existing_submission["id"],)).fetchone()
        db.close()
        if eval_done:
            flash("You have already completed this assessment.", "info")
            return redirect(url_for("results", evaluation_id=eval_done["id"]))
        else:
            flash("You have already submitted your answers. Please complete the verification.", "info")
            return redirect(url_for("verify_task", submission_id=existing_submission["id"]))

    if request.method == "POST":
        deadline_dt = parse_deadline(assignment["deadline"])
        if deadline_dt and datetime.now() > deadline_dt:
            flash("⏱ Submission deadline has passed!", "error")
            db.close()
            return redirect(url_for("my_submissions"))

        sol_easy = request.form.get("solution_easy", "")
        sol_med  = request.form.get("solution_medium", "")
        sol_hard = request.form.get("solution_hard", "")
        # Combined view for legacy compatibility
        full_solution = f"--- EASY ---\n{sol_easy}\n\n--- MEDIUM ---\n{sol_med}\n\n--- HARD ---\n{sol_hard}"

        if existing_submission:
            db.execute(
                """UPDATE submissions SET solution=?, solution_easy=?, solution_medium=?, solution_hard=? 
                   WHERE assignment_id=?""",
                (full_solution, sol_easy, sol_med, sol_hard, assignment_id)
            )
            submission_id = existing_submission["id"]
        else:
            db.execute(
                """INSERT INTO submissions (assignment_id, solution, solution_easy, solution_medium, solution_hard) 
                   VALUES (?, ?, ?, ?, ?)""",
                (assignment_id, full_solution, sol_easy, sol_med, sol_hard)
            )
            submission_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]

        db.commit()
        # ... (Email logic omitted for brevity in snippet)
        db.close()
        return redirect(url_for("verify_task", submission_id=submission_id))

    deadline_iso = format_deadline_iso(assignment["deadline"])
    deadline_passed = is_deadline_passed(assignment["deadline"])

    db.close()
    return render_template("solve_task.html", 
        user_name=session["user_name"], 
        assignment=assignment,
        v_easy=v_easy, v_med=v_med, v_hard=v_hard,
        existing_submission=existing_submission,
        deadline_iso=deadline_iso,
        deadline_passed=deadline_passed
    )

@app.route("/api/run_code", methods=["POST"])
def run_code():
    if "user_id" not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    data = request.get_json()
    code = data.get("code", "")
    language = data.get("language", "Python")
    sample_input = str(data.get("sample_input") or "")


    if not code.strip():
        return jsonify({"status": "error", "output": "", "error": "Code is empty. Write something first!"}), 400

    output, error = "", ""

    # ─────────── PYTHON ───────────
    if language == "Python":
        # Normalize code: convert tabs to spaces and standardize line endings
        code = code.replace('\t', '    ').replace('\r\n', '\n').replace('\r', '\n')
        
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "solution.py")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)
            try:
                res = subprocess.run(
                    [sys.executable, file_path],
                    input=sample_input,
                    capture_output=True, text=True, timeout=10,
                    encoding='utf-8'
                )
                output = res.stdout
                error  = res.stderr
            except subprocess.TimeoutExpired as te:
                output = te.stdout.decode() if isinstance(te.stdout, bytes) else (te.stdout or "")
                error = "⏱ Execution timed out (10 second limit reached). Your program may be in an infinite loop or waiting for more input than provided."
            except Exception as e:
                error = f"Execution error: {str(e)}"

    # ─────────── JAVASCRIPT (via js2py) ───────────
    elif language == "JavaScript":
        try:
            import js2py
            log_lines = []

            # Build a JS context that captures console.log
            context = js2py.EvalJs()
            context.execute("""
                var _output = [];
                var console = {
                    log:   function() { var args = Array.prototype.slice.call(arguments); _output.push(args.join(' ')); },
                    warn:  function() { var args = Array.prototype.slice.call(arguments); _output.push('[WARN] ' + args.join(' ')); },
                    error: function() { var args = Array.prototype.slice.call(arguments); _output.push('[ERROR] ' + args.join(' ')); },
                    info:  function() { var args = Array.prototype.slice.call(arguments); _output.push('[INFO] ' + args.join(' ')); }
                };
            """)
            try:
                context.execute(code)
                # Retrieve captured output from JS context
                raw = context._output.to_list() if hasattr(context._output, 'to_list') else list(context._output)
                output = "\n".join(str(x) for x in raw) if raw else ""
            except Exception as js_err:
                error = f"JavaScript Error: {str(js_err)}"
        except ImportError:
            error = "JavaScript engine not available. Please install: pip install js2py"
        except Exception as e:
            error = f"JavaScript execution error: {str(e)}"

    # ─────────── C ───────────
    elif language == "C":
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "solution.c")
            exec_path = os.path.join(temp_dir, "solution.exe")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)
            try:
                compile_res = subprocess.run(
                    ["gcc", file_path, "-o", exec_path],
                    capture_output=True, text=True, timeout=15,
                    encoding='utf-8'
                )
                if compile_res.returncode != 0:
                    error = "Compilation Error:\n" + compile_res.stderr
                else:
                    res = subprocess.run([exec_path], input=sample_input, capture_output=True, text=True, timeout=10, encoding='utf-8')
                    output = res.stdout
                    error  = res.stderr
            except FileNotFoundError:
                error = "⚠️ GCC compiler not found on this server. C execution is not available."
            except subprocess.TimeoutExpired as te:
                output = te.stdout.decode() if isinstance(te.stdout, bytes) else (te.stdout or "")
                error = "⏱ Execution timed out (10 second limit reached). Your program may be in an infinite loop or waiting for more input than provided."
            except Exception as e:
                error = f"Execution error: {str(e)}"

    # ─────────── C++ ───────────
    elif language == "C++":
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "solution.cpp")
            exec_path = os.path.join(temp_dir, "solution.exe")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)
            try:
                compile_res = subprocess.run(
                    ["g++", file_path, "-o", exec_path],
                    capture_output=True, text=True, timeout=15,
                    encoding='utf-8'
                )
                if compile_res.returncode != 0:
                    error = "Compilation Error:\n" + compile_res.stderr
                else:
                    res = subprocess.run([exec_path], input=sample_input, capture_output=True, text=True, timeout=10, encoding='utf-8')
                    output = res.stdout
                    error  = res.stderr
            except FileNotFoundError:
                error = "⚠️ G++ compiler not found on this server. C++ execution is not available."
            except subprocess.TimeoutExpired as te:
                output = te.stdout.decode() if isinstance(te.stdout, bytes) else (te.stdout or "")
                error = "⏱ Execution timed out (10 second limit reached). Your program may be in an infinite loop or waiting for more input than provided."
            except Exception as e:
                error = f"Execution error: {str(e)}"

    # ─────────── JAVA ───────────
    elif language == "Java":
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "Solution.java")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)
            try:
                compile_res = subprocess.run(
                    ["javac", file_path],
                    capture_output=True, text=True, timeout=15,
                    encoding='utf-8'
                )
                if compile_res.returncode != 0:
                    error = "Compilation Error:\n" + compile_res.stderr
                else:
                    res = subprocess.run(
                        ["java", "-cp", temp_dir, "Solution"],
                        input=sample_input,
                        capture_output=True, text=True, timeout=10,
                        encoding='utf-8'
                    )
                    output = res.stdout
                    error  = res.stderr
            except FileNotFoundError:
                error = "⚠️ Java (JDK) not found on this server. Java execution is not available."
            except subprocess.TimeoutExpired as te:
                output = te.stdout.decode() if isinstance(te.stdout, bytes) else (te.stdout or "")
                error = "⏱ Execution timed out (10 second limit reached). Your program may be in an infinite loop or waiting for more input than provided."
            except Exception as e:
                error = f"Execution error: {str(e)}"

    else:
        error = f"Language '{language}' is not supported."

    # Always return both output and error so frontend can show both
    return jsonify({
        "status":  "success",
        "output":  output.strip() if output else "",
        "error":   error.strip()  if error  else ""
    })

@app.route("/api/update_language", methods=["POST"])
def update_language():
    if "user_id" not in session:
        return jsonify({"status": "error"}), 401
    data = request.get_json()
    assignment_id = data.get("assignment_id")
    language = data.get("language", "Python")
    allowed = ["Python", "C", "C++", "Java", "JavaScript"]
    if language not in allowed:
        return jsonify({"status": "error", "message": "Invalid language"}), 400
    db = get_db()
    db.execute("UPDATE assignments SET language = ? WHERE id = ? AND student_id = ?",
               (language, assignment_id, session["user_id"]))
    db.commit()
    db.close()
    return jsonify({"status": "ok"})

@app.route("/api/log_activity", methods=["POST"])
def log_activity():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    assignment_id = data.get("assignment_id")
    event_type = data.get("event_type")
    
    db = get_db()
    db.execute("INSERT INTO activity_logs (assignment_id, event_type) VALUES (?, ?)", (assignment_id, event_type))
    db.commit()
    db.close()
    return jsonify({"status": "logged"})

@app.route("/api/autosave", methods=["POST"])
def autosave():
    if "user_id" not in session:
        return jsonify({"status": "error"}), 401
    data = request.get_json()
    assignment_id = data.get("assignment_id")
    level = data.get("level", "easy")
    solution = data.get("solution", "")
    
    db = get_db()
    existing = db.execute("SELECT id FROM submissions WHERE assignment_id = ?", (assignment_id,)).fetchone()
    
    col = f"autosave_{level}"
    if existing:
        db.execute(f"UPDATE submissions SET {col} = ? WHERE assignment_id = ?", (solution, assignment_id))
    else:
        db.execute(f"INSERT INTO submissions (assignment_id, {col}) VALUES (?, ?)", (assignment_id, solution))
    
    db.commit()
    db.close()
    return jsonify({"status": "ok"})



@app.route("/student/verify/<int:submission_id>", methods=["GET", "POST"])
def verify_task(submission_id):
    if "user_id" not in session or session["role"] != "student": 
        return redirect(url_for("login"))

    db = get_db()
    submission = db.execute(
        "SELECT s.*, a.task_id FROM submissions s JOIN assignments a ON s.assignment_id = a.id WHERE s.id = ?", 
        (submission_id,)
    ).fetchone()

    if submission:
        existing_eval = db.execute("SELECT id FROM evaluations WHERE submission_id = ?", (submission_id,)).fetchone()
        if existing_eval:
            db.close()
            flash("Verification already completed.", "info")
            return redirect(url_for("results", evaluation_id=existing_eval["id"]))


    if not submission:
        flash("Submission not found!", "error")
        db.close()
        return redirect(url_for("task_list"))

    questions = db.execute(
        "SELECT * FROM verification_questions WHERE task_id = ?", 
        (submission["task_id"],)
    ).fetchall()

    if request.method == "POST":
        for q in questions:
            answered = request.form.get(f"q_{q['id']}", "")
            db.execute(
                "INSERT INTO verification_answers (submission_id, question_id, student_answer) VALUES (?, ?, ?)", 
                (submission_id, q["id"], answered)
            )

        verification_score = 0
        solution_score = 0
        total_score = 0

        existing_eval = db.execute("SELECT * FROM evaluations WHERE submission_id = ?", (submission_id,)).fetchone()
        
        if existing_eval:
            db.execute("UPDATE evaluations SET verification_score=?, solution_score=?, total_score=? WHERE submission_id=?", 
                       (verification_score, solution_score, total_score, submission_id))
            eval_id = existing_eval["id"]
        else:
            db.execute("INSERT INTO evaluations (submission_id, solution_score, verification_score, total_score, status) VALUES (?, ?, ?, ?, 'Pending')", 
                       (submission_id, solution_score, verification_score, total_score))
            eval_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]

        db.commit()
        db.close()
        return redirect(url_for("results", evaluation_id=eval_id))

    db.close()
    return render_template("verify_task.html", 
        user_name=session["user_name"], 
        questions=questions, 
        submission_id=submission_id, 
        total=len(questions)
    )

@app.route("/student/results/<int:evaluation_id>")
def results(evaluation_id):
    if "user_id" not in session or session["role"] != "student": 
        return redirect(url_for("login"))

    db = get_db()
    evaluation = db.execute(
        """SELECT e.*, t.title, u.name as company_name FROM evaluations e 
           JOIN submissions s ON e.submission_id = s.id 
           JOIN assignments a ON s.assignment_id = a.id 
           JOIN tasks t ON a.task_id = t.id 
           JOIN users u ON t.company_id = u.id 
           WHERE e.id = ?""", 
        (evaluation_id,)
    ).fetchone()
    db.close()

    if not evaluation:
        flash("Results not found!", "error")
        return redirect(url_for("task_list"))

    return render_template("results.html", user_name=session["user_name"], evaluation=evaluation)

@app.route("/student/leaderboard")
def leaderboard():
    if "user_id" not in session or session["role"] != "student":
        return redirect(url_for("login"))

    db = get_db()
    company_filter = request.args.get("company_id")
    
    companies = db.execute("SELECT id, name FROM users WHERE role = 'company'").fetchall()

    query = """
        SELECT
            u.id                                                           AS student_id,
            u.name                                                         AS student_name,
            COUNT(DISTINCT e.id)                                           AS tasks_done,
            COALESCE(SUM(e.total_score), 0)                                AS total_score,
            COALESCE(AVG(CASE WHEN e.id IS NOT NULL THEN e.total_score END), 0) AS avg_score,
            MAX(e.total_score)                                             AS best_score,
            SUM(CASE WHEN e.status = 'Selected'    THEN 1 ELSE 0 END)     AS selected_count,
            SUM(CASE WHEN e.status = 'Shortlisted' THEN 1 ELSE 0 END)     AS shortlisted_count
        FROM users u
        LEFT JOIN assignments a ON a.student_id = u.id
        LEFT JOIN submissions s ON s.assignment_id = a.id
        LEFT JOIN evaluations e ON e.submission_id = s.id
        LEFT JOIN tasks t ON a.task_id = t.id
        WHERE u.role = 'student'
    """
    params = []
    if company_filter:
        query += " AND t.company_id = ?"
        params.append(company_filter)
        
    query += """
        GROUP BY u.id, u.name
        ORDER BY total_score DESC, avg_score DESC, tasks_done DESC
    """
    
    rows = db.execute(query, params).fetchall()

    leaderboard_data = []
    rank = 0
    for row in rows:
        entry = dict(row)
        entry["is_me"] = (row["student_id"] == session["user_id"])
        entry["avg_score"] = round(entry["avg_score"] or 0, 1)
        if entry["tasks_done"] > 0:
            rank += 1
            entry["rank"] = rank
            leaderboard_data.append(entry)

    my_rank = next((e["rank"] for e in leaderboard_data if e["is_me"]), None)

    # Safely convert company_filter to int only if it's a non-empty string of digits
    current_company_id = None
    if company_filter and company_filter.isdigit():
        current_company_id = int(company_filter)

    db.close()
    return render_template("leaderboard.html", 
        user_name=session["user_name"], 
        leaderboard=leaderboard_data,
        companies=companies,
        current_company=current_company_id,
        my_rank=my_rank
    )




@app.route("/student/submissions")
def my_submissions():
    if "user_id" not in session or session["role"] != "student": 
        return redirect(url_for("login"))

    db = get_db()
    
    submissions = db.execute(
        """SELECT s.id as sub_id, s.solution, s.submitted_at, 
                  t.title as task_title, t.difficulty, 
                  a.task_code, a.deadline, a.language, 
                  e.total_score, e.solution_score, e.verification_score, 
                  e.status, e.feedback, e.evaluated_at, e.id as eval_id, 
                  u.name as company_name 
           FROM submissions s 
           JOIN assignments a ON s.assignment_id = a.id 
           JOIN tasks t ON a.task_id = t.id 
           JOIN users u ON t.company_id = u.id 
           LEFT JOIN evaluations e ON e.submission_id = s.id 
           WHERE a.student_id = ? 
           ORDER BY s.submitted_at DESC""", 
        (session["user_id"],)
    ).fetchall()

    total = len(submissions)
    evaluated = sum(1 for s in submissions if s["total_score"] is not None)
    selected = sum(1 for s in submissions if s["status"] == "Selected")
    shortlisted = sum(1 for s in submissions if s["status"] == "Shortlisted")
    
    db.close()

    return render_template("my_submissions.html", 
        user_name=session["user_name"], 
        submissions=submissions, 
        total=total, 
        evaluated=evaluated, 
        selected=selected, 
        shortlisted=shortlisted
    )

# ─── PROFILE ROUTE ─────────────────────────────────────
@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session: 
        return redirect(url_for("login"))

    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        new_pass = request.form.get("new_password")
        curr_pass = request.form["current_password"]

        if not check_password_hash(user["password"], curr_pass):
            flash("Current password is incorrect!", "error")
            db.close()
            return redirect(url_for("profile"))

        if new_pass:
            new_hashed = generate_password_hash(new_pass)
            db.execute(
                "UPDATE users SET name=?, email=?, password=? WHERE id=?", 
                (name, email, new_hashed, session["user_id"])
            )
        else:
            db.execute(
                "UPDATE users SET name=?, email=? WHERE id=?", 
                (name, email, session["user_id"])
            )

        db.commit()
        session["user_name"] = name
        flash("Profile updated successfully!", "success")
        db.close()
        return redirect(url_for("profile"))

    db.close()
    return render_template("profile.html", user=user, user_name=session["user_name"])

# ─── COMPANY ROUTES ──────────────────────────────────────
@app.route("/company/dashboard")
def company_dashboard():
    if "user_id" not in session or session["role"] != "company":
        return redirect(url_for("login"))

    db = get_db()
    
    # Fetch verification status
    company = db.execute("SELECT verification_status FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    v_status = company["verification_status"] if company else "Pending"


    active_tasks = db.execute(
        "SELECT COUNT(*) as count FROM tasks WHERE company_id = ? AND status = 'Active'",
        (session["user_id"],)
    ).fetchone()

    total_submissions = db.execute(
        """SELECT COUNT(*) as count FROM submissions s
           JOIN assignments a ON s.assignment_id = a.id
           JOIN tasks t ON a.task_id = t.id
           WHERE t.company_id = ?""",
        (session["user_id"],)
    ).fetchone()

    shortlisted = db.execute(
        """SELECT COUNT(*) as count FROM evaluations e
           JOIN submissions s ON e.submission_id = s.id
           JOIN assignments a ON s.assignment_id = a.id
           JOIN tasks t ON a.task_id = t.id
           WHERE t.company_id = ? AND e.status = 'Shortlisted'""",
        (session["user_id"],)
    ).fetchone()

    selected = db.execute(
        """SELECT COUNT(*) as count FROM evaluations e
           JOIN submissions s ON e.submission_id = s.id
           JOIN assignments a ON s.assignment_id = a.id
           JOIN tasks t ON a.task_id = t.id
           WHERE t.company_id = ? AND e.status = 'Selected'""",
        (session["user_id"],)
    ).fetchone()

    recent_tasks = db.execute(
        "SELECT * FROM tasks WHERE company_id = ? ORDER BY id DESC LIMIT 5",
        (session["user_id"],)
    ).fetchall()

    db.close()

    return render_template("company_dashboard.html",
        user_name=session["user_name"],
        active_tasks=active_tasks["count"],
        total_submissions=total_submissions["count"],
        shortlisted=shortlisted["count"],
        selected=selected["count"],
        recent_tasks=recent_tasks,
        v_status=v_status
    )


@app.route("/company/tasks/new", methods=["GET", "POST"])
def post_task():
    if "user_id" not in session or session["role"] != "company": 
        return redirect(url_for("login"))
    
    db = get_db()
    company = db.execute("SELECT verification_status FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    if not company or company["verification_status"] != "Verified":
        db.close()
        flash("Your account must be verified by an admin before you can post tasks.", "error")
        return redirect(url_for("company_dashboard"))

    
    all_languages = ["Python", "C", "C++", "Java", "JavaScript", "TypeScript", "Go", "Rust", "Ruby", "Swift", "C#", "Kotlin", "PHP", "Scala", "R", "Haskell"]

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        time_limit = request.form["time_limit"]
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")

        # Convert empty strings to None
        if not start_time: start_time = None
        if not end_time: end_time = None

        db = get_db()
        try:
            # 1. Insert the main Task (container)
            db.execute(
                "INSERT INTO tasks (title, description, company_id, status, time_limit, start_time, end_time) VALUES (?, ?, ?, 'Active', ?, ?, ?)", 
                (title, description, session["user_id"], time_limit, start_time, end_time)
            )
            task_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]


            # 2. Insert EASY variants
            desc_easy = request.form.get("desc_easy")
            for i in range(1, 4):
                v_text = request.form.get(f"easy_v{i}")
                v_in   = request.form.get(f"easy_in{i}")
                v_out  = request.form.get(f"easy_out{i}")
                # We store the main desc_easy as part of the variant or we could store it separately. 
                # For simplicity, we combine them or use the variant_description.
                full_desc = f"{desc_easy}\n\nSPECIFIC REQUIREMENT: {v_text}"
                db.execute(
                    "INSERT INTO task_variants (task_id, level, variant_description, sample_input, sample_output) VALUES (?, 'Easy', ?, ?, ?)", 
                    (task_id, full_desc, v_in, v_out)
                )

            # 3. Insert MEDIUM variants
            desc_med = request.form.get("desc_medium")
            for i in range(1, 4):
                v_text = request.form.get(f"med_v{i}")
                v_in   = request.form.get(f"med_in{i}")
                v_out  = request.form.get(f"med_out{i}")
                full_desc = f"{desc_med}\n\nSPECIFIC REQUIREMENT: {v_text}"
                db.execute(
                    "INSERT INTO task_variants (task_id, level, variant_description, sample_input, sample_output) VALUES (?, 'Medium', ?, ?, ?)", 
                    (task_id, full_desc, v_in, v_out)
                )

            # 4. Insert HARD variants
            desc_hard = request.form.get("desc_hard")
            for i in range(1, 4):
                v_text = request.form.get(f"hard_v{i}")
                v_in   = request.form.get(f"hard_in{i}")
                v_out  = request.form.get(f"hard_out{i}")
                full_desc = f"{desc_hard}\n\nSPECIFIC REQUIREMENT: {v_text}"
                db.execute(
                    "INSERT INTO task_variants (task_id, level, variant_description, sample_input, sample_output) VALUES (?, 'Hard', ?, ?, ?)", 
                    (task_id, full_desc, v_in, v_out)
                )

            # 5. Insert Verification Questions
            for i in range(1, 4):
                q = request.form.get(f"q{i}")
                exp = request.form.get(f"q{i}_expected", "")
                db.execute(
                    "INSERT INTO verification_questions (task_id, question, expected_answer) VALUES (?, ?, ?)", 
                    (task_id, q, exp)
                )

            db.commit()
            flash("Multi-level Assessment Suite posted successfully!", "success")
            return redirect(url_for("company_dashboard")) 
        except Exception as e:
            flash(f"Error posting task: {str(e)}", "error")
        finally:
            db.close()
            
    return render_template("post_task.html", user_name=session["user_name"], all_languages=all_languages)

@app.route("/company/tasks")
def manage_tasks():
    if "user_id" not in session or session["role"] != "company": 
        return redirect(url_for("login"))
        
    db = get_db()
    tasks = db.execute("SELECT * FROM tasks WHERE company_id = ? ORDER BY id DESC", (session["user_id"],)).fetchall()
    
    tasks_list = []
    for t in tasks:
        task_dict = dict(t)
        task_dict["start_pretty"] = format_pretty_date(task_dict.get("start_time"))
        task_dict["end_pretty"] = format_pretty_date(task_dict.get("end_time"))
        tasks_list.append(task_dict)
    db.close()
    
    return render_template("manage_tasks.html", user_name=session["user_name"], tasks=tasks_list)

@app.route("/company/tasks/delete/<int:task_id>")
def delete_task(task_id):
    if "user_id" not in session or session["role"] != "company": 
        return redirect(url_for("login"))
        
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id = ? AND company_id = ?", (task_id, session["user_id"]))
    db.commit()
    db.close()
    
    flash("Task deleted successfully!", "success")
    return redirect(url_for("manage_tasks"))

@app.route("/company/tasks/toggle/<int:task_id>")
def toggle_task(task_id):
    if "user_id" not in session or session["role"] != "company": 
        return redirect(url_for("login"))
        
    db = get_db()
    task = db.execute("SELECT * FROM tasks WHERE id = ? AND company_id = ?", (task_id, session["user_id"])).fetchone()
    
    if not task:
        db.close()
        flash("Task not found!", "error")
        return redirect(url_for("manage_tasks"))

    new_status = "Draft" if task["status"] == "Active" else "Active"
    
    db.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
    db.commit()
    db.close()
    
    flash(f"Task '{task['title']}' is now {new_status}!", "success")
    return redirect(url_for("manage_tasks"))


@app.route("/company/task/<int:task_id>/ranking")
def task_ranking(task_id):
    if "user_id" not in session or session["role"] != "company":
        return redirect(url_for("login"))

    db = get_db()
    
    # Verify task ownership
    task = db.execute("SELECT title FROM tasks WHERE id = ? AND company_id = ?", (task_id, session["user_id"])).fetchone()
    if not task:
        db.close()
        flash("Task not found or access denied.", "error")
        return redirect(url_for("manage_tasks"))

    # Fetch ranked students for this specific task
    rankings = db.execute(
        """SELECT u.name as student_name, e.total_score, e.solution_score, e.verification_score, e.status, e.evaluated_at
           FROM evaluations e
           JOIN submissions s ON e.submission_id = s.id
           JOIN assignments a ON s.assignment_id = a.id
           JOIN users u ON a.student_id = u.id
           WHERE a.task_id = ?
           ORDER BY e.total_score DESC, e.evaluated_at ASC""",
        (task_id,)
    ).fetchall()

    db.close()
    return render_template("task_ranking.html", user_name=session["user_name"], task_title=task["title"], rankings=rankings)

@app.route("/company/invite", methods=["POST"])
def invite_candidate():
    if "user_id" not in session or session["role"] != "company":
        return redirect(url_for("login"))
    
    email = request.form.get("email")
    name = request.form.get("name")
    task_id = request.form.get("task_id")
    
    db = get_db()
    task = db.execute("SELECT title, company_id FROM tasks WHERE id = ?", (task_id,)).fetchone()
    
    if not task:
        db.close()
        flash("Task not found!", "error")
        return redirect(url_for("manage_tasks"))

    # Record the invitation in the database
    db.execute(
        "INSERT INTO task_invitations (email, task_id, company_id) VALUES (?, ?, ?)",
        (email, task_id, task["company_id"])
    )
    db.commit()
    db.close()

    subject = f"Invitation to Assessment: {task['title']}"
    body = f"""
    <h2 style="color:#fff;margin-top:0;">You're Invited!</h2>
    <p style="color:#94a3b8;font-size:16px;line-height:1.6;">
        Hello <strong>{name}</strong>,<br><br>
        <strong>{session['user_name']}</strong> has invited you to take the <strong>{task['title']}</strong> technical assessment on SkillHire.
    </p>
    <div style="margin:30px 0;text-align:center;">
        <a href="{request.host_url}login" style="background:#6366f1;color:#fff;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:bold;display:inline-block;">Accept Invitation</a>
    </div>
    <p style="color:#64748b;font-size:14px;">
        Log in to your student dashboard. Since you are invited, you will see <strong>only</strong> this specific task to avoid confusion.
    </p>
    """
    
    send_email(email, name, subject, body)
    flash(f"Invitation sent to {email} and recorded!", "success")
    return redirect(url_for("manage_tasks"))

@app.route("/company/submissions")


def view_submissions():
    if "user_id" not in session or session["role"] != "company": 
        return redirect(url_for("login"))

    db = get_db()
    
    submissions = db.execute(
        """SELECT s.id as sub_id, s.solution, s.submitted_at, 
                  u.name as student_name, u.email as student_email, 
                  t.title as task_title, t.difficulty, 
                  a.task_code, a.language, 
                  e.total_score, e.solution_score, e.verification_score, 
                  e.status, e.feedback, e.id as eval_id 
           FROM submissions s 
           JOIN assignments a ON s.assignment_id = a.id 
           JOIN tasks t ON a.task_id = t.id 
           JOIN users u ON a.student_id = u.id 
           LEFT JOIN evaluations e ON e.submission_id = s.id 
           WHERE t.company_id = ? 
           ORDER BY s.submitted_at DESC""", 
        (session["user_id"],)
    ).fetchall()
    
    db.close()

    return render_template("view_submissions.html", user_name=session["user_name"], submissions=submissions)

@app.route("/company/submissions/evaluate/<int:sub_id>", methods=["GET", "POST"])
def evaluate_submission(sub_id):
    if "user_id" not in session or session["role"] != "company": 
        return redirect(url_for("login"))
        
    db = get_db()
    
    eval_record = db.execute("SELECT * FROM evaluations WHERE submission_id = ?", (sub_id,)).fetchone()
    
    if request.method == "POST":
        sol_score = int(request.form.get("solution_score", 0))
        ver_score = int(request.form.get("verification_score", 0))
        feedback = request.form.get("feedback", "")
        status = request.form.get("status", "Pending")
        
        total_score = sol_score + ver_score
        
        if eval_record:
            db.execute("""UPDATE evaluations 
                          SET solution_score=?, verification_score=?, total_score=?, 
                              feedback=?, status=?, evaluated_at=CURRENT_TIMESTAMP 
                          WHERE submission_id=?""", 
                       (sol_score, ver_score, total_score, feedback, status, sub_id))
        else:
            db.execute("""INSERT INTO evaluations 
                          (submission_id, solution_score, verification_score, total_score, feedback, status) 
                          VALUES (?, ?, ?, ?, ?, ?)""", 
                       (sub_id, sol_score, ver_score, total_score, feedback, status))
            
        db.commit()

        # ── Notify student via email ──────────────────────────
        notif = db.execute("""
            SELECT u.email, u.name, t.title
            FROM submissions s
            JOIN assignments a ON s.assignment_id = a.id
            JOIN users u ON a.student_id = u.id
            JOIN tasks t ON a.task_id = t.id
            WHERE s.id = ?""", (sub_id,)).fetchone()
        if notif:
            sc = {"Selected": "#10b981", "Shortlisted": "#a5b4fc",
                  "Rejected": "#f87171", "Pending": "#f59e0b"}.get(status, "#94a3b8")
            send_email(
                to_email=notif["email"], to_name=notif["name"],
                subject=f"Evaluation Result – {notif['title']}",
                body_html=(
                    f'<h2 style="color:#a5b4fc;margin:0 0 12px;">&#128202; Your Evaluation Result</h2>'
                    f'<p style="color:#94a3b8;line-height:1.7;margin:0 0 16px;">'
                    f'Hi <strong style="color:#e2e8f0;">{notif["name"]}</strong>, your submission for '
                    f'<strong style="color:#a5b4fc;">{notif["title"]}</strong> has been evaluated.</p>'
                    f'<div style="background:#0f172a;border-radius:10px;padding:16px 18px;'
                    f'margin:0 0 16px;border:1px solid #334155;">'
                    f'<table style="width:100%;border-collapse:collapse;">'
                    f'<tr><td style="color:#64748b;font-size:12px;padding:5px 0;">Status</td>'
                    f'<td style="text-align:right;"><strong style="color:{sc};">{status}</strong></td></tr>'
                    f'<tr><td style="color:#64748b;font-size:12px;padding:5px 0;">Total Score</td>'
                    f'<td style="text-align:right;color:#e2e8f0;font-weight:700;">{total_score}</td></tr>'
                    f'<tr><td style="color:#64748b;font-size:12px;padding:5px 0;">Solution Score</td>'
                    f'<td style="text-align:right;color:#e2e8f0;">{sol_score}</td></tr>'
                    f'<tr><td style="color:#64748b;font-size:12px;padding:5px 0;">Verification Score</td>'
                    f'<td style="text-align:right;color:#e2e8f0;">{ver_score}</td></tr>'
                    f'</table>'
                    f'{f"""<p style="color:#94a3b8;font-size:13px;margin:12px 0 0;border-top:1px solid #334155;padding-top:10px;"><em>{feedback}</em></p>""" if feedback else ""}'
                    f'</div>'
                    f'<p style="color:#94a3b8;font-size:14px;">Log in to SkillHire to view your full results and leaderboard position.</p>'
                )
            )

        db.close()
        flash("Evaluation saved successfully!", "success")
        return redirect(url_for("view_submissions"))

    submission = db.execute(
        """SELECT s.*, u.name as student_name, a.language, a.task_code, 
                  t.title as task_title,
                  ve.variant_description as desc_easy,
                  vm.variant_description as desc_medium,
                  vh.variant_description as desc_hard
           FROM submissions s 
           JOIN assignments a ON s.assignment_id = a.id 
           JOIN tasks t ON a.task_id = t.id 
           JOIN users u ON a.student_id = u.id 
           LEFT JOIN task_variants ve ON a.variant_easy_id = ve.id 
           LEFT JOIN task_variants vm ON a.variant_medium_id = vm.id 
           LEFT JOIN task_variants vh ON a.variant_hard_id = vh.id 
           WHERE s.id = ?""", 
        (sub_id,)
    ).fetchone()

    
    answers = db.execute(
        """SELECT va.*, vq.question, vq.expected_answer 
           FROM verification_answers va 
           JOIN verification_questions vq ON va.question_id = vq.id 
           WHERE va.submission_id = ?""", 
        (sub_id,)
    ).fetchall()
    
    db.close()
    
    return render_template("evaluate_task.html", 
        user_name=session["user_name"], 
        submission=submission, 
        answers=answers, 
        evaluation=eval_record
    )

@app.route("/company/candidates")
def candidates():
    if "user_id" not in session or session["role"] != "company": 
        return redirect(url_for("login"))

    db = get_db()
    
    all_candidates = db.execute(
        """SELECT u.name as student_name, u.email as student_email, 
                  t.title as task_title, t.difficulty, 
                  e.total_score, e.solution_score, e.verification_score, 
                  e.status, e.feedback, e.evaluated_at, 
                  a.task_code, a.language, s.submitted_at, 
                  e.id as eval_id, s.id as sub_id 
           FROM evaluations e 
           JOIN submissions s ON e.submission_id = s.id 
           JOIN assignments a ON s.assignment_id = a.id 
           JOIN tasks t ON a.task_id = t.id 
           JOIN users u ON a.student_id = u.id 
           WHERE t.company_id = ? 
           ORDER BY e.total_score DESC""", 
        (session["user_id"],)
    ).fetchall()

    shortlisted = [c for c in all_candidates if c["status"] == "Shortlisted"]
    selected    = [c for c in all_candidates if c["status"] == "Selected"]
    rejected    = [c for c in all_candidates if c["status"] == "Rejected"]
    pending     = [c for c in all_candidates if c["status"] == "Pending"]

    db.close()

    return render_template("candidates.html", 
        user_name=session["user_name"], 
        all_candidates=all_candidates, 
        shortlisted=shortlisted, 
        selected=selected, 
        rejected=rejected, 
        pending=pending, 
        total=len(all_candidates), 
        total_short=len(shortlisted), 
        total_select=len(selected), 
        total_reject=len(rejected)
    )

@app.route("/company/candidates/update/<int:eval_id>/<string:new_status>")
def update_candidate_status(eval_id, new_status):
    if "user_id" not in session or session["role"] != "company": 
        return redirect(url_for("login"))

    if new_status not in ["Pending", "Shortlisted", "Selected", "Rejected"]:
        flash("Invalid status!", "error")
        return redirect(url_for("candidates"))

    db = get_db()
    db.execute("UPDATE evaluations SET status = ? WHERE id = ?", (new_status, eval_id))
    db.commit()
    db.close()

    flash(f"Candidate status successfully updated to {new_status}!", "success")
    return redirect(url_for("candidates"))

@app.route("/company/reports")
def reports():
    if "user_id" not in session or session["role"] != "company": 
        return redirect(url_for("login"))
        
    db = get_db()
    
    task_stats = db.execute(
        """SELECT t.title, COUNT(s.id) as count 
           FROM tasks t 
           LEFT JOIN assignments a ON t.id = a.task_id 
           LEFT JOIN submissions s ON a.id = s.assignment_id 
           WHERE t.company_id = ? 
           GROUP BY t.id""", 
        (session["user_id"],)
    ).fetchall()
    
    status_stats = db.execute(
        """SELECT e.status, COUNT(e.id) as count 
           FROM evaluations e 
           JOIN submissions s ON e.submission_id = s.id 
           JOIN assignments a ON s.assignment_id = a.id 
           JOIN tasks t ON a.task_id = t.id 
           WHERE t.company_id = ? 
           GROUP BY e.status""", 
        (session["user_id"],)
    ).fetchall()
    
    avg_scores = db.execute(
        """SELECT AVG(e.solution_score) as avg_sol, 
                  AVG(e.verification_score) as avg_ver, 
                  AVG(e.total_score) as avg_tot 
           FROM evaluations e 
           JOIN submissions s ON e.submission_id = s.id 
           JOIN assignments a ON s.assignment_id = a.id 
           JOIN tasks t ON a.task_id = t.id 
           WHERE t.company_id = ?""", 
        (session["user_id"],)
    ).fetchone()
    
    db.close()
    
    bar_labels = [row["title"] for row in task_stats] if task_stats else []
    bar_data = [row["count"] for row in task_stats] if task_stats else []
    
    pie_labels = [row["status"] for row in status_stats] if status_stats else []
    pie_data = [row["count"] for row in status_stats] if status_stats else []
    
    return render_template("reports.html", 
        user_name=session["user_name"], 
        bar_labels=bar_labels, 
        bar_data=bar_data, 
        pie_labels=pie_labels, 
        pie_data=pie_data, 
        avg=avg_scores
    )

# ─── ADMIN ROUTES ──────────────────────────────────────
@app.route("/admin/dashboard")
def admin_dashboard():
    if "user_id" not in session or session["role"] != "admin": 
        return redirect(url_for("login"))

    db = get_db()
    
    # 1. Verification Data
    companies = db.execute("SELECT * FROM users WHERE role = 'company' ORDER BY id DESC").fetchall()
    pending_count = db.execute("SELECT COUNT(*) as count FROM users WHERE role = 'company' AND verification_status = 'Pending'").fetchone()["count"]
    verified_count = db.execute("SELECT COUNT(*) as count FROM users WHERE role = 'company' AND verification_status = 'Verified'").fetchone()["count"]
    
    # 2. General Stats
    total_students = db.execute("SELECT COUNT(*) as c FROM users WHERE role = 'student'").fetchone()["c"]
    total_tasks = db.execute("SELECT COUNT(*) as c FROM tasks").fetchone()["c"]
    total_submissions = db.execute("SELECT COUNT(*) as c FROM submissions").fetchone()["c"]
    
    db.close()
    
    return render_template("admin_dashboard.html", 
        companies=companies,
        pending_count=pending_count,
        verified_count=verified_count,
        total_students=total_students,
        total_tasks=total_tasks,
        total_submissions=total_submissions
    )

@app.route("/admin/verify-action/<int:user_id>/<action>", methods=["POST"])
def admin_verify_action(user_id, action):
    db = get_db()
    status = "Verified" if action == "approve" else "Rejected"
    db.execute("UPDATE users SET verification_status = ? WHERE id = ?", (status, user_id))
    db.commit()
    db.close()
    flash(f"Company status updated to {status}!", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/users/delete/<int:uid>", methods=["POST"])
def admin_delete_user(uid):
    if "user_id" not in session or session["role"] != "admin": 
        return redirect(url_for("login"))
    
    if uid == session["user_id"]:
        flash("You cannot delete your own admin account!", "error")
        return redirect(url_for("admin_users"))
    
    db = get_db()
    db.execute("DELETE FROM users WHERE id = ?", (uid,))
    db.commit()
    db.close()
    
    flash("User deleted successfully from the platform.", "success")
    return redirect(url_for("admin_users"))


@app.route("/admin/analytics-old")

@app.route("/admin/logs")
def system_logs():
    if "user_id" not in session or session["role"] != "admin": 
        return redirect(url_for("login"))
        
    db = get_db()
    
    logs = db.execute("""
        SELECT al.id, al.event_type, al.logged_at, 
               u.name as student_name, u.email as student_email,
               t.title as task_title
        FROM activity_logs al
        JOIN assignments a ON al.assignment_id = a.id
        JOIN users u ON a.student_id = u.id
        JOIN tasks t ON a.task_id = t.id
        ORDER BY al.logged_at DESC LIMIT 100
    """).fetchall()
    
    db.close()
    return render_template("system_logs.html", user_name=session["user_name"], logs=logs)


# ─── JOB POSTINGS (Company Side) ──────────────────────────────────────────────
@app.route("/company/jobs", methods=["GET"])
def company_jobs():
    if "user_id" not in session or session["role"] != "company":
        return redirect(url_for("login"))
    db = get_db()
    jobs = db.execute(
        "SELECT * FROM job_postings WHERE company_id = ? ORDER BY id DESC",
        (session["user_id"],)
    ).fetchall()
    # Count applications per job
    app_counts = {}
    for j in jobs:
        c = db.execute(
            "SELECT COUNT(*) as c FROM job_applications WHERE job_id = ?", (j["id"],)
        ).fetchone()["c"]
        app_counts[j["id"]] = c
    db.close()
    return render_template("company_jobs.html",
        user_name=session["user_name"], jobs=jobs, app_counts=app_counts)

@app.route("/company/jobs/new", methods=["GET", "POST"])
def post_job():
    if "user_id" not in session or session["role"] != "company":
        return redirect(url_for("login"))
    if request.method == "POST":
        title       = request.form["title"]
        description = request.form["description"]
        location    = request.form.get("location", "Remote")
        job_type    = request.form.get("job_type", "Full-Time")
        salary      = request.form.get("salary", "")
        skills      = request.form.get("skills", "")
        openings    = int(request.form.get("openings", 1))
        db = get_db()
        db.execute(
            """INSERT INTO job_postings
               (company_id, title, description, location, job_type, salary, skills, openings)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (session["user_id"], title, description, location, job_type, salary, skills, openings)
        )
        db.commit()
        db.close()
        flash("Job posted successfully! Students can now apply.", "success")
        return redirect(url_for("company_jobs"))
    return render_template("post_job.html", user_name=session["user_name"])

@app.route("/company/jobs/toggle/<int:job_id>")
def toggle_job(job_id):
    if "user_id" not in session or session["role"] != "company":
        return redirect(url_for("login"))
    db = get_db()
    job = db.execute("SELECT status FROM job_postings WHERE id = ? AND company_id = ?",
                     (job_id, session["user_id"])).fetchone()
    if job:
        new_status = "Closed" if job["status"] == "Open" else "Open"
        db.execute("UPDATE job_postings SET status = ? WHERE id = ?", (new_status, job_id))
        db.commit()
        flash(f"Job status changed to {new_status}.", "success")
    db.close()
    return redirect(url_for("company_jobs"))

@app.route("/company/jobs/delete/<int:job_id>")
def delete_job(job_id):
    if "user_id" not in session or session["role"] != "company":
        return redirect(url_for("login"))
    db = get_db()
    db.execute("DELETE FROM job_applications WHERE job_id = ?", (job_id,))
    db.execute("DELETE FROM job_postings WHERE id = ? AND company_id = ?",
               (job_id, session["user_id"]))
    db.commit()
    db.close()
    flash("Job posting deleted.", "success")
    return redirect(url_for("company_jobs"))

@app.route("/company/jobs/<int:job_id>/applications")
def job_applicants(job_id):
    if "user_id" not in session or session["role"] != "company":
        return redirect(url_for("login"))
    db = get_db()
    job = db.execute("SELECT * FROM job_postings WHERE id = ? AND company_id = ?",
                     (job_id, session["user_id"])).fetchone()
    if not job:
        flash("Job not found!", "error")
        db.close()
        return redirect(url_for("company_jobs"))
    applicants = db.execute(
        """SELECT ja.*, u.name as student_name, u.email as student_email
           FROM job_applications ja
           JOIN users u ON ja.student_id = u.id
           WHERE ja.job_id = ?
           ORDER BY ja.applied_at DESC""",
        (job_id,)
    ).fetchall()
    db.close()
    return render_template("job_applicants.html",
        user_name=session["user_name"], job=job, applicants=applicants)

@app.route("/company/jobs/applications/update/<int:app_id>/<string:new_status>")
def update_application_status(app_id, new_status):
    if "user_id" not in session or session["role"] != "company":
        return redirect(url_for("login"))
    allowed = ["Applied", "Reviewing", "Shortlisted", "Accepted", "Rejected"]
    if new_status not in allowed:
        flash("Invalid status!", "error")
        return redirect(url_for("company_jobs"))
    db = get_db()
    app_row = db.execute("SELECT ja.*, jp.company_id, jp.id as job_id FROM job_applications ja JOIN job_postings jp ON ja.job_id=jp.id WHERE ja.id=?", (app_id,)).fetchone()
    if app_row and app_row["company_id"] == session["user_id"]:
        db.execute("UPDATE job_applications SET status = ? WHERE id = ?", (new_status, app_id))
        db.commit()
        flash(f"Application status updated to {new_status}.", "success")
        db.close()
        return redirect(url_for("job_applicants", job_id=app_row["job_id"]))
    db.close()
    return redirect(url_for("company_jobs"))

# ─── JOB POSTINGS (Student Side) ──────────────────────────────────────────────
@app.route("/student/jobs")
def student_jobs():
    if "user_id" not in session or session["role"] != "student":
        return redirect(url_for("login"))
    db = get_db()
    jobs = db.execute(
        """SELECT jp.*, u.name as company_name
           FROM job_postings jp
           JOIN users u ON jp.company_id = u.id
           WHERE jp.status = 'Open'
           ORDER BY jp.id DESC"""
    ).fetchall()
    applied_ids = [r["job_id"] for r in db.execute(
        "SELECT job_id FROM job_applications WHERE student_id = ?", (session["user_id"],)
    ).fetchall()]
    db.close()
    return render_template("student_jobs.html",
        user_name=session["user_name"], jobs=jobs, applied_ids=applied_ids)

@app.route("/student/jobs/<int:job_id>/apply", methods=["POST"])
def apply_job(job_id):
    if "user_id" not in session or session["role"] != "student":
        return redirect(url_for("login"))
    cover_letter = request.form.get("cover_letter", "")
    resume_link  = request.form.get("resume_link", "")
    db = get_db()
    try:
        db.execute(
            "INSERT INTO job_applications (job_id, student_id, cover_letter, resume_link) VALUES (?, ?, ?, ?)",
            (job_id, session["user_id"], cover_letter, resume_link)
        )
        db.commit()
        flash("Application submitted successfully! 🎉", "success")
    except Exception:
        flash("You have already applied for this job.", "error")
    finally:
        db.close()
    return redirect(url_for("student_jobs"))

@app.route("/student/my-applications")
def my_applications():
    if "user_id" not in session or session["role"] != "student":
        return redirect(url_for("login"))
    db = get_db()
    applications = db.execute(
        """SELECT ja.*, jp.title as job_title, jp.location, jp.job_type,
                  jp.salary, jp.skills, u.name as company_name
           FROM job_applications ja
           JOIN job_postings jp ON ja.job_id = jp.id
           JOIN users u ON jp.company_id = u.id
           WHERE ja.student_id = ?
           ORDER BY ja.applied_at DESC""",
        (session["user_id"],)
    ).fetchall()
    db.close()
    total = len(applications)
    accepted = sum(1 for a in applications if a["status"] == "Accepted")
    shortlisted = sum(1 for a in applications if a["status"] == "Shortlisted")
    rejected = sum(1 for a in applications if a["status"] == "Rejected")
    return render_template("my_applications.html",
        user_name=session["user_name"],
        applications=applications,
        total=total, accepted=accepted,
        shortlisted=shortlisted, rejected=rejected)

@app.route("/admin/users")
def admin_users():
    if "user_id" not in session or session["role"] != "admin":
        return redirect(url_for("login"))
    db = get_db()
    users = db.execute("SELECT id, name, email, role, verification_status FROM users ORDER BY id DESC").fetchall()
    db.close()
    return render_template("admin_users.html", users=users)

@app.route("/admin/analytics")
def admin_analytics():
    if "user_id" not in session or session["role"] != "admin":
        return redirect(url_for("login"))
    db = get_db()
    stats = {
        "total_students": db.execute("SELECT COUNT(*) FROM users WHERE role='student'").fetchone()[0],
        "total_companies": db.execute("SELECT COUNT(*) FROM users WHERE role='company'").fetchone()[0],
        "total_tasks": db.execute("SELECT COUNT(*) FROM tasks").fetchone()[0],
        "total_submissions": db.execute("SELECT COUNT(*) FROM submissions").fetchone()[0],
        "total_jobs": db.execute("SELECT COUNT(*) FROM job_postings").fetchone()[0],
        "total_applications": db.execute("SELECT COUNT(*) FROM job_applications").fetchone()[0],
    }
    db.close()
    return render_template("admin_analytics.html", stats=stats)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

