from django.conf import settings
from django.core.management.base import BaseCommand
from accounts.models import CustomUser

class Command(BaseCommand):

    def handle(self, *args, **options):
        if CustomUser.objects.count() == 0:
            username = settings.SU_USERNAME
            email = settings.SU_EMAIL
            password = settings.SU_PASSWORD
            print(f'Creating account for {username} {email}')
            admin = CustomUser.objects.create_superuser(email=email, username=username, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')