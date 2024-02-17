from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # name of the url where to redirect after a successful registration

    def form_valid(self, form):
        # save the new user
        form.save()
        return super().form_valid(form)
    

class UserLoginView(LoginView):
    template_name = 'login.html'
    

class UserLogoutView(LogoutView):
    next_page = 'login'  # specify the page to redirect to after logout, usually homepage
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class LoginSuccessView(TemplateView):
    template_name = 'login_success.html'