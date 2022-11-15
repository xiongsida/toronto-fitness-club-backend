from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import RetrieveAPIView, ListAPIView
from django.shortcuts import get_object_or_404
from studios.serializers import StudioSerializer, StudioDetailSerializer
from studios.models.studio import Studio
from studios.pagination import CustomPagination
from django.db.models import F
from studios.utils import get_distance

    
# Create your views here.
class StudiosListView(ListAPIView):
    serializer_class = StudioSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name','amenities__type','classes__name','classes__coach']
    search_fields = ['name','amenities__type','classes__name','classes__coach']

    def get_queryset(self):
        queryset = Studio.objects.all().order_by("id")
        if 'user_lat' and 'user_lng' in self.request.query_params:
            origin=(float(self.request.query_params['user_lat']),float(self.request.query_params['user_lng']))
            queryset=Studio.objects.annotate(distance=get_distance(origin,(F('latitude'),F('longitude')))).order_by('distance')
            # should return queryset instead of list in order to make filter work, really tricky to get queryset ordered
            return queryset
        return queryset

    
class StudioDetailView(RetrieveAPIView):
    serializer_class = StudioDetailSerializer

    def get_object(self):        
        return get_object_or_404(Studio, id=self.kwargs['studio_id'])

    
