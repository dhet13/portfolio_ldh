document.addEventListener('DOMContentLoaded', function() {
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');

    // --- 페이지 로드 시 대화 기록 및 질문 수 불러오기 ---
    loadChatHistory();

    // 전송 버튼 클릭 또는 Enter 키 입력 시 sendMessage 함수 호출
    sendButton.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    function sendMessage() {
        const messageText = chatInput.value.trim();
        if (messageText === '') return;

        appendMessage(messageText, 'user-message');
        chatInput.value = '';

        // AI 응답을 담을 메시지 div 생성 (미리 생성, 내용은 비움)
        const aiMessageDiv = document.createElement('div');
        aiMessageDiv.classList.add('message', 'ai-message');
        aiMessageDiv.innerHTML = '';

        let isFirstChunk = true;
        let textBuffer = ''; // 표시 대기 중인 텍스트
        let typingInterval = null; // 타이핑 interval 참조

        // 타이핑 interval 시작 (한 번만 실행)
        function startTyping() {
            if (typingInterval !== null) return; // 이미 실행 중이면 무시

            typingInterval = setInterval(() => {
                if (textBuffer.length > 0) {
                    const char = textBuffer.charAt(0);
                    textBuffer = textBuffer.substring(1);

                    // 줄바꿈 처리
                    const displayChar = char === '\n' ? '<br>' : char;
                    aiMessageDiv.innerHTML += displayChar;
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }
                // 버퍼가 비어도 interval은 계속 실행 (새 청크 대기)
            }, 30); // 30ms per character
        }

        fetch('/chat/send/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ message: messageText })
        })
        .then(response => {
            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            function readStream() {
                reader.read().then(({ done, value }) => {
                    if (done) {
                        return;
                    }

                    const chunk = decoder.decode(value);
                    const lines = chunk.split('\n');

                    lines.forEach(line => {
                        if (line.startsWith('data: ')) {
                            const jsonData = line.substring(6);
                            try {
                                const data = JSON.parse(jsonData);

                                if (data.chunk) {
                                    // 첫 청크가 왔을 때 메시지 div 추가 & 타이핑 시작
                                    if (isFirstChunk) {
                                        chatMessages.appendChild(aiMessageDiv);
                                        startTyping(); // 타이핑 interval 시작
                                        isFirstChunk = false;
                                    }

                                    // 버퍼에 텍스트 추가 (interval이 자동으로 처리)
                                    textBuffer += data.chunk;

                                } else if (data.done) {
                                    // 스트림 완료 - interval 정리
                                    if (typingInterval !== null) {
                                        // 남은 버퍼가 모두 표시될 때까지 기다림
                                        const checkComplete = setInterval(() => {
                                            if (textBuffer.length === 0) {
                                                clearInterval(typingInterval);
                                                clearInterval(checkComplete);
                                                typingInterval = null;
                                            }
                                        }, 100);
                                    }
                                    updateRemainingCount(data.remaining);

                                } else if (data.error) {
                                    // 에러 처리
                                    appendMessage(data.error, 'ai-message', 'error');
                                }
                            } catch (e) {
                                console.error('JSON parse error:', e);
                            }
                        }
                    });

                    readStream();
                });
            }

            readStream();
        })
        .catch(error => {
            console.error('Error:', error);
            appendMessage('에러가 발생했습니다. 다시 요청해주세요.', 'ai-message', 'error');
        });
    }

    // --- 대화 기록 로드 함수 (새로 추가) ---
    function loadChatHistory() {
        fetch('/chat/history/')
            .then(response => response.json())
            .then(data => {
                // 남은 질문 수 업데이트
                updateRemainingCount(data.remaining);

                // 기존 대화 내용 화면에 표시
                if (data.history && data.history.length > 0) {
                    data.history.forEach(conv => {
                        appendMessage(conv.question, 'user-message');
                        appendMessage(conv.answer, 'ai-message');
                    });
                }
            })
            .catch(error => console.error('Error loading history:', error));
    }

    // --- 남은 질문 수 업데이트 함수 (새로 추가) ---
    function updateRemainingCount(count) {
        const remainingDisplay = document.getElementById('remaining-questions-display');
        if (remainingDisplay && count !== undefined) {
            remainingDisplay.textContent = count;
        }
        // 상단 환영 메시지에 있는 카운터도 함께 업데이트
        const initialCounter = document.getElementById('remaining-count');
        if(initialCounter) {
            initialCounter.textContent = count;
        }
    }

    function appendMessage(text, ...classNames) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', ...classNames);

        // 줄바꿈 처리: \n을 <br> 태그로 변환
        const formattedText = text.replace(/\n/g, '<br>');
        messageDiv.innerHTML = formattedText;

        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});