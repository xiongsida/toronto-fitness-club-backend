from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from studios.models.studio import Studio
from classes.models.classInstance import ClassInstance
from classes.models.classParent import ClassParent
from classes.serializers import ClassInstanceSerializer
from accounts.models import TFCUser
from studios.pagination import CustomPagination
from classes.filter import ClassInstanceFilter
from django.db.models import Q
import datetime

# Create your views here.

class ClassesListView(ListAPIView):
    serializer_class = ClassInstanceSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ClassInstanceFilter
    search_fields = ['class_parent__name','coach','date','start_time','end_time']
    
    def get_queryset(self):
        studio_id=self.request.GET.get('studio_id',None)
        if studio_id:
            studio=get_object_or_404(Studio, id=studio_id)
            classParents=studio.classes.all()
            classParent_ids=[x.id for x in classParents]
            q1=Q(class_parent__id__in=classParent_ids)
            q2=Q(is_cancelled=False)
            q3=Q(date__gt=datetime.date.today()) | (Q(date=datetime.date.today())&Q(start_time__gte=datetime.datetime.now().time()))
            queryset=ClassInstance.objects.filter(q1 & q2 & q3).order_by('date','start_time','end_time')
            return queryset
        elif self.request.user: # if not studio_id is specified, we think the user want to see his own classes
            student=self.request.user
            scope=self.request.GET.get('scope',None)
            queryset=student.class_instances.all().order_by('date','start_time','end_time')
            if scope=="myschedule":
                q11=Q(is_cancelled=False)
                q22=Q(date__gt=datetime.date.today()) | (Q(date=datetime.date.today())&Q(start_time__gte=datetime.datetime.now().time()))
                queryset=queryset.filter(q11 & q22).order_by('date','start_time','end_time')
            elif scope=="myhistory":
                q33=Q(date__lt=datetime.date.today()) | (Q(date=datetime.date.today())&Q(start_time__lte=datetime.datetime.now().time()))
                queryset=queryset.filter(q33).order_by('date','start_time','end_time')
            return queryset
        else:
            return ClassInstance.objects.all().order_by('date','start_time','end_time')


class ClassEnrollView(APIView):

    def post(self,request, *args, **kwargs):
        if not request.user:
            return Response({'detail':'user not logged in'})
        student=request.user
        apply_for_future=request.data.get('for_future',0)
        class_instance_id=kwargs.get('class_id',None)
        classinstance=get_object_or_404(ClassInstance,id=class_instance_id)
        class_parent_id=classinstance.class_parent.id
        classparent=get_object_or_404(ClassParent,id=class_parent_id)
        
        if datetime.datetime.combine(classinstance.date,classinstance.start_time)<=datetime.datetime.now():
            return Response({'detail':'enroll failed, the class you selected was in the past'})
        # print(classinstance.capacity)
        if classinstance.capacity>len(classinstance.students.all()):
            student.class_instances.add(classinstance)
        else:
            return Response({'detail':'enroll failed, this class is full'})
        
        if classinstance.is_cancelled==False:
            student.class_instances.add(classinstance)
        else:
            return Response({'detail':'enroll failed, this class is cancelled'})
        
        invalid_classes=[]
        if apply_for_future==1:
            student.class_parents.add(classparent)
            future_instances=ClassInstance.objects.filter(Q(class_parent__id=class_parent_id) & Q(date__gt=classinstance.date))
            for future_instance in future_instances:
                if future_instance.capacity>len(future_instance.students.all()) and (not future_instance.is_cancelled):
                    student.class_instances.add(future_instance)
                else:
                    invalid_classes.append(future_instance.id)
                
        return Response({'detail':'enroll success'}) if not invalid_classes else Response({'detail':'enroll success partially','already full or cancelled before':invalid_classes})

class ClassDropView(APIView):
    
    def post(self,request, *args, **kwargs):
        if not request.user:
            return Response({'detail':'user not logged in'})
        student=request.user
        apply_for_future=request.data.get('for_future',0)
        class_instance_id=kwargs.get('class_id',None)
        
        classinstance=get_object_or_404(ClassInstance,id=class_instance_id)
        class_parent_id=classinstance.class_parent.id
        classparent=get_object_or_404(ClassParent,id=class_parent_id)
        
        if datetime.datetime.combine(classinstance.date,classinstance.start_time)<=datetime.datetime.now():
            return Response({'detail':'drop not allowed, the class you selected was in the past'})
        
        student.class_instances.remove(classinstance)
        
        if apply_for_future==1:
            student.class_parents.remove(classparent)
            future_instances=ClassInstance.objects.filter(Q(class_parent__id=class_parent_id) & Q(date__gt=classinstance.date))
            for future_instance in future_instances:
                student.class_instances.remove(future_instance)
                
        return Response({'detail':'drop success, or you do not have specified classes to drop at the first place'})
        