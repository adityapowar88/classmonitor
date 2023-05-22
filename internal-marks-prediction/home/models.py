from re import sub
from django.db import models
from django.contrib.auth.models import User
import jsonfield
from datetime import datetime


class TestImages(models.Model):
    image = models.ImageField(upload_to='media/images')
    def __str__(self):
        return str(self.image)


class user_type(models.Model):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        if self.is_teacher == True:
            return " Teacher--" + str(' ') +  str(self.user)

        elif self.is_student == True:
            return " Student--" + str(' ') + str(self.user)
        
        elif self.is_driver == True:
            return " Driver--" + str(' ') + str(self.user)


class DriverCoord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    def __str__(self):
        return str(self.user)
        

class Student(models.Model):
    first_name = models.CharField(max_length=105)
    last_name = models.CharField(max_length=105)
    email = models.CharField(max_length=105)
    mobile = models.CharField(max_length=105)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='images')
    year = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    div = models.CharField(max_length=10)
    roll_no = models.CharField(max_length=10)
    def __str__(self):
        return str(self.first_name)
        

class AttendanceList(models.Model):
    attendance = jsonfield.JSONField()
    teacher = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    div = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    date = models.DateField(default=datetime.now, blank=True)
    teacher_name = models.CharField(max_length=100)
    is_expired = models.BooleanField(default=False)
    def __str__(self):
        return str(self.teacher)