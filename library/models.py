from django.db import models
from student.models import Student
# Create your models here.
class Author(models.Model):
    name=models.CharField(max_length=350)
    description=models.CharField(max_length=450)
    def __str__(self):
        return self.name
    
class Book(models.Model):
    name=models.CharField(max_length=350)
    author=models.ForeignKey(Author,on_delete=models.CASCADE)
    image=models.ImageField()
    category=models.CharField(max_length=220)

    def __str__(self):
        return self.name
    
class Issue(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    created_at=models.DateTimeField( auto_now=True)
    issued=models.BooleanField(default=False)
    issued_at=models.DateTimeField( auto_now=False,null=True,blank=True)
    returned=models.BooleanField(default=False)
    return_date=models.DateTimeField(auto_now=False,auto_created=False,auto_now_add=False,null=True,blank=True)

    def __str__(self):
        return "{}_{} book issue request".format(self.student,self.book)
    
class Fine(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    issue=models.ForeignKey(Issue,on_delete=models.CASCADE)
    amount=models.DecimalField(default=0.00,max_digits=10,decimal_places=2)

    def __str__(self):
        return "{} fine->{}".format(self.issue,self.amount)