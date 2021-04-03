from django.contrib import admin
from .models import Student,Department
from library.admin import FineInline,IssueInline
# Register your models here.




@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    search_fields=['student_id__username','first_name','department']
    fields=(('first_name','last_name'),('student_id','department'))
    list_display=('first_name','last_name','student_id','department')
    list_display_links = ('first_name', 'student_id')
    list_filter=('department__name',)
    list_per_page=30
    inlines = [
        FineInline,IssueInline
    ]
    
admin.site.register(Department)
