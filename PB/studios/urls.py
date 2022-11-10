from django.urls import path
from studios.views import StudiosListView, StudioDetailView, StudioDirectionView

urlpatterns = [
    path('all/', StudiosListView.as_view()),
    path('<int:studio_id>/details/', StudioDetailView.as_view()),
    path('<int:studio_id>/direction/',StudioDirectionView.as_view()),
]