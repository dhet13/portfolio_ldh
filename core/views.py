# -*- coding: utf-8 -*-
"""
Core 앱의 뷰 함수들
HTTP 요청을 처리하고 적절한 템플릿을 렌더링합니다.
비즈니스 로직은 services.py에 위임합니다.
"""
from django.shortcuts import render
from . import services


def home(request):
    """
    포트폴리오 홈페이지 뷰
    서비스 계층에서 데이터를 조회하여 템플릿에 전달합니다.
    """
    context = services.get_portfolio_context()
    return render(request, 'core/home.html', context) 
