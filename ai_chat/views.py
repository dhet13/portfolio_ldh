"""
AI Chat 앱의 뷰 함수들
HTTP 요청을 처리하고 스트리밍 응답을 생성합니다.
비즈니스 로직은 services.py에 위임합니다.
"""
from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import time
from .models import ChatSession, ChatConversation
from . import services

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
            return JsonResponse(
                {
                    'notice': '일일 질문 한도(10회)를 초과했습니다. 만나서 더 이야기를 나누면 좋을 것 같아요. :)',
                    'remaining': 0,
                },
                status=429,
            )

        # 스트리밍 응답 생성
        def stream_response():
            start_time = time.time()
            full_response = ""

            try:
                context_data = services.get_portfolio_context_for_ai()

                # 스트리밍 API 호출
                for chunk_text in services.generate_ai_response_stream(user_input, context_data):
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

