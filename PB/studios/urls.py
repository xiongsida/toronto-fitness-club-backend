from django.urls import path
from studios.views import StudiosListView, StudioDetailView

app_name = 'studios'

urlpatterns = [
    path('studios', StudiosListView.as_view()),
    path('studios/<int:studio_id>', StudioDetailView.as_view(), name='details'),
]