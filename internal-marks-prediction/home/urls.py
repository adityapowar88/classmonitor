from django.contrib import admin
import home
from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('result/',views.result,name='result'),
    path('home',views.Index,name='Index'),
    path('face-mask-detection',views.MaskDetection,name='face-mask-detection'),
    path('attandance_first',views.AttandancePage,name='attandance_first'),
    path('attandance',views.AttendanceUrl,name='attandance'),
    path('video_stream', views.video_stream, name='video_stream'),
    path('student/select-bus', views.select_bus, name='select_bus'),
]
