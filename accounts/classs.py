from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .utils import generate_class_code
from .models import Classrooms, Teachers, Students, Assignments

from itertools import chain

@login_required(login_url='login')
def render_class(request,id):
    """This function makes sure that the courses in which a student is registered are only visible in his dashboard./n
    and teacher can only see the courses he created in his dashboard.
    """
    classroom = Classrooms.objects.get(pk=id)
    try: 
        assignments = Assignments.objects.filter(classroom_id = id)
    except Exception as e:
        assignments = None

    try:
        students = Students.objects.filter(classroom_id = id)
    except Exception as e:
        students = None
    
    teachers = Teachers.objects.filter(classroom_id = id)
    teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
    student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
    mappings = chain(teacher_mapping,student_mapping) 
    return render(request,'accounts/class_page.html',{'classroom':classroom,'assignments':assignments,'students':students,'teachers':teachers,"mappings":mappings})

@login_required(login_url='login')
def create_class_request(request):
    """"Creates the class with given details and generates a unique Passcode which can be used by students to join in the class.
    
    """
    if request.POST.get('action') == 'post':
        classrooms = Classrooms.objects.all()
        existing_codes=[]
        for classroom in classrooms:
            existing_codes.append(classroom.class_code)
        
        class_name = request.POST.get('class_name')
        description = request.POST.get('description')

        class_code = generate_class_code(6,existing_codes)
        classroom = Classrooms(classroom_name=class_name,description=description,class_code=class_code)
        classroom.save()
        teacher = Teachers(teacher_id=request.user,classroom_id=classroom)
        teacher.save()
        return JsonResponse({'status':'SUCCESS'})

@login_required(login_url='login')
def join_class_request(request):
    """Students join the class with the respective passcode and save it in database
    """
    if request.POST.get('action') == 'post':
        code = request.POST.get('class_code')
        try:
            classroom = Classrooms.objects.get(class_code=code)
            student = Students.objects.filter(student_id = request.user, classroom_id = classroom)
            if (student.count()!=0):
                return redirect('home1')
        except Exception as e:
            
            return JsonResponse({'status':'FAIL','message':str(e)})
        student = Students(student_id = request.user, classroom_id = classroom)
        student.save()
        return JsonResponse({'status':'SUCCESS'})