from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView

from .forms import StudentSignUpForm
from .models import user
from .views import home1
class StudentSignUpView(CreateView):
    """Creates the user with details contained in the form and bool valued field "is_student" assigned as true
    """
    model = user
    form_class = StudentSignUpForm
    template_name = 'accounts/register_student.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(home1)