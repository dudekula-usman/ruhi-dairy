import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "create django superuser"

    def handle(self, *args, **options):
        user_model = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write("superuser environment variables not configured")
            return

        if user_model.objects.filter(username=username).exists():
            self.stdout.write(f"superuser '{username}' already exists")
            return

        user_model.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        self.stdout.write(
            self.style.SUCCESS(f"superuser '{username}' created successfully")
        )