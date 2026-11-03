from django.test import TestCase, Client
from django.urls import reverse
from main.models import Project, ContactMessage


class PortfolioViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.project1 = Project.objects.create(
            title="Student Management System",
            slug="student-management-system",
            category="django",
            short_description="A comprehensive web application to manage student enrollment.",
            technologies="Python, Django, SQLite, Bootstrap 5",
            is_featured=True,
            order=1
        )
        self.project2 = Project.objects.create(
            title="Paddy Moisture Detection System",
            slug="paddy-moisture-detection-system",
            category="machine-learning",
            short_description="An intelligent IoT & ML-driven system to detect moisture content.",
            technologies="Python, Scikit-Learn, Pandas, NumPy",
            is_featured=True,
            order=2
        )

    def test_home_page_status_and_content(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jitendra Jena")
        self.assertContains(response, "Python Developer")
        self.assertContains(response, "Student Management System")
        self.assertContains(response, "Paddy Moisture Detection System")
        self.assertContains(response, "NumPy &amp; Pandas")

    def test_about_page_status_and_content(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "About")
        self.assertContains(response, "Bachelor of Technology")
        self.assertContains(response, "Jitendra_Jena_Resume.pdf")
        self.assertContains(response, "AI &amp; Data Science Learning Journey")

    def test_projects_page_status_and_content(self):
        response = self.client.get(reverse('projects'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Student Management System")
        self.assertContains(response, "Paddy Moisture Detection System")
        self.assertContains(response, "Python, Django, SQLite, Bootstrap 5")

    def test_contact_page_get(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Send a Direct Message")

    def test_contact_form_valid_submission(self):
        post_data = {
            'name': 'Anita Roy',
            'email': 'anita.roy@example.com',
            'subject': 'Exciting Python Developer Role',
            'message': 'Hello Jitendra, we loved your portfolio and would like to invite you for an interview.'
        }
        response = self.client.post(reverse('contact'), data=post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        # Check database record created
        self.assertEqual(ContactMessage.objects.count(), 1)
        msg = ContactMessage.objects.first()
        self.assertEqual(msg.name, 'Anita Roy')
        self.assertEqual(msg.email, 'anita.roy@example.com')
        # Check success message present
        self.assertContains(response, "Your message has been sent successfully!")

    def test_contact_form_invalid_submission(self):
        # Invalid email and message too short
        post_data = {
            'name': 'A',
            'email': 'not-an-email',
            'subject': '',
            'message': 'Hi'
        }
        response = self.client.post(reverse('contact'), data=post_data)
        self.assertEqual(response.status_code, 200)
        # Check database record NOT created
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertContains(response, "Enter a valid email address.")
