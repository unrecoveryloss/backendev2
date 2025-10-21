from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.shortcuts import redirect, render
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
)
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import (
    CustomLoginForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
    CustomUserCreationForm
)

Usuario = get_user_model()

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST) 
        if form.is_valid():
            user = form.get_user()   
            login(request, user)

            cargo = getattr(user, 'cargo', None)
            cargo_str = str(cargo).upper() if cargo else None

            if cargo_str == 'ADMIN':
                return redirect('admin_dashboard')
            if cargo_str == 'SUPERVISOR':
                return redirect('supervisor_dashboard')
            if cargo_str == 'OPERADOR':
                return redirect('operador_dashboard')
            if cargo_str == 'CLIENTE':
                return redirect('cliente_dashboard')

            messages.error(request, "No se pudo determinar el cargo del usuario.")
            return redirect('login')
        else:
            return render(request, 'accounts/login.html', {'form': form})
    else:
        form = AuthenticationForm(request)
        return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('login')


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

        cargo = getattr(user, 'cargo', None)
        if cargo:
            cargo_str = str(cargo).lower()
            if cargo_str == 'admin':
                return redirect('admin_dashboard')
            elif cargo_str == 'supervisor':
                return redirect('supervisor_dashboard')
            elif cargo_str == 'operador':
                return redirect('operador_dashboard')
            elif cargo_str == 'cliente':
                return redirect('cliente_dashboard')

        return redirect('login')

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear la cuenta. Revisa los campos.")
        return super().form_invalid(form)


def verificar_cargo(usuario, cargos_permitidos):
    cargo_actual = str(usuario.cargo).upper() if usuario.cargo else None
    return usuario.is_authenticated and cargo_actual in cargos_permitidos


@login_required
def admin_dashboard(request):
    if not verificar_cargo(request.user, ['ADMIN']):
        return redirect('login')
    return render(request, 'dashboards/admin_dashboard.html')


@login_required
def supervisor_dashboard(request):
    if not verificar_cargo(request.user, ['SUPERVISOR', 'ADMIN']):
        return redirect('login')
    return render(request, 'dashboards/supervisor_dashboard.html')


@login_required
def operador_dashboard(request):
    if not verificar_cargo(request.user, ['OPERADOR', 'SUPERVISOR', 'ADMIN']):
        return redirect('login')
    return render(request, 'dashboards/operador_dashboard.html')


@login_required
def cliente_dashboard(request):
    if not verificar_cargo(request.user, ['CLIENTE', 'ADMIN']):
        return redirect('login')
    return render(request, 'dashboards/cliente_dashboard.html')
