from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from subscriptions import views

urlpatterns = [
    path('plans/', views.PlanList.as_view(), name='plan_list'),
    path('subscription/', views.SubDetail.as_view(), name='subscription')
]

urlpatterns = format_suffix_patterns(urlpatterns)
