# SkillHire – Skill-Based Reverse Internship Platform

## 📌 Project Overview

SkillHire is a web-based **Skill-Based Reverse Internship Platform** designed to provide an alternative to traditional resume-based recruitment.

In conventional recruitment, companies often depend on resumes, academic scores, and profile information to shortlist candidates. However, these details may not always represent a candidate's actual problem-solving ability or practical skills.

SkillHire follows a **skill-first approach**, where candidates get an opportunity to demonstrate their abilities by solving practical, job-related tasks. Companies can then evaluate candidates based on their actual task performance.

The platform integrates job posting, applications, task assignment, practical assessments, submissions, evaluation, and company-specific leaderboards into a single system.

---

## 🎯 Problem Statement

Traditional internship and recruitment platforms mainly depend on resumes, academic performance, and profile-based screening.

This can create a gap between a candidate's qualifications and their actual practical abilities. A candidate may have good academic credentials but may not be able to demonstrate the practical skills required for a particular role.

The problem addressed by SkillHire is:

> **How can candidates be evaluated based on their actual practical skills and problem-solving abilities instead of relying primarily on resumes and academic scores?**

SkillHire addresses this problem by allowing companies to create practical tasks and enabling applicants to demonstrate their skills through structured assessments.

---

## 💡 Proposed Solution

SkillHire provides a centralized platform where:

- Students can register and log in.
- Companies can register and undergo verification.
- Verified companies can create job postings.
- Companies can create practical tasks for applicants.
- Students can view available jobs and apply.
- Candidates receive practical assessments.
- Tasks are provided in **Easy, Medium, and Hard** difficulty levels.
- Different task variants can be randomly assigned to candidates.
- Assessments are time-bound.
- Candidates can save their work through auto-save functionality.
- Verification questions can be used to check conceptual understanding.
- Candidates submit their solutions through the platform.
- Companies review and evaluate submissions.
- Candidate performance can be represented through a company-specific leaderboard.
- Admins can monitor and manage the platform.

---

# 🔄 Reverse Internship Concept

Traditional recruitment generally follows:

**Resume → Shortlisting → Interview → Selection**

SkillHire follows a skill-based approach:

**Job → Practical Task → Skill Demonstration → Evaluation → Selection**

The idea is to allow candidates to demonstrate their abilities directly through practical tasks relevant to the internship or job.

---

# 🏗️ System Architecture

The overall architecture of SkillHire can be represented as:

```text
                ┌──────────────────────┐
                │       Users          │
                │ Student / Company    │
                │       / Admin        │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Authentication &     │
                │ Role-Based Access    │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │    Flask Backend     │
                │   Python Application │
                └──────────┬───────────┘
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
       ┌──────────┐  ┌──────────┐  ┌──────────┐
       │ Student  │  │ Company  │  │  Admin   │
       │ Module   │  │ Module   │  │ Module   │
       └────┬─────┘  └────┬─────┘  └────┬─────┘
            │             │             │
            └─────────────┼─────────────┘
                          ▼
                ┌──────────────────────┐
                │ Job & Task Management│
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Task Assignment &    │
                │ Random Variants      │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Practical Assessment │
                │ Easy / Medium / Hard │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Submission &         │
                │ Verification         │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Evaluation & Results │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Company-Specific     │
                │ Leaderboard          │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │    SQLite Database   │
                └──────────────────────┘
🔁 System Workflow
Start
  ↓
Student / Company Registration
  ↓
Login & Authentication
  ↓
Role-Based Access
  ↓
Admin Verifies Company
  ↓
Company Creates Job
  ↓
Company Creates Practical Tasks
  ↓
Student Views Available Jobs
  ↓
Student Applies
  ↓
Task Assignment
  ↓
Random Task Variant Selection
  ↓
Easy / Medium / Hard Assessment
  ↓
Time-Bound Task Solving
  ↓
Submission
  ↓
Verification Questions
  ↓
Company Evaluation
  ↓
Result Processing
  ↓
Company-Specific Leaderboard
  ↓
Selection / Rejection
  ↓
End
👥 User Modules
1. Student Module

Students can:

Register on the platform.
Log in securely.
View available job postings.
Apply for opportunities.
Access assigned assessments.
Solve practical tasks.
Attempt Easy, Medium, and Hard tasks.
Work within the given time limit.
Save their progress automatically.
Answer verification questions.
Submit completed solutions.
View submission/result status.
2. Company Module

Companies can:

Register on the platform.
Log in using company credentials.
Submit company information for verification.
Create job postings after verification.
Create practical assessment tasks.
Configure task difficulty.
Assign tasks to candidates.
View candidate submissions.
Evaluate candidate solutions.
Shortlist candidates.
Select or reject candidates.
View candidate performance through the company-specific leaderboard.
3. Admin Module

The Admin module provides platform-level management.

The administrator can:

Verify company registrations.
Manage platform users.
Monitor platform activity.
View platform-level information and analytics.
Control company access to recruitment features.

The Admin does not perform the candidate's technical evaluation; candidate submissions are handled through the company evaluation process.

📝 Task-Based Assessment

One of the main features of SkillHire is practical task-based assessment.

Companies can create tasks based on the skills required for a particular internship or job.

Tasks can be organized into:

Easy
  ↓
Medium
  ↓
Hard

This allows candidates to demonstrate their abilities at multiple difficulty levels.

🎲 Randomized Task Variants

The system supports multiple variants of a task.

For example:

Task
 ├── Easy
 │    ├── Variant 1
 │    ├── Variant 2
 │    └── Variant 3
 │
 ├── Medium
 │    ├── Variant 1
 │    ├── Variant 2
 │    └── Variant 3
 │
 └── Hard
      ├── Variant 1
      ├── Variant 2
      └── Variant 3

When an assessment is assigned, the system can randomly select a variant from each available difficulty level.

This helps provide different task versions to candidates and can reduce direct copying between submissions.

⏱️ Time-Bound Assessments

Each assessment can have a configured time limit.

When a candidate starts an assessment, the system creates a deadline for the assignment.

The candidate must submit the solution before the deadline.

This provides a structured assessment environment and ensures that the assessment is completed within the defined time period.

💾 Auto-Save

SkillHire includes an auto-save mechanism for candidate solutions.

The candidate's work can be periodically stored in the database while the assessment is in progress.

This helps reduce the possibility of losing work because of:

Browser issues
Accidental refresh
Temporary interruptions
Connectivity problems
❓ Verification Questions

The platform can include verification questions after the practical task.

These questions are intended to check whether the candidate understands the solution and the concepts used while solving the task.

This provides an additional layer of assessment beyond simply receiving a submitted solution.

📤 Submission & Evaluation

After completing the assessment, candidates submit their solutions through the platform.

The submission process stores:

Easy-level solution
Medium-level solution
Hard-level solution
Complete submission
Assignment information

Companies can then review the submitted solutions and evaluate candidates.

The current implementation uses a manual/hybrid evaluation approach, providing a foundation for future automated evaluation.

🏆 Company-Specific Leaderboard

SkillHire provides a leaderboard for candidate performance within a company's assessment.

The leaderboard can be used to compare candidates based on their assessment performance.

The leaderboard is associated with the respective company rather than being a single global ranking across all companies.

🔐 Authentication & Role-Based Access Control

The platform supports separate access for:

Student
Company
Admin

Role-based access ensures that each type of user accesses only the features relevant to their role.

For example:

Student → Jobs, Applications, Tasks, Submissions

Company → Jobs, Tasks, Candidates, Evaluation

Admin → Verification, User Management, Monitoring

Flask sessions are used to maintain authenticated user information.

🏢 Company Verification

When a company registers, its verification status is initially set to:

Pending

The administrator can verify the company before allowing it to use recruitment functionality.

This provides an additional control layer for company participation on the platform.

🗄️ Database

SkillHire uses SQLite as its database.

The project database contains tables supporting the major platform operations, including:

users
tasks
task_variants
assignments
submissions
verification_questions
verification_answers
evaluations
activity_logs
job_postings
job_applications
task_invitations

The database stores information related to users, companies, jobs, tasks, assignments, submissions, and evaluations.

🛠️ Technology Stack
Frontend
HTML5
CSS3
JavaScript
Jinja2 Templates
Backend
Python
Flask
Database
SQLite
Authentication & Security
Flask Sessions
Password Hashing
Role-Based Access Control
Development Tools
Visual Studio Code
Git
GitHub
Python Virtual Environment
Operating Environment
Windows
📚 Methodology

The development methodology consists of the following stages:

1. User Registration & Authentication

Students and companies register and log in according to their roles.

2. Company Verification

Registered companies are verified by the administrator.

3. Job Posting

Verified companies create internship/job opportunities.

4. Task Creation

Companies create practical tasks with different difficulty levels.

5. Application & Assignment

Students apply for opportunities and receive relevant assessments.

6. Random Variant Selection

The system assigns available task variants to candidates.

7. Practical Assessment

Candidates solve the assigned Easy, Medium, and Hard tasks within the given time limit.

8. Submission & Verification

Candidates submit their solutions and answer verification questions where applicable.

9. Evaluation

Companies review and evaluate candidate submissions.

10. Results & Leaderboard

Candidate performance is processed and displayed through company-specific results and leaderboards.

🎯 Objectives

The main objectives of SkillHire are:

Evaluate candidates based on practical skills.
Reduce excessive dependence on resume-based screening.
Provide companies with job-specific skill assessments.
Enable candidates to demonstrate real-world problem-solving abilities.
Improve the structure and transparency of internship recruitment.
Provide randomized and time-bound assessments.
Integrate the complete recruitment and assessment process into one platform.
⭐ Key Features
Skill-based recruitment
Reverse internship model
Student and company portals
Admin verification
Role-based authentication
Job posting
Job application
Practical task creation
Easy / Medium / Hard assessments
Randomized task variants
Time-bound assessments
Auto-save
Verification questions
Candidate submissions
Company evaluation
Shortlist / Select / Reject workflow
Company-specific leaderboard
Centralized database
🌱 Benefits
For Students
Opportunity to demonstrate practical skills.
Direct participation in skill-based assessments.
Reduced dependence on resume presentation alone.
Exposure to practical job-related tasks.
Transparent assessment workflow.
For Companies
Ability to create job-specific tasks.
Direct access to candidate submissions.
Practical skill assessment.
Structured candidate evaluation.
Candidate comparison through leaderboards.
For Administrators
Centralized platform management.
Company verification.
User management.
Platform monitoring.
🌍 Impact

SkillHire aims to create a more practical recruitment environment by connecting internship opportunities with direct skill demonstration.

The platform can help:

Encourage skill-based evaluation.
Provide students with opportunities to demonstrate practical abilities.
Help companies assess candidates using job-related tasks.
Reduce the gap between theoretical knowledge and practical requirements.
Streamline internship recruitment and assessment.
📊 Feasibility
Technical Feasibility

The system is developed using commonly available technologies such as Python, Flask, HTML, CSS, JavaScript, and SQLite.

Economic Feasibility

The project uses open-source technologies and does not require expensive software for its basic implementation.

Operational Feasibility

The platform provides separate interfaces for students, companies, and administrators, making the workflow structured and manageable.

Scalability

The current version is designed as a prototype using SQLite. The architecture can later be extended using a production database and cloud infrastructure.

💻 System Requirements
Hardware
Computer/Laptop
Minimum 4 GB RAM
Internet connection for development/deployment activities
Software
Python 3.x
Flask
Visual Studio Code
Git
Web Browser
SQLite
📁 Project Structure
skill_hire/
│
├── templates/
│   ├── admin templates
│   ├── student templates
│   ├── company templates
│   └── assessment templates
│
├── static/
│   ├── CSS
│   ├── JavaScript
│   └── other static files
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
└── database files

Local database files, virtual environments, environment files, and other sensitive/local files are excluded from Git using .gitignore.

🚀 How to Run the Project
1. Clone the Repository
git clone https://github.com/Shreep07/Skill-based-reverse-internship-platform.git
2. Open the Project
cd Skill-based-reverse-internship-platform
3. Create a Virtual Environment
python -m venv venv
4. Activate the Virtual Environment
Windows PowerShell
venv\Scripts\Activate.ps1
Windows Command Prompt
venv\Scripts\activate
5. Install Flask
pip install flask

If additional dependencies are added to the project in the future, install them before running the application.

6. Run the Application
python app.py
7. Open in Browser
http://127.0.0.1:5000
🔒 Data & Security Considerations

The project uses .gitignore to prevent local and sensitive files from being uploaded to GitHub.

The following types of files are excluded:

Virtual environments
SQLite databases
Environment files
Python cache
IDE files
Logs
Temporary tunnel files

This prevents local database information and environment-specific files from being unnecessarily exposed in the public repository.

⚠️ Current Limitations

The current version of SkillHire has some limitations:

Candidate evaluation is currently manual/hybrid.
Fully automated code evaluation is not implemented.
Advanced plagiarism detection is not implemented.
SQLite is used as the current database for the prototype.
Advanced AI-based candidate evaluation is not currently implemented.
The current system is primarily designed as a prototype and can be extended for production deployment.
🔮 Future Enhancements

Possible future improvements include:

AI-Based Evaluation

Introduce automated evaluation of candidate solutions using AI and rule-based assessment techniques.

Intelligent Candidate Matching

Recommend suitable candidates to companies based on demonstrated skills and assessment performance.

Advanced Plagiarism Detection

Introduce more advanced similarity and plagiarism detection mechanisms for candidate submissions.

Video Interviews

Add an integrated video interview module for shortlisted candidates.

Advanced Analytics

Provide detailed dashboards for candidate performance, assessment statistics, and recruitment analytics.

Cloud Deployment

Deploy the platform on cloud infrastructure for wider accessibility and scalability.

Production Database

Migrate from SQLite to a production database such as PostgreSQL or MySQL for larger deployments.

🔍 Difference from Conventional Recruitment Platforms
Conventional Recruitment	SkillHire
Resume-focused screening	Skill-focused assessment
Academic/profile information is commonly used	Practical task performance is emphasized
Separate recruitment and assessment tools may be used	Integrated recruitment and assessment workflow
General interviews/tests	Job-related practical tasks
Candidate profile is a major input	Demonstrated task performance is an important input
Limited task personalization	Company-created tasks and variants

SkillHire does not completely eliminate resumes or other recruitment methods. Instead, it provides an additional practical assessment approach for evaluating candidate skills.

📌 Project Highlights
✔ Skill-Based Reverse Internship Platform
✔ Practical Job-Related Assessments
✔ Easy / Medium / Hard Tasks
✔ Randomized Task Variants
✔ Time-Bound Assessments
✔ Auto-Save
✔ Verification Questions
✔ Company Verification
✔ Role-Based Access Control
✔ Job Posting & Applications
✔ Candidate Submission & Evaluation
✔ Company-Specific Leaderboard
✔ Centralized Recruitment Workflow
📈 Project Status

Current Status: Working Prototype

The current implementation supports the major workflow from user authentication and company verification to job posting, applications, task assignment, assessment, submission, evaluation, and leaderboard generation.

The system provides a foundation that can be extended with automated evaluation, AI-based assessment, advanced analytics, cloud deployment, and additional recruitment features.

👩‍💻 Contributors
Shree P

Computer Science Engineering (Data Science)

Rithu R

Computer Science Engineering (Data Science)

📜 License

This project has been developed as an academic mini-project.

It is intended for educational, demonstration, and development purposes.