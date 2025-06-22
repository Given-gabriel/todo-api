from django.shortcuts import render
from .models import Task
from .serializers import TaskSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime,timedelta
from django.utils.timezone import make_aware
from rest_framework.permissions import AllowAny
import pytz

class TaskListCreate(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        filter_type = self.request.query_params.get('filter')
        category = self.request.query_params.get('category')
        tz_name = self.request.query_params.get('timezone', 'UTC')
        try:
            user_tz = pytz.timezone(tz_name)
        except Exception:
            user_tz = pytz.UTC

        now = datetime.now(user_tz)
        today_start = user_tz.localize(datetime(now.year, now.month, now.day, 0, 0)).astimezone(pytz.UTC)
        today_end = today_start +timedelta(days=1)

        if filter_type == 'today':
            return queryset.filter(start_time__gte=today_start, start_time__lt=today_end)
        elif filter_type == 'upcoming':
            return queryset.filter(start_time__gte=today_end)
        elif filter_type == 'past':
            return queryset.filter(end_time__lt = today_start)
        
        #apply category filter if provided
        if category:
            return queryset.filter(category__iexact = category)

        return queryset #default: all tasks

    def delete(self, *args, **kwargs):
        Task.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TaskRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'pk'


class TasksByDate(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        date_str = request.query_params.get('date')

        if not date_str:
            return Response({"error:" "Provide a date in YYYY-MM-DD format."}, status=400)
        
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            start = make_aware(datetime.combine(date_obj, datetime.min.time()))
            end = make_aware(datetime.combine(date_obj,datetime.max.time()))
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)
        
        tasks = Task.objects.filter(start_time__gte=start, start_time__lte=end)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=200)