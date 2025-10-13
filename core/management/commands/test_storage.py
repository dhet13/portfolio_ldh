from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.base import ContentFile
from core.models import Profile

class Command(BaseCommand):
    help = 'Test if Supabase Storage is working'

    def handle(self, *args, **options):
        self.stdout.write('=' * 80)
        self.stdout.write('Storage Configuration Check')
        self.stdout.write('=' * 80)

        # Check settings
        self.stdout.write(f'\nSUPABASE_URL: {settings.SUPABASE_URL[:30]}...' if settings.SUPABASE_URL else 'SUPABASE_URL: NOT SET')
        self.stdout.write(f'SUPABASE_KEY: {settings.SUPABASE_KEY[:20]}...' if settings.SUPABASE_KEY else 'SUPABASE_KEY: NOT SET')
        self.stdout.write(f'SUPABASE_BUCKET: {settings.SUPABASE_BUCKET}')

        default_storage = getattr(settings, 'DEFAULT_FILE_STORAGE', 'default')
        self.stdout.write(f'DEFAULT_FILE_STORAGE: {default_storage}')

        if settings.SUPABASE_URL and settings.SUPABASE_KEY:
            self.stdout.write(self.style.SUCCESS('\n✓ Supabase credentials are configured'))

            # Test file upload
            self.stdout.write('\nTesting file upload to Supabase...')

            try:
                from portfolio.storage import SupabaseStorage
                storage = SupabaseStorage()

                # Create test file
                test_content = b'This is a test file'
                test_file = ContentFile(test_content, name='test.txt')

                # Save to photos/ directory
                saved_path = storage.save('photos/test.txt', test_file)

                self.stdout.write(self.style.SUCCESS(f'✓ File saved to: {saved_path}'))

                # Generate URL
                url = storage.url(saved_path)
                self.stdout.write(self.style.SUCCESS(f'✓ File URL: {url}'))

                # Check if exists
                exists = storage.exists(saved_path)
                self.stdout.write(self.style.SUCCESS(f'✓ File exists: {exists}'))

                # Clean up
                storage.delete(saved_path)
                self.stdout.write(self.style.SUCCESS('✓ Test file deleted'))

                self.stdout.write(self.style.SUCCESS('\n✓✓✓ Supabase Storage is working correctly! ✓✓✓'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'\n✗ Storage test failed: {e}'))
                import traceback
                self.stdout.write(traceback.format_exc())
        else:
            self.stdout.write(self.style.ERROR('\n✗ Supabase credentials are NOT configured'))
            self.stdout.write(self.style.WARNING('Files will be saved to local MEDIA_ROOT'))

        self.stdout.write('\n' + '=' * 80)
