from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView
from django.shortcuts import get_object_or_404
from studios.serializers import StudioSerializer
from studios.models.studio import Studio
from studios.pagination import CustomPagination

# Create your views here.
class StudiosListView(ListAPIView):
    serializer_class = StudioSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Studio.objects.all()
    
class StudioDetailView(RetrieveAPIView):
    serializer_class = StudioSerializer

    def get_object(self):
        
        # loc=self.request.query_params.get("loc",None)
        
        return get_object_or_404(Studio, id=self.kwargs['studio_id'])