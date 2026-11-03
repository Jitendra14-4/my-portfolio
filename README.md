# Modern Animated Full-Stack Developer Portfolio
### Jitendra Kumar Jena — Python Full Stack Developer & AI/Data Science Enthusiast

A production-grade, responsive, full-stack personal developer portfolio built with **Python (Flask)**, **SQLite**, **HTML5**, **CSS3**, and **Vanilla JavaScript (ES6+)**. Features modern glassmorphism UI, interactive particle constellation physics, smooth scroll-triggered animations, project filtering, light/dark themes, and an asynchronous contact form integrated with a backend database.

---

## 🌟 Key Features

### 🎨 Frontend & UI/UX Design
- **Futuristic Dark Obsidian Aesthetic:** Default dark theme with neon cyan (`#06b6d4`), electric blue (`#38bdf8`), purple (`#a855f7`), and emerald (`#10b981`) accents.
- **Dark & Light Mode Toggle:** Seamless transitions between night and daylight palettes, persisted across sessions in `localStorage`.
- **Interactive Particle Constellation Background:** Lightweight HTML5 Canvas particle network that connects adjacent nodes and reacts gracefully to cursor movement at 60 FPS.
- **Animated Glowing Rotating Avatar:** Conic-gradient halo effect surrounding profile artwork with floating technology badges.
- **Hero Typewriter Effect:** Cycles automatically through developer titles with smooth typing and deletion cadences.
- **Scroll-Triggered Reveals & Counter Animation:** Built with native `IntersectionObserver` for zero-lag scroll animations and numerical metric counting.
- **Project Filter & Real-Time Search:** Instant client-side search by title or technology (e.g. *Flask*, *RAG*, *Pandas*, *SQL*), plus category pills (*Full Stack*, *Machine Learning*, *Data Analytics*).
- **Interactive Project Modal (Lightbox):** Detailed view of system architecture, metrics, technologies, source code, and live demo links.
- **Mobile-First Responsive Layout:** Tested and optimized for smartphones, tablets, laptops, and ultra-wide desktop monitors.

### ⚙️ Backend & API Architecture
- **Flask REST API:** Modular endpoints with complete separation of presentation, routing, database persistence, and business logic.
- **`POST /api/contact`:** Asynchronous endpoint processing form submissions via the Fetch API without page reload.
  - **Spam Protection:** Invisible honeypot field traps automated bots without affecting human visitors.
  - **Server-Side Validation:** Validates required fields, character lengths, and email format via RFC-compliant regular expressions.
  - **HTML Sanitization:** Escapes all user inputs to eliminate Cross-Site Scripting (XSS) risks.
  - **Unique ID Generation:** Assigns each message a unique tracking code (e.g., `CNT-3FAF9E98`).
  - **HTTP Status Codes:** Delivers RFC-standard responses (`200 OK`, `400 Bad Request`, `500 Internal Server Error`).
- **`GET /api/contacts`:** Inspection endpoint to audit stored submissions in the SQLite database (includes live modal inspector in UI).
- **`GET /api/projects`:** Returns JSON representation of portfolio projects, supporting optional category filtering (`?category=...`).
- **`GET /download-resume`:** Directly delivers Jitendra's professional multi-section PDF resume.
- **`GET /api/health`:** Diagnostic endpoint reporting database connectivity and system status.
- **Security Headers:** Enforces `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, and `X-XSS-Protection`.

### 🗄️ Database Architecture
- **SQLite Database (`database.db`):** Pre-configured, zero-config relational database that automatically initializes tables on startup.
- **Table `contacts`:**
  - `id` (TEXT PRIMARY KEY) — Unique submission tracking identifier.
  - `name` (TEXT NOT NULL) — Visitor's full name.
  - `email` (TEXT NOT NULL) — Verified email address.
  - `phone` (TEXT) — Optional phone or WhatsApp number.
  - `subject` (TEXT NOT NULL) — Message topic or job subject.
  - `message` (TEXT NOT NULL) — Full inquiry text.
  - `created_at` (TIMESTAMP) — Auto-recorded UTC/local submission timestamp.
- **Table `projects`:** Stores project titles, slugs, categories, descriptions, static images, technologies, and repository links.
- **Parameterized SQL Queries:** 100% prepared statements throughout `database.py` to prevent SQL injection vulnerabilities.
- **Production Migration Ready:** Database access layer is decoupled to allow one-line migration to MySQL or PostgreSQL.

---

## 📁 Project Structure

```
jitendra_portfolio/
│
├── app.py                      # Flask backend application & REST API routes
├── database.py                 # Decoupled database access layer & SQL queries
├── database.db                 # Persistent SQLite database file
├── requirements.txt            # Python dependencies (Flask, Werkzeug)
├── README.md                   # Project documentation & run guide
│
├── templates/
│   └── index.html              # Primary modern single-page portfolio template
│
└── static/
    ├── css/
    │   └── style.css           # Modern CSS3 stylesheet (Dark/Light, Glassmorphism, Animations)
    ├── js/
    │   └── script.js           # Vanilla ES6+ JS (Particles, Fetch API, Typewriter, Modals)
    ├── images/
    │   ├── profile-avatar.svg  # Animated profile vector artwork
    │   └── projects/
    │       ├── student_mgmt.svg        # Student Management & RAG Chatbot
    │       ├── hospital_mgmt.svg       # Hospital Management System
    │       ├── sales_analytics.svg     # Sales Data Analysis Dashboard
    │       ├── paddy_moisture.svg      # Paddy Moisture Detection System
    │       ├── student_marks_pred.svg  # Student Marks Prediction System
    │       └── job_finder.svg          # AI Job Finder & NLP Match Engine
    └── docs/
        └── Jitendra_Jena_Resume.pdf    # Complete professional PDF resume
```

---

## 🚀 Getting Started (Run Locally)

### 1. Prerequisites
Ensure you have **Python 3.10+** (tested on Python 3.14.6) installed on your machine.

Verify installation:
```bash
python --version
```

### 2. Navigate to the Project Directory
```bash
cd C:\Users\SIE202608DS15\.gemini\antigravity\scratch\jitendra_portfolio
```

### 3. Install Required Dependencies
Install the required packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```
*(Dependencies: `Flask>=3.0.0`, `Werkzeug>=3.0.0`)*

### 4. Run the Flask Development Server
```bash
python app.py
```

You will see output similar to:
```
=======================================================
  Jitendra Kumar Jena — Developer Portfolio Server
  Running at: http://127.0.0.1:5000
=======================================================
[INFO] Database initialized and ready.
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
```

### 5. Open in Your Browser
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🧪 Testing & Verification Guide

### 1. Testing Contact Form Submission
1. Scroll down to the **Contact** section (`#contact`) or click "Contact" in the navigation bar.
2. Fill out the fields:
   - **Full Name:** `Alex Taylor`
   - **Email Address:** `alex@example.com`
   - **Phone Number:** `+91 9876543210`
   - **Subject:** `Interview Invitation - Full-Stack Developer`
   - **Message:** `Hello Jitendra, We are pleased to invite you for an interview regarding our Python Backend role.`
3. Click **"Send Message via API"**.
4. The button displays a loading spinner and disables during request processing.
5. An animated green alert will appear without page reload:
   > **Message Received Successfully!**
   > *Thank you, Alex Taylor! Your message has been sent successfully. Jitendra has received it and will respond promptly.*
   > `Submission Ref: CNT-XXXXXXXX`

### 2. Verifying Persistent Database Storage (Live SQLite Inspector)
You can verify that contact submissions are genuinely saved in `database.db` via two methods:

#### Method A: Built-in Live UI Inspector
In the Contact section on the left, click the button:
**"Inspect Database Submissions (Live SQLite)"**
This triggers an asynchronous query to `GET /api/contacts` and displays all saved submissions inside a modal window, showing IDs, timestamps, and full messages!

#### Method B: Command Line Query
Run the following Python one-liner to query `database.db` directly:
```bash
python -c "import sqlite3; conn=sqlite3.connect('database.db'); print(conn.cursor().execute('SELECT id, name, email, subject, created_at FROM contacts ORDER BY created_at DESC').fetchall())"
```

---

## 🔌 REST API Specification

### `POST /api/contact`
Submits a new contact message.
- **Request Body (JSON):**
  ```json
  {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "+1-555-0199",
    "subject": "Collaboration Opportunity",
    "message": "Hello Jitendra, I would love to collaborate on a Python ML project.",
    "website": ""
  }
  ```
- **Response `200 OK`:**
  ```json
  {
    "status": "success",
    "message": "Thank you, Jane Doe! Your message has been sent successfully.",
    "submission_id": "CNT-09B8905E",
    "created_at": "2026-11-03 11:43:54"
  }
  ```
- **Response `400 Bad Request`:**
  ```json
  {
    "status": "error",
    "message": "Validation failed. Please correct the highlighted errors.",
    "errors": [
      "Please provide a valid, active email address."
    ]
  }
  ```

### `GET /api/contacts?limit=50`
Returns stored contact submissions.
- **Response `200 OK`:**
  ```json
  {
    "status": "success",
    "count": 3,
    "contacts": [
      {
        "id": "CNT-3FAF9E98",
        "name": "DeepMind Recruiter",
        "email": "recruiter@deepmind.com",
        "phone": "+1-650-555-0199",
        "subject": "Senior Full-Stack AI Engineer Interview",
        "message": "...",
        "created_at": "2026-11-03 11:51:51"
      }
    ]
  }
  ```

### `GET /api/projects`
Returns project entries in JSON format.
- Optional query parameter: `?category=fullstack` or `?category=machine-learning` or `?category=data-analysis`.

### `GET /download-resume`
Downloads `Jitendra_Kumar_Jena_Resume.pdf` with `Content-Type: application/pdf` and `Content-Disposition: attachment`.

### `GET /api/health`
Returns health check status:
```json
{
  "status": "healthy",
  "database": "connected",
  "contacts_count": 3,
  "projects_count": 6,
  "framework": "Flask 3.1.3",
  "python_version": "3.14.6"
}
```

---

## 🔄 Migrating to MySQL or PostgreSQL

The database layer in `database.py` is isolated and uses standard ANSI SQL. To migrate:

### Migrating to PostgreSQL:
1. Install `psycopg2-binary`:
   ```bash
   pip install psycopg2-binary
   ```
2. In `database.py`, replace `get_connection()`:
   ```python
   import psycopg2
   from psycopg2.extras import RealDictCursor

   def get_connection():
       return psycopg2.connect(
           os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost:5432/portfolio_db'),
           cursor_factory=RealDictCursor
       )
   ```
3. Update parameter markers in queries from `?` to `%s`.

### Migrating to MySQL:
1. Install `mysql-connector-python`:
   ```bash
   pip install mysql-connector-python
   ```
2. In `database.py`, replace `get_connection()`:
   ```python
   import mysql.connector

   def get_connection():
       return mysql.connector.connect(
           host=os.environ.get('MYSQL_HOST', 'localhost'),
           user=os.environ.get('MYSQL_USER', 'root'),
           password=os.environ.get('MYSQL_PASSWORD', ''),
           database=os.environ.get('MYSQL_DB', 'portfolio_db'),
           dictionary=True
       )
   ```
3. Update parameter markers in queries from `?` to `%s`.

---

## 👨‍💻 Author Information

**Jitendra Kumar Jena**
- **Title:** Python Full Stack Developer | AI & Data Science Enthusiast
- **Email:** [jitendrax144@gmail.com](mailto:jitendrax144@gmail.com)
- **Phone:** [+91-9348896398](tel:+919348896398)
- **Location:** Kendrapara, Odisha, India
- **GitHub:** [https://github.com/Jitendra14-4](https://github.com/Jitendra14-4)
- **LinkedIn:** [https://www.linkedin.com/in/jitendrax144/](https://www.linkedin.com/in/jitendrax144/)

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
