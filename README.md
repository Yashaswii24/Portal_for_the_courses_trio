# Portal for Courses
 We developed a learning environment/Course Management System similar to Moodle. Using **Django (Python)**.
## Tech
 - Django(Python)
 - HTML
 - CSS

## Features Implemented
+ Login and Logout pages
+ signup - 2 different pages for students and teachers 
+ Change Profile and Password
+ User Profile
+ Features that teachers can access:
  - create a course which generates a random code with which students can join the course. 
  - can view the course created by him.
  - can create an assignment.
  - can delete the assignment created by him.
  - can view created assignments.
  - can specify the valid extensions for the file to be submitted.
  - can specify the submission file directory tree.
  - can download the submissions of the students.
  - can evaluate the submissions and give feedback.
  
+ Features that students can access:
  - can join the course using the course code.
  - can view all assignments created by teachers.
  - can make the submissions only in given extension.
  - can view his marks,feedback given by the instructor,time and date of submissions.
  - can make multiple submissions.
  - can update his password.

## Contribution of each:
### 210050127
+ Login and Logout.
+ Change Password.
+ User Profile.
+ Create Assignment by teacher.
+ view list of Assignment.
### 210050086
+ SignUp for teacher and student.
+ Create the Course.
+ View the list course.
+ Upload the submissions of students.
+ Restriction in extensions of submission files.
+ File directory tree comparision.
### 210050012
+ Generating the unique code when teacher creates a course.
+ Students joining the course using the code.
+ Downloading the submission files both teacher and student.
+ evaluating the submissions.
+ visibility of marks,time and date of submission of students.
+ Update user profile
## Requirements
Make sure that the following are installed in your terminal before you runserver:
1. Django: pip3 install django
2. django-jquery: pip3 install django-jquery
3. whitenoise: pip3 install whitenoise
4. crispy forms: pip3 install django-crispy-forms
5. django-bootstrap4: pip3 install django-bootstrap4
6. tree : sudo apt-get install tree
## Commands to RunServer
1. python manage.py makemigrations
2. python manage.py migrate
3. python manage.py runserver 
## Features
### Login and SignUp
 Student and Teacher have different signup pages. Username is unique i.e no 2 users can have same username. Both teacher and student has same login page which directs them to different dashboards
### Profile
  Users profile contains the information given during the signup and have a option to change the password 
## Teachers   
### Dashboard
  Dashboard contains options create course,join course,profile and logout  
  
  create course: creates a course with given course name and description,and generates a unique course code which is useful for students to join the course  
  
  courses that are created are visible in the dashboard
### Course Page
 Course page has course name and course code and a option to create assignment  
 
 create assignment: creates assignmnt with following details:
  - Assignment name
  - Due date
  - Due time
  - Instructions
  - Marks
  - Valid Extension 
  - file directory tree
 In valid Extension we can mention multiple extensions ex: '.zip,.tar'.  
 In file directory teacher submits a file which contains the submission file tree directory and the file tree directory should be given through the Instructions by the instructor.
 created assignments are visible in the course page allowing with assignment summary
 
### Assignment Summary
  summary shows number of students registered in the course.Delete assignment option to delete complete assignment  
  
  shows number of submissions,if there are no submission then page is empty or else it contains:
   - submitted student username.
   - submitted time.
   - option to download the sbmission.
   - option to mark and give feedback to the submission.  
   If the submission file directory does not match with given directory tree then there will be no option for teachers to mark or download submission and marks are alloted as zero and feedback will be provided as Incorrect file directory by default.
## Student
### Dashboard
Dashboard contains the options join course,profile and logout  

Join course:  With the help of the code that generated during the create course student can join the respective course  

courses in which a student is joined are visible in the dashboard
### Course Page 
If there are no assignments in course then the course page is empty or else there will be the details of the assignements  

 - Assignment name and description
 - Due date and time
 - Extension in which file to be submitted
 - option to submit assignment and submission summary  

There is facility for students to submit multiple files.
### Submission Summary
submission Summary page is empty if there are no submissions or else it contains details about submission file  

 - Submission date and time
 - Option to download submitted file
 - Marks alloted are visble  
 - feedback is visible  
 
If a student submit multiple files him and the instructor can view only the details of latest submission

