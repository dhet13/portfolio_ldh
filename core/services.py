"""
Core app의 비즈니스 로직을 담당하는 서비스 계층
뷰에서 독립적으로 재사용 가능한 함수들을 정의합니다.
"""
from datetime import date
from dateutil.relativedelta import relativedelta
from typing import Optional
from .models import Experience


def calculate_total_experience(experiences=None) -> str:
    """
    경력(Experience) 객체들의 총 경력 기간을 계산합니다.
    중복되는 기간은 병합하여 실제 근무 기간만 계산합니다.

    Args:
        experiences: Experience QuerySet 또는 리스트. None이면 전체 조회.

    Returns:
        str: "X년 Y개월" 형식의 총 경력 문자열. 경력이 없으면 "0개월"

    Examples:
        >>> calculate_total_experience()
        "3년 6개월"

        >>> from core.models import Experience
        >>> exps = Experience.objects.filter(company="ABC Corp")
        >>> calculate_total_experience(exps)
        "1년 2개월"
    """
    # experiences가 None이면 전체 조회
    if experiences is None:
        experiences = Experience.objects.all().order_by('-start_date')

    if not experiences:
        return "0개월"

    # 모든 경력 기간을 (시작일, 종료일) 튜플 리스트로 변환
    periods = []
    for exp in experiences:
        start = exp.start_date
        end = exp.end_date if exp.end_date else date.today()
        periods.append((start, end))

    # 시작일 기준으로 정렬
    periods.sort(key=lambda x: x[0])

    # 겹치는 기간 병합 (Interval Merging 알고리즘)
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

    # 년/월 형식으로 변환
    total_years = total_months // 12
    remaining_months = total_months % 12

    result_parts = []
    if total_years > 0:
        result_parts.append(f"{total_years}년")
    if remaining_months > 0:
        result_parts.append(f"{remaining_months}개월")

    return " ".join(result_parts) if result_parts else "0개월"


def get_portfolio_context() -> dict:
    """
    포트폴리오 홈페이지에 필요한 모든 데이터를 조회하여 컨텍스트로 반환합니다.

    Returns:
        dict: 템플릿 렌더링에 필요한 컨텍스트 딕셔너리
    """
    from .models import MainPageContent, Profile, Skill, Education
    from projects.models import Project

    # 메인 컨텐츠 및 프로필 조회
    try:
        main_content = MainPageContent.objects.first()
        profile = Profile.objects.first()
    except Exception:
        main_content = None
        profile = None

    # 관련 데이터 조회
    skills = Skill.objects.all().order_by('order')
    experiences = Experience.objects.all().order_by('-start_date')
    educations = Education.objects.all().order_by('-start_date')
    skill_categories = Skill.get_category_averages()

    # 프로젝트 조회 (최신 6개, 관련 이미지 prefetch)
    projects = Project.objects.select_related('company').prefetch_related('images').order_by('-start_date')[:6]

    # 총 경력 기간 계산
    total_experience_duration = calculate_total_experience(experiences)

    return {
        'main_content': main_content,
        'profile': profile,
        'skills': skills,
        'experiences': experiences,
        'educations': educations,
        'skill_categories': skill_categories,
        'projects': projects,
        'total_experience_duration': total_experience_duration,
    }
