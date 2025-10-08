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

        fetch('/chat/send/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ message: messageText })
        })
        .then(response => response.json())
        .then(data => {
            if (data.response) {
                appendMessage(data.response, 'ai-message');
            } else if (data.error) {
                appendMessage('Error: ' + data.error, 'ai-message', 'error');
            }
            // 남은 질문 수 업데이트
            updateRemainingCount(data.remaining);
        })
        .catch(error => {
            console.error('Error:', error);
            appendMessage('통신 중 오류가 발생했습니다.', 'ai-message', 'error');
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
        messageDiv.textContent = text;
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