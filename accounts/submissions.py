from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .decorators import student_required
from .models import Assignments, Students, Submissions
from .forms import *     
from django.utils.timesince import timesince
from datetime import datetime
from itertools import chain
from django.core.exceptions import ValidationError
from django.contrib import messages
import os,shutil,sys
from pathlib import Path



@csrf_exempt
@login_required(login_url='login')
@student_required('home1')
def submit_assignment_request(request,assignment_id):
    
    """Takes the file students submitted if it has has given file extension  and stores in the correct directory in media folder./n
    Also creates a new submission record in the database and also verifies the file directory
    
    """
    assignment = Assignments.objects.get(pk=assignment_id)
    student_id = Students.objects.get(classroom_id=assignment.classroom_id,student_id=request.user.id)
    file_name = request.FILES.get('myfile')
    storage = messages.get_messages(request)
    for _ in storage:
        pass
    extensions = assignment.valid_extensions.split(",")
    
    for extension in extensions:
        if str(file_name).endswith(extension):
            try:
                submission = Submissions.objects.get(assignment_id=assignment, student_id = student_id)
                submission.submission_file = file_name
                submission.save()
                

            except Exception as e:  
               submission = Submissions(assignment_id = assignment,student_id= student_id,submission_file = file_name)
            dt1=datetime.now()
            dt2=datetime.combine(assignment.due_date,assignment.due_time)
            dt_string = dt1.strftime("%d/%m/%Y %H:%M:%S")
            datetime1 = dt_string.split(" ")
            date = datetime1[0].split("/")
            submission.submitted_date = date[2]+"-"+date[1]+"-"+date[0]
            submission.submitted_time = datetime1[1]
            time = timesince(dt1, dt2)
            if time[0]=='0':
                submission.submitted_on_time=False
            submission.save()
            name = os.path.basename(str(submission.submission_file))
            name1 = name.split(".")
            
            shutil.unpack_archive(submission.submission_file.path,"media/"+os.path.dirname(str(submission.submission_file))+"/"+name1[0])
            startpath = "media/"+os.path.dirname(str(submission.submission_file))+"/"+name1[0]
            
            os.chdir(startpath)
            os.system("tree > myfile.txt")
            os.system('diff myfile.txt '+str(assignment.file_directory.path)+" > output.txt")
            if os.stat("output.txt").st_size == 0:
                submission.feedback = "not yet graded"
                submission.filedirectory = True
            else:
                submission.feedback = "Incorrect file directory"
                submission.filedirectory = False
            
            submission.marks_alloted = 0
            
            submission.save(update_fields=["filedirectory","submitted_date","submitted_time","marks_alloted","feedback"])
            
            os.chdir("..")
            os.chdir("..")
            os.chdir("..")
            os.chdir("..")
            
            
            return JsonResponse({'status':'SUCCESS'})
    messages.success(request, 'Form submission successful')
    return render(request,"accounts/class_page.html")

def mark_submission_request(request,submission_id,teacher_id):
    """Teacher can mark the submission made by the student
    """
    if request.POST.get('action') == 'post':
        marks = request.POST.get('submission_marks')
        feedback = request.POST.get('feedback')
        
        submission = Submissions.objects.get(pk=submission_id)
        submission.marks_alloted = marks
        submission.feedback = feedback
        submission.save(update_fields=["marks_alloted","feedback"])
        return JsonResponse({'status':'SUCCESS'})


@login_required(login_url='login')
@student_required('home1')
def get_submission_request(request,assignment_id):
    """Displays the Submission details on students side by getting data of submission into web page
    """
    assignment = Assignments.objects.filter(pk = assignment_id).first()
    submissions = Submissions.objects.filter(assignment_id = assignment_id)
    teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
    student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
    no_of_students = Students.objects.filter(classroom_id=assignment.classroom_id)
    mappings = chain(teacher_mapping,student_mapping)
    return render(request,'accounts/submission.html',{'assignment':assignment,'submissions':submissions,'mappings':mappings,'no_of_students':no_of_students})