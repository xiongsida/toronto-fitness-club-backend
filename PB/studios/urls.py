from django.urls import path
from studios.views import StudiosListView, StudioDetailView, StudioClassesView, ClassEnrollView, ClassDropView

app_name = 'studios'

urlpatterns = [
    path('all/', StudiosListView.as_view()),
    path('<int:studio_id>/details/', StudioDetailView.as_view(), name='details'),
    path('<int:studio_id>/classes/',StudioClassesView.as_view(), name='classes'),
    path('<int:studio_id>/classes/<int:class_instance_id>/enroll/', ClassEnrollView.as_view(), name='class-enroll'),
    path('<int:studio_id>/classes/<int:class_instance_id>/drop/', ClassDropView.as_view(), name='class-drop'),
]