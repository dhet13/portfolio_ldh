  # -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import MainPageContent, Profile, Skill, Experience, Education
from projects.models import Project
from datetime import date
from dateutil.relativedelta import relativedelta

def home(request):
    try:
        main_content = MainPageContent.objects.first()      
        profile = Profile.objects.first()
    except:
        main_content = None
        profile = None

    skills = Skill.objects.all().order_by('order')
    experiences = Experience.objects.all().order_by('-start_date')
    
    # 총 경력 계산 로직 (중복 기간 제외)
    if experiences:
        # 모든 경력 기간을 (시작일, 종료일) 튜플 리스트로 변환
        periods = []
        for exp in experiences:
            start = exp.start_date
            end = exp.end_date if exp.end_date else date.today()
            periods.append((start, end))

        # 시작일 기준으로 정렬
        periods.sort(key=lambda x: x[0])

        # 겹치는 기간 병합
        merged = [periods[0]]
        for current_start, current_end in periods[1:]:
            last_start, last_end = merged[-1]

            # 현재 기간이 마지막 병합 기간과 겹치거나 연속되면 병합
            if current_start <= last_end:
                # 더 늦은 종료일로 갱신
                merged[-1] = (last_start, max(last_end, current_end))
            else:
                # 겹치지 않으면 새로운 기간으로 추가
                merged.append((current_start, current_end))

        # 병합된 기간들의 총 개월 수 계산
        total_months = 0
        for start, end in merged:
            diff = relativedelta(end, start)
            total_months += diff.years * 12 + diff.months

        total_years = total_months // 12
        remaining_months = total_months % 12

        total_experience_duration = ""
        if total_years > 0:
            total_experience_duration += f"{total_years}년 "
        if remaining_months > 0:
            total_experience_duration += f"{remaining_months}개월"
        total_experience_duration = total_experience_duration.strip()
    else:
        total_experience_duration = "0개월"
    
    educations = Education.objects.all().order_by('-start_date')
    skill_categories = Skill.get_category_averages()

    projects = Project.objects.select_related('company').prefetch_related('images').order_by('-start_date')[:6]

    context = {
        'main_content': main_content,
        'profile': profile,
        'skills': skills,
        'experiences': experiences,
        'educations': educations,
        'skill_categories': skill_categories,
        'projects':projects,
        'total_experience_duration': total_experience_duration,
    }
    return render(request, 'core/home.html', context) 
