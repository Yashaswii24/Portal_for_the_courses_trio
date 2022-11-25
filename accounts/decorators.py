from django.contrib.auth.models import User 
from django.shortcuts import redirect

from .models import Classrooms,Students,Teachers,Assignments


def teacher_required(redirect_to):
    """ Makes sure that only teacher is able to access this page"""
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if kwargs.get('classroom_id'):
                query_id = kwargs['classroom_id']
            elif kwargs.get('assignment_id'):
                try:
                    assignment = Assignments.objects.get(pk=kwargs['assignment_id'])
                except Exception as e:
                    print(str(e))
                    return redirect('home2')
                query_id = assignment.classroom_id.id  
            
            try:
                classroom = Classrooms.objects.get(pk=query_id)
            except Exception as e:
                print(str(e))
                return redirect('render_class',id=query_id)

            teacher_count = Teachers.objects.filter(teacher_id=request.user,classroom_id=classroom).count()
            if teacher_count == 0:
                return redirect('render_class',id=query_id)
            return view_method(request,*args,**kwargs)
        return _arguments_wrapper
    return _method_wrapper 

def student_required(redirect_to):
    """ Makes sure that the only student is able to access this page"""
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            print(kwargs)
            if kwargs.get('classroom_id'):
                query_id = kwargs['classroom_id']
            elif kwargs.get('assignment_id'):
                try:
                    assignment = Assignments.objects.get(pk=int(kwargs['assignment_id']))
                except Exception as e:
                    return redirect('home1')
                query_id = assignment.classroom_id.id  
            
            try:
                classroom = Classrooms.objects.get(pk=query_id)
            except Exception as e:
                return redirect('render_class',id=query_id)

            student_count = Students.objects.filter(student_id=request.user,classroom_id=classroom).count()
            if student_count == 0:
                return redirect('render_class',id=query_id)
            return view_method(request,*args,**kwargs)
        return _arguments_wrapper
    return _method_wrapper 