import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

from core.models import Profile

try:
    profile = Profile.objects.first()
    if profile:
        print(f"Profile found: {profile.name}")
        print(f"Photo field value: {profile.photo}")
        print(f"Photo field name: {profile.photo.name if profile.photo else 'None'}")
        if profile.photo:
            try:
                print(f"Generated URL: {profile.photo.url}")
            except Exception as e:
                print(f"Error generating URL: {e}")
    else:
        print("No profile found in database")
except Exception as e:
    print(f"Error: {e}")
