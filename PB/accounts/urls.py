from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from accounts import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('users/', views.UserList.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
