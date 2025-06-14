
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import UserProfile


class Command(BaseCommand):
    help = "Create UserProfile for existing users"

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            try:
                UserProfile.objects.get(user=user)
                self.stdout.write(
                    self.style.SUCCESS(f"User {user.username} already has a profile")
                )
            except UserProfile.DoesNotExist:
                UserProfile.objects.create(user=user)
                self.stdout.write(
                    self.style.SUCCESS(f"Created profile for {user.username}")
                )
