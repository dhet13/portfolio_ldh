document.addEventListener('DOMContentLoaded', function() {
    // 요소 선택
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const chatToggle = document.querySelector('.mobile-chat-toggle');
    const leftSidebar = document.querySelector('.left-sidebar');
    const rightSidebar = document.querySelector('.right-sidebar-wrapper');
    const overlay = document.querySelector('.overlay');

    // 햄버거 버튼 클릭 시
    menuToggle.addEventListener('click', () => {
        leftSidebar.classList.toggle('active');
        overlay.classList.toggle('active');
    });

    // 채팅 버튼 클릭 시
    chatToggle.addEventListener('click', () => {
        rightSidebar.classList.toggle('active');
        overlay.classList.toggle('active');
    });

    // 오버레이 클릭 시 모든 사이드 닫기
    overlay.addEventListener('click', ()=> {
        leftSidebar.classList.remove('active');
        rightSidebar.classList.remove('active');
        overlay.classList.remove('active');
    })
});