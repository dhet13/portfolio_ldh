from django.core.management.base import BaseCommand
from django.core.files import File
from core.models import Profile, MainPageContent
from projects.models import ProjectImage
import os
from pathlib import Path

class Command(BaseCommand):
    help = 'Re-upload all images from local media folder to Supabase with correct paths'

    def handle(self, *args, **options):
        from django.conf import settings
        base_dir = settings.BASE_DIR
        media_dir = base_dir / 'media'

        if not media_dir.exists():
            self.stdout.write(self.style.ERROR(f'Media directory not found: {media_dir}'))
            return

        self.stdout.write(self.style.SUCCESS(f'Media directory: {media_dir}'))

        # 1. Profile 사진 재업로드
        self.stdout.write('\n=== Re-uploading Profile Photos ===')
        profiles = Profile.objects.all()

        for profile in profiles:
            if profile.photo:
                old_path = str(profile.photo.name)
                self.stdout.write(f'Profile: {profile.name}')
                self.stdout.write(f'  Old path: {old_path}')

                # 로컬 파일 찾기
                local_file = media_dir / old_path

                if not local_file.exists():
                    # photos/ 폴더에서 직접 찾기
                    photos_dir = media_dir / 'photos'
                    if photos_dir.exists():
                        for file_path in photos_dir.glob('*'):
                            if file_path.is_file():
                                local_file = file_path
                                break

                if local_file.exists():
                    self.stdout.write(f'  Found local file: {local_file}')

                    # 파일 재업로드
                    with open(local_file, 'rb') as f:
                        profile.photo.save(
                            local_file.name,
                            File(f),
                            save=True
                        )

                    self.stdout.write(self.style.SUCCESS(f'  ✓ New path: {profile.photo.name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'  ✗ Local file not found: {local_file}'))

        # 2. MainPageContent 배너 재업로드
        self.stdout.write('\n=== Re-uploading Main Banners ===')
        main_contents = MainPageContent.objects.all()

        for content in main_contents:
            if content.main_banner:
                old_path = str(content.main_banner.name)
                self.stdout.write(f'Banner: {content.title}')
                self.stdout.write(f'  Old path: {old_path}')

                local_file = media_dir / old_path

                if not local_file.exists():
                    # banners/ 폴더에서 찾기
                    banners_dir = media_dir / 'banners'
                    if banners_dir.exists():
                        for file_path in banners_dir.glob('*'):
                            if file_path.is_file():
                                local_file = file_path
                                break

                if local_file.exists():
                    self.stdout.write(f'  Found local file: {local_file}')

                    with open(local_file, 'rb') as f:
                        content.main_banner.save(
                            local_file.name,
                            File(f),
                            save=True
                        )

                    self.stdout.write(self.style.SUCCESS(f'  ✓ New path: {content.main_banner.name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'  ✗ Local file not found'))

        # 3. ProjectImage 재업로드
        self.stdout.write('\n=== Re-uploading Project Images ===')
        project_images = ProjectImage.objects.all()

        for img in project_images:
            if img.image:
                old_path = str(img.image.name)
                self.stdout.write(f'Project: {img.project.title} - Image {img.order}')
                self.stdout.write(f'  Old path: {old_path}')

                local_file = media_dir / old_path

                if not local_file.exists():
                    # project/img/ 폴더에서 찾기
                    project_img_dir = media_dir / 'project' / 'img'
                    if project_img_dir.exists():
                        # 파일명으로 찾기
                        filename = Path(old_path).name
                        potential_file = project_img_dir / filename
                        if potential_file.exists():
                            local_file = potential_file

                if local_file.exists():
                    self.stdout.write(f'  Found local file: {local_file}')

                    with open(local_file, 'rb') as f:
                        img.image.save(
                            local_file.name,
                            File(f),
                            save=True
                        )

                    self.stdout.write(self.style.SUCCESS(f'  ✓ New path: {img.image.name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'  ✗ Local file not found'))

        self.stdout.write(self.style.SUCCESS('\n=== Image re-upload completed ==='))
