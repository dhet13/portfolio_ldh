// core/static/core/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    
    // --- 기존 코드: 경력 섹션 아코디언 기능 (모바일용) ---
    const experienceItems = document.querySelectorAll('.experience-item');

    experienceItems.forEach(item => {
        // .experience-meta 요소를 클릭 타겟으로 변경합니다.
        const clickableArea = item.querySelector('.experience-meta');
        
        if (clickableArea) {
            clickableArea.addEventListener('click', () => {
                // 화면 너비가 768px 이하일 때만 동작 (모바일/태블릿)
                if (window.innerWidth <= 768) {
                    const isActive = item.classList.contains('active');

                    // 모든 아이템에서 'active' 클래스를 먼저 제거합니다.
                    experienceItems.forEach(otherItem => {
                        otherItem.classList.remove('active');
                    });

                    // 현재 아이템이 비활성 상태였다면 'active' 클래스를 추가하여 펼칩니다.
                    if (!isActive) {
                        item.classList.add('active');
                    }
                    // 이미 활성 상태였다면, 위에서 제거되었으므로 아코디언이 닫힙니다.
                }
            });
        }
    });

    // --- 신규 코드: 스크롤 스파이 및 부드러운 스크롤 기능 ---

    // 1. 필요한 DOM 요소 선택
    const sections = document.querySelectorAll('section[id]'); // ID가 있는 모든 섹션
    const navLinks = document.querySelectorAll('.side-navigation .nav-link'); // 사이드 네비게이션 링크
    const sectionMargin = 200; // 섹션 활성화 감지 여백 (px)

    // 2. Intersection Observer 설정
    // 섹션이 뷰포트의 특정 영역에 들어왔을 때 감지하기 위한 옵션
    const observerOptions = {
        root: null, // 뷰포트를 기준으로 감지
        rootMargin: `-${sectionMargin}px 0px -${sectionMargin}px 0px`, // 뷰포트 상하단을 200px씩 축소
        threshold: 0.1 // 섹션이 10% 이상 보일 때 콜백 실행
    };

    // Intersection Observer 인스턴스 생성
    const sectionObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            // 섹션이 뷰포트와 교차하고 있을 때
            if (entry.isIntersecting) {
                // 모든 네비게이션 링크의 'active' 클래스 제거
                navLinks.forEach(link => {
                    link.classList.remove('active');
                });

                // 현재 보이는 섹션에 해당하는 네비게이션 링크를 찾아 'active' 클래스 추가
                const currentNavLink = document.querySelector(`.side-navigation .nav-link[href="#${entry.target.id}"]`);
                if (currentNavLink) {
                    currentNavLink.classList.add('active');
                }
            }
        });
    }, observerOptions);

    // 3. 모든 섹션에 대해 Observer 등록
    sections.forEach(section => {
        sectionObserver.observe(section);
    });

    // 4. 부드러운 스크롤 기능 구현
    // 각 네비게이션 링크에 클릭 이벤트 리스너 추가
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault(); // 기본 앵커 동작 방지

            const targetId = this.getAttribute('href'); // 클릭된 링크의 href 값 (e.g., "#about")
            const targetSection = document.querySelector(targetId); // 해당 ID를 가진 섹션 요소

            if (targetSection) {
                // 해당 섹션으로 부드럽게 스크롤
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start' // 섹션의 시작 부분을 뷰포트 상단에 맞춤
                });
            }
        });
    });
});