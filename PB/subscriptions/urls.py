from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import re_path
from subscriptions.views import *

urlpatterns = [
    re_path(
        r'^plans/?$',
        PlanList.as_view(),
        name='plan-list',
    ),
    re_path(
        r'^plans/<int:pk>/?$',
        PlanDetail.as_view(),
        name='plan-detail',
    ),
    re_path(
        r'^subscriptions/?$',
        SubList.as_view(),
        name='subscriptions-list',
    ),
    re_path(
        r'^subscriptions/<int:pk>/?$',
        SubDetail.as_view(),
        name='subscription-detail',
    ),
    re_path(
        r'^payment-methods/?$',
        PaymentMethodList.as_view(),
        name='paymentmethod-list',
    ),
    re_path(
        r'^payment-methods/<int:pk>/?$',
        PaymentMethodDetail.as_view(),
        name='paymentmethod-detail',
    ),
    re_path(
        r'^upcoming-plans/?$',
        UpComingPlanList.as_view(),
        name='upcomingplan-list',
    ),
    re_path(
        r'^upcoming-plans/<int:pk>/?$',
        UpComingPlanDetail.as_view(),
        name='upcomingplan-detail',
    ),
    re_path(
        r'^receipts/<int:pk>/?$',
        ReceiptDetail.as_view(),
        name='receipt-detail',
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
