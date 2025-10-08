document.addEventListener('DOMContentLoaded', function() {
    // 모든 상세보기 버튼 찾기
    const readMoreButtons = document.querySelectorAll('.read-more-btn');
    
    readMoreButtons.forEach(button => {
        //각 버튼 바로 위에 있는 설명 div를 찾기
        const description = button.previousElementSibling;
        
        if (description.scrollHeight <= 136) {// css의 max-height 값과 일치
            button.style.display = 'none';
        }

        //버튼에 클릭 이벤트 리스너 추가
        button.addEventListener('click', () => {
            const isCollapsed = description.classList.contains('collapsible');

            // 클래스를 토글하여 css스타일 변경
            description.classList.toggle('collapsible');
            description.classList.toggle('expanded');

            // 버튼의 텍스트를 변경합니다.
            if (isCollapsed) {
                button.textContent = '간략히 보기';
            }
            else {
                button.textContent = '상세보기';
            }
        });
    });
});