from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import re_path
from accounts import views
urlpatterns = [
    re_path(r'^users/?$', views.UserList.as_view(), name='tfcuser-list'),
    re_path(r'^users/<int:pk>/?$', views.UserDetail.as_view(),
            name='tfcuser-detail'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
