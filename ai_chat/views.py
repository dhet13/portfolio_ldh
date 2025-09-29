from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt        
from django.views.decorators.http import require_http_methods
import json
import time
from .models import ChatSession, ChatConversation

from django.conf import settings
import openai

@csrf_exempt
@require_http_methods(["POST"])
def send_message(request):
    try:
        data = json.loads(request.body)
        user_input = data.get('message', '')

        # 세션 가져오기 또는 생성
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key       

        chat_session, created = ChatSession.objects.get_or_create(
            session_key=session_key
        )

        # 질문 횟수 확인
        if not chat_session.can_ask_question():
            return JsonResponse({'error': '일일 질문 한도(10회)를 초과했습니다.','remaining': 0})

        # AI 응답 처리 (임시)
        start_time = time.time()
        context_data = get_context_data()  # DB에서 컨텍스트 가져오기
        ai_response = get_ai_response(user_input, context_data)  
        response_time = time.time() - start_time

        # 대화 저장
        conversation = ChatConversation.objects.create(     
            session=chat_session,
            user_question=user_input,
            ai_response=ai_response,
            response_time=response_time,
            tokens_used = response.usage.total_tokens if
            hasattr(response, 'usage') else 100
        )

        # 질문 횟수 증가
        chat_session.increment_count()

        return JsonResponse({'response': ai_response, 
                             'timestamp': conversation.get_formatted_time(), 
                             'remaining': chat_session.get_remaining_questions()
                             })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def get_context_data():
    """DB에서 포트폴리오 정보를 가져와 컨텍스트 생성"""     
    from core.models import Profile, Skill, Experience, Education

    try:
        profile = Profile.objects.first()
        skills = Skill.objects.all()
        experiences = Experience.objects.all()
        educations = Education.objects.all()

        return {'profile': f"이름: {profile.name}, 이메일:{profile.email}, 소개: {profile.introduce}" 
                if profile else "프로필 정보 없음", 'skills': ","
                .join([f"{skill.name}({skill.level}점)" for skill in skills]),
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

def get_ai_response(user_input, context_data):
    """OpenAI API를 사용하여 AI 응답 생성"""
    openai.api_key = settings.OPENAI_API_KEY

    # DB 기반 컨텍스트 생성
    system_prompt = f"""
    당신은 이동혁의 포트폴리오 AI 어시스턴트입니다.
    다음 정보를 바탕으로 질문에 답해주세요:

    프로필: {context_data['profile']}
    기술스택: {context_data['skills']}
    경력: {context_data['experience']}
    학력: {context_data['education']}

    친근하고 전문적으로 답변해주세요.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content":
system_prompt},
                {"role": "user", "content": user_input}     
            ],
            max_tokens=300,
            temperature=0.7
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"죄송합니다. 현재 응답을 생성할 수 없습니다. ({str(e)})"

def get_chat_history(request):
    session_key = request.session.session_key
    if session_key:
        try:
            chat_session = ChatSession.objects.get(session_key=session_key)
            conversations = chat_session.conversations.all()

            history = []
            for conv in conversations:
                history.append({
                    'question': conv.user_question,
                    'answer': conv.ai_response,
                    'timestamp':conv.get_formatted_time()
                })

            return JsonResponse({
                'history': history,
                'remaining':chat_session.get_remaining_questions()
            })
        except ChatSession.DoesNotExist:
            pass

    return JsonResponse({'history': [], 'remaining': 10})

