from django.contrib import admin
from .models import Project, ProjectFile, ProjectImage
from django.utils.html import format_html
# Register your models here.

# ProjectImage Inline 설정
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ['image', 'image_preview', 'order', 'is_thumnbnail']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 80px;" />',
                obj.image.url
            )
        return "이미지 없음"
    image_preview.short_description = "미리보기"

# ProjectFile Inline 설정
class ProjectFileInline(admin.TabularInline):
    model = ProjectFile
    extra = 1
    fields = ['file', 'title', 'file_type', 'order']
    readonly_fields = ['file_type'] # 읽기 전용 표시

# Project Admin 설정
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'start_date', 'end_date'] #프로젝트 목록에서 한 눈에 볼 정보
    list_filter = ['company', 'start_date'] # 회사별, 날짜별 필터링
    search_fields = ['title', 'description'] # 프로젝트 명이나 설명으로 검색
    ordering = ['-start_date']
    inlines = [ProjectImageInline, ProjectFileInline]

    fieldsets = (
        ('기본 정보', {
            'fields': ('company', 'title', 'description')
        }),
        ('프로젝트 기간', {
            'fields': ('start_date', 'end_date')
        }),
        ('링크', {
            'fields': ('figma_url', 'github_url', 'demo_url')
        }),
    )

    def get_period_display(self,obj): # 목록에 계산된 값 표시
        if obj.end_date:
            return  f"{obj.start_date} ~ {obj.end_date}"
        return f"{obj.start_date} ~ 진행 중"
    
    get_period_display.short_description = "프로젝트 기간"