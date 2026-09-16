import sqlite3

def get_db():
    conn = sqlite3.connect("skillhire.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # 1. USERS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('student', 'company', 'admin')),
            website TEXT,
            contact TEXT,
            tax_id TEXT,
            verification_status TEXT DEFAULT 'Pending' -- For companies: Pending, Verified, Rejected
        )

    ''')

    # 2. TASKS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            difficulty TEXT CHECK(difficulty IN ('Easy', 'Medium', 'Hard')),
            company_id INTEGER,
            status TEXT DEFAULT 'Active',
            time_limit INTEGER DEFAULT 45,
            start_time TIMESTAMP,
            end_time TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES users(id)
        )
    ''')


    # 3. TASK VARIANTS TABLE (Anti-Cheat)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS task_variants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            level TEXT CHECK(level IN ('Easy', 'Medium', 'Hard')),
            variant_description TEXT,
            sample_input TEXT,
            sample_output TEXT,
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        )
    ''')

    # 4. ASSIGNMENTS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            student_id INTEGER,
            variant_easy_id INTEGER,
            variant_medium_id INTEGER,
            variant_hard_id INTEGER,
            task_code TEXT UNIQUE,
            assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            deadline TIMESTAMP,
            language TEXT,
            FOREIGN KEY (task_id) REFERENCES tasks(id),
            FOREIGN KEY (student_id) REFERENCES users(id)
        )
    ''')

    # 5. SUBMISSIONS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assignment_id INTEGER,
            solution TEXT,
            solution_easy TEXT,
            solution_medium TEXT,
            solution_hard TEXT,
            autosave_easy TEXT,
            autosave_medium TEXT,
            autosave_hard TEXT,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            autosave TEXT,
            FOREIGN KEY (assignment_id) REFERENCES assignments(id)
        )
    ''')

    # 6. VERIFICATION QUESTIONS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS verification_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            question TEXT NOT NULL,
            expected_answer TEXT,
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        )
    ''')

    # 7. VERIFICATION ANSWERS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS verification_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submission_id INTEGER,
            question_id INTEGER,
            student_answer TEXT,
            FOREIGN KEY (submission_id) REFERENCES submissions(id),
            FOREIGN KEY (question_id) REFERENCES verification_questions(id)
        )
    ''')

    # 8. EVALUATIONS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submission_id INTEGER,
            solution_score INTEGER DEFAULT 0,
            verification_score INTEGER DEFAULT 0,
            total_score INTEGER DEFAULT 0,
            feedback TEXT,
            status TEXT DEFAULT 'Pending' CHECK(status IN ('Pending', 'Shortlisted', 'Selected', 'Rejected')),
            evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (submission_id) REFERENCES submissions(id)
        )
    ''')

    # 9. ACTIVITY LOGS TABLE (For Admin System Logs / Anti-cheat)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assignment_id INTEGER,
            event_type TEXT,
            logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (assignment_id) REFERENCES assignments(id)
        )
    ''')

    # 10. JOB POSTINGS TABLE (Companies post job openings)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_postings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            location TEXT DEFAULT 'Remote',
            job_type TEXT DEFAULT 'Full-Time',
            salary TEXT DEFAULT '',
            skills TEXT DEFAULT '',
            openings INTEGER DEFAULT 1,
            status TEXT DEFAULT 'Open',
            posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES users(id)
        )
    ''')

    # 11. JOB APPLICATIONS TABLE (Students apply to job postings)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            cover_letter TEXT DEFAULT '',
            resume_link TEXT DEFAULT '',
            status TEXT DEFAULT 'Applied',
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (job_id) REFERENCES job_postings(id),
            FOREIGN KEY (student_id) REFERENCES users(id),
            UNIQUE(job_id, student_id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Database created successfully with all tables!")


if __name__ == "__main__":
    init_db()
