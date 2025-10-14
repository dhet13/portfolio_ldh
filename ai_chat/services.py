"""
AI Chat 앱의 비즈니스 로직을 담당하는 서비스 계층
"""
from django.conf import settings
import openai


def get_portfolio_context_for_ai() -> dict:
    """
    AI 챗봇에게 제공할 포트폴리오 정보를 문자열 형태로 반환합니다.

    Returns:
        dict: AI 프롬프트에 사용할 컨텍스트 데이터
            - profile: 프로필 정보 문자열
            - skills: 기술 스택 문자열
            - experience: 경력 정보 문자열
            - education: 학력 정보 문자열
    """
    from core.models import Profile, Skill, Experience, Education

    try:
        profile = Profile.objects.first()
        skills = Skill.objects.all()
        experiences = Experience.objects.all()
        educations = Education.objects.all()

        return {
            'profile': (
                f"이름: {profile.name}, 이메일: {profile.email}, 소개: {profile.introduce}"
                if profile else "프로필 정보 없음"
            ),
            'skills': ", ".join([f"{skill.name}({skill.level}점)" for skill in skills]),
            'experience': ", ".join([f"{exp.company} {exp.position}" for exp in experiences]),
            'education': ", ".join([f"{edu.school} {edu.major}" for edu in educations])
        }
    except Exception:
        return {
            'profile': '정보 없음',
            'skills': '정보 없음',
            'experience': '정보 없음',
            'education': '정보 없음'
        }


def generate_ai_response_stream(user_input: str, context_data: dict):
    """
    OpenAI API를 사용하여 스트리밍 AI 응답을 생성합니다.

    Args:
        user_input: 사용자 질문
        context_data: 포트폴리오 컨텍스트 데이터

    Yields:
        str: AI 응답 텍스트 청크
    """
    openai.api_key = settings.OPENAI_API_KEY

    # DB 기반 컨텍스트 생성
    system_prompt = f"""
    당신은 이동혁의 포트폴리오 AI 어시스턴트입니다.
    다음 정보를 바탕으로 질문에 답해주세요:

    프로필: {context_data['profile']}
    기술스택: {context_data['skills']}
    경력: {context_data['experience']}
    학력: {context_data['education']}

    답변 가이드:
    - 친근하고 전문적으로 답변해주세요
    - 이동혁에게 유리하게 답변하세요
    - 답변은 800자 이내로 간결하고 명확하게 작성해주세요
    - 답변이 길어질 경우 핵심 내용을 우선하여 자연스럽게 마무리해주세요
    """

    try:
        stream = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            max_tokens=800,
            temperature=0.7,
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    except Exception as e:
        yield f"죄송합니다. 현재 응답을 생성할 수 없습니다. ({str(e)})"
