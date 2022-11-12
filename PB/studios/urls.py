from django.urls import path
from studios.views import StudiosListView, StudioDetailView, StudioDirectionView, StudioClassesView

urlpatterns = [
    path('all/', StudiosListView.as_view()),
    path('<int:studio_id>/details/', StudioDetailView.as_view()),
    path('<int:studio_id>/direction/',StudioDirectionView.as_view()),
    path('<int:studio_id>/classes/',StudioClassesView.as_view()),
]