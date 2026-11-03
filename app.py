"""
==============================================================================
Jitendra Kumar Jena — Modern Animated Full-Stack Developer Portfolio
Backend: Flask REST API + SQLite Database
Features:
- REST API endpoint: POST /api/contact with spam & server validation
- SQLite persistent storage in database.db with unique ID generation
- REST API endpoint: GET /api/contacts for verification & inspection
- REST API endpoint: GET /api/projects with category filtering
- Resume delivery endpoint: GET /download-resume
- Complete separation of routes, database logic, and frontend templates
==============================================================================
"""

import os
import re
import html
import logging
from flask import Flask, render_template, request, jsonify, send_from_directory, abort
import database

# Configure application logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)

# Application Paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(
    __name__,
    template_folder=TEMPLATES_DIR,
    static_folder=STATIC_DIR
)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'jitendra-jena-portfolio-secret-key-2026')
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB maximum payload

# Ensure database tables exist and projects are seeded
with app.app_context():
    database.init_db()
    logging.info("Database initialized and ready.")

# Simple Email Regex validation (RFC-compliant standard format)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')


# -----------------------------------------------------------------------------
# Security Headers Middleware
# -----------------------------------------------------------------------------
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response


# -----------------------------------------------------------------------------
# Primary Frontend Route
# -----------------------------------------------------------------------------
@app.route('/')
def index():
    """
    Renders the modern animated portfolio homepage with dynamic project lists,
    skills matrix, timeline data, and interactive widgets.
    """
    all_projects = database.get_all_projects()
    featured_projects = database.get_featured_projects(limit=4)

    profile_data = {
        'name': 'Jitendra Kumar Jena',
        'title': 'Python Full Stack Developer | AI & Data Science Enthusiast',
        'location': 'Kendrapara, Odisha, India',
        'email': 'jitendrax144@gmail.com',
        'phone': '+91-9348896398',
        'github': 'https://github.com/Jitendra14-4',
        'linkedin': 'https://www.linkedin.com/in/jitendrax144/',
        'summary': (
            "Motivated and detail-oriented IT professional with 2 years of experience in Quality Analysis, "
            "specialized in Python Full Stack Development, and internship experience as a Python Developer. "
            "Skilled in architecting robust web applications, data science pipelines, database modeling, "
            "and software quality validation. Passionate about solving mission-critical operational challenges "
            "with modern software engineering and intelligent machine learning models."
        ),
        'stats': [
            {'value': '2+', 'label': 'Years Experience', 'sub': 'Quality Analysis & Dev'},
            {'value': '90%', 'label': 'RAG Accuracy', 'sub': 'Embedded QA Chatbot'},
            {'value': '6+', 'label': 'Core Projects', 'sub': 'Full-Stack & ML Models'},
            {'value': '100%', 'label': 'Commitment', 'sub': 'Code Quality & Testing'}
        ]
    }

    return render_template(
        'index.html',
        profile=profile_data,
        projects=all_projects,
        featured_projects=featured_projects
    )


# -----------------------------------------------------------------------------
# Contact Form REST API Endpoint
# -----------------------------------------------------------------------------
@app.route('/api/contact', methods=['POST'])
def submit_contact():
    """
    REST API endpoint to process contact form submissions.
    Supports both JSON payloads and standard x-www-form-urlencoded data.
    Implements spam protection (honeypot), server-side input validation,
    sanitization, and SQLite parameterized persistence.
    """
    # Extract data regardless of content type
    if request.is_json:
        data = request.get_json() or {}
    else:
        data = request.form.to_dict() or {}

    # 1. Anti-spam honeypot verification
    # A hidden 'website' or 'honeypot' field that real users never fill
    honeypot = data.get('website', '').strip() or data.get('honeypot', '').strip()
    if honeypot:
        logging.warning(f"Spam detected from bot targeting honeypot. IP: {request.remote_addr}")
        # Return faux success so spam bots don't retry with altered payloads
        return jsonify({
            'status': 'success',
            'message': 'Your message has been processed successfully.',
            'id': 'CNT-SPAM-FILTERED'
        }), 200

    # 2. Extract and sanitize fields
    name = html.escape(data.get('name', '').strip())
    email = data.get('email', '').strip().lower()
    phone = html.escape(data.get('phone', '').strip())
    subject = html.escape(data.get('subject', '').strip())
    message = html.escape(data.get('message', '').strip())

    errors = []

    # 3. Server-side Validation
    if not name or len(name) < 2:
        errors.append("Full Name is required and must be at least 2 characters long.")
    elif len(name) > 100:
        errors.append("Full Name cannot exceed 100 characters.")

    if not email:
        errors.append("Email Address is required.")
    elif not EMAIL_REGEX.match(email) or len(email) > 120:
        errors.append("Please provide a valid, active email address (e.g. yourname@domain.com).")

    if phone and len(phone) > 30:
        errors.append("Phone number cannot exceed 30 characters.")

    if not subject or len(subject) < 3:
        errors.append("Subject is required and must be at least 3 characters long.")
    elif len(subject) > 200:
        errors.append("Subject cannot exceed 200 characters.")

    if not message or len(message) < 10:
        errors.append("Message is required and must be at least 10 characters long.")
    elif len(message) > 4000:
        errors.append("Message cannot exceed 4000 characters.")

    # Return errors if validation fails
    if errors:
        return jsonify({
            'status': 'error',
            'message': 'Validation failed. Please correct the highlighted errors.',
            'errors': errors
        }), 400

    # 4. Save to Database using parameterized statement
    try:
        saved_record = database.save_contact(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        logging.info(f"New contact saved with ID {saved_record['id']} from {email}")

        return jsonify({
            'status': 'success',
            'message': f"Thank you, {name}! Your message has been sent successfully. Jitendra has received it and will respond promptly.",
            'submission_id': saved_record['id'],
            'created_at': saved_record['created_at']
        }), 200

    except Exception as e:
        logging.error(f"Error persisting contact submission: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': "A server error occurred while processing your message. Please try again or reach out directly at jitendrax144@gmail.com."
        }), 500


# -----------------------------------------------------------------------------
# REST API: View Contact Submissions (Inspection & Admin Verification)
# -----------------------------------------------------------------------------
@app.route('/api/contacts', methods=['GET'])
def list_contacts():
    """
    REST API endpoint to inspect stored contact submissions from the SQLite database.
    Useful for verifying that messages are persistently recorded.
    """
    limit = request.args.get('limit', default=50, type=int)
    contacts = database.get_all_contacts(limit=limit)
    return jsonify({
        'status': 'success',
        'count': len(contacts),
        'contacts': contacts
    }), 200


# -----------------------------------------------------------------------------
# REST API: Projects Listing
# -----------------------------------------------------------------------------
@app.route('/api/projects', methods=['GET'])
def list_projects():
    """
    REST API returning project entries in JSON format.
    Supports filtering by category: ?category=fullstack, machine-learning, data-analysis
    """
    category = request.args.get('category', default=None, type=str)
    projects = database.get_all_projects(category=category)
    return jsonify({
        'status': 'success',
        'count': len(projects),
        'projects': projects
    }), 200


# -----------------------------------------------------------------------------
# Resume Download Route
# -----------------------------------------------------------------------------
@app.route('/download-resume')
def download_resume():
    """
    Serves Jitendra Kumar Jena's professional resume as a downloadable PDF file.
    """
    docs_dir = os.path.join(STATIC_DIR, 'docs')
    filename = 'Jitendra_Jena_Resume.pdf'
    filepath = os.path.join(docs_dir, filename)

    if not os.path.exists(filepath):
        # Fallback if specific file missing
        abort(404, description="Resume file not found.")

    return send_from_directory(
        docs_dir,
        filename,
        as_attachment=True,
        download_name='Jitendra_Kumar_Jena_Resume.pdf',
        mimetype='application/pdf'
    )


# -----------------------------------------------------------------------------
# Health Check Endpoint
# -----------------------------------------------------------------------------
@app.route('/api/health')
def health_check():
    """
    Returns application and database status.
    """
    try:
        contacts_count = len(database.get_all_contacts())
        projects_count = len(database.get_all_projects())
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'contacts_count': contacts_count,
            'projects_count': projects_count,
            'python_version': '3.14.6',
            'framework': 'Flask 3.1.3'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500


# -----------------------------------------------------------------------------
# Error Handlers
# -----------------------------------------------------------------------------
@app.errorhandler(404)
def not_found_error(error):
    if request.path.startswith('/api/'):
        return jsonify({'status': 'error', 'message': 'Endpoint not found'}), 404
    return render_template('index.html', error_message="Page not found, redirected to Home."), 404


@app.errorhandler(500)
def internal_server_error(error):
    if request.path.startswith('/api/'):
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500
    return "Internal Server Error", 500


if __name__ == '__main__':
    # Local development server execution
    port = int(os.environ.get('PORT', 5000))
    print(f"\n=======================================================")
    print(f"  Jitendra Kumar Jena — Developer Portfolio Server")
    print(f"  Running at: http://127.0.0.1:{port}")
    print(f"=======================================================\n")
    app.run(host='0.0.0.0', port=port, debug=True)
