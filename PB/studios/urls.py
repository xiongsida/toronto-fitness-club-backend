from django.urls import re_path
from studios.views import StudiosListView, StudioDetailView

app_name = 'studios'

urlpatterns = [
    re_path(r'^studios/?$', StudiosListView.as_view()),
    re_path(r'^studios/<int:studio_id>/?$', StudioDetailView.as_view(), name='details'),
]