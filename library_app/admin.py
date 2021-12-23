from django.contrib import admin
from .models import *

# Librarian Username=Rahul_Roy Password=Rahul1234

# Register your models here.
class StudentProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'date_created')

class PublisherAdmin(admin.ModelAdmin):
    fields = ('name')

class AuthorAdmin(admin.ModelAdmin):
    fields = ('name')

class BookAdmin(admin.ModelAdmin):
    fields = ('title', 'category', 'publisher')

class IssueAdmin(admin.ModelAdmin):
    fields = ('book','user','date_of_issue')


admin.site.register(StudentProfile)
admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Issue)