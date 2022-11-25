from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView

from .forms import TeacherSignUpForm
from .models import user
from .views import home2

class TeacherSignUpView(CreateView):
    """Creates the user with details contained in the form and bool valued field "is_teacher" assigned as true
    """
    model = user
    form_class = TeacherSignUpForm
    template_name = 'accounts/register_teacher.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(home2)