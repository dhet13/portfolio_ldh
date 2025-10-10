from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Prefetch
from .models import Project, ProjectImage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

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

    #응답 데이터 구성
    data = {
        'title': project.title,
        'description': project.description,
        'company': project.company.company,
        'period': period,
        'demo_url': project.demo_url or '',
        'github_url': project.github_url or '',
        'figma_url': project.figma_url or '',
        'images': images,
        'files': files,
    }

    # JSON 응답 변환
    return JsonResponse(data)