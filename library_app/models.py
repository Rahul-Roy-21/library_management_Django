from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class StudentProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True, blank=True)
    date_created = models.DateField(verbose_name='Card Issued on', auto_now_add=True)
    profile_pic = models.ImageField(default="default_profile_pic.png", null=True, blank=True)

    def __str__(self):
        return '{} -> EMAIL: {}'.format(self.user.username, self.user.email)
        
class Publisher(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=500, null=True)
    date_of_publication = models.DateField()
    publisher = models.ForeignKey(Publisher, on_delete=models.RESTRICT)
    author = models.ManyToManyField(Author, blank=True)
    category = models.ForeignKey(Category, blank=True, on_delete=models.RESTRICT)
    num_copies = models.IntegerField(default=0)

    def __str__(self):
        return '{} by {}'.format(self.title, self.publisher.name)

class Issue(models.Model):
    status_choices = [("Pending","Issue Pending"),("Issued","Issued"),("Returned","Returned")]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, blank=True, null=True)
    date_of_issue = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=status_choices, default="Pending")

    def __str__(self):
        return "{} ISSUED by {} on {}".format(self.book.title, self.user.username, self.date_of_issue)