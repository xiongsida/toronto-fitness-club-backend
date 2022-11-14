from .models import *
from .serializers import *
from rest_framework import generics, permissions, mixins, exceptions
from accounts.permissions import *
from .utils import *
from .business_logic import *
import datetime


class PlanList(mixins.ListModelMixin,
               generics.GenericAPIView):
    queryset = Plan.objects.filter(is_active=True)
    serializer_class = PlanSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PlanDetail(mixins.RetrieveModelMixin,
                 generics.GenericAPIView):
    queryset = Plan.objects.filter(is_active=True)
    serializer_class = PlanSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class SubList(mixins.CreateModelMixin,
              mixins.ListModelMixin,
              generics.GenericAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        isDebugingOrSecretForGet,
    ]

    def create(self, request, *args, **kwargs):
        if hasattr(request.user, "subscription") and request.user.subscription != None:
            raise exceptions.PermissionDenied(
                detail='You already has subscription, please cancel previous one before adding new.')
        elif not hasattr(request.user, "payment_method") or request.user.payment_method == None:
            raise exceptions.PermissionDenied(
                detail='You don\'t have a payment method yet.')
        else:
            return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        make_subscription(self.request.user,
                          serializer.validated_data.get('plan'))
        return serializer.save(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SubDetail(mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                generics.GenericAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        IsTheUser,
    ]

    # def retrieve(self, request, *args, **kwargs):
    #     rtn = super().retrieve(request, *args, **kwargs)
    #     a = request.user.subscription.subscribed_time.replace(
    #         tzinfo=timezone.ets).replace(tzinfo=None)
    #     print(type(a))
    #     import pytz
    #     b = datetime.datetime.now()
    #     print(a, b)
    #     print(a - b, b - a)
    #     return rtn

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def perform_destroy(self, instance):
        cancel_subscription(self.request.user)
        return super().perform_destroy(instance)

    def delete(self, request, *args, **kwargs):
        if not user_has_x(request.user, "subscription"):
            raise exceptions.PermissionDenied(
                detail='You don\'t have subscription.')
        elif not user_has_x(request.user, "payment_method"):
            raise exceptions.PermissionDenied(
                detail='You don\'t have a payment method for refund, please add one.')
        else:
            return self.destroy(request, *args, **kwargs)


class PaymentMethodList(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        generics.GenericAPIView):
    serializer_class = PaymentMethodSerializer
    queryset = PaymentMethod.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        isDebugingOrSecretForGet,
    ]

    def create(self, request, *args, **kwargs):
        if user_has_x(request.user, 'payment_method'):
            raise exceptions.PermissionDenied(
                detail='You already has payment method, please delete previous one before adding new.')
        else:
            return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        if not is_card_valid(
                serializer.validated_data.get('card_number'),
                serializer.validated_data.get('card_expire'),
                serializer.validated_data.get('security_code'),
        ):
            raise exceptions.PermissionDenied(
                detail='Your payment method is invalid.')
        return serializer.save(user=self.request.user)

    def get(self, request, *args, **kwargs):
        print(datetime.datetime.now())
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PaymentMethodDetail(mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          generics.GenericAPIView):

    serializer_class = PaymentMethodSerializer
    queryset = PaymentMethod.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        IsTheUser,
    ]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        if not is_card_valid(
                serializer.validated_data.get('card_number'),
                serializer.validated_data.get('card_expire'),
                serializer.validated_data.get('security_code'),
        ):
            raise exceptions.PermissionDenied(
                detail='Your payment method is invalid.')

        return super().perform_update(serializer)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        # delete up coming plan when delete payment method
        if user_has_x(self.request.user, 'upcoming_plan'):
            self.request.user.upcoming_plan.delete()
        return super().perform_destroy(instance)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UpComingPlanList(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       generics.GenericAPIView):
    serializer_class = UpComingPlanSerializer
    queryset = UpComingPlan.objects.all()
    permission_classes = [
        isDebugingOrSecretForGet,
        permissions.IsAuthenticated,
        IsTheUser,
    ]

    def create(self, request, *args, **kwargs):
        if user_has_x(request.user, 'upcoming_plan'):
            raise exceptions.PermissionDenied(
                detail='You already has upcoming plan, please cancel previous one before adding new.')
        else:
            return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UpComingPlanDetail(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         generics.GenericAPIView):

    serializer_class = UpComingPlanSerializer
    queryset = UpComingPlan.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        IsTheUser,
    ]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ReceiptDetail(mixins.RetrieveModelMixin,
                    generics.GenericAPIView):

    serializer_class = ReceiptSerializer
    queryset = Receipt.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        IsTheUser,
    ]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
