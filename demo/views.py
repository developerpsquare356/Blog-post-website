from email.message import Message

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.db.models import Q ,Sum
# Create your views here.





def home(request):
    post=AddBlogs.objects.all()
    return render(request,"index.html",context={"post_data":post})


def about_page(request):

    return render(request,"about.html")


def contact_page(request):
    if request.method == "POST":
        msg_sent = True

        data = request.POST
        Contact_Me_info.objects.create(
            Name=data.get('Name'),
            Email=data.get('Email'),
            PhoneNo=data.get("PhoneNo"),
            Message=data.get('Message')
        )
        # send_email(data["name"], data["email"], data["phone"], data["message"])
        return render(request,"contact.html",context={"msg_sent":msg_sent})
    return render(request,"contact.html")


def post_page(request,id):
    post_data = AddBlogs.objects.filter(id=id).get()
    return render(request,"post.html",context={"post_data":post_data})

@login_required(login_url='/login/')
def blog_add(request):
    if request.method == "POST":
        msg_sent = True
        print("hello")

        data = request.POST
        AddBlogs.objects.create(
            user=request.user,
            AuthorName=data.get('name'),
            Title=data.get('title'),
            Subtitle=data.get("subtitle"),
            Body=data.get('body')
        )
        # send_email(data["name"], data["email"], data["phone"], data["message"])
        return render(request,"blog_add.html",context={"msg_sent":msg_sent})
    return render(request,"blog_add.html")

@login_required(login_url='/login/')
def update_blog(request,id):
    post_data = AddBlogs.objects.filter(id=id).get()

    if request.method == "POST":
        msg_sent = True

        data = request.POST
        AddBlogs.objects.filter(id=id).update(
            AuthorName=data.get('name'),
            Title=data.get('title'),
            Subtitle=data.get("subtitle"),
            Body=data.get('body')
        )
        # send_email(data["name"], data["email"], data["phone"], data["message"])
        return render(request,"update_blog.html",context={"msg_sent":msg_sent})

    return render(request,"update_blog.html",context={"post":post_data})

def login_page(request):
    if request.method == "POST":
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid Username")
            return redirect('/login/')

        user=authenticate(username=username,password=password)
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/')
    return render(request,'login.html')

def register_page(request):
    if request.method == "POST":
        data = request.POST
        user=User.objects.filter(username=data.get('username'))

        if user.exists():
            messages.info(request, "Username Already exist")
            return redirect('/register/')

        user = User.objects.create(
            first_name=data.get('name'),
            username=data.get('username'),
            email=data.get("email")
        )
        user.set_password(data.get('password'))
        user.save()
        messages.info(request, "Account created successfully")
        return redirect('/login/')
    return render(request,'register.html')


def logout_page(request):
    logout(request)
    return redirect('/login/')



#===========================     Student DATA code

from .seed import *

def get_student_data(request):
    # hi_send_email() this help to send email to someone else
    queryset=Student.objects.all()
    if request.GET.get("search"):
        search=request.GET.get("search")
        queryset=queryset.filter(Q(student_name__icontains=search)|Q(student_email__icontains=search)|Q(student_id__student_id__icontains=search)|Q(department__department__icontains=search))

# pagination code
    paginator = Paginator(queryset, 10)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request,'student/student.html',context={"queryset":page_obj})

def student_mark(request,student_id):
    queryset=StudentMarks.objects.filter(student__student_id__student_id=student_id)
    rank_data=StudentReportCard.objects.filter(student__student_id__student_id=student_id)
    return render(request,"student/see_student_marks.html",context={"queryset":queryset,'data':rank_data})




def hi_send_email():
    subject='DIWALI INVITATION'
    message='My name is Prantik Pal. I wish that you have an happy diwali.'
    from_email=settings.EMAIL_HOST_USER
    receiver_email=['prantikpal.399@gmail.com']

    send_mail(
        subject,
        message,
        from_email,
        receiver_email
    )



