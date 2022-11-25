from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .decorators import teacher_required
from .models import Teachers, Students, Assignments, Submissions
from .forms import * 

from itertools import chain

@login_required(login_url='login')
@teacher_required('home2')
def create_assignment(request,classroom_id):
    """This method is used to create assugnments inside a class with help pf classroom_id./n
       First find the teachers and students present in class and then check if form valid or not(according to our custom form)./n
       If valid we create the assignment or else we render the page till the modified form becomes valid.

    """
    teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
    student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
    mappings = chain(teacher_mapping,student_mapping)

    if request.method == 'POST':
        form = CreateAssignmentForm(request.POST,request.FILES)
        if form.is_valid():
            assignment_name = form.cleaned_data.get('assignment_name')
            due_date = form.cleaned_data.get('due_date')
            due_time = form.cleaned_data.get('due_time')
            classroom_id = Classrooms.objects.get(pk=classroom_id)
            instructions = form.cleaned_data.get('instructions')
            total_marks = form.cleaned_data.get('total_marks')
            valid_extensions = form.cleaned_data.get('valid_extensions')
            file_directory = request.FILES['file_directory']
            assignment = Assignments(assignment_name = assignment_name,due_date = due_date,due_time=due_time,instructions = instructions,total_marks = total_marks,classroom_id=classroom_id,valid_extensions=valid_extensions,file_directory=file_directory)
            assignment.save()
            
            return redirect('render_class',id=classroom_id.id)
        else:
            return render(request,'accounts/create_assignment.html',{'form':form,'mappings':mappings})
    form = CreateAssignmentForm()
    return render(request,'accounts/create_assignment.html',{'form':form,'mappings':mappings})


@login_required(login_url='login')
@teacher_required('home2')
def assignment_summary(request,assignment_id):
    """Gives details about the assignment :/n
    * Number of Submissions/n
    * Download the submissions/n
    * Grade the submissions/n
    By rendering data to the webpage

    """
    assignment = Assignments.objects.filter(pk = assignment_id).first()
    submissions = Submissions.objects.filter(assignment_id = assignment_id)
    teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
    student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
    no_of_students = Students.objects.filter(classroom_id=assignment.classroom_id)
    mappings = chain(teacher_mapping,student_mapping)
    return render(request,'accounts/assignment_summary.html',{'assignment':assignment,'submissions':submissions,'mappings':mappings,'no_of_students':no_of_students})

@login_required(login_url='login')
@teacher_required('home2')
def delete_assignment(request,assignment_id):
    """Deletes the Assignment/n
       Delete the data related to assignment from the database
    """
    try:
        assignment = Assignments.objects.get(pk=assignment_id)
        classroom_id = assignment.classroom_id.id 
        Assignments.objects.get(pk=assignment_id).delete()
        return redirect('render_class', id=classroom_id)
    except Exception(e):
        return redirect('home')
        


                

           