from django.db import models
from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.validators import MinValueValidator, MaxValueValidator



class MainPageContent(models.Model):
    title = models.CharField(max_length=200, verbose_name="메인 제목")
    subtitle = models.TextField(verbose_name="부제목")
    main_banner = models.ImageField(upload_to='banners/', blank=True, null=True,
    verbose_name="메인 배너 이미지")

    class Meta:
        verbose_name = "1.메인 페이지 설정"
        verbose_name_plural = "1.메인 페이지 설정"

    def __str__(self):
        return self.title
    
class Profile(models.Model):
    name = models.CharField(max_length=200, verbose_name="이름")
    english_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="photos/", blank=True, null=True, verbose_name="프로필 사진")
    introduce = models.TextField(verbose_name="자기 소개")
    birth_date = models.DateField()
    email = models.CharField(max_length=200, verbose_name="이메일")
    phone = models.CharField(max_length=20, verbose_name="핸드폰")

    resume_file = models.FileField(upload_to="resumes/", blank=True, null=True, verbose_name="이력서 파일",
    help_text="PDF, DOC, DOCX 파일만 업로드")

    class Meta:
        verbose_name = "2.프로필"
        verbose_name_plural = "2.프로필"
    
    def __str__(self):
        return self.name
    
class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    school = models.CharField(max_length=100, verbose_name="학교명")
    degree_type = models.CharField(max_length=20, verbose_name="학위")
    major = models.CharField(max_length=50, verbose_name="전공")
    is_major = models.BooleanField(default=True, verbose_name="주전공 여부")
    minor = models.CharField(max_length=50, blank=True, null=True, verbose_name="부전공")
    start_date = models.DateField(verbose_name="입학일")
    end_date = models.DateField(blank=True, null=True, verbose_name="졸업일")

    
class Skill(models.Model):
    name = models.CharField(max_length=100, verbose_name="스킬명")
    category = models.CharField(max_length=50, verbose_name="카테고리")
    order = models.IntegerField(verbose_name="정렬순서")
    level = models.FloatField(default=0.0,
    validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
    verbose_name="숙련도(별점)")

    class Meta:
        verbose_name = "3.기술스택"
        verbose_name_plural = "3.기술스택"
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.name} - {self.level}"  #
    
    @classmethod
    def get_category_averages(cls):
        from django.db.models import Avg
        return cls.objects.values('category').annotate(avg_level=Avg('level'))

    def get_star_rating(self):
        # 5점 만점을 5개 별로 변환
        return int(self.level)
        

class Experience(models.Model):
    company = models.CharField(max_length=200, verbose_name="회사명")
    position = models.CharField(max_length=100, verbose_name="직책")
    start_date = models.DateField(verbose_name="시작일")
    end_date = models.DateField(blank=True, null=True, verbose_name="종료일")
    description = models.TextField(verbose_name="회사 및 업무 내용")
    is_current = models.BooleanField(default=False, verbose_name="현재 재직중")

    def get_duration(self):
        """재직 기간을 문자열로 반환"""
        end_date = self.end_date if self.end_date else date.today()

        diff = relativedelta(end_date, self.start_date)

        years = diff.years
        months = diff.months

        if years > 0 and months > 0:
            return f"{years}년 {months}개월"
        elif years > 0:
            return f"{years}년"
        elif months > 0:
            return f"{months}개월"
        else:
              return "1개월 미만"
        
    def get_period_display(self):
        """기간을 년.월 ~ 년.월 형태로 표시"""
        start = self.start_date.strftime("%Y.%m")

        if self.is_current:
            return f"{start} ~ 현재"
        elif self.end_date:
            end = self.end_date.strftime("%Y.%m")
            return f"{start} ~ {end}"
        else:
            return f"{start} ~ 현재"

    class Meta:
        verbose_name = "4.경력"
        verbose_name_plural = "4.경력"
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.company} - {self.position}"