from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import StudentForm, IssueForm, CreateUserForm
from .filters import IssueFilter, BookFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)

		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, 'Library Card Issued Successfully for '+username)
			return redirect('login')
	
	context = {'form':form}
	return render(request, 'app/register.html', context)

@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')

		else:
			if User.objects.filter(username=username).exists():
				messages.error(request, 'Invalid Password!!')
			else:
				messages.error(request, 'This UserName Doesn\'t Exist!!')

	context = {}
	return render(request, 'app/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
	books = Book.objects.all()
	students = StudentProfile.objects.all()
	issues = Issue.objects.all()

	total_books = books.count()
	total_students = students.count()
	total_issues = issues.count()

	pending_issues = issues.filter(status='Pending').count()
	issued = issues.filter(status='Issued').count()
	returned_issues = issues.filter(status='Returned').count()
	
	context = {
		'books':books,
		'students':students,
		'issues':issues, 
		'bookscount':total_books, 
		'issuescount': total_issues, 
		'studentscount': total_students,
		'pending': pending_issues, 
		'issued': issued, 
		'returned': returned_issues,
	}
	# print(context)
	return render(request, 'app/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Student'])
def userPage(request):
	studentProfile = StudentProfile.objects.get(user=request.user)
	issues = Issue.objects.filter(user=request.user)
	total_issues = issues.count()
	pending_issues = issues.filter(status='Pending').count()
	issued = issues.filter(status='Issued').count()
	returned_issues = issues.filter(status='Returned').count()
	context = {
		'studentProfile': studentProfile,
		'issues':issues,  
		'issuescount': total_issues,
		'pending': pending_issues, 
		'issued': issued, 
		'returned': returned_issues,
	}
	# print(context)
	return render(request, 'app/userpage.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Student'])
def profileSettings(request, pk):
	print(request.user, request.user.groups.first())
	student = StudentProfile.objects.get(id=pk)
	form = StudentForm(instance=student)

	if request.method == 'POST':
		form = StudentForm(request.POST, request.FILES, instance=student)
		if form.is_valid():
			form.save()
			return redirect('user-page')

	context = {'form':form}
	return render(request, 'app/profile_settings.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Librarian'])
def books(request):
	books = Book.objects.all()

	myFilter = BookFilter(request.GET, queryset=books)
	books = myFilter.qs

	context = {
		'books':books,
		'myBookFilter':myFilter,
	}
	return render(request, 'app/books.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Librarian'])
def student_info(request, pk):
	student = StudentProfile.objects.get(id=pk)

	issues = student.user.issue_set.all()
	issue_count = issues.count()

	myFilter = IssueFilter(request.GET, queryset=issues)
	issues = myFilter.qs 

	context = {
		'student':student, 
		'issues':issues, 
		'issue_count':issue_count,
		'myFilter':myFilter
	}
	return render(request, 'app/student_details.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Librarian','Student'])
def createIssue(request, pk):
	IssueFormSet = inlineformset_factory(User, Issue, fields=('book', 'status'), extra=6)
	student = StudentProfile.objects.get(id=pk)
	formset = IssueFormSet(queryset=Issue.objects.none(),instance=student.user)

	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = IssueForm(request.POST)
		formset = IssueFormSet(request.POST, instance=student.user)
		
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset, 'student':student}
	return render(request, 'app/issue_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Librarian'])
def updateIssue(request, pk):
	issue = Issue.objects.get(id=pk)
	form = IssueForm(instance=issue)
	print('ISSUE:', issue)

	if request.method == 'POST':
		form = IssueForm(request.POST,instance=issue)
		form = IssueForm(request.POST, instance=issue)
		
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'app/update_issue.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Librarian'])
def deleteIssue(request, pk):
	issue = Issue.objects.get(id=pk)

	if request.method == "POST":
		issue.delete()
		return redirect('user')

	context = {'issue':issue}
	return render(request, 'app/delete_issue.html', context)