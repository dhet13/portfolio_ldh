  # -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import MainPageContent, Profile, Skill, Experience, Education

def home(request):
    try:
        main_content = MainPageContent.objects.first()      
        profile = Profile.objects.first()
    except:
        main_content = None
        profile = None

    skills = Skill.objects.all().order_by('order')
    experiences = Experience.objects.all().order_by('-start_date')
    educations = Education.objects.all().order_by('-start_date')  # 추가     
    skill_categories = Skill.get_category_averages() 

    context = {
        'main_content': main_content,
        'profile': profile,
        'skills': skills,
        'experiences': experiences,
        'educations': educations,
        'skill_categories': skill_categories,  # 추가       
    }
    return render(request, 'core/home.html', context) 
