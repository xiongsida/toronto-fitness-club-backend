from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView
from django.shortcuts import get_object_or_404
from studios.serializers import StudioSerializer, StudioDetailSerializer, StudioClassesSerializer
from studios.models.studio import Studio
from studios.models.classInstance import ClassInstance
from studios.pagination import CustomPagination
from django.db.models import F, Q
from studios.utils import gmaps, get_distance
import datetime
import bisect
# from django.db.models.functions import datetime
    
# Create your views here.
class StudiosListView(ListAPIView):
    serializer_class = StudioSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter] # works on queryset
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

    
class StudioClassesView(ListAPIView):
    serializer_class = StudioClassesSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['coach','class_parent__name','date']

    def get_queryset(self):
        studio=get_object_or_404(Studio, id=self.kwargs['studio_id'])
        classParents=studio.classes.all()
        classParent_ids=[x.id for x in classParents]
        q1=Q(class_parent__id__in=classParent_ids)
        q2=Q(is_cancelled=False)
        q3=Q(date__gt=datetime.date.today()) | (Q(date=datetime.date.today())&Q(start_time__gte=datetime.datetime.now().time()))
        queryset=ClassInstance.objects.filter(q1 & q2 & q3).order_by('date','start_time','end_time')
        # for classParent in classParents:
        #     for classInstance in classParent.class_instances.all():
        #         if (not classInstance.is_cancelled) \
        #             and datetime.datetime.combine(classInstance.date,classInstance.start_time) >= datetime.datetime.now():
        #             bisect.insort(queryset,classInstance,key=lambda x:(x.date,x.start_time,x.end_time))
        return queryset

