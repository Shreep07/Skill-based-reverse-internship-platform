# SkillHire – Skill-Based Reverse Internship Platform

## 1. Project Overview

SkillHire is a web-based Skill-Based Reverse Internship Platform designed to provide an alternative approach to traditional resume-based recruitment.

In conventional recruitment, companies often depend on resumes, academic scores, and profile information to shortlist candidates. However, these details may not always represent a candidate's actual practical skills and problem-solving ability.

SkillHire follows a skill-first approach where candidates get an opportunity to demonstrate their abilities by solving practical, job-related tasks. Companies can then evaluate candidates based on their actual task performance.

The platform integrates job posting, job applications, task assignment, practical assessments, submissions, evaluation, result processing, and company-specific leaderboards into a single system.

---

## 2. Problem Statement

Traditional internship and recruitment platforms mainly depend on resumes, academic performance, and profile-based screening.

This can create a gap between a candidate's qualifications and their actual practical abilities. A candidate may have good academic credentials but may not always be able to demonstrate the practical skills required for a particular role.

The problem addressed by SkillHire is:

> How can candidates be evaluated based on their actual practical skills and problem-solving abilities instead of relying primarily on resumes and academic scores?

SkillHire addresses this problem by allowing companies to create practical tasks and enabling applicants to demonstrate their skills through structured assessments.

---

## 3. Proposed Solution

SkillHire provides a centralized platform where students, companies, and administrators can interact through role-based portals.

Students can apply for job opportunities and demonstrate their skills through practical assessments. Companies can create job postings and job-specific tasks and evaluate candidate submissions. Administrators verify companies and manage the overall platform.

The proposed system includes:

- Student registration and login
- Company registration and login
- Admin authentication and management
- Company verification
- Job posting
- Job applications
- Practical task creation
- Easy, Medium, and Hard difficulty levels
- Randomized task variants
- Time-bound assessments
- Auto-save functionality
- Verification questions
- Candidate submissions
- Company evaluation
- Candidate status management
- Company-specific leaderboards
- Result processing
- Centralized database management

---

## 4. Reverse Internship Concept

**Traditional recruitment generally follows:**

```
Resume → Shortlisting → Interview → Selection
```

**SkillHire follows a skill-based approach:**

```
Job Opportunity → Practical Task → Skill Demonstration → Evaluation → Selection
```

The main idea is to allow candidates to demonstrate their abilities directly through practical tasks relevant to the internship or job. Instead of depending only on a candidate's resume or academic profile, companies can use practical task performance as an additional basis for evaluation.

---

## 5. System Architecture

The SkillHire system follows a layered web application architecture. The major components of the architecture are:

1. User Layer
2. Authentication and Role-Based Access Layer
3. Flask Backend Layer
4. Application Modules
5. Assessment and Evaluation Layer
6. Database Layer

### 5.1 Architecture Diagram

```text
                         ┌─────────────────────────┐
                         │         USERS           │
                         │                         │
                         │ Student | Company |     │
                         │ Admin                   │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │ Authentication &        │
                         │ Role-Based Access       │
                         │ Control                 │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │      FLASK BACKEND      │
                         │       Python            │
                         └────────────┬────────────┘
                                      │
             ┌────────────────────────┼────────────────────────┐
             │                        │                        │
             ▼                        ▼                        ▼
     ┌────────────────┐      ┌────────────────┐      ┌────────────────┐
     │ Student Module │      │ Company Module │      │  Admin Module  │
     │                │      │                │      │                │
     │ • Jobs         │      │ • Jobs         │      │ • Verification │
     │ • Applications │      │ • Tasks        │      │ • Users        │
     │ • Tasks        │      │ • Candidates   │      │ • Monitoring   │
     │ • Submissions  │      │ • Evaluation   │      │ • Analytics    │
     └───────┬────────┘      └───────┬────────┘      └───────┬────────┘
             │                       │                       │
             └───────────────────────┼───────────────────────┘
                                     │
                                     ▼
                         ┌─────────────────────────┐
                         │ Job & Task Management   │
                         │                         │
                         │ • Job Posting           │
                         │ • Job Application       │
                         │ • Task Creation         │
                         │ • Task Configuration    │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │ Task Assignment         │
                         │ & Random Variant        │
                         │ Selection               │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │ Practical Assessment    │
                         │                         │
                         │ Easy | Medium | Hard    │
                         │                         │
                         │ Time Limit + Auto-Save  │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │ Submission &            │
                         │ Verification            │
                         │                         │
                         │ • Solutions             │
                         │ • Verification Questions│
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │ Company Evaluation      │
                         │                         │
                         │ Pending                 │
                         │ Shortlisted             │
                         │ Selected                │
                         │ Rejected                │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │ Results & Company       │
                         │ Specific Leaderboard    │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │      SQLite Database    │
                         │                         │
                         │ Users                   │
                         │ Jobs                    │
                         │ Tasks                   │
                         │ Assignments             │
                         │ Submissions             │
                         │ Evaluations             │
                         │ Applications            │
                         └─────────────────────────┘
```

### 5.2 Architecture Components

**User Layer**

The system supports three major user roles:

- Student
- Company
- Admin

Each role has separate functionality and permissions.

**Authentication Layer**

The authentication layer manages:

- Registration
- Login
- Logout
- Password verification
- User sessions
- Role-based access

Flask sessions are used to maintain the authenticated user's information.

**Flask Backend**

Python Flask acts as the central backend framework. It handles:

- HTTP requests
- User authentication
- Database operations
- Job management
- Task management
- Assignment creation
- Submission handling
- Evaluation workflow
- Result processing

**Student Module**

The Student module allows candidates to:

- Register
- Login
- View available jobs
- Apply for jobs
- View assigned tasks
- Start assessments
- Solve practical tasks
- Save progress
- Submit solutions
- Answer verification questions
- View submission status

**Company Module**

The Company module allows companies to:

- Register
- Login
- Complete company verification
- Create job postings
- Create practical tasks
- Configure difficulty levels
- Assign tasks
- View candidate submissions
- Evaluate candidates
- Shortlist candidates
- Select candidates
- Reject candidates
- View company-specific leaderboard

**Admin Module**

The Admin module provides platform-level control. The administrator can:

- Verify companies
- Manage users
- Monitor the platform
- View platform-level information
- Manage company access

> The Admin does not perform the technical evaluation of student submissions.

**Assessment Layer**

The assessment layer manages:

- Task assignment
- Randomized task variants
- Difficulty levels
- Time limits
- Auto-save
- Verification questions
- Candidate submissions

**Evaluation Layer**

The evaluation layer allows companies to review candidate submissions and update candidate status. Possible statuses include:

- Pending
- Shortlisted
- Selected
- Rejected

**Database Layer**

SQLite is used as the central database. It stores information related to users, jobs, applications, tasks, assignments, submissions, verification questions, evaluations, and other platform operations.

---

## 6. System Workflow

The complete workflow of SkillHire is:

```text
                         START
                           |
                           ▼
              Student / Company Registration
                           |
                           ▼
                  Login & Authentication
                           |
                           ▼
                Role-Based Access Control
                           |
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
          STUDENT       COMPANY       ADMIN
              │            │            │
              │            ▼            ▼
              │      Company Registration
              │            │
              │            ▼
              │      Admin Verification
              │            │
              │            ▼
              │      Job & Task Creation
              │            │
              ▼            │
        View Available Jobs│
              │            │
              ▼            │
          Apply for Job    │
              │            │
              └──────┬─────┘
                     │
                     ▼
               Task Assignment
                     │
                     ▼
           Random Variant Selection
                     │
                     ▼
        ┌────────────────────────────┐
        │      PRACTICAL TEST        │
        │                            │
        │ Easy → Medium → Hard       │
        │                            │
        │ Time-Bound + Auto-Save     │
        └─────────────┬──────────────┘
                      │
                      ▼
                  Submission
                      │
                      ▼
             Verification Questions
                      │
                      ▼
              Company Evaluation
                      │
                      ▼
              Result Processing
                      │
                      ▼
          Company-Specific Leaderboard
                      │
                      ▼
             Selected / Rejected
                      │
                      ▼
                     END
```

---

## 7. User Modules

### 7.1 Student Module

Students can:

- Register on the platform
- Login securely
- View available job postings
- Apply for opportunities
- View assigned assessments
- Access practical tasks
- Solve Easy, Medium, and Hard tasks
- Work within the given time limit
- Save their progress automatically
- Answer verification questions
- Submit solutions
- View submission and result status

### 7.2 Company Module

Companies can:

- Register on the platform
- Login using company credentials
- Submit company information for verification
- Create job postings after verification
- Create practical assessment tasks
- Configure task difficulty
- Assign tasks to candidates
- View candidate submissions
- Evaluate candidate solutions
- Shortlist candidates
- Select candidates
- Reject candidates
- View candidate performance through the company-specific leaderboard

### 7.3 Admin Module

The Admin module provides platform-level management. The administrator can:

- Verify company registrations
- Manage platform users
- Monitor the platform
- View platform-level analytics
- Control company access to recruitment functionality

> The Admin does not perform technical evaluation of candidate submissions.

---

## 8. Job Posting and Application Module

Verified companies can create internship or job opportunities.

A job posting can be associated with practical tasks that candidates must complete during the recruitment process.

Students can:

- View available job postings
- Select a suitable opportunity
- Apply for the opportunity
- Receive access to the required assessment
- Complete the assigned task

This connects the job application process directly with practical skill assessment.

---

## 9. Task Management Module

Companies can create practical tasks based on the skills required for a particular job or internship.

Tasks can be organized into three difficulty levels:

- Easy
- Medium
- Hard

The task management system supports the creation and assignment of different task variants.

---

## 10. Randomized Task Variants

SkillHire supports multiple variants for practical tasks. The structure can be represented as:

```text
Task
│
├── Easy
│   ├── Variant 1
│   ├── Variant 2
│   └── Variant 3
│
├── Medium
│   ├── Variant 1
│   ├── Variant 2
│   └── Variant 3
│
└── Hard
    ├── Variant 1
    ├── Variant 2
    └── Variant 3
```

When a candidate starts an assessment, the system randomly selects an available variant from each difficulty level. This provides different task versions to candidates and helps reduce direct copying between submissions.

---

## 11. Practical Assessment

Candidates solve practical tasks instead of being evaluated only through their resumes or academic information.

The assessment contains:

- Easy-level task
- Medium-level task
- Hard-level task
- Time limit
- Candidate solution fields
- Verification questions
- Submission functionality

The assessment is designed to evaluate practical problem-solving and understanding.

---

## 12. Time-Bound Assessment

Each task can have a configured time limit.

When a candidate starts an assessment:

1. The system identifies the configured time limit.
2. A deadline is generated for the assignment.
3. The candidate works on the assigned tasks.
4. The candidate must submit before the deadline.
5. Submission after the deadline is restricted.

This provides a structured assessment environment.

---

## 13. Auto-Save Functionality

SkillHire provides an auto-save mechanism for candidate solutions.

Candidate progress can be stored periodically while the assessment is in progress.

Auto-save helps reduce the possibility of losing work because of:

- Accidental refresh
- Browser issues
- Temporary interruptions
- Connectivity problems

---

## 14. Verification Questions

Verification questions are used as an additional layer of assessment.

After completing the practical task, candidates may be required to answer questions related to their solution.

This helps check whether the candidate understands the concepts and approach used in their submission.

---

## 15. Submission Module

Candidates submit their solutions through the platform.

The submission process handles:

- Easy-level solution
- Medium-level solution
- Hard-level solution
- Complete submission
- Assignment information

The submitted information is stored in the database and made available for company evaluation.

---

## 16. Evaluation Module

Companies can review candidate submissions through their dashboard.

The current system follows a manual/hybrid evaluation approach. Companies can review solutions and update candidate status.

The candidate workflow includes:

```
Pending → Shortlisted → Selected
```

or

```
Pending → Rejected
```

Fully automated code evaluation is not part of the current implementation and can be added as a future enhancement.

---

## 17. Company-Specific Leaderboard

The platform generates a leaderboard based on candidate performance for a company's assessment.

The leaderboard allows companies to compare candidates participating in their assessment.

The ranking is company-specific rather than being a single global ranking across the platform.

---

## 18. Authentication and Security

SkillHire uses role-based authentication.

The three major roles are:

- Student
- Company
- Admin

The backend verifies the user's role before allowing access to role-specific routes.

The system also uses password hashing for storing user passwords securely.

Flask sessions maintain information such as:

- User ID
- User role
- User name

This allows the application to identify authenticated users during their session.

---

## 19. Company Verification

When a company registers, its verification status is initially stored as:

```
Pending
```

The administrator can review and verify the company.

After successful verification, the company can access recruitment functionality such as job and task creation.

This provides an additional level of control over company participation.

---

## 20. Database Design

SkillHire uses SQLite as the database management system.

The current project database contains tables including:

- `users`
- `tasks`
- `task_variants`
- `assignments`
- `submissions`
- `verification_questions`
- `verification_answers`
- `evaluations`
- `activity_logs`
- `job_postings`
- `job_applications`
- `task_invitations`

### Main Database Relationships

```text
Users
 │
 ├──────────────► Job Postings
 │                     │
 │                     ▼
 │               Job Applications
 │                     │
 │                     ▼
 │                   Tasks
 │                     │
 │                     ▼
 │               Task Variants
 │                     │
 │                     ▼
 │                Assignments
 │                     │
 │                     ▼
 │                Submissions
 │                     │
 │                     ▼
 │                Evaluations
 │                     │
 │                     ▼
 │                 Results
```

---

## 21. Technology Stack

**Frontend**
- HTML5
- CSS3
- JavaScript
- Jinja2 Templates

**Backend**
- Python
- Flask

**Database**
- SQLite

**Authentication and Security**
- Flask Sessions
- Password Hashing
- Role-Based Access Control

**Development Tools**
- Visual Studio Code
- Git
- GitHub
- Python Virtual Environment

**Operating Environment**
- Windows

---

## 22. Methodology

The development methodology consists of the following stages:

| Stage | Description |
|-------|-------------|
| 1 | User Registration and Authentication — Students and companies register and log in according to their roles |
| 2 | Company Verification — Registered companies are verified by the administrator |
| 3 | Job Posting — Verified companies create internship and job opportunities |
| 4 | Task Creation — Companies create practical tasks and define their difficulty levels |
| 5 | Application — Students browse job opportunities and apply for suitable positions |
| 6 | Task Assignment — Candidates receive practical assessments associated with the job opportunity |
| 7 | Random Variant Selection — The system randomly selects available task variants |
| 8 | Practical Assessment — Candidates solve Easy, Medium, and Hard tasks within the configured time limit |
| 9 | Submission — Candidates submit their solutions through the platform |
| 10 | Verification — Verification questions may be used to validate candidate understanding |
| 11 | Evaluation — Companies review and evaluate candidate submissions |
| 12 | Result Processing — Candidate statuses and evaluation results are updated |
| 13 | Leaderboard — Candidate performance is represented through a company-specific leaderboard |

---

## 23. Objectives

The main objectives of SkillHire are:

- Evaluate candidates based on practical skills
- Reduce excessive dependence on resume-based screening
- Provide companies with job-specific practical assessments
- Allow candidates to demonstrate real-world problem-solving abilities
- Improve the structure and transparency of internship recruitment
- Provide randomized and time-bound assessments
- Integrate recruitment and assessment processes into a single platform

---

## 24. Key Features

- Skill-based recruitment
- Reverse internship model
- Student portal
- Company portal
- Admin portal
- Company verification
- Role-based authentication
- Job posting
- Job applications
- Practical task creation
- Easy / Medium / Hard tasks
- Randomized task variants
- Time-bound assessments
- Auto-save
- Verification questions
- Candidate submissions
- Company evaluation
- Candidate status management
- Company-specific leaderboard
- Centralized database

---

## 25. Benefits

**Benefits for Students**
- Opportunity to demonstrate practical skills
- Direct participation in skill-based assessments
- Reduced dependence on resume presentation alone
- Exposure to practical job-related tasks
- Structured assessment workflow

**Benefits for Companies**
- Ability to create job-specific practical tasks
- Direct access to candidate submissions
- Practical skill assessment
- Structured candidate evaluation
- Candidate comparison through company-specific leaderboards

**Benefits for Administrators**
- Centralized platform management
- Company verification
- User management
- Platform monitoring

---

## 26. Impact

SkillHire aims to create a more practical recruitment environment by connecting internship opportunities with direct skill demonstration.

The platform can help:

- Encourage skill-based evaluation
- Provide students with opportunities to demonstrate practical abilities
- Help companies assess candidates using job-related tasks
- Reduce the gap between theoretical knowledge and practical requirements
- Streamline internship recruitment and assessment

---

## 27. Feasibility

**Technical Feasibility**
The system is developed using commonly available technologies such as Python, Flask, HTML, CSS, JavaScript, and SQLite. These technologies are suitable for developing and testing the current web-based prototype.

**Economic Feasibility**
The project uses open-source technologies and does not require expensive software for its basic implementation.

**Operational Feasibility**
The platform provides separate interfaces for students, companies, and administrators, making the workflow structured and manageable.

**Scalability**
The current version uses SQLite and is designed as a prototype. The system can later be extended using a production database and cloud infrastructure.

---

## 28. System Requirements

**Hardware Requirements**
- Computer or Laptop
- Minimum 4 GB RAM
- Internet connection for development and deployment activities

**Software Requirements**
- Python 3.x
- Flask
- Visual Studio Code
- Git
- Web Browser
- SQLite

---

## 29. Project Structure

```text
skill_hire/
│
├── templates/
│   ├── Admin templates
│   ├── Student templates
│   ├── Company templates
│   └── Assessment templates
│
├── static/
│   ├── CSS
│   ├── JavaScript
│   └── Other static files
│
├── app.py
├── database.py
├── create_admin.py
├── migrate.py
├── migrate_db.py
├── reset_password.py
├── start_tunnel.py
├── upgrade_to_suite.py
│
├── README.md
├── .gitignore
│
└── Database files
```

Local database files, virtual environments, environment files, cache files, logs, and temporary tunnel files are excluded from Git using `.gitignore`.

---

## 30. How to Run the Project

**Step 1 – Clone the Repository**
```bash
git clone https://github.com/Shreep07/Skill-based-reverse-internship-platform.git
```

**Step 2 – Open the Project**
```bash
cd Skill-based-reverse-internship-platform
```

**Step 3 – Create a Virtual Environment**
```bash
python -m venv venv
```

**Step 4 – Activate the Virtual Environment**

For Windows PowerShell:
```powershell
venv\Scripts\Activate.ps1
```

For Windows Command Prompt:
```cmd
venv\Scripts\activate
```

**Step 5 – Install Flask**
```bash
pip install flask
```

**Step 6 – Run the Application**
```bash
python app.py
```

**Step 7 – Open the Application**
```
http://127.0.0.1:5000
```

---

## 31. Data and Security Considerations

The project uses `.gitignore` to prevent local and sensitive files from being uploaded to GitHub.

The following types of files are excluded:

- Virtual environments
- SQLite databases
- Environment files
- Python cache
- IDE files
- Logs
- Temporary tunnel files

This helps prevent local database information and environment-specific files from being unnecessarily exposed in the public repository.

---

## 32. Current Limitations

The current version of SkillHire has some limitations:

- Candidate evaluation is currently manual/hybrid
- Fully automated code evaluation is not implemented
- Advanced plagiarism detection is not implemented
- SQLite is used as the current database for the prototype
- Advanced AI-based candidate evaluation is not currently implemented
- The current system is primarily designed as a prototype and can be extended for production deployment

---

## 33. Future Enhancements

**AI-Based Evaluation**
Introduce automated evaluation of candidate solutions using AI and rule-based assessment techniques.

**Intelligent Candidate Matching**
Recommend suitable candidates to companies based on demonstrated skills and assessment performance.

**Advanced Plagiarism Detection**
Introduce advanced similarity and plagiarism detection mechanisms for candidate submissions.

**Video Interviews**
Add an integrated video interview module for shortlisted candidates.

**Advanced Analytics**
Provide detailed dashboards for candidate performance, assessment statistics, and recruitment analytics.

**Cloud Deployment**
Deploy the platform on cloud infrastructure for wider accessibility and scalability.

**Production Database**
Migrate from SQLite to a production database such as PostgreSQL or MySQL for larger deployments.

---

## 34. Difference from Conventional Recruitment Platforms

| Conventional Recruitment | SkillHire |
|---|---|
| Resume-focused screening | Skill-focused assessment |
| Academic/profile information is commonly used | Practical task performance is emphasized |
| Recruitment and assessment may be handled separately | Integrated recruitment and assessment workflow |
| General interviews or tests | Job-related practical tasks |
| Candidate profile is a major input | Demonstrated task performance is an important input |
| Limited task personalization | Company-created tasks and task variants |

SkillHire does not completely eliminate resumes or other recruitment methods. Instead, it provides an additional practical assessment approach for evaluating candidate skills.

---

## 35. Project Highlights

- Skill-Based Reverse Internship Platform
- Practical Job-Related Assessments
- Easy / Medium / Hard Tasks
- Randomized Task Variants
- Time-Bound Assessments
- Auto-Save
- Verification Questions
- Company Verification
- Role-Based Access Control
- Job Posting and Applications
- Candidate Submission and Evaluation
- Candidate Status Management
- Company-Specific Leaderboard
- Centralized Recruitment Workflow

---

## 36. Project Status

**Current Status: Working Prototype**

The current implementation supports the major workflow from user authentication and company verification to job posting, applications, task assignment, assessment, submission, evaluation, and leaderboard generation.

The system provides a foundation that can be extended with automated evaluation, AI-based assessment, advanced analytics, cloud deployment, production database support, and additional recruitment features.

---

## 37. Contributors

**Shree P**
Computer Science Engineering (Data Science)

**Rithu R**
Computer Science Engineering (Data Science)

---

## 38. License

This project has been developed as an academic mini-project.

It is intended for educational, demonstration, and development purposes.