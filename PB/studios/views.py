from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView
from django.shortcuts import get_object_or_404
from studios.serializers import StudioSerializer
from studios.models.studio import Studio
from studios.pagination import CustomPagination
from django.db.models import F
from studios.utils import gmaps
    
# Create your views here.
class StudiosListView(ListAPIView):
    serializer_class = StudioSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Studio.objects.all().order_by("id")
        if 'user_lat' and 'user_long' in self.request.query_params:
            origins=[self.request.query_params['user_lat'] + " " + self.request.query_params['user_long']]
            destinations=["{} {}".format(x.latitude,x.longitude) for x in queryset]
            responses=gmaps.distance_matrix(origins, destinations)
            if responses['status']!='OK':
                return queryset
            responses=responses['rows'][0]['elements']
            distances=[responses[x]['distance']['value'] if 'distance' in responses[x] else float("inf") for x in range(len(responses))]
            
            return [x[0] for x in sorted(zip(queryset,distances),key=lambda x:x[1])]
        return queryset

    
    
class StudioDetailView(RetrieveAPIView):
    serializer_class = StudioSerializer

    def get_object(self):
        
        # loc=self.request.query_params.get("loc",None)
        
        return get_object_or_404(Studio, id=self.kwargs['studio_id'])

# class StudioDerectionView(APIView):
    