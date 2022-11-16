from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from subscriptions.views import *

urlpatterns = [
    path(
        'plans',
        PlanList.as_view(),
        name='plan-list',
    ),
    path(
        'plans/<int:pk>',
        PlanDetail.as_view(),
        name='plan-detail',
    ),
    path(
        'subscriptions',
        SubList.as_view(),
        name='subscriptions-list',
    ),
    path(
        'subscriptions/<int:pk>',
        SubDetail.as_view(),
        name='subscription-detail',
    ),
    path(
        'payment-methods',
        PaymentMethodList.as_view(),
        name='paymentmethod-list',
    ),
    path(
        'payment-methods/<int:pk>',
        PaymentMethodDetail.as_view(),
        name='paymentmethod-detail',
    ),
    path(
        'upcoming-plans',
        UpComingPlanList.as_view(),
        name='upcomingplan-list',
    ),
    path(
        'upcoming-plans/<int:pk>',
        UpComingPlanDetail.as_view(),
        name='upcomingplan-detail',
    ),
    path(
        'receipts/<int:pk>',
        ReceiptDetail.as_view(),
        name='receipt-detail',
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
