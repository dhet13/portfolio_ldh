from django.urls import path
from .views import ProjectListView, project_detail_json

app_name = 'projects'

urlpatterns = [
    path('', ProjectListView.as_view(), name='list'),
    path('<int:pk>/json/', project_detail_json, name='detail_json'),
]