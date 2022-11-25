from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

class user(AbstractUser):
    """ Created customer user model with two extra boolean fields to determine whether it is teacher or students"""
    is_student = models.BooleanField('student status', default=False)
    is_teacher = models.BooleanField('teacher status', default=False)
    email = models.EmailField()
class Classrooms(models.Model):
    """ Contains name, description and classcode fields"""
    classroom_name=models.CharField(max_length=100,default='')
    description = models.CharField(max_length=100,default='')
    class_code = models.CharField(max_length = 10,default='0000000')

    def __str__(self):
        return self.classroom_name
class Students(models.Model):
    """ Contains foreign keys (similar to relations) to user and classroom"""
    student_id=models.ForeignKey(user,on_delete=models.CASCADE,null=True)
    classroom_id=models.ForeignKey(Classrooms,on_delete=models.CASCADE,null=True)

class Teachers(models.Model):
    """ Contains foreign keys (similar to relations) to user and classroom"""
    teacher_id=models.ForeignKey(user,on_delete=models.CASCADE,null=True)
    classroom_id=models.ForeignKey(Classrooms,on_delete=models.CASCADE,null=True)

class Assignments(models.Model):
    """ Contains fields required for storing assignment details and has foreign keys (similar to relations) to user and classroom"""
    assignment_name=models.CharField(max_length=50)
    classroom_id=models.ForeignKey(Classrooms,on_delete=models.CASCADE,null=True)
    due_date=models.DateField()
    due_time=models.TimeField(default=datetime.time(10,10))
    posted_date=models.DateField(auto_now_add=True)
    instructions=models.TextField()
    total_marks=models.IntegerField(default=100)
    valid_extensions = models.CharField(max_length=50,null = True)
    file_directory = models.FileField(upload_to="")
    def __str__(self):
        return self.assignment_name

def upload_location(instance, filename):
    """ location to which the file is to be uploaded """
    return '%s/%s/%s' % (instance.assignment_id.classroom_id.classroom_name,instance.assignment_id.assignment_name, filename)
class Submissions(models.Model):
    """ Contains fields required for storing submission details and has foreign keys (similar to relations) to user and classroom"""
    assignment_id=models.ForeignKey(Assignments,on_delete=models.CASCADE,null=True)
    student_id=models.ForeignKey(Students,on_delete=models.CASCADE,null=True)
    submitted_date=models.DateField(auto_now_add=True)
    submitted_time=models.TimeField(auto_now_add=True)
    submitted_on_time=models.BooleanField(default=True)
    marks_alloted=models.IntegerField(default=0)
    feedback = models.CharField(default="Not yet graded",max_length=100)
    submission_file = models.FileField(upload_to=upload_location)
    filedirectory = models.BooleanField(default= False)
    
class Profile(models.Model):
    """Contains user details along with additional details """
    about_me = models.TextField()
    user_details = models.OneToOneField(user, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_details.username