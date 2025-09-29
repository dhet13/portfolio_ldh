from django.contrib import admin
from .models import MainPageContent, Profile, Skill, Experience, Education
from django.utils.html import format_html

class EducationInline(admin.TabularInline):
    model = Education
    extra = 1  # 기본으로 빈 폼 1개 표시
    fields = ['school', 'degree_type', 'major', 'is_major', 'minor','start_date',
'end_date']

  # 코딩 순서대로 등록
@admin.register(MainPageContent) 
class MainPageContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'image_preview']
    readonly_fields = ['image_preview']  # 읽기 전용으로 미리보기 추가

    def image_preview(self, obj):
          if obj.main_banner:
              return format_html(
                  '<img src="{}" style="max-height: 100px; max-width: 200px;" />',      
                  obj.main_banner.url
              )
          return "이미지 없음"
    image_preview.short_description = "이미지 미리보기"

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'image_preview']
    inlines = [EducationInline]
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
          if obj.photo:
              return format_html(
                  '<img src="{}" style="max-height: 100px; max-width: 100px; border-radius: 50%;" />',
                  obj.photo.url
              )
          return "사진 없음"
    image_preview.short_description = "프로필 사진"

@admin.register(Skill) 
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'level', 'order']
    list_filter = ['category']
    ordering = ['order', 'name']

@admin.register(Experience) 
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['company', 'position', 'get_period_display', 'get_duration',      
'is_current']
    list_filter = ['is_current', 'start_date']
    ordering = ['-start_date']

    def get_period_display(self, obj):
        return obj.get_period_display()
    get_period_display.short_description = "근무기간"

    def get_duration(self, obj):
        return obj.get_duration()
    get_duration.short_description = "재직기간"

