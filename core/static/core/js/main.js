document.addEventListener('DOMContentLoaded', function() {
    const experienceItems = document.querySelectorAll('.experience-item');

    experienceItems.forEach(item => {
        const btn = item.querySelector('.details-btn');
        
        // 모바일 화면에서만 버튼에 이벤트 리스너를 추가합니다.
        // 데스크탑에서는 이 버튼이 숨겨져 있습니다.
        if (btn) {
            btn.addEventListener('click', () => {
                // 현재 클릭된 아이템의 active 상태를 토글합니다.
                const isActive = item.classList.contains('active');

                // 다른 모든 아이템의 active 상태는 제거합니다 (하나만 열리도록).
                experienceItems.forEach(otherItem => {
                    otherItem.classList.remove('active');
                });

                // 현재 아이템이 이미 active였다면 토글로 닫히게 되므로,
                // active가 아니었을 때만 다시 active를 추가해 열린 상태를 유지합니다.
                if (!isActive) {
                    item.classList.add('active');
                }
            });
        }
    });
});
