from django.shortcuts import render,redirect
from .models import Student,Department 
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
def home(request):
    return render(request, 'home.html')


def logout(request):
    auth.logout(request)
    messages.success(request,'Logout successful')
    return redirect('home')


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(request,
                                 username=request.POST['studentID'], 
                                 password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {"message": 'Invalid CREDENTIALS', 'user': user})
        else:
            auth.login(request, user)
            messages.success(request,'Login successful')
            return redirect('home')
    else:
        return render(request, 'login.html')


def signup(request):
    
    if request.method=='POST':
        try:
            user=User.objects.get(username=request.POST['studentID'])
            return render(request,'signup.html',{"message":"user exists already !!", "departments":Department.objects.all()})

        except User.DoesNotExist:
            user=User.objects.create_user(username=request.POST['studentID'],password=request.POST['password'])

            newstudent=Student.objects.create(first_name=request.POST['firstname'],last_name=request.POST['lastname'],
            department=Department.objects.get(id=request.POST['department']),student_id=user
            )

            auth.login(request,user)
            messages.success(request,'Signup successful')
            return redirect('home')

    else:
        return render(request,'signup.html',{
            "departments":Department.objects.all()
        })

