from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomLoginForm, CustomPasswordResetForm, CustomSetPasswordForm, CustomUserCreationForm
from django.contrib.auth import logout

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomLoginForm

def logout_view(request):
    logout(request)
    return render(request, 'accounts/logout.html')
    
class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    form_class = CustomPasswordResetForm
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('login')


class CustomRegisterView(CreateView):
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user) 
        messages.success(self.request, "Tu cuenta ha sido creada correctamente.")
        return redirect('inicio')  

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear la cuenta. Revisa los campos.")
        return super().form_invalid(form)

