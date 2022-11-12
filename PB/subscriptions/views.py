from .models import Plan
from .serializers import PlanSerializer
from rest_framework import generics, permissions, mixins
from accounts.permissions import IsSelfOrReadOnly


class PlanList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    queryset = Plan.objects.filter(is_active=True)
    serializer_class = PlanSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SubDetail(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                generics.GenericAPIView):

    serializer_class = TFCUserSerializer
    queryset = TFCUser.objects.all()
    permission_classes = [
        # permissions.IsAuthenticated(),
        IsSelfOrReadOnly,
    ]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
