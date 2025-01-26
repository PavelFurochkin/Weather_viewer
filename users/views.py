from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import FormView
from users.forms import RegistrationForm, AuthorizationForm


class UserRegistration(FormView):
    form_class = RegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class UserLogin(FormView):
    form_class = AuthorizationForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    # success_url = reverse_lazy('weather_app:main')

    def get_success_url(self):
        return reverse_lazy('weather_app:main')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class LogoutUser(LogoutView):
    next_page = reverse_lazy('users:login')
