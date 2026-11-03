from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Project, ContactMessage
from .forms import ContactForm


# Default project data to ensure the website is fully populated immediately
DEFAULT_PROJECTS = [
    {
        'title': 'Student Management System',
        'slug': 'student-management-system',
        'category': 'django',
        'short_description': 'A comprehensive web application to manage student enrollment, course allocation, grading, and attendance tracking with role-based access.',
        'description': 'A full-featured student management portal built with Django. Allows administrators, instructors, and students to access customized dashboards. Includes dynamic grade calculations, automated attendance records, PDF report generation, and MySQL/SQLite support.',
        'image_static': 'images/projects/student_mgmt.svg',
        'technologies': 'Python, Django, SQLite, Bootstrap 5, HTML/CSS, JavaScript',
        'github_url': 'https://github.com/jitendrajena',
        'demo_url': '#',
        'is_featured': True,
        'order': 1
    },
    {
        'title': 'Hospital Management System',
        'slug': 'hospital-management-system',
        'category': 'django',
        'short_description': 'An integrated healthcare management platform for doctor-patient scheduling, medical record history, billing, and prescription tracking.',
        'description': 'Designed to streamline clinical and administrative operations. Features secure patient record management, automated appointment scheduling, prescription tracking, and billing invoice generation with clean analytics dashboards.',
        'image_static': 'images/projects/hospital_mgmt.svg',
        'technologies': 'Python, Django, MySQL, Django REST Framework, Chart.js',
        'github_url': 'https://github.com/jitendrajena',
        'demo_url': '#',
        'is_featured': True,
        'order': 2
    },
    {
        'title': 'Paddy Moisture Detection System',
        'slug': 'paddy-moisture-detection-system',
        'category': 'machine-learning',
        'short_description': 'An intelligent IoT & ML-driven system to detect moisture content in paddy crops, preventing grain spoilage and optimizing storage conditions.',
        'description': 'Combines sensor data acquisition and Machine Learning regression/classification models to predict moisture levels accurately in real-time. Features automated alerts, threshold monitoring, and an interactive analytics dashboard for farmers and mill owners.',
        'image_static': 'images/projects/paddy_moisture.svg',
        'technologies': 'Python, Scikit-Learn, Pandas, NumPy, Flask/Django, IoT Sensors',
        'github_url': 'https://github.com/jitendrajena',
        'demo_url': '#',
        'is_featured': True,
        'order': 3
    },
    {
        'title': 'Sales Data Analysis Dashboard',
        'slug': 'sales-data-analysis-dashboard',
        'category': 'data-analysis',
        'short_description': 'An interactive visual analytics platform analyzing historical sales performance, revenue trends, customer segments, and demand forecasts.',
        'description': 'End-to-end data analysis pipeline built to extract, clean, and visualize multi-channel retail sales data. Features automated KPI tracking, exploratory data analysis with Seaborn & Matplotlib, interactive filtering, and business insights generation.',
        'image_static': 'images/projects/sales_analytics.svg',
        'technologies': 'Python, Pandas, NumPy, Matplotlib, Seaborn, Plotly, Streamlit/Django',
        'github_url': 'https://github.com/jitendrajena',
        'demo_url': '#',
        'is_featured': True,
        'order': 4
    }
]


def get_all_projects():
    """Retrieve projects from DB or fall back to default project specifications."""
    db_projects = list(Project.objects.all())
    if db_projects:
        return db_projects
    # Return mock model-like objects if DB is not yet populated
    class MockProject:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def tech_list(self):
            return [t.strip() for t in self.technologies.split(',') if t.strip()]
        def get_image_url(self):
            return None
    return [MockProject(**item) for item in DEFAULT_PROJECTS]


def home(request):
    projects = get_all_projects()
    featured_projects = [p for p in projects if getattr(p, 'is_featured', True)][:4]
    return render(request, 'home.html', {
        'featured_projects': featured_projects,
        'active_page': 'home'
    })


def about(request):
    return render(request, 'about.html', {
        'active_page': 'about'
    })


def projects(request):
    all_projs = get_all_projects()
    return render(request, 'projects.html', {
        'projects': all_projs,
        'active_page': 'projects'
    })


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 
                "Your message has been sent successfully! Jitendra will get in touch with you shortly."
            )
            return redirect('contact')
        else:
            messages.error(
                request, 
                "There was an error with your submission. Please check the highlighted fields below."
            )
    else:
        form = ContactForm()

    return render(request, 'contact.html', {
        'form': form,
        'active_page': 'contact'
    })
