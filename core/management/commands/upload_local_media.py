from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from pathlib import Path

class Command(BaseCommand):
    help = 'Upload all local media files to Supabase Storage'

    def handle(self, *args, **options):
        from portfolio.storage import SupabaseStorage

        storage = SupabaseStorage()
        base_dir = settings.BASE_DIR
        media_dir = base_dir / 'media'

        if not media_dir.exists():
            self.stdout.write(self.style.ERROR(f'Media directory not found: {media_dir}'))
            return

        self.stdout.write(self.style.SUCCESS(f'Media directory: {media_dir}'))
        self.stdout.write('=' * 80)

        # Find all image files
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        all_files = []

        for ext in image_extensions:
            all_files.extend(media_dir.rglob(f'*{ext}'))

        self.stdout.write(f'\nFound {len(all_files)} image files\n')

        uploaded_count = 0
        failed_count = 0

        for local_file in all_files:
            # Get relative path from media directory
            relative_path = local_file.relative_to(media_dir)
            supabase_path = str(relative_path).replace('\\', '/')

            self.stdout.write(f'\nUploading: {local_file.name}')
            self.stdout.write(f'  Local: {relative_path}')
            self.stdout.write(f'  Supabase path: {supabase_path}')

            try:
                # Check if file already exists
                if storage.exists(supabase_path):
                    self.stdout.write(self.style.WARNING(f'  ⊙ Already exists, skipping'))
                    continue

                # Upload file
                with open(local_file, 'rb') as f:
                    saved_path = storage.save(supabase_path, File(f))

                url = storage.url(saved_path)
                self.stdout.write(self.style.SUCCESS(f'  ✓ Uploaded to: {saved_path}'))
                self.stdout.write(f'  URL: {url}')
                uploaded_count += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Failed: {e}'))
                failed_count += 1

        self.stdout.write('\n' + '=' * 80)
        self.stdout.write(self.style.SUCCESS(f'\n✓ Upload completed!'))
        self.stdout.write(f'  Uploaded: {uploaded_count}')
        self.stdout.write(f'  Failed: {failed_count}')
        self.stdout.write(f'  Skipped: {len(all_files) - uploaded_count - failed_count}')
