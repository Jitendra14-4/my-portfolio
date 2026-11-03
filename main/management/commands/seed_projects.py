from django.core.management.base import BaseCommand
from main.models import Project
from main.views import DEFAULT_PROJECTS


class Command(BaseCommand):
    help = 'Seeds initial portfolio projects into the database'

    def handle(self, *args, **options):
        for data in DEFAULT_PROJECTS:
            obj, created = Project.objects.update_or_create(
                slug=data['slug'],
                defaults=data
            )
            action = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{action} project: {obj.title}"))
        self.stdout.write(self.style.SUCCESS("Projects successfully seeded!"))
