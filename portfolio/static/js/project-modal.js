document.addEventListener('DOMContentLoaded', function(){
    // 모달 관련 요소
    const modal = document.getElementById('projectDetailModal');
    const modalClose = document.querySelector('.modal-close');
    const modalOverlay = document.querySelector('.modal-overlay');

    // 모달 내부 콘텐츠 요소
    const modalTitle = document.getElementById('modal-title');
    const modalCompany = document.getElementById('modal-company');
    const modalPeriod = document.getElementById('modal-period');
    const modalDescription = document.getElementById('modal-description');

    // 섹션들
    const imagesSection = document.getElementById('modal-images-section');
    const filesSection = document.getElementById('modal-files-section');

    // 동적 콘텐츠 컨테이너
    const modalImages = document.getElementById('modal-images');
    const modalFiles = document.getElementById('modal-files');
    const iframeTabs = document.getElementById('iframe-tabs');
    const linksIframe = document.getElementById('modal-links-iframe');
    const openInNewTab = document.getElementById('open-in-new-tab');

    // 모달 열기 함수
    function openModal(projectId) {
        console.log(`프로젝트 ${projectId} 모달 열기`);

        // 모달 표시
        modal.style.display = 'flex';

        // AJAX로 데이터 가져오기
        fetch(`/projects/${projectId}/json/`)
            .then(response => response.json())
            .then(data => {
                console.log('프로젝트 데이터:', data);
                populateModal(data);
            })
            .catch(error => {
                console.error('데이터 로딩 실패:', error);
                alert('프로젝트 정보를 불러올 수 없습니다.');
                closeModal();
            });
    }

    // 모달 닫기 함수
    function closeModal() {
        modal.style.display = 'none';

        // iframe src 초기화(리소스 절약)
        linksIframe.src = '';
        console.log('모달 닫기');
    }

    function populateModal(data) {
        modalTitle.textContent = data.title;
        modalCompany.textContent = data.company;
        modalPeriod.textContent = data.period;
        modalDescription.innerHTML = data.description; // 마크다운 HTML 지원

        modalImages.innerHTML = ''; // 기존 내용 초기화

        if (data.images && data.images.length > 0) {
            //이미지가 있으면
            data.images.forEach(img => {
                const imgElement = document.createElement('img');
                imgElement.src = img.url;
                imgElement.alt = img.caption;
                modalImages.appendChild(imgElement);
            });
            imagesSection.style.display = 'block'; // 섹션 표시
        } else {
            // 이미지가 없으면
            imagesSection.style.display = 'none'; // 섹션 숨김
        }

        modalFiles.innerHTML = ''; //초기화

        if (data.files && data.files.length > 0) {
            const ul = document.createElement('ul');
            data.files.forEach(file => {
                const li = document.createElement('li');
                const a = document.createElement('a');
                a.href = file.url;
                a.textContent = file.name;
                a.download = file.name; // 다운로드 속성
                li.appendChild(a);
                ul.appendChild(li);
            });
            modalFiles.appendChild(ul);
            filesSection.style.display = 'block';
        } else {
            filesSection.style.display = 'none';
        }

        iframeTabs.innerHTML = ''; // 기존 탭 제거
        let isFirstTab = true;

        //URL이 있으면 탭 생성
        if (data.figma_url) {
            const btn = document.createElement('button');
            btn.textContent = 'Figma';
            btn.classList.add('iframe-tab');
            if (isFirstTab) {
             btn.classList.add('actitve');
             linksIframe.src = data.figma_url; // 첫 탭은 기본 로드
             isFirstTab = false;
            }
            btn.addEventListener('click', () => {
                linksIframe.src = data.figma_url;
                document.querySelectorAll('.iframe-tab').forEach (t => t.classList.remove('acitve'));
            });
            iframeTabs.appendChild(btn);
        }
        if (data.github_url) {
            const btn = document.createElement('button');
            btn.textContent = 'GitHub';
            btn.classList.add('iframe-tab');
            if (isFirstTab) {
             btn.classList.add('actitve');
             linksIframe.src = data.github_url; // 첫 탭은 기본 로드
             isFirstTab = false;
            }
            btn.addEventListener('click', () => {
                linksIframe.src = data.github_url;
                document.querySelectorAll('.iframe-tab').forEach (t => t.classList.remove('acitve'));
            });
            iframeTabs.appendChild(btn);
        }
        if (data.demo_url) {
            const btn = document.createElement('button');
            btn.textContent = 'Demo';
            btn.classList.add('iframe-tab');
            if (isFirstTab) {
             btn.classList.add('actitve');
             linksIframe.src = data.demo_url; // 첫 탭은 기본 로드
             isFirstTab = false;
            }
            btn.addEventListener('click', () => {
                linksIframe.src = data.demo_url;
                document.querySelectorAll('.iframe-tab').forEach (t => t.classList.remove('acitve'));
            });
            iframeTabs.appendChild(btn);
        }
        // 탭이 하나도 없으면 iframe 섹션 전체 숨김
        if (!isFirstTab) {
            // 탭이 하나라도 생성됨 (isFirtsTab이 Fasle로 바뀜)
            document.getElementById('iframe-section').style.display = 'block';
        } else {
            //탭이 하나도 없음
            document.getElementById('iframe-section').style.display = 'none';
            linksIframe.src = ''; //iframe도 비우기
        }
    }

    // 이벤트 리스너 등록, 모든 상세보기 버튼에 이벤트 리스너 추가
    const detailButtons = document.querySelectorAll('.project-detail-btn');
    detailButtons.forEach(button => {
        button.addEventListener('click', function() {
            const projectId = this.getAttribute('data-project-id');
            openModal(projectId);
        });
    });

    // 닫기 버튼 이벤트
    modalClose.addEventListener('click', closeModal);

    // 오버레이 클릭 시 닫기
    modalOverlay.addEventListener('click', function(e) {
        if (e.target === modalOverlay) {
            closeModal();
        }
    });

    // ESC 키로 닫기
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.style.display === 'flex') {
            closeModal();
        }
    });

    console.log('프로젝트 모달 스크립트 로드됨');
});

