from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView
from django.shortcuts import get_object_or_404
from studios.serializers import StudioSerializer, StudioDetailSerializer
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
        
        if 'user_lat' and 'user_lng' in self.request.query_params:
            origins=[self.request.query_params['user_lat'] + " " + self.request.query_params['user_lng']]
            destinations=["{} {}".format(x.latitude,x.longitude) for x in queryset]
            responses=gmaps.distance_matrix(origins, destinations)
            if responses['status']!='OK':
                return queryset
            responses=responses['rows'][0]['elements']
            distances=[responses[x]['distance']['value'] if 'distance' in responses[x] else float("inf") for x in range(len(responses))]
            
            return [x[0] for x in sorted(zip(queryset,distances),key=lambda x:x[1])]
        return queryset

    
    
class StudioDetailView(RetrieveAPIView):
    serializer_class = StudioDetailSerializer

    def get_object(self):        
        return get_object_or_404(Studio, id=self.kwargs['studio_id'])

class StudioDirectionView(APIView):
    def get(self, request, *args, **kwargs):
        dest_loc=get_object_or_404(Studio, id=self.kwargs['studio_id'])
        if 'user_lat' and 'user_lng' in request.query_params:
            destination='{} {}'.format(dest_loc.latitude,dest_loc.longitude)
            origin='{} {}'.format(request.query_params['user_lat'],request.query_params['user_lng'])
            response=gmaps.directions(origin, destination)
            return Response(response)
        return Response({'detail':'user location required'})
    