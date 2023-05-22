#urls.py code:
from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',views.home,name='home'),
    path('result/',views.result,name='result'),
    path('home',views.Index,name='Index'),
    path('face-mask-detection',views.MaskDetection,name='face-mask-detection'),
    # path('attandance_first',views.AttandancePage,name='attandance_first'),
    path('attandance',views.AttendanceUrl,name='attandance'),
    path('video_stream', views.video_stream, name='video_stream'),

    path('',views.HomePage,name='HomePage'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('register',views.register,name='register'),
    path('students/add-couse-details',views.AddCourseDetails,name='students/add-couse-details'),
    
    # Teachers 
    path('teacher',views.TeacherDashboard,name='teacher'),
    path('teacher/attandance_first',views.AttendancePageTeacher,name='AttandancePage'),
    path('teacher/attendace/start',views.AttendanceStartTeacher,name='teacher/attendace/start'),

    # Students 
    path('students',views.StudentDashboard,name='students'),
    path('student/attandance_first',views.AttendancePageStudent,name='AttandancePage'),
    path('student/attendace/requests',views.AttendanceRequests,name='/student/attendace/requests'),
    path('student/attendace/start',views.AttendanceStartStudent,name='student/attendace/start'),
    path('student/marks-grading',views.MarksGreding,name='marksgreding'),
    path('driver/dashboard', views.driver_dash, name='driver/dashboard'),
    path('student/select-bus', views.select_bus, name='select_bus'),
    path('driver/location-success', views.location_selected, name='location_selected'),

    

]