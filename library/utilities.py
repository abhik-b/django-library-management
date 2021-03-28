import datetime
from django.utils import timezone
from .models import Fine

def calcFine(issue):
    if(issue.issued==True and issue.returned==False):
        y,m,d=str(timezone.now().date()).split('-')
        today=datetime.date(int(y),int(m),int(d))
        y2,m2,d2=str(issue.return_date.date()).split('-')
        lastdate=datetime.date(int(y2),int(m2),int(d2))
        if(today>lastdate):
            diff=today-lastdate
            fine,created=Fine.objects.get_or_create(issue=issue,student=issue.student)
            fine.amount=diff.days*10
            fine.save()
        else:
            return 'no fine'
    else:
        return 'no fine'