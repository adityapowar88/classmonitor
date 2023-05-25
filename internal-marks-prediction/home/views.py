from email import message
from lib2to3.pgen2.token import AT
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
import joblib
from django.http.response import StreamingHttpResponse
from .camera import VideoCamera
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from home.models import *
from django.contrib.auth import login as auth_login
import pandas as pd
import cv2
from django.contrib import messages
from datetime import datetime


def Index(request):
    return render(request, 'index.html')


def HomePage(request):
    if request.user.is_authenticated:
        print(user_type.objects.get(user=request.user))
        if user_type.objects.get(user=request.user).is_teacher == True:
            return redirect('/teacher')
        
        elif user_type.objects.get(user=request.user).is_driver == True:
            return redirect('/driver/dashboard')
        
        elif request.user.is_authenticated:
            return redirect('/students')
    else:
        return redirect('/login')

url_list = []

def login(request):
    page_data = {}
    page_data['page_name'] = "auth/login.html"
    page_data['title'] = "Login"
    if request.POST:
        loginusername = request.POST['username']
        loginpassword = request.POST['password']
        try:
            user = User.objects.get(username=loginusername)
            if user is not None:
                auth_login(request, user)
                return redirect('/')
            else:
                page_data['error'] = 'Invalid credentials! Please try again'
        except:
            page_data['error'] = "Account Not Found.."

    # page_data['page_name'] = "auth/login.html"
    return render(request, 'auth/login.html', {'page_data': page_data})

def logout(request):
    auth.logout(request)
    return redirect('/login')

def register(request):
    page_data = {}
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        mobile = request.POST['phone']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                page_data['error'] = 'Username Taken'
                # return redirect('register')

            elif User.objects.filter(email=email).exists():
                page_data['error'] = 'email Taken'
                # return redirect('register')

            else:
                user = User.objects.create_user(
                    first_name=first_name, last_name=last_name, username=username,  email=email, password=password1)
                user.save()

                new_student = Student(first_name=first_name, last_name=last_name, user=user,mobile=mobile, email=email)

                user_type(user=user, is_student=True).save()
                new_student.save()
                messages.info(
                    request, 'Successfully registered, Please enter course details')
                return redirect('students/add-couse-details')
                # return redirect('login')

        else:
            page_data['error'] = 'password not maching'
            # return redirect('register')

    return render(request, 'auth/register.html', {'page_data': page_data})


def AddCourseDetails(request):
    if request.POST or request.FILES:
        year = int(request.POST['year'])
        department = int(request.POST['department'])
        div = int(request.POST['division'])
        roll_no = request.POST['roll_no']
        image_path = request.FILES.get("src")
        user_name = request.POST['username']

        if year == 1:
            year = 'First Year'
        elif year == 2:
            year = 'Second Year'
        elif year == 3:
            year = 'Third Year'
        elif year == 4:
            year = 'Last Year'

        if department == 1:
            department = 'ENTC'
        if department == 2:
            department = 'CO'
        if department == 3:
            department = 'ETRC'
        if department == 4:
            department = 'ME'
        if department == 5:
            department = 'Civil'

        if div == 1:
            div = 'A'
        elif div == 2:
            div = 'B'

        if User.objects.filter(username=user_name).exists():
            user_name = User.objects.get(username=user_name)
            update_stud = Student.objects.get(user=user_name)
            update_stud.year = year
            update_stud.department = department
            update_stud.div = div
            update_stud.roll_no = roll_no
            update_stud.photo = image_path
            update_stud.save()
            messages.success(
                request, 'Successfully profile created, Please login')
            return redirect('login')

        messages.error(request, 'User not found, Please Try Again.')
    return render(request, 'home/students/add_couse_details.html')


def home(request):
    return render(request, 'home.html', {'is_result': is_result})


def MaskDetection(request):
    return render(request, 'face-mask.html')


def getPred(cie1, cie2, cie3, presenty, behaviour):
    lr = joblib.load(open('marks2.sav', 'rb'))
    prediction = round(lr.predict([[cie1, cie2,cie3, presenty, behaviour]])[0], 2)

    if prediction > 30:
        return 30
    else:
        return prediction


def result(request):
    return render(request, 'result.html', {'result': result})


def AttendanceUrl(request):
    return render(request, 'attendance.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_stream(request):
    return StreamingHttpResponse(gen(VideoCamera()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

# Student View


def StudentDashboard(request):
    return render(request, 'home/students/students_dash.html')


def AttendancePageStudent(request):
    if request.user.is_authenticated and user_type.objects.get(user=request.user).is_teacher == True:
        return redirect('/teacher/attandance_first')
    
    return render(request, 'home/students/attendance_page.html')


def AttendanceRequests(request):
    try:
        latest_ob = AttendanceList.objects.last()
        if latest_ob.is_expired == False:
            attendance = latest_ob
            return render(request, 'home/students/attendance_requests.html',
                          {'attendance': attendance})
        else:
            return HttpResponse('Session Expired.. Wait for new Session')
    except:
        return HttpResponse('Session Expired.. Wait for new Session')


def AttendanceStartStudent(request):
    if request.FILES.get("src"):
        image_path = request.FILES.get("src")
        TestImages(image=image_path).save()
        img = TestImages.objects.last().image

        img = cv2.imread(str(img))
        is_found = VideoCamera(img)
        if is_found == True:
            stud = attendance(request.user)
            return render(request, 'home/students/success_attendance.html', {'stud': stud})
        else:
            return HttpResponse('Sorry you have not created your profile yet...')
    return render(request, 'home/students/attendance.html')


def attendance(user):
    current_user = Student.objects.get(user=user)
    f_name = current_user.first_name
    l_name = current_user.last_name
    roll_no = current_user.roll_no
    div = current_user.div
    # sub =
    time_now = datetime.now()
    tStr = time_now.strftime('%H:%M:%S')
    dStr = time_now.strftime('%d/%m/%Y')
    data_list = list()
    data_dict = {
        'f_name': f_name,
        'l_name': l_name,
        'roll_no': roll_no,
        'div': div,
        'tStr': tStr,
        'dStr': dStr,
    }
    data_list.append(data_dict)
    roll_numbers = []
    try:
        attendance_list = AttendanceList.objects.last()
        attendance_list.attendance.append(data_list)
        attendance_list.save()

    except:
        attendance_list = AttendanceList.objects.last()
        attendance_list.attendance = data_list
        attendance_list.save()
    return data_dict


def MarksGreding(request):
    i = 1
    error = None
    result = ''
    is_result = False
    if request.GET:
        is_result = True
        cie1 = int(request.GET['cie1'])
        cie2 = int(request.GET['cie2'])
        cie3 = int(request.GET['cie3'])
        presenty = int(request.GET['presenty'])
        try:
            behaviour = int(request.GET['behaviour'])
        except:
            error = 'Please select the Behaviour of the student!'

        if int(cie1) > 50 or int(cie2) > 50 or int(cie3 >50):
            error = 'Marks should be less than 50'
        if error:
            result = 'Predict'
        else:
            result = getPred(cie1, cie2, cie3,presenty, behaviour)

    return render(request, 'home/students/marks_greding.html', {'result': result, 'is_result': is_result, 'error': error})

import json
def select_bus(request):
    if request.POST:
        try:
            bus = request.POST.get('bus')
            user_coord = request.POST.get('user_coord')
            user_id = User.objects.get(username=bus)
            driver = DriverCoord.objects.get(user=user_id)
            coord = {'lat':driver.lat,'lon':driver.lon}

            lat = 16.391708
            lon = 74.381701
            coord = json.dumps(coord)
            url = "https://www.google.com/maps/dir/" + lat + "," + lon + "/"+driver.lat+","+driver.lon+""
            return redirect(url)

            return render(request,'home/students/select_bus.html',{"coord":coord})
        except:
            pass
    
    return render(request,'home/students/select_bus.html')
    



# Teachers View

def TeacherDashboard(request):
    return render(request, 'home/teacher/teachers_dash.html')


def AttendancePageTeacher(request):
    return render(request, 'home/teacher/attendance_page.html')



@login_required(redirect_field_name='next', login_url='/login')
def AttendanceStartTeacher(request):
    if request.POST.get('end_session'):
        id = request.POST['end_session']
        ob = AttendanceList.objects.get(id=int(id))
        ob.is_expired = True
        print('expiring..')
        ob.save()
        
    elif request.POST:
        presenty_data = {}
        presenty_data['class'] = request.POST.get('class')
        presenty_data['course'] = request.POST.get('subject')
        presenty_data['session'] = int(request.POST.get('time'))
        presenty_data['div'] = request.POST.get('div')
        presenty_data['teacher'] = str(request.user)
        user_ob = User.objects.get(username=request.user)
        presenty_data['teacher_name'] = str(
            user_ob.first_name) + str(' ') + str(user_ob.last_name)

        if int(presenty_data['div']) == 1:
            presenty_data['div'] = 'A'
        else:
            presenty_data['div'] = 'B'

        if int(presenty_data['course']) == 1:
            presenty_data['course'] = 'Microwave Engineering'
        elif int(presenty_data['course']) == 2:
            presenty_data['course'] = 'Video Engineering'
        else:
            presenty_data['course'] = 'Computer Networking'

            AttendanceList(
                teacher=str(request.user),
                subject=presenty_data['course'],
                div=presenty_data['div'],
                year=presenty_data['class'],
                is_expired = False,
                teacher_name=presenty_data['teacher_name']).save()
            
    
    df = AttendanceList.objects.last()
    
    time_now = datetime.now()
    dStr = time_now.strftime('%d/%m/%Y')
    params = {'attendace_data': df.attendance,'df':df, 'dStr': dStr}
    return render(request, 'home/teacher/attendance.html', params
                  )


# Driver Dashboard

def driver_dash(request):
    
    return render(request,'home/driver/driver_dash.html')

def location_selected(request):
    
    return render(request,'home/driver/loc_selected.html')