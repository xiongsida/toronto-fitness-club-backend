from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.generics import RetrieveAPIView, ListAPIView
from django.shortcuts import get_object_or_404
from studios.serializers import StudioSerializer, StudioDetailSerializer, ClassInstanceSerializer
from studios.models.studio import Studio
from studios.models.classInstance import ClassInstance
from studios.models.classParent import ClassParent
from accounts.models import TFCUser
from studios.pagination import CustomPagination
from django.db.models import F, Q
from studios.utils import gmaps, get_distance
import datetime
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
    serializer_class = ClassInstanceSerializer
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

        return queryset


class ClassEnrollView(APIView):
    
    def get(self,request, *args, **kwargs):
        if not request.user:
            return Response({'detail':'user not logged in'})
        student=request.user
        # print(student)
        apply_for_future=request.query_params.get('for_future','0')
        studio_id=kwargs.get('studio_id',None)
        class_instance_id=kwargs.get('class_instance_id',None)
        studio=get_object_or_404(Studio, id=studio_id)
        classinstance=get_object_or_404(ClassInstance,id=class_instance_id)
        class_parent_id=classinstance.class_parent.id
        classparent=get_object_or_404(ClassParent,id=class_parent_id)
        
        if classparent.studio.id!=studio.id:
            return Response({'detail':'enroll failed, class and studio is not matched'})
        
        if datetime.datetime.combine(classinstance.date,classinstance.start_time)<=datetime.datetime.now():
            return Response({'detail':'enroll failed, the class you selected was in the past'})
        
        if classinstance.capacity>len(classinstance.students.all()):
            student.class_instances.add(classinstance)
        else:
            return Response({'detail':'enroll failed, this class is full'})
        
        full_classes=[]
        if apply_for_future=='1':
            student.class_parents.add(classparent)
            future_instances=ClassInstance.objects.filter(Q(class_parent__id=class_parent_id) & Q(date__gt=classinstance.date))
            for future_instance in future_instances:
                if future_instance.capacity>len(future_instance.students.all()):
                    student.class_instances.add(future_instance)
                else:
                    full_classes.append(future_instance.id)
                
        return Response({'detail':'enroll success'}) if not full_classes else Response({'detail':'enroll success partially','already full before':full_classes})

class ClassDropView(APIView):
    
    def get(self,request, *args, **kwargs):
        if not request.user:
            return Response({'detail':'user not logged in'})
        student=request.user
        apply_for_future=request.query_params.get('for_future','0')
        studio_id=kwargs.get('studio_id',None)
        class_instance_id=kwargs.get('class_instance_id',None)
        
        studio=get_object_or_404(Studio, id=studio_id)
        classinstance=get_object_or_404(ClassInstance,id=class_instance_id)
        class_parent_id=classinstance.class_parent.id
        classparent=get_object_or_404(ClassParent,id=class_parent_id)
        
        if classparent.studio.id!=studio.id:
            return Response({'detail':'drop failed, class and studio is not matched'})
        
        if datetime.datetime.combine(classinstance.date,classinstance.start_time)<=datetime.datetime.now():
            return Response({'detail':'drop not allowed, the class you selected was in the past'})
        
        student.class_instances.remove(classinstance)
        
        if apply_for_future=='1':
            student.class_parents.remove(classparent)
            future_instances=ClassInstance.objects.filter(Q(class_parent__id=class_parent_id) & Q(date__gt=classinstance.date))
            for future_instance in future_instances:
                student.class_instances.remove(future_instance)
                
        return Response({'detail':'drop success, or you do not have specified classes to drop at the first place'})
        

class UserClassScheduleView(ListAPIView):
    serializer_class = ClassInstanceSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        student=get_object_or_404(TFCUser, id=self.kwargs['user_id'])
        # print(student)
        q=Q(date__gt=datetime.date.today()) | (Q(date=datetime.date.today())&Q(start_time__gte=datetime.datetime.now().time()))
        queryset=student.class_instances.filter(q).order_by('date','start_time','end_time')
        return queryset


class UserClasseHistoryView(ListAPIView):
    serializer_class = ClassInstanceSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        student=get_object_or_404(TFCUser, id=self.kwargs['user_id'])
        q=Q(date__lt=datetime.date.today()) | (Q(date=datetime.date.today())&Q(start_time__lte=datetime.datetime.now().time()))
        queryset=student.class_instances.filter(q).order_by('date','start_time','end_time')
        return queryset
    