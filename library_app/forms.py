from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

class StudentForm(ModelForm):
	class Meta:
		model = StudentProfile
		fields = '__all__'
		exclude = ['user']

class IssueForm(ModelForm):
	class Meta:
		model = Issue
		fields = '__all__'

	# def __init__(self, *args, **kwargs):
	# 	IssueForm.base_fields['book'].queryset = IssueForm.base_fields['book'].queryset.exclude(num_copies=0)
	# 	return super(IssueForm, self).__init__(*args, **kwargs)
		

class CreateUserForm(UserCreationForm):
	first_name = forms.CharField(label='First Name' ,widget=forms.TextInput(attrs={'placeholder':'Enter First Name', 'autofocus':True}))
	last_name = forms.CharField(label='SurName' ,widget=forms.TextInput(attrs={'placeholder':'Enter Last Name'}))

	username = forms.CharField(label='Username' ,widget=forms.TextInput(attrs={'placeholder':'Enter a Username','autofocus':False}))

	email = forms.EmailField(label='Email Address' ,min_length=9, widget=forms.EmailInput(attrs={'placeholder':'Enter Email Address'}))
	
	password1 = forms.CharField(label='Password' ,widget=forms.PasswordInput(attrs={'placeholder':'Enter an Unique Password'}))
	password2 = forms.CharField(label='Confirm Password' ,widget=forms.PasswordInput(attrs={'placeholder':'Re-type your Password'}))
	

	class Meta:
		model = User
		fields = ['first_name','last_name','username', 'email', 'password1', 'password2']
