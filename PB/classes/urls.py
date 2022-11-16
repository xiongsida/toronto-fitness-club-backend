app_name = 'classes'
from django.urls import re_path
from classes.views import ClassesListView, ClassEnrollView, ClassDropView

urlpatterns = [
    re_path(r'^classes/?$', ClassesListView.as_view(), name='classes-list'),
    re_path(r'^classes/<int:class_id>/enroll/?$', ClassEnrollView.as_view(), name='class-enroll'),
    re_path(r'^classes/<int:class_id>/drop/?$', ClassDropView.as_view(), name='class-drop'),
]
