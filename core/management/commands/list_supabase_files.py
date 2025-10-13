from django.core.management.base import BaseCommand
from django.conf import settings
from supabase import create_client

class Command(BaseCommand):
    help = 'List all files in Supabase Storage bucket'

    def handle(self, *args, **options):
        if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
            self.stdout.write(self.style.ERROR('Supabase credentials not configured'))
            return

        client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        bucket = settings.SUPABASE_BUCKET

        self.stdout.write(self.style.SUCCESS(f'Bucket: {bucket}'))
        self.stdout.write('=' * 80)

        try:
            # List all files in root
            files = client.storage.from_(bucket).list()

            self.stdout.write(f'\n=== Root Level ({len(files)} items) ===')
            for file in files:
                if file.get('id'):  # It's a file
                    self.stdout.write(f"  FILE: {file['name']}")
                else:  # It's a folder
                    self.stdout.write(f"  DIR:  {file['name']}/")

                    # List files in subdirectory
                    try:
                        subfiles = client.storage.from_(bucket).list(file['name'])
                        for subfile in subfiles:
                            if subfile.get('id'):
                                self.stdout.write(f"    FILE: {file['name']}/{subfile['name']}")
                    except Exception as e:
                        self.stdout.write(f"    Error listing: {e}")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))

        self.stdout.write('\n' + '=' * 80)
