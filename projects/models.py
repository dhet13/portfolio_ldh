from django.db import models
from core.models import Experience
from datetime import date
from dateutil.relativedelta import relativedelta
from pathlib import Path
import mimetypes

class Project(models.Model):
    company = models.ForeignKey(
        'core.Experience',
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name="회사명",
    )

    title = models.CharField(max_length=200, verbose_name="프로젝트명")
    description = models.TextField(verbose_name="프로젝트 설명")
    start_date = models.DateField(verbose_name="시작일")
    end_date = models.DateField(verbose_name="종료일", blank=True, null=True)
    figma_url = models.URLField(max_length=500, blank=True, verbose_name="Figma URL")
    github_url = models.URLField(max_length=500, blank=True, verbose_name="Github URL")
    demo_url = models.URLField(max_length=500, blank=True, verbose_name="Demo URL")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "5.프로젝트"
        verbose_name_plural = "5.프로젝트"
        ordering = ["-start_date"]

    def __str__(self):
        return self.title
    
class ProjectImage(models.Model):
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="프로젝트명",
    )
    image = models.ImageField(upload_to="project/img", blank=True, null=True, 
                              verbose_name="프로젝트 이미지")
    order = models.IntegerField(default=0, verbose_name="순서")
    is_thumbnail = models.BooleanField(default=False, verbose_name="대표 이미지")

    class Meta:
        verbose_name = "프로젝트 이미지"
        verbose_name_plural = "프로젝트 이미지"
        ordering = ['order']
    
    def __str__(self):
        return f"{self.project.title} - 이미지 {self.order}"
    
class ProjectFile(models.Model):
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name="프로젝트 파일",
    )

    file = models.FileField (
        upload_to='project/file', blank=True, null=True, verbose_name="프로젝트 파일"
    )
    original_filename = models.CharField(max_length=200) #원본명 저장
    file_type = models.CharField(max_length=20, blank=True, editable=False, verbose_name="파일 타입")
    title = models.CharField(max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    order = models.BigIntegerField(default=0, verbose_name="순서")

    def save(self, *args, **kwargs):
        if self.file: #원본 파일명 저장
            if not self.original_filename:
                self.original_filename = self.file.name

            # MIME 타입 추출 및 저장 (수정된 부분)
            mime_type, _= mimetypes.guess_type(self.file.name)
            self.file_type = mime_type if mime_type else 'application/octet-stream'


        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "프로젝트 파일"
        verbose_name_plural = "프로젝트 파일"
        ordering = ['order']
    def __str__(self):
        return f"{self.project.title} - 파일{self.title}"
        










# Create your models here.
