from django.shortcuts import render,redirect
from .models import Book,Author,Issue,Fine
from student.models import Student
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.utils import timezone
import datetime
from .utilities import calcFine
from django.db.models import Q
from django.contrib.auth.models import User



# Book
def allbooks(request):
    allbooks=Book.objects.all()
    return render(request,'library/home.html',{'books':allbooks})

def search(request):
    search_query=request.GET.get('search-query')
    search_by_author=request.GET.get('author')
    if search_by_author is not None:
        author_results=Author.objects.filter(name__icontains=search_query)
        return render(request,'library/home.html',{'author_results':author_results})
    else:
        books_results=Book.objects.filter(Q(name__icontains=search_query) | Q(category__icontains=search_query))
        return render(request,'library/home.html',{'books_results':books_results})



@login_required(login_url='/student/login/')
@user_passes_test(lambda u: u.is_superuser,login_url='/student/login/')
def addbook(request):
    authors=Author.objects.all()
    if request.method=="POST":
        name=request.POST['name']
        category=request.POST['category']
        author=Author.objects.get(id=request.POST['author'])
        image=request.FILES['book-image']
        if author is not None or author != '':
            newbook,created=Book.objects.get_or_create(name=name,image=image,category=category,author=author)
            messages.success(request,'Book - {} Added succesfully '.format(newbook.name))
            return render(request,'library/addbook.html',{'authors':authors,})
        else:
            messages.error(request,'Author not found !')
            return render(request,'library/addbook.html',{'authors':authors,})
    else:
        return render(request,'library/addbook.html',{'authors':authors})



@login_required(login_url='/student/login/')
@user_passes_test(lambda u: u.is_superuser,login_url='/student/login/')
def deletebook(request,bookID):
    book=Book.objects.get(id=bookID)
    messages.success(request,'Book - {} Deleted succesfully '.format(book.name))
    book.delete()
    return redirect('/')



#  ISSUES

@login_required(login_url='/student/login/')
@user_passes_test(lambda u: not u.is_superuser,login_url='/student/login/')
def issuerequest(request,bookID):
    book=Book.objects.get(id=bookID)
    student=Student.objects.filter(student_id=request.user)[0]
    issue,created=Issue.objects.get_or_create(book=book,student=student)
    messages.success(request,'Book - {} Requested succesfully '.format(book.name))
    return redirect('home')

@login_required(login_url='/student/login/')
@user_passes_test(lambda u: not u.is_superuser ,login_url='/student/login/')
def myissues(request):
    student=Student.objects.filter(student_id=request.user)[0]
    
    if request.GET.get('issued') is not None:
        issues=Issue.objects.filter(student=student,issued=True)
    elif request.GET.get('notissued') is not None:
        issues=Issue.objects.filter(student=student,issued=False)
    else:
        issues=Issue.objects.filter(student=student)

    return render(request,'library/myissues.html',{'issues':issues})


@login_required(login_url='/admin/')
@user_passes_test(lambda u:  u.is_superuser ,login_url='/admin/')
def allissues(request):
    if request.GET.get('studentID') is not None and request.GET.get('studentID') != '':
        try:
            user= User.objects.get(username=request.GET.get('studentID'))
            student=Student.objects.filter(student_id=user)[0]
            issues=Issue.objects.filter(student=student)
            return render(request,'allissues.html',{'issues':issues})
        except User.DoesNotExist:
            messages.error(request,'No user found')
            return redirect('/all-issues/')

    else:
        issues=Issue.objects.all()
        return render(request,'library/allissues.html',{'issues':issues})



@login_required(login_url='/admin/')
@user_passes_test(lambda u:  u.is_superuser ,login_url='/student/login/')
def issue_book(request,issueID):
    issue=Issue.objects.get(id=issueID)
    issue.return_date=timezone.now() + datetime.timedelta(days=15)
    issue.issued_at=timezone.now()
    issue.issued=True
    issue.save()
    return redirect('/all-issues/')


@login_required(login_url='/student/login/')
@user_passes_test(lambda u:  u.is_superuser ,login_url='/admin/')
def return_book(request,issueID):
    issue=Issue.objects.get(id=issueID)
    calcFine(issue)
    issue.returned=True
    issue.save()
    return redirect('/all-issues/')


#  FINES

@login_required(login_url='/student/login/')
@user_passes_test(lambda u: not u.is_superuser ,login_url='/student/login/')
def myfines(request):
    student=Student.objects.filter(student_id=request.user)[0]
    issues=Issue.objects.filter(student=student)
    for issue in issues:
        calcFine(issue)
    fines=Fine.objects.filter(student=student)
    return render(request,'library/myfines.html',{'fines':fines})


@login_required(login_url='/student/login/')
@user_passes_test(lambda u:  u.is_superuser ,login_url='/admin/')
def allfines(request):
    issues=Issue.objects.all()
    for issue in issues:
        calcFine(issue)
    if request.GET.get('studentID') is not None and request.GET.get('studentID') != '':
        try:
            user= User.objects.get(username=request.GET.get('studentID'))
            student=Student.objects.filter(student_id=user)[0]
            fines=Fine.objects.filter(student=student)
            return render(request,'allfines.html',{'fines':fines})
        except User.DoesNotExist:
            messages.error(request,'No user found')
            return redirect('/all-fines/')
    else:
        fines=Fine.objects.all()
        return render(request,'library/allfines.html',{'fines':fines})

@login_required(login_url='/student/login/')
@user_passes_test(lambda u:  u.is_superuser ,login_url='/admin/')
def deletefine(request,fineID):
    fine=Fine.objects.get(id=fineID)
    fine.delete()
    return redirect('/all-fines/')