from multiprocessing import context
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
#from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
# Create your views here.
from .models import Students,Teachers,user,Profile

from itertools import chain

@login_required(login_url='login')
def home1(request):
    """Displays the homepage of students
    
    """
    teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
    student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
    teachers_all = Teachers.objects.all()
    mappings = chain(teacher_mapping,student_mapping) 
    return render(request,'accounts/dashboard_student.html',{'mappings':mappings,'teachers_all':teachers_all})

@login_required(login_url='login')
def home2(request):
    """ Displays the homepage of teachers"""
    teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
    student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
    teachers_all = Teachers.objects.all()
    mappings = chain(teacher_mapping,student_mapping) 
    return render(request,'accounts/dashboard_teacher.html',{'mappings':mappings,'teachers_all':teachers_all})



def loginPage(request):
    """ Authenticates the user with username and password  differently for teachers and students """
    if request.user.is_authenticated and request.user.is_student:
        return redirect('home1')
    elif request.user.is_authenticated and request.user.is_teacher:
        return redirect('home2')
    else:
        if request.method=='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user = authenticate(request,username=username, password=password)
            if user is not None and user.is_student:
                login(request,user)
                return redirect('home1')
            elif user is not None and user.is_teacher:
                login(request,user)
                return redirect('home2')
            else:
                messages.info(request,'Incorrect Credentials')
        context={}
        return render(request,'accounts/login.html',context)

def change_password(request):
    """ Changes password using default form /n
     On successful password change it redirects to homepage"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })

def logoutUser(request):
    """ Logouts the user"""
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile(request):
    """ Renders the data required to create the profile page of the  user"""
    user_get = get_object_or_404(user, username=request.user.username)
    profile = get_object_or_404(Profile, user_details=user_get)
    return render(request, 'accounts/profile.html', {'profile': profile, 'user': user_get})

@login_required(login_url='login')
def edit_profile(request):
    """ Allows user to edit their profile data """
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST,instance=request.user.profile)
        u_form = UserUpdateForm(request.POST,instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,'Your Profile has been updated!')
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user)
        u_form = UserUpdateForm(instance=request.user.profile)

    context={'p_form': p_form, 'u_form': u_form}
    return render(request, 'accounts/edit_profile.html',context )