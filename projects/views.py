from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Prefetch
from .models import Project, ProjectImage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import markdown
from django.utils.safestring import mark_safe
import requests
import re
import base64

def fetch_github_readme(github_url):
    """
    GitHub URL에서 README 파일을 가져와 HTML로 변환
    지원 형식: https://github.com/username/repo
    """
    if not github_url:
        return None

    # GitHub URL에서 owner/repo 추출
    pattern = r'github\.com/([^/]+)/([^/]+)'
    match = re.search(pattern, github_url)

    if not match:
        return None

    owner, repo = match.groups()
    # URL 끝의 .git 제거
    repo = repo.replace('.git', '')

    # GitHub API로 README 가져오기
    api_url = f'https://api.github.com/repos/{owner}/{repo}/readme'

    try:
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            # Base64 디코딩
            readme_content = base64.b64decode(data['content']).decode('utf-8')
            # Markdown을 HTML로 변환
            readme_html = markdown.markdown(
                readme_content,
                extensions=['fenced_code', 'tables', 'nl2br', 'codehilite']
            )
            return readme_html
    except Exception as e:
        print(f"GitHub README fetch error: {e}")

    return None

# Create your views here.
class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects' #템플릿에서 {{ projects }} 사용

    def get_queryset(self):
        # N+1 문제 방지를 위한 쿼리 최적화
        # company는 ForeignKey이므로 selected_related로 조인
        # images는 역참조이므로 prefetch_related 사용
        # 썸네일 이미지만 먼저 가져오도록 Prefectch 객체 사용
        thumbnail_images = Prefetch(
            'images',
            queryset=ProjectImage.objects.filter(is_thumbnail=True),
            to_attr='thumbnail_list'
        )

        return Project.objects.select_related('company').prefetch_related(
            thumbnail_images,
            'images' #전체 이미지도 필요한 경우 대비
        )
    
def project_detail_json(request, pk):
    # 프로젝트 객체 조회 (없으면 404)
    project = get_object_or_404(Project.objects.prefetch_related('images', 'files'), pk=pk)

    # 기간 계산
    period = f"{project.start_date.strftime('%Y.%m')} - "
    period += project.end_date.strftime('%Y.%m') if project.end_date else "진행중"

    # 이미지 리스트 생성
    images = [
        {'url': img.image.url, 'order': img.order}
        for img in project.images.all() if img.image
    ]

    # 파일 리스트 생성
    files = [
        {
            'url': f.file.url,
            'name': f.original_filename,
            'type': f.file_type,
            'title': f.title
        }
        for f in project.files.all() if f.file
    ]

    # Markdown을 HTML로 변환 (nl2br: 줄바꿈을 <br> 태그로 변환)
    description_html = mark_safe(markdown.markdown(
        project.description,
        extensions=['fenced_code', 'tables', 'nl2br']
    ))

    # GitHub README 가져오기
    readme_html = None
    if project.github_url:
        readme_html = fetch_github_readme(project.github_url)

    # Demo URL iframe 지원 여부 확인
    iframe_supported = True
    if project.demo_url:
        try:
            response = requests.head(project.demo_url, timeout=3)
            x_frame_options = response.headers.get('X-Frame-Options', '').upper()
            if x_frame_options in ['DENY', 'SAMEORIGIN']:
                iframe_supported = False
        except:
            # 요청 실패시 일단 true로 (프론트에서 onerror로 처리)
            iframe_supported = True

    #응답 데이터 구성
    data = {
        'title': project.title,
        'description': description_html,
        'company': project.company.company if project.company else '개인/기타',
        'period': period,
        'demo_url': project.demo_url or '',
        'github_url': project.github_url or '',
        'figma_url': project.figma_url or '',
        'readme_html': readme_html,
        'iframe_supported': iframe_supported,
        'images': images,
        'files': files,
    }

    # JSON 응답 변환
    return JsonResponse(data)