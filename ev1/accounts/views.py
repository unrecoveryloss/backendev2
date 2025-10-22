from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.shortcuts import redirect, render
from django.utils import timezone
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
)

from .models import Usuario
from catalogo.models import Producto, Categoria
from gestion.models  import Cliente, Proveedor, Pedido, Turno, Bodega, MovimientoInventario, Cargo
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import (
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
            # Actualizar último acceso
            user.ultimo_acceso = timezone.now()
            user.session_count += 1
            user.save()
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
    
    context = {
        'user': request.user,
        'usuarios': Usuario.objects.all(),
        'productos': Producto.objects.all(),
        'categorias': Categoria.objects.all(),
        'proveedores': Proveedor.objects.all(),
        'pedidos': Pedido.objects.all(),
        'inventarios': Bodega.objects.all(),
        'reportes': True 
    }
    return render(request, 'dashboards/admin_dashboard.html', context)


@login_required
def supervisor_dashboard(request):
    if not verificar_cargo(request.user, ['SUPERVISOR', 'ADMIN']):
        return redirect('login')
    
    context = {
        'user': request.user,
        'productos': Producto.objects.all(),
        'proveedores': Proveedor.objects.all(),
        'pedidos': Pedido.objects.all(),
        'inventarios': Bodega.objects.all(),
        'turnos': Turno.objects.all(),
        'movimientos': MovimientoInventario.objects.all(),
        'clientes': Cliente.objects.all()
    }
    return render(request, 'dashboards/supervisor_dashboard.html', context)


@login_required
def operador_dashboard(request):
    if not verificar_cargo(request.user, ['OPERADOR', 'SUPERVISOR', 'ADMIN']):
        return redirect('login')
    
    context = {
        'user': request.user,
        'productos': Producto.objects.all(),
        'categorias': Categoria.objects.all(),
        'pedidos': Pedido.objects.all(),
        'inventarios': Bodega.objects.all(),
        'clientes': Cliente.objects.all()
    }
    return render(request, 'dashboards/operador_dashboard.html', context)


@login_required
def cliente_dashboard(request):
    if not verificar_cargo(request.user, ['CLIENTE', 'ADMIN']):
        return redirect('login')
    
    # Buscar el cliente asociado al usuario actual
    try:
        cliente = Cliente.objects.get(email=request.user.email)
        pedidos = Pedido.objects.filter(cliente=cliente)
    except Cliente.DoesNotExist:
        # Si no existe el cliente, crear uno automáticamente
        cliente = Cliente.objects.create(
            nombre=request.user.nombre or request.user.usuario,
            email=request.user.email,
            telefono=request.user.telefono
        )
        pedidos = Pedido.objects.none()
    
    context = {
        'user': request.user,
        'productos': Producto.objects.all(),  # Mostrar todos los productos para clientes
        'pedidos': pedidos,
        'perfil': request.user,
        'cliente': cliente
    }
    return render(request, 'dashboards/cliente_dashboard.html', context)


@login_required
def dashboard_view(request):
    user = request.user
    cargo = user.cargo

    context = {'user': user}

    if cargo == 'ADMIN':
        context.update({
            'usuarios': Usuario.objects.all(),
            'productos': Producto.objects.all(),
            'proveedores': Proveedor.objects.all(),
            'pedidos': Pedido.objects.all(),
            'inventarios': Bodega.objects.all(),
            'reportes': True 
        })
        return render(request, 'admin_dashboard.html', context)

    elif cargo == 'SUPERVISOR':
        context.update({
            'productos': Producto.objects.all(),
            'proveedores': Proveedor.objects.all(),
            'pedidos': Pedido.objects.all(),
            'inventarios': Bodega.objects.all(),
            'turnos': Turno.objects.all(),
            'movimientos': MovimientoInventario.objects.all(),
            'clientes': Cliente.objects.all()
        })
        return render(request, 'dashboards/supervisor_dashboard.html', context)

    elif cargo == 'OPERADOR':
        context.update({
            'productos': Producto.objects.all(),
            'pedidos': Pedido.objects.all(),
            'inventarios': Bodega.objects.all(),
            'clientes': Cliente.objects.all()
        })
        return render(request, 'operador_dashboard.html', context)

    elif cargo == 'CLIENTE':
        context.update({
            'productos': Producto.objects.filter(activo=True),
            'pedidos': Pedido.objects.filter(cliente=user),
            'perfil': user
        })
        return render(request, 'cliente_dashboard.html', context)

    else:
        return render(request, 'error.html', {'mensaje': 'No se reconoce el rol del usuario'})
    
