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

    // 1. 이미지 갤러리 처리 (data.images)
    modalImages.innerHTML = ''; // 기존 내용 초기화
    if (data.images && data.images.length > 0) {
        data.images.forEach(img => {
            const imgElement = document.createElement('img');
            imgElement.src = img.url;
            imgElement.alt = img.caption || data.title;
            modalImages.appendChild(imgElement);
        });
        imagesSection.style.display = 'block'; // 섹션 표시
    } else {
        imagesSection.style.display = 'none'; // 섹션 숨김
    }

    // 2. 첨부 파일 처리 (data.files) - 미리보기 기능 포함
    modalFiles.innerHTML = ''; //초기화
    if (data.files && data.files.length > 0) {
        data.files.forEach(file => {
            const fileContainer = document.createElement('div');
            fileContainer.classList.add('file-item');

            const fileTitle = document.createElement('h6');
            fileTitle.textContent = file.title || file.name;
            fileContainer.appendChild(fileTitle);

            if (file.type.startsWith('image/')) {
                const img = document.createElement('img');
                img.src = file.url;
                img.alt = file.title;
                img.style.maxWidth = '100%';
                img.style.height = 'auto';
                img.style.marginBottom = '10px';
                fileContainer.appendChild(img);
            } else if (file.type === 'application/pdf') {
                const iframe = document.createElement('iframe');
                iframe.src = file.url;
                iframe.classList.add('pdf-preview');
                fileContainer.appendChild(iframe);
            }

            const downloadLink = document.createElement('a');
            downloadLink.href = file.url;
            downloadLink.textContent = `다운로드: ${file.name}`; // 구문 오류 수정
            downloadLink.download = file.name;
            fileContainer.appendChild(downloadLink);

            modalFiles.appendChild(fileContainer);
        });
        filesSection.style.display = 'block';
    } else {
        filesSection.style.display = 'none';
    }

    // 3. 외부 링크 탭 처리 (Figma, GitHub, Demo)
    iframeTabs.innerHTML = ''; // 기존 탭 제거
    let isFirstTab = true;

    const createTab = (url, text) => {
        if (!url) return;
        const btn = document.createElement('button');
        btn.textContent = text;
        btn.classList.add('iframe-tab');
        if (isFirstTab) {
            btn.classList.add('active');
            linksIframe.src = url;
            isFirstTab = false;
        }
        btn.addEventListener('click', () => {
            linksIframe.src = url;
            document.querySelectorAll('.iframe-tab').forEach(t => t.classList.remove('active'));
            btn.classList.add('active');
        });
        iframeTabs.appendChild(btn);
    };

    createTab(data.figma_url, 'Figma');
    createTab(data.github_url, 'GitHub');
    createTab(data.demo_url, 'Demo');
    
    // 탭 유무에 따라 iframe 섹션 표시/숨김
    if (!isFirstTab) {
        document.getElementById('iframe-section').style.display = 'block';
    } else {
        document.getElementById('iframe-section').style.display = 'none';
        linksIframe.src = '';
    }
}

    // 이벤트 리스너 등록, 모든 상세보기 버튼에 이벤트 리스너 추가
    const detailButtons = document.querySelectorAll('.project-detail-btn');
    detailButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation(); // 이벤트 버블링 방지
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

