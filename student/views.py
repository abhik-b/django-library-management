from django.shortcuts import render
from .models import Student,Department 
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage



def home(request):
    return render(request, 'homepage.html')


def logout(request):
    auth.logout(request)
    return render(request, 'homepage.html')


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(request,
                                 username=request.POST['studentID'], 
                                 password=request.POST['password'])

        if user is not None:
            auth.login(request, user)
            return render(request, 'homepage.html', {'message': 'logged in'})
        else:
            return render(request, 'login.html', {"error": 'Invalid credenTIALS', 'user': user})
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
            return render(request,'homepage.html',{'message':"signed in"})

    else:
        return render(request,'signup.html',{
            "departments":Department.objects.all()
        })

def uploadfile_view(request):
    if request.method=="POST":
        f=request.FILES['file']
        fs=FileSystemStorage()
        filename,ext=str(f).split('.')
        file1=fs.save(str(f),f)
        fileurl=fs.url(file1)
        fileSize=fs.size(file1)
        return render(request,'upload.html',{'fileUrl':fileurl,'fileName':filename,'ext':ext,'fileSize':fileSize})
    else:
         return render(request,'upload.html',{})

