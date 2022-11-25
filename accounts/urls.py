from atexit import register
from django.urls import path
#from . import views,students,teachers
from django.conf.urls.static import static
from django.conf import settings
from . import views,students,teachers,classs,assignments,submissions
urlpatterns = [
    path("home/student", views.home1,name="home1"),
    path("home/teacher", views.home2,name="home2"),
    path("register/student",students.StudentSignUpView.as_view(),name="register_student"),
    path("register/teacher",teachers.TeacherSignUpView.as_view(),name="register_teacher"),
    path("",views.loginPage,name="login"),
    path("logout/",views.logoutUser,name="logout"),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path("change_password/", views.change_password, name='change_password'),
    path('class/<int:id>',classs.render_class,name='render_class'),
    path('create_class_request/',classs.create_class_request,name='create_class_request'),
    path('join_class_request/',classs.join_class_request,name='join_class_request'),
    path('create_assignment/<int:classroom_id>',assignments.create_assignment,name='create_assignment'),
    path('assignment_summary/<int:assignment_id>',assignments.assignment_summary,name='assignment_summary'),
    path('delete_assignment/<int:assignment_id>',assignments.delete_assignment,name='delete_assignment'),
    path('submit_assignment_request/<int:assignment_id>',submissions.submit_assignment_request,name='submit_assignment_request'),
    path('mark_submission_request/<int:submission_id>/<int:teacher_id>',submissions.mark_submission_request,name='mark_submission_request'),
    path('submission_feedback/<int:assignment_id>',submissions.get_submission_request,name='submission_feedback'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
