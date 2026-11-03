"""
Database Access Layer for Jitendra Kumar Jena Portfolio
Supports SQLite natively, with an architectural abstraction ready for MySQL and PostgreSQL.
Separates all SQL and persistence logic cleanly from routing and UI.
"""

import os
import sqlite3
import uuid
from datetime import datetime

# Database file location
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_FILE = os.path.join(BASE_DIR, 'database.db')


def get_connection():
    """
    Returns a configured database connection with dictionary-like row access.
    Can be swapped or extended for psycopg2 (PostgreSQL) or mysql-connector-python.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Creates necessary tables and seeds default project data if empty.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Contacts Table (Mandatory per specification)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # 2. Projects Table (Allows dynamic addition and management of portfolio projects)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            short_description TEXT NOT NULL,
            description TEXT NOT NULL,
            image_static TEXT NOT NULL,
            technologies TEXT NOT NULL,
            github_url TEXT DEFAULT '',
            demo_url TEXT DEFAULT '',
            is_featured INTEGER DEFAULT 1,
            display_order INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()

    # Pre-populate project records if not yet populated
    seed_default_projects()


def seed_default_projects():
    """
    Seeds comprehensive real projects reflecting Jitendra's actual resume and required projects.
    """
    default_projects = [
        {
            'slug': 'student-marks-prediction',
            'title': 'Student Marks Prediction System',
            'category': 'machine-learning',
            'short_description': 'A Machine Learning regression system analyzing study habits, attendance, and historical metrics to forecast student academic performance.',
            'description': 'End-to-end predictive analytics application built with Python, Scikit-learn, and Flask. Evaluates student performance data across historical test results, study hours, and classroom attendance. Employs Random Forest and Linear Regression models with 92% R² accuracy, delivering actionable insights and automated risk alerts to educators.',
            'image_static': 'images/projects/student_marks_pred.svg',
            'technologies': 'Python, Scikit-Learn, Flask, NumPy, Pandas, Matplotlib, HTML5/CSS3',
            'github_url': 'https://github.com/Jitendra14-4',
            'demo_url': '#',
            'is_featured': 1,
            'display_order': 1
        },
        {
            'slug': 'student-management-system',
            'title': 'Student Management System & RAG QA Chatbot',
            'category': 'fullstack',
            'short_description': 'Enterprise student portal with role-based access, automated grading, and a Retrieval-Augmented Generation (RAG) QA chatbot achieving 90% test accuracy.',
            'description': 'Production-ready full-stack academic management system built with Python, Flask/Django, and MySQL. Implemented dynamic course enrollments, grade calculations, fee tracking, and an integrated in-memory cached RAG chatbot answering student academic queries with 90% validated test accuracy.',
            'image_static': 'images/projects/student_mgmt.svg',
            'technologies': 'Python, Flask, MySQL, RAG, LangChain, HTML5, Bootstrap 5, REST API',
            'github_url': 'https://github.com/Jitendra14-4',
            'demo_url': '#',
            'is_featured': 1,
            'display_order': 2
        },
        {
            'slug': 'hospital-management-system',
            'title': 'Electronic Hospital Management System',
            'category': 'fullstack',
            'short_description': 'A clinical healthcare management platform streamlining doctor appointment scheduling, patient EHR records, and billing with REST endpoints.',
            'description': 'Developed a secure Python backend app to automate hospital workflow, patient consultation scheduling, and medical records management. Implemented multi-tier authentication, doctor shift allocation, invoice generation, and secure REST endpoints to handle sensitive healthcare data.',
            'image_static': 'images/projects/hospital_mgmt.svg',
            'technologies': 'Python, Django, Flask, MySQL, REST API, JavaScript, Bootstrap 5',
            'github_url': 'https://github.com/Jitendra14-4',
            'demo_url': '#',
            'is_featured': 1,
            'display_order': 3
        },
        {
            'slug': 'sales-data-analysis-dashboard',
            'title': 'Sales Data Analysis Dashboard',
            'category': 'data-analysis',
            'short_description': 'Interactive visual analytics dashboard analyzing enterprise sales trends, regional performance KPIs, and profit margins using Pandas and SQL.',
            'description': 'Cleaned and structured massive multi-channel commercial sales datasets using Python and Pandas. Executed complex SQL aggregations to isolate profit leaks, seasonality spikes, and customer segments. Designed interactive visual dashboards using Matplotlib, Seaborn, and Power BI.',
            'image_static': 'images/projects/sales_analytics.svg',
            'technologies': 'Python, Pandas, NumPy, SQL, Seaborn, Matplotlib, Power BI, Excel',
            'github_url': 'https://github.com/Jitendra14-4',
            'demo_url': '#',
            'is_featured': 1,
            'display_order': 4
        },
        {
            'slug': 'paddy-moisture-detection',
            'title': 'Paddy Moisture Detection System',
            'category': 'machine-learning',
            'short_description': 'Government agricultural IoT & Machine Learning system to determine grain moisture suitability, preventing spoilage and ensuring procurement compliance.',
            'description': 'Built for agricultural grain evaluation during Quality Analysis workflow. Ingests grain sensor telemetry, performs exploratory data analysis in Python, and applies classification algorithms to flag acceptable moisture thresholds (under 14% compliance) for Government procurement.',
            'image_static': 'images/projects/paddy_moisture.svg',
            'technologies': 'Python, Scikit-Learn, Pandas, NumPy, Data Analysis, SQLite, Flask',
            'github_url': 'https://github.com/Jitendra14-4',
            'demo_url': '#',
            'is_featured': 1,
            'display_order': 5
        },
        {
            'slug': 'ai-job-finder',
            'title': 'AI-Based Job Finder & Semantic Match Engine',
            'category': 'machine-learning',
            'short_description': 'Intelligent career matching platform parsing resume skills and ranking live job openings using NLP embeddings and cosine similarity scoring.',
            'description': 'An intelligent automated candidate-job recommendation platform. Extracts unstructured developer resume competencies (Python, Django, SQL, Data Science) and parses web-scraped job requisitions. Employs NLP vector embeddings to score candidate fit with sub-second matching latency.',
            'image_static': 'images/projects/job_finder.svg',
            'technologies': 'Python, Flask, NLP, Cosine Similarity, BeautifulSoup, SQLite, REST API',
            'github_url': 'https://github.com/Jitendra14-4',
            'demo_url': '#',
            'is_featured': 1,
            'display_order': 6
        }
    ]

    conn = get_connection()
    cursor = conn.cursor()

    for proj in default_projects:
        cursor.execute("""
            INSERT INTO projects (
                slug, title, category, short_description, description, 
                image_static, technologies, github_url, demo_url, is_featured, display_order
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(slug) DO UPDATE SET
                title = excluded.title,
                category = excluded.category,
                short_description = excluded.short_description,
                description = excluded.description,
                image_static = excluded.image_static,
                technologies = excluded.technologies,
                github_url = excluded.github_url,
                demo_url = excluded.demo_url,
                is_featured = excluded.is_featured,
                display_order = excluded.display_order;
        """, (
            proj['slug'], proj['title'], proj['category'],
            proj['short_description'], proj['description'],
            proj['image_static'], proj['technologies'],
            proj['github_url'], proj['demo_url'],
            proj['is_featured'], proj['display_order']
        ))

    conn.commit()
    conn.close()


def save_contact(name, email, phone, subject, message):
    """
    Inserts a contact form submission into the SQLite database.
    Uses parameterized queries to safeguard against SQL injection.
    Generates a unique submission ID and logs the timestamp.
    """
    submission_id = f"CNT-{uuid.uuid4().hex[:8].upper()}"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO contacts (id, name, email, phone, subject, message, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (submission_id, name, email, phone or None, subject, message, now_str))

    conn.commit()
    conn.close()

    return {
        'id': submission_id,
        'name': name,
        'email': email,
        'phone': phone,
        'subject': subject,
        'message': message,
        'created_at': now_str
    }


def get_all_contacts(limit=100):
    """
    Retrieves latest contact submissions for inspection and verification.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, email, phone, subject, message, created_at
        FROM contacts
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()

    contacts = []
    for r in rows:
        contacts.append({
            'id': r['id'],
            'name': r['name'],
            'email': r['email'],
            'phone': r['phone'],
            'subject': r['subject'],
            'message': r['message'],
            'created_at': r['created_at']
        })
    return contacts


def get_contact_by_id(contact_id):
    """
    Retrieves a single contact record by unique ID.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, email, phone, subject, message, created_at
        FROM contacts
        WHERE id = ?
    """, (contact_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return dict(row)
    return None


def get_all_projects(category=None):
    """
    Fetches all projects, optionally filtered by category.
    Includes a helper parsed list of technologies.
    """
    conn = get_connection()
    cursor = conn.cursor()

    if category and category != 'all':
        cursor.execute("""
            SELECT * FROM projects 
            WHERE category = ?
            ORDER BY display_order ASC, id ASC
        """, (category,))
    else:
        cursor.execute("""
            SELECT * FROM projects 
            ORDER BY display_order ASC, id ASC
        """)
    rows = cursor.fetchall()
    conn.close()

    projects = []
    for r in rows:
        proj = dict(r)
        proj['tech_list'] = [t.strip() for t in proj['technologies'].split(',') if t.strip()]
        projects.append(proj)
    return projects


def get_featured_projects(limit=4):
    """
    Fetches featured projects for homepage presentation.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM projects 
        WHERE is_featured = 1
        ORDER BY display_order ASC, id ASC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()

    featured = []
    for r in rows:
        proj = dict(r)
        proj['tech_list'] = [t.strip() for t in proj['technologies'].split(',') if t.strip()]
        featured.append(proj)
    return featured
