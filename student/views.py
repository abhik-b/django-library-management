from django.shortcuts import render,redirect
from .models import Student,Department 
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.storage import FileSystemStorage




def uploadfile_view(request):
    fileContext=[]
    if request.method=="POST":
        files=request.FILES.getlist('file')
        fs=FileSystemStorage()
        for f in files:
            filename,ext=str(f).split('.')
            file1=fs.save(str(f),f)
            fileurl=fs.url(file1)
            fileSize=fs.size(file1)
            fileContext.append({'fileUrl':fileurl,'fileName':filename,'ext':ext,'fileSize':fileSize})
        return render(request,'student/fileupload.html',{'fileContext':fileContext})
    else:
         return render(request,'student/fileupload.html',{})

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
            return render(request, 'student/login.html', {"message": 'Invalid CREDENTIALS', 'user': user})
        else:
            auth.login(request, user)
            messages.success(request,'Login successful')
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return redirect('home')
    else:
        return render(request, 'student/login.html')


def signup(request):
    
    if request.method=='POST':
        try:
            user=User.objects.get(username=request.POST['studentID'])
            return render(request,'student/signup.html',{"message":"user exists already !!", "departments":Department.objects.all()})

        except User.DoesNotExist:
            user=User.objects.create_user(username=request.POST['studentID'],password=request.POST['password'])

            newstudent=Student.objects.create(first_name=request.POST['firstname'],last_name=request.POST['lastname'],
            department=Department.objects.get(id=request.POST['department']),student_id=user
            )

            auth.login(request,user)
            messages.success(request,'Signup successful')
            if "next" in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('home')

    else:
        return render(request,'student/signup.html',{
            "departments":Department.objects.all()
        })

