from django.core.management.base import BaseCommand
#from django.contrib.auth.models import User
from authentication.models import User
from django.conf import settings


class Command(BaseCommand):
    print("Creatting services users")

    def handle(self, *args, **options):
        users_data = [
            {
                'username': settings.MS_METADATA_USER,
                'password': settings.MS_METADATA_PASSWORD,
                'email': settings.MS_METADATA_USER + '@sentimail.com',
            },
            {
                'username': settings.MS_CONTENT_USER,
                'password': settings.MS_CONTENT_PASSWORD,
                'email': settings.MS_CONTENT_USER + '@sentimail.com',
            },
            {
                'username': settings.MS_ATTACHMENT_USER,
                'password': settings.MS_ATTACHMENT_PASSWORD,
                'email': settings.MS_ATTACHMENT_USER + '@sentimail.com',
            },
        ]
        for user_data in users_data:
            if not User.objects.filter(username=user_data['username']).exists():
                print(f"Creating user {user_data['username']}")
                User.objects.create_user(**user_data)
                print(f"User {user_data['username']} created")
            else:
                print(f"User {user_data['username']} already exists")