from django.contrib.auth.forms import UserCreationForm
from django import forms
import datetime
from .models import *


class CreateClassForm(forms.Form):
    """ Form for the Creation of course"""
    def __init__(self,*args,**kwargs):
        super(CreateClassForm,self).__init__()
        self.fields['class_name'].label=''
        self.fields['description'].label=''
        self.fields['class_name'].widget.attrs['placeholder']='Class Name'
        self.fields['description'].widget.attrs['placeholder']='Description'
    
    class_name = forms.CharField(max_length=100,label='Class name')
    description = forms.CharField(max_length=100,label='Description')


class StudentSignUpForm(UserCreationForm):
    """ Form for signup of students"""
    class Meta(UserCreationForm.Meta):
        model = user
        fields=['username','first_name','last_name','email','password1','password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        if commit:
            user.save()
        return user

class TeacherSignUpForm(UserCreationForm):
    """ Form for signup of teachers"""
    class Meta(UserCreationForm.Meta):
        model = user
        fields=['username','first_name','last_name','email','password1','password2']
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user

class CreateAssignmentForm(forms.Form):
    """ Form for the creation of assignments """
    assignment_name = forms.CharField(max_length=50,label='Assignment Name')
    due_date = forms.DateField(initial=datetime.date.today(),label='Due Date')
    due_time = forms.TimeField(initial=datetime.time(10,10),label='Due Time')
    instructions = forms.CharField(label='Instructions',widget=forms.Textarea)
    total_marks = forms.IntegerField(label='Total Marks')
    valid_extensions = forms.CharField(label = 'valid extensions')
    file_directory = forms.FileField(label = 'file directory')
    
class UserUpdateForm(forms.ModelForm):
    """ Form for update user details used for registration """
    class Meta:
        model=user
        fields=['username','first_name','last_name','email']

class ProfileUpdateForm(forms.ModelForm):
    """ Form for profile update of field created aditionally for the user """
    class Meta:
        model=Profile
        fields=['about_me',]

