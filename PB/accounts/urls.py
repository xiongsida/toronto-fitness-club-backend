from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from accounts import views
from studios.views import UserClassScheduleView, UserClasseHistoryView
urlpatterns = [
    path('users/', views.UserList.as_view(), name='tfcuser-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='tfcuser-detail'),
    path('users/<int:user_id>/classes/schedule/',
         UserClassScheduleView.as_view(), name='user-classes-schedule'),
    path('users/<int:user_id>/classes/history/',
         UserClasseHistoryView.as_view(), name='user-classes-history'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
