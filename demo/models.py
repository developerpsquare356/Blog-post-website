from django.db import models
from datetime import date
# Create your models here.
from django.contrib.auth.models import User
from django.db.models import ForeignKey
from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete,pre_save,pre_delete


class Contact_Me_info(models.Model):
    Name=models.CharField(max_length=100)
    Email=models.EmailField()
    PhoneNo=models.IntegerField()
    Message=models.TextField()


class AddBlogs(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="user_detail")
    AuthorName=models.CharField(max_length=100)
    Title = models.CharField(max_length=250)
    Subtitle= models.TextField()
    Body = models.TextField()
    Date=models.DateField(default=date.today)


#===============     Student data Class   ===========================

class Department(models.Model):
    department=models.CharField(max_length=100)

    def __str__(self)->str:
        return self.department

    class Meta:
        ordering=['department']

class StudentId(models.Model):
    student_id=models.CharField(max_length=100)
    def __str__(self)->str:
        return self.student_id


class Student(models.Model):
    department=models.ForeignKey(Department,related_name='depart',on_delete=models.CASCADE)
    student_id = models.OneToOneField(StudentId, related_name='studentid', on_delete=models.CASCADE)
    student_name=models.CharField(max_length=100)
    student_email = models.EmailField(unique=True)
    student_age = models.IntegerField(default=18)
    student_address=models.TextField()

    def __str__(self)->str:
        return self.student_name

    class Meta:
        ordering=['student_name']
        verbose_name='student'


class Subject(models.Model):
    subject_name=models.CharField(max_length=100,null=False)
    def __str__(self) -> str:
        return self.subject_name


class StudentMarks(models.Model):
    student=models.ForeignKey(Student,related_name='studentmarks',on_delete=models.CASCADE)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    marks=models.IntegerField()
    def __str__(self)->str:
        return f'{self.student.student_name} {self.subject.subject_name}'

    class Meta:
        unique_together=['student','subject']

class StudentReportCard(models.Model):
    student = models.ForeignKey(Student, related_name='studentreportcard', on_delete=models.CASCADE)
    total_marks=models.IntegerField()
    student_rank= models.IntegerField()
    date_of_report_card= models.DateField(auto_now_add=True)

    class Meta:
        unique_together=['student_rank','date_of_report_card']



