from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Profile, MainPageContent
from projects.models import ProjectImage
from supabase import create_client
import re

class Command(BaseCommand):
    help = 'Fix image paths by matching DB records with actual Supabase files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be changed without actually changing it',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
            self.stdout.write(self.style.ERROR('Supabase not configured'))
            return

        client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        bucket = settings.SUPABASE_BUCKET

        # Get all files from Supabase
        self.stdout.write('Scanning Supabase Storage...')
        all_files = []

        try:
            # List root
            root_files = client.storage.from_(bucket).list()

            for item in root_files:
                name = item.get('name', '')
                if item.get('id'):  # File
                    all_files.append(name)
                else:  # Directory
                    try:
                        subfiles = client.storage.from_(bucket).list(name)
                        for subfile in subfiles:
                            if subfile.get('id'):
                                all_files.append(f"{name}/{subfile['name']}")
                    except:
                        pass

            self.stdout.write(self.style.SUCCESS(f'Found {len(all_files)} files in Supabase'))

            # Create lookup by base filename (for matching)
            file_lookup = {}
            for filepath in all_files:
                # Extract base name without extension
                base = filepath.split('/')[-1]
                base_clean = re.sub(r'_[a-zA-Z0-9]{7,}\.', '.', base)  # Remove Django suffix
                file_lookup[base] = filepath
                file_lookup[base_clean] = filepath

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error scanning Supabase: {e}'))
            return

        self.stdout.write('\n' + '=' * 80)

        # Fix Profile photos
        self.stdout.write('\n=== Fixing Profile Photos ===')
        profiles = Profile.objects.filter(photo__isnull=False)

        for profile in profiles:
            old_path = str(profile.photo.name)
            filename = old_path.split('/')[-1]

            self.stdout.write(f'\nProfile: {profile.name}')
            self.stdout.write(f'  Current DB path: {old_path}')

            # Try to find matching file
            matched_file = None

            # Direct match
            if old_path in all_files:
                matched_file = old_path
            # Filename match
            elif filename in file_lookup:
                matched_file = file_lookup[filename]
            # Try without extension suffix
            else:
                base_name = filename.split('.')[0]
                for supabase_file in all_files:
                    if base_name in supabase_file:
                        matched_file = supabase_file
                        break

            if matched_file:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Matched: {matched_file}'))

                if matched_file != old_path:
                    if not dry_run:
                        profile.photo.name = matched_file
                        profile.save(update_fields=['photo'])
                        self.stdout.write(self.style.SUCCESS(f'  → Updated in DB'))
                    else:
                        self.stdout.write(f'  → Would update to: {matched_file}')
            else:
                self.stdout.write(self.style.WARNING(f'  ✗ No match found in Supabase'))

        # Fix MainPageContent banners
        self.stdout.write('\n=== Fixing Main Banners ===')
        contents = MainPageContent.objects.filter(main_banner__isnull=False)

        for content in contents:
            old_path = str(content.main_banner.name)
            filename = old_path.split('/')[-1]

            self.stdout.write(f'\nBanner: {content.title}')
            self.stdout.write(f'  Current DB path: {old_path}')

            matched_file = None

            if old_path in all_files:
                matched_file = old_path
            elif filename in file_lookup:
                matched_file = file_lookup[filename]
            else:
                base_name = filename.split('.')[0]
                for supabase_file in all_files:
                    if base_name in supabase_file:
                        matched_file = supabase_file
                        break

            if matched_file:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Matched: {matched_file}'))

                if matched_file != old_path:
                    if not dry_run:
                        content.main_banner.name = matched_file
                        content.save(update_fields=['main_banner'])
                        self.stdout.write(self.style.SUCCESS(f'  → Updated in DB'))
                    else:
                        self.stdout.write(f'  → Would update to: {matched_file}')
            else:
                self.stdout.write(self.style.WARNING(f'  ✗ No match found'))

        # Fix ProjectImage
        self.stdout.write('\n=== Fixing Project Images ===')
        images = ProjectImage.objects.filter(image__isnull=False)

        for img in images:
            old_path = str(img.image.name)
            filename = old_path.split('/')[-1]

            self.stdout.write(f'\nProject: {img.project.title} - Image {img.order}')
            self.stdout.write(f'  Current DB path: {old_path}')

            matched_file = None

            if old_path in all_files:
                matched_file = old_path
            elif filename in file_lookup:
                matched_file = file_lookup[filename]
            else:
                base_name = filename.split('.')[0]
                for supabase_file in all_files:
                    if base_name in supabase_file:
                        matched_file = supabase_file
                        break

            if matched_file:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Matched: {matched_file}'))

                if matched_file != old_path:
                    if not dry_run:
                        img.image.name = matched_file
                        img.save(update_fields=['image'])
                        self.stdout.write(self.style.SUCCESS(f'  → Updated in DB'))
                    else:
                        self.stdout.write(f'  → Would update to: {matched_file}')
            else:
                self.stdout.write(self.style.WARNING(f'  ✗ No match found'))

        self.stdout.write('\n' + '=' * 80)
        if dry_run:
            self.stdout.write(self.style.WARNING('\nDRY RUN - No changes were made'))
            self.stdout.write('Run without --dry-run to apply changes')
        else:
            self.stdout.write(self.style.SUCCESS('\n✓ Image paths have been fixed!'))
