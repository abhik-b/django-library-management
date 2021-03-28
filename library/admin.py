from django.contrib import admin
from .models import Author,Book,Fine,Issue
# Register your models here.
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Issue)
admin.site.register(Fine)