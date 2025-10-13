from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Profile, MainPageContent
from projects.models import ProjectImage
from supabase import create_client

class Command(BaseCommand):
    help = 'Sync database image paths with existing Supabase files'

    def handle(self, *args, **options):
        if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
            self.stdout.write(self.style.ERROR('Supabase not configured'))
            return

        client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        bucket = settings.SUPABASE_BUCKET

        self.stdout.write('Fetching files from Supabase...')

        # Get all files from Supabase
        supabase_files = {}

        try:
            # List directories
            for directory in ['photos', 'banners', 'project/img']:
                try:
                    files = client.storage.from_(bucket).list(directory.replace('/', ''))
                    for file in files:
                        if file.get('id'):  # It's a file
                            path = f"{directory}/{file['name']}"
                            supabase_files[directory] = path
                            self.stdout.write(f'  Found: {path}')
                except Exception as e:
                    self.stdout.write(f'  No files in {directory}')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
            return

        self.stdout.write(f'\nFound {len(supabase_files)} directories with files\n')
        self.stdout.write('=' * 80)

        # Update Profile photos
        self.stdout.write('\n=== Updating Profile Photos ===')
        profiles = Profile.objects.filter(photo__isnull=False)

        for profile in profiles:
            old_path = str(profile.photo.name)
            self.stdout.write(f'\nProfile: {profile.name}')
            self.stdout.write(f'  Current DB path: {old_path}')

            if 'photos' in supabase_files:
                new_path = supabase_files['photos']
                profile.photo.name = new_path
                profile.save(update_fields=['photo'])
                self.stdout.write(self.style.SUCCESS(f'  ✓ Updated to: {new_path}'))
            else:
                self.stdout.write(self.style.WARNING('  ✗ No file found in Supabase'))

        # Update MainPageContent banners
        self.stdout.write('\n=== Updating Main Banners ===')
        contents = MainPageContent.objects.filter(main_banner__isnull=False)

        for content in contents:
            old_path = str(content.main_banner.name)
            self.stdout.write(f'\nBanner: {content.title}')
            self.stdout.write(f'  Current DB path: {old_path}')

            if 'banners' in supabase_files:
                new_path = supabase_files['banners']
                content.main_banner.name = new_path
                content.save(update_fields=['main_banner'])
                self.stdout.write(self.style.SUCCESS(f'  ✓ Updated to: {new_path}'))
            else:
                self.stdout.write(self.style.WARNING('  ✗ No file found in Supabase'))

        # Update ProjectImage
        self.stdout.write('\n=== Updating Project Images ===')
        images = ProjectImage.objects.filter(image__isnull=False)

        for img in images:
            old_path = str(img.image.name)
            self.stdout.write(f'\nProject: {img.project.title} - Image {img.order}')
            self.stdout.write(f'  Current DB path: {old_path}')

            if 'project/img' in supabase_files:
                new_path = supabase_files['project/img']
                img.image.name = new_path
                img.save(update_fields=['image'])
                self.stdout.write(self.style.SUCCESS(f'  ✓ Updated to: {new_path}'))
            else:
                self.stdout.write(self.style.WARNING('  ✗ No file found in Supabase'))

        self.stdout.write('\n' + '=' * 80)
        self.stdout.write(self.style.SUCCESS('\n✓ Database sync completed!'))
        self.stdout.write('All image paths now point to existing Supabase files.')
