from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
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
            return JsonResponse({'error': '일일 질문 한도(10회)를 초과했습니다. 만나서 더 이야기를 나누면 좋을 것 같아요. :)','remaining': 0})

        # 스트리밍 응답 생성
        def stream_response():
            start_time = time.time()
            full_response = ""

            try:
                context_data = get_context_data()

                # 스트리밍 API 호출
                for chunk_text in get_ai_response_stream(user_input, context_data):
                    full_response += chunk_text
                    # SSE 형식으로 전송
                    yield f"data: {json.dumps({'chunk': chunk_text})}\n\n"

                response_time = time.time() - start_time

                # 스트림 완료 후 DB 저장
                conversation = ChatConversation.objects.create(
                    session=chat_session,
                    user_question=user_input,
                    ai_response=full_response,
                    response_time=response_time,
                    tokens_used=0  # 스트리밍에서는 토큰 수 계산 어려움
                )

                # 질문 횟수 증가
                chat_session.increment_count()

                # 완료 신호 전송
                yield f"data: {json.dumps({'done': True, 'remaining': chat_session.get_remaining_questions()})}\n\n"

            except Exception as e:
                # 에러 발생 시
                yield f"data: {json.dumps({'error': '에러가 발생했습니다. 다시 요청해주세요.'})}\n\n"

        return StreamingHttpResponse(stream_response(), content_type='text/event-stream')

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

def get_ai_response_stream(user_input, context_data):
    """OpenAI API를 사용하여 스트리밍 AI 응답 생성"""
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
            max_tokens=800,  # 더 긴 답변 허용 (약 400-600자)
            temperature=0.7,
            stream=True  # 스트리밍 활성화
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    except Exception as e:
        yield f"죄송합니다. 현재 응답을 생성할 수 없습니다. ({str(e)})"

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

