from django.contrib import admin
from .models import Project, ProjectFile, ProjectImage
from django.utils.html import format_html
from django import forms
# Register your models here.

class ProjectAdminform(forms.ModelForm):
    # URL 필드를 CharField로 오버라이드 (iframe 코드 입력 가능하도록)
    figma_url = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Figma URL 또는 iframe 코드 입력'}),
        label='Figma URL'
    )
    github_url = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'GitHub URL 또는 iframe 코드 입력'}),
        label='GitHub URL'
    )
    demo_url = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Demo URL 또는 iframe 코드 입력'}),
        label='Demo URL'
    )

    class Meta:
        model = Project
        fields = '__all__'

    def clean_figma_url(self):
        import re
        figma_url = self.cleaned_data.get('figma_url', '')

        print(f"🔍 clean_figma_url 실행됨! 입력값: {figma_url[:100] if figma_url else 'None'}")

        if figma_url and '<iframe' in figma_url:
            match = re.search(r'src=["\']([^"\']+)["\']', figma_url)
            if match:
                extracted_url = match.group(1)
                print(f"✅ URL 추출 성공: {extracted_url}")
                return extracted_url

        print(f"⚠️ iframe 코드 아님, 원본 반환: {figma_url[:100] if figma_url else 'None'}")
        return figma_url
    
    def clean_github_url(self):
        import re
        github_url = self.cleaned_data.get('github_url', '')
        
        if github_url and '<iframe' in github_url:
            match = re.search(r'src=["\']([^"\']+)["\']', github_url)
            if match:
                return match.group(1)
        
        return github_url
    
    def clean_demo_url(self):
        import re
        demo_url = self.cleaned_data.get('demo_url', '')
        
        if demo_url and '<iframe' in demo_url:
            match = re.search(r'src=["\']([^"\']+)["\']', demo_url)
            if match:
                return match.group(1)
        
        return demo_url

# ProjectImage Inline 설정
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ['image', 'image_preview', 'order', 'is_thumbnail']
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
    form = ProjectAdminform
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