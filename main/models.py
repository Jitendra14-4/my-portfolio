from django.db import models
from django.utils.text import slugify


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.created_at.strftime('%Y-%m-%d')})"


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('all', 'All'),
        ('python', 'Python'),
        ('django', 'Django'),
        ('data-analysis', 'Data Analysis'),
        ('machine-learning', 'Machine Learning'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='python')
    short_description = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    image_static = models.CharField(
        max_length=255, 
        blank=True, 
        default='images/projects/default.jpg',
        help_text="Path relative to static/ (e.g. images/projects/student_mgmt.svg)"
    )
    technologies = models.CharField(
        max_length=250, 
        help_text="Comma-separated list, e.g. Python, Django, SQLite, Bootstrap"
    )
    github_url = models.URLField(blank=True, default='')
    demo_url = models.URLField(blank=True, default='')
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def tech_list(self):
        """Returns list of trimmed technology strings."""
        if self.technologies:
            return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]
        return []

    def get_image_url(self):
        """Returns uploaded media URL or fallback static path."""
        if self.image:
            return self.image.url
        return None

    def __str__(self):
        return self.title
