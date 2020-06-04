from django import forms
from crudApp.models import UserProfileInfo, Project
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'password', 'email')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic')


class ProjectForm(forms.ModelForm):
    class Meta():
        model = Project
        fields = ['title', 'slug', 'project_image',
                  'project_type', 'project_body']
