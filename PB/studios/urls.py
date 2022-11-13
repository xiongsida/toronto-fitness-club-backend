from django.urls import path
from studios.views import StudiosListView, StudioDetailView, StudioClassesView

app_name = 'studios'

urlpatterns = [
    path('all/', StudiosListView.as_view()),
    path('<int:studio_id>/details/', StudioDetailView.as_view(), name='details'),
    path('<int:studio_id>/classes/',StudioClassesView.as_view(), name='classes'),
]