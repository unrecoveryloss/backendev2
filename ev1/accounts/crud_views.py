from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
import json

from .models import Usuario
from catalogo.models import Producto, Categoria
from gestion.models import Cliente, Proveedor, Pedido, Turno, Bodega, MovimientoInventario, Cargo, Trabajador
from .forms import (
    UsuarioForm, ProductoForm, CategoriaForm, 
    ProveedorForm, ClienteForm, PedidoForm, BodegaForm,
    TurnoForm, MovimientoInventarioForm
)
from .views import verificar_cargo

# ==================== USUARIOS CRUD ====================

@login_required
def usuarios_list(request):
    """Lista de usuarios con filtros y paginación"""
    search = request.GET.get('search', '')
    rol_filter = request.GET.get('rol', '')
    estado_filter = request.GET.get('estado', '')
    
    usuarios = Usuario.objects.all()
    
    if search:
        usuarios = usuarios.filter(
            Q(usuario__icontains=search) | 
            Q(nombre__icontains=search) | 
            Q(apellido__icontains=search) |
            Q(email__icontains=search)
        )
    
    if rol_filter:
        usuarios = usuarios.filter(cargo=rol_filter)
    
    if estado_filter:
        usuarios = usuarios.filter(estado=estado_filter)
    
    paginator = Paginator(usuarios, 10)
    page_number = request.GET.get('page')
    usuarios = paginator.get_page(page_number)
    
    context = {
        'usuarios': usuarios,
        'search': search,
        'rol_filter': rol_filter,
        'estado_filter': estado_filter,
    }
    return render(request, 'crud/usuarios_list.html', context)

@login_required
def usuario_create(request):
    """Crear nuevo usuario"""
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('usuarios_list')
        else:
            messages.error(request, 'Error al crear el usuario. Revisa los campos.')
    else:
        form = UsuarioForm()
    
    return render(request, 'crud/usuario_form.html', {'form': form, 'action': 'create'})

@login_required
def usuario_edit(request, id):
    """Editar usuario existente"""
    usuario = get_object_or_404(Usuario, id=id)
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado exitosamente.')
            return redirect('usuarios_list')
        else:
            messages.error(request, 'Error al actualizar el usuario. Revisa los campos.')
    else:
        form = UsuarioForm(instance=usuario)
    
    return render(request, 'crud/usuario_form.html', {'form': form, 'action': 'edit', 'usuario': usuario})

@login_required
def usuario_delete(request, id):
    """Eliminar usuario"""
    if request.method == 'POST':
        usuario = get_object_or_404(Usuario, id=id)
        usuario.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
        return JsonResponse({'success': True, 'message': 'Usuario eliminado exitosamente.'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

# ==================== CATEGORÍAS CRUD ====================

@login_required
def categorias_list(request):
    """Lista de categorías"""
    search = request.GET.get('search', '')
    
    categorias = Categoria.objects.all()
    
    if search:
        categorias = categorias.filter(nombre__icontains=search)
    
    paginator = Paginator(categorias, 10)
    page_number = request.GET.get('page')
    categorias = paginator.get_page(page_number)
    
    context = {
        'categorias': categorias,
        'search': search,
    }
    return render(request, 'crud/categorias_list.html', context)

@login_required
def categoria_create(request):
    """Crear nueva categoría"""
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('categorias_list')
        else:
            messages.error(request, 'Error al crear la categoría. Revisa los campos.')
    else:
        form = CategoriaForm()
    
    return render(request, 'crud/categoria_form.html', {'form': form, 'action': 'create'})

@login_required
def categoria_edit(request, id):
    """Editar categoría existente"""
    categoria = get_object_or_404(Categoria, id=id)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente.')
            return redirect('categorias_list')
        else:
            messages.error(request, 'Error al actualizar la categoría. Revisa los campos.')
    else:
        form = CategoriaForm(instance=categoria)
    
    return render(request, 'crud/categoria_form.html', {'form': form, 'action': 'edit', 'categoria': categoria})

@login_required
def categoria_delete(request, id):
    """Eliminar categoría"""
    if request.method == 'POST':
        categoria = get_object_or_404(Categoria, id=id)
        categoria.delete()
        messages.success(request, 'Categoría eliminada exitosamente.')
        return JsonResponse({'success': True, 'message': 'Categoría eliminada exitosamente.'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

# ==================== PRODUCTOS CRUD ====================

@login_required
def productos_list(request):
    """Lista de productos con filtros"""
    search = request.GET.get('search', '')
    categoria_filter = request.GET.get('categoria', '')
    
    productos = Producto.objects.all()
    
    if search:
        productos = productos.filter(
            Q(nombre__icontains=search) | 
            Q(sku__icontains=search) |
            Q(descripcion__icontains=search)
        )
    
    if categoria_filter:
        productos = productos.filter(categoria_id=categoria_filter)
    
    paginator = Paginator(productos, 10)
    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)
    
    context = {
        'productos': productos,
        'categorias': Categoria.objects.all(),
        'search': search,
        'categoria_filter': categoria_filter,
    }
    return render(request, 'crud/productos_list.html', context)

@login_required
def producto_create(request):
    """Crear nuevo producto"""
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('productos_list')
        else:
            messages.error(request, 'Error al crear el producto. Revisa los campos.')
    else:
        form = ProductoForm()
    
    categorias = Categoria.objects.all()
    return render(request, 'crud/producto_form.html', {
        'form': form, 
        'action': 'create',
        'categorias': categorias
    })

@login_required
def producto_edit(request, id):
    """Editar producto existente"""
    producto = get_object_or_404(Producto, id=id)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('productos_list')
        else:
            messages.error(request, 'Error al actualizar el producto. Revisa los campos.')
    else:
        form = ProductoForm(instance=producto)
    
    categorias = Categoria.objects.all()
    return render(request, 'crud/producto_form.html', {
        'form': form, 
        'action': 'edit', 
        'producto': producto,
        'categorias': categorias
    })

@login_required
def producto_delete(request, id):
    """Eliminar producto"""
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=id)
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return JsonResponse({'success': True, 'message': 'Producto eliminado exitosamente.'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

# ==================== PROVEEDORES CRUD ====================

@login_required
def proveedores_list(request):
    """Lista de proveedores con filtros"""
    search = request.GET.get('search', '')
    estado_filter = request.GET.get('estado', '')
    
    proveedores = Proveedor.objects.all()
    
    if search:
        proveedores = proveedores.filter(
            Q(rut_nif__icontains=search) | 
            Q(razon_social__icontains=search) |
            Q(nombre_fantasia__icontains=search)
        )
    
    if estado_filter:
        proveedores = proveedores.filter(estado=estado_filter)
    
    paginator = Paginator(proveedores, 10)
    page_number = request.GET.get('page')
    proveedores = paginator.get_page(page_number)
    
    context = {
        'proveedores': proveedores,
        'search': search,
        'estado_filter': estado_filter,
    }
    return render(request, 'crud/proveedores_list.html', context)

@login_required
def proveedor_create(request):
    """Crear nuevo proveedor"""
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor creado exitosamente.')
            return redirect('proveedores_list')
        else:
            messages.error(request, 'Error al crear el proveedor. Revisa los campos.')
    else:
        form = ProveedorForm()
    
    return render(request, 'crud/proveedor_form.html', {'form': form, 'action': 'create'})

@login_required
def proveedor_edit(request, id):
    """Editar proveedor existente"""
    proveedor = get_object_or_404(Proveedor, id=id)
    
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor actualizado exitosamente.')
            return redirect('proveedores_list')
        else:
            messages.error(request, 'Error al actualizar el proveedor. Revisa los campos.')
    else:
        form = ProveedorForm(instance=proveedor)
    
    return render(request, 'crud/proveedor_form.html', {'form': form, 'action': 'edit', 'proveedor': proveedor})

@login_required
def proveedor_delete(request, id):
    """Eliminar proveedor"""
    if request.method == 'POST':
        proveedor = get_object_or_404(Proveedor, id=id)
        proveedor.delete()
        messages.success(request, 'Proveedor eliminado exitosamente.')
        return JsonResponse({'success': True, 'message': 'Proveedor eliminado exitosamente.'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

# ==================== CLIENTES CRUD ====================

@login_required
def clientes_list(request):
    """Lista de clientes con filtros"""
    search = request.GET.get('search', '')
    
    clientes = Cliente.objects.all()
    
    if search:
        clientes = clientes.filter(
            Q(nombre__icontains=search) | 
            Q(email__icontains=search)
        )
    
    paginator = Paginator(clientes, 10)
    page_number = request.GET.get('page')
    clientes = paginator.get_page(page_number)
    
    context = {
        'clientes': clientes,
        'search': search,
    }
    return render(request, 'crud/clientes_list.html', context)

@login_required
def cliente_create(request):
    """Crear nuevo cliente"""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado exitosamente.')
            return redirect('clientes_list')
        else:
            messages.error(request, 'Error al crear el cliente. Revisa los campos.')
    else:
        form = ClienteForm()
    
    return render(request, 'crud/cliente_form.html', {'form': form, 'action': 'create'})

@login_required
def cliente_edit(request, id):
    """Editar cliente existente"""
    cliente = get_object_or_404(Cliente, id=id)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado exitosamente.')
            return redirect('clientes_list')
        else:
            messages.error(request, 'Error al actualizar el cliente. Revisa los campos.')
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'crud/cliente_form.html', {'form': form, 'action': 'edit', 'cliente': cliente})

@login_required
def cliente_delete(request, id):
    """Eliminar cliente"""
    if request.method == 'POST':
        cliente = get_object_or_404(Cliente, id=id)
        cliente.delete()
        messages.success(request, 'Cliente eliminado exitosamente.')
        return JsonResponse({'success': True, 'message': 'Cliente eliminado exitosamente.'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

# ==================== PEDIDOS CRUD ====================

@login_required
def pedidos_list(request):
    """Lista de pedidos con filtros"""
    search = request.GET.get('search', '')
    estado_filter = request.GET.get('estado', '')
    
    pedidos = Pedido.objects.all().select_related('cliente')
    
    if search:
        pedidos = pedidos.filter(
            Q(id__icontains=search) | 
            Q(cliente__nombre__icontains=search) |
            Q(direccion_envio__icontains=search)
        )
    
    if estado_filter:
        pedidos = pedidos.filter(estado=estado_filter)
    
    paginator = Paginator(pedidos, 10)
    page_number = request.GET.get('page')
    pedidos = paginator.get_page(page_number)
    
    context = {
        'pedidos': pedidos,
        'search': search,
        'estado_filter': estado_filter,
    }
    return render(request, 'crud/pedidos_list.html', context)

@login_required
def pedido_create(request):
    """Crear nuevo pedido"""
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pedido creado exitosamente.')
            return redirect('pedidos_list')
        else:
            messages.error(request, 'Error al crear el pedido. Revisa los campos.')
    else:
        form = PedidoForm()
    
    # Solo usuarios con cargo CLIENTE
    clientes = Usuario.objects.filter(cargo='CLIENTE')
    productos = Producto.objects.all()
    return render(request, 'crud/pedido_form.html', {
        'form': form, 
        'action': 'create',
        'clientes': clientes,
        'productos': productos,
        'module_title': 'Crear Nuevo Pedido',
        'module_description': 'Registra un nuevo pedido para un cliente.'
    })

@login_required
def pedido_edit(request, id):
    """Editar pedido existente"""
    pedido = get_object_or_404(Pedido, id=id)
    
    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pedido actualizado exitosamente.')
            return redirect('pedidos_list')
        else:
            messages.error(request, 'Error al actualizar el pedido. Revisa los campos.')
    else:
        form = PedidoForm(instance=pedido)
    
    # Solo usuarios con cargo CLIENTE
    clientes = Usuario.objects.filter(cargo='CLIENTE')
    productos = Producto.objects.all()
    return render(request, 'crud/pedido_form.html', {
        'form': form, 
        'action': 'edit', 
        'pedido': pedido,
        'clientes': clientes,
        'productos': productos,
        'module_title': 'Editar Pedido',
        'module_description': 'Modifica la información del pedido.'
    })

@login_required
def pedido_delete(request, id):
    """Eliminar pedido"""
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=id)
        pedido.delete()
        messages.success(request, 'Pedido eliminado exitosamente.')
        return JsonResponse({'success': True, 'message': 'Pedido eliminado exitosamente.'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

# ==================== BODEGAS CRUD ====================

@login_required
def bodegas_list(request):
    """Lista de bodegas con filtros"""
    search = request.GET.get('search', '')
    
    bodegas = Bodega.objects.all()
    
    if search:
        bodegas = bodegas.filter(
            Q(nombre__icontains=search) | 
            Q(ubicacion__icontains=search)
        )
    
    paginator = Paginator(bodegas, 10)
    page_number = request.GET.get('page')
    bodegas = paginator.get_page(page_number)
    
    context = {
        'bodegas': bodegas,
        'search': search,
    }
    return render(request, 'crud/bodegas_list.html', context)

@login_required
def bodega_create(request):
    """Crear nueva bodega"""
    if request.method == 'POST':
        form = BodegaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bodega creada exitosamente.')
            return redirect('bodegas_list')
        else:
            messages.error(request, 'Error al crear la bodega. Revisa los campos.')
    else:
        form = BodegaForm()
    
    return render(request, 'crud/bodega_form.html', {'form': form, 'action': 'create'})

@login_required
def bodega_edit(request, id):
    """Editar bodega existente"""
    bodega = get_object_or_404(Bodega, id=id)
    
    if request.method == 'POST':
        form = BodegaForm(request.POST, instance=bodega)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bodega actualizada exitosamente.')
            return redirect('bodegas_list')
        else:
            messages.error(request, 'Error al actualizar la bodega. Revisa los campos.')
    else:
        form = BodegaForm(instance=bodega)
    
    return render(request, 'crud/bodega_form.html', {'form': form, 'action': 'edit', 'bodega': bodega})

@login_required
def bodega_delete(request, id):
    """Eliminar bodega"""
    if request.method == 'POST':
        bodega = get_object_or_404(Bodega, id=id)
        bodega.delete()
        messages.success(request, 'Bodega eliminada exitosamente.')
        return JsonResponse({'success': True, 'message': 'Bodega eliminada exitosamente.'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

# ==================== TURNOS CRUD ====================

@login_required
def turnos_list(request):
    """Lista de turnos con filtros"""
    search = request.GET.get('search', '')
    fecha_filter = request.GET.get('fecha', '')
    
    turnos = Turno.objects.all().select_related('trabajador', 'trabajador__cargo')
    
    if search:
        turnos = turnos.filter(
            Q(trabajador__nombre__icontains=search) | 
            Q(trabajador__rut__icontains=search)
        )
    
    if fecha_filter:
        turnos = turnos.filter(fecha=fecha_filter)
    
    paginator = Paginator(turnos, 10)
    page_number = request.GET.get('page')
    turnos = paginator.get_page(page_number)
    
    context = {
        'turnos': turnos,
        'search': search,
        'fecha_filter': fecha_filter,
    }
    return render(request, 'crud/turnos_list.html', context)

@login_required
def turno_create(request):
    """Crear nuevo turno"""
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Turno creado exitosamente.')
            return redirect('turnos_list')
        else:
            messages.error(request, 'Error al crear el turno. Revisa los campos.')
    else:
        form = TurnoForm()
    
    # Obtener todos los usuarios excepto clientes
    trabajadores = Usuario.objects.exclude(cargo='CLIENTE')
    return render(request, 'crud/turno_form.html', {
        'form': form, 
        'action': 'create',
        'trabajadores': trabajadores,
        'module_title': 'Crear Nuevo Turno',
        'module_description': 'Asigna un turno de trabajo a un empleado.'
    })

@login_required
def turno_edit(request, id):
    """Editar turno existente"""
    turno = get_object_or_404(Turno, id=id)
    
    if request.method == 'POST':
        form = TurnoForm(request.POST, instance=turno)
        if form.is_valid():
            form.save()
            messages.success(request, 'Turno actualizado exitosamente.')
            return redirect('turnos_list')
        else:
            messages.error(request, 'Error al actualizar el turno. Revisa los campos.')
    else:
        form = TurnoForm(instance=turno)
    
    # Obtener todos los usuarios excepto clientes
    trabajadores = Usuario.objects.exclude(cargo='CLIENTE')
    return render(request, 'crud/turno_form.html', {
        'form': form, 
        'action': 'edit', 
        'turno': turno,
        'trabajadores': trabajadores,
        'module_title': 'Editar Turno',
        'module_description': 'Modifica la información del turno de trabajo.'
    })

@login_required
def turno_delete(request, id):
    """Eliminar turno"""
    if request.method == 'POST':
        turno = get_object_or_404(Turno, id=id)
        turno.delete()
        messages.success(request, 'Turno eliminado exitosamente.')
        return JsonResponse({'success': True, 'message': 'Turno eliminado exitosamente.'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

# ==================== MOVIMIENTOS DE INVENTARIO CRUD ====================

@login_required
def movimientos_list(request):
    """Lista de movimientos de inventario con filtros"""
    search = request.GET.get('search', '')
    tipo_filter = request.GET.get('tipo', '')
    fecha_filter = request.GET.get('fecha', '')
    
    movimientos = MovimientoInventario.objects.all().select_related('producto', 'proveedor', 'bodega')
    
    if search:
        movimientos = movimientos.filter(
            Q(producto__nombre__icontains=search) | 
            Q(producto__sku__icontains=search) |
            Q(lote__icontains=search) |
            Q(serie__icontains=search)
        )
    
    if tipo_filter:
        movimientos = movimientos.filter(tipo=tipo_filter)
    
    if fecha_filter:
        movimientos = movimientos.filter(fecha__date=fecha_filter)
    
    paginator = Paginator(movimientos, 10)
    page_number = request.GET.get('page')
    movimientos = paginator.get_page(page_number)
    
    context = {
        'movimientos': movimientos,
        'search': search,
        'tipo_filter': tipo_filter,
        'fecha_filter': fecha_filter,
    }
    return render(request, 'crud/movimientos_list.html', context)

@login_required
def movimiento_create(request):
    """Crear nuevo movimiento de inventario"""
    if request.method == 'POST':
        form = MovimientoInventarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movimiento de inventario creado exitosamente.')
            return redirect('movimientos_list')
        else:
            messages.error(request, 'Error al crear el movimiento. Revisa los campos.')
    else:
        form = MovimientoInventarioForm()
    
    productos = Producto.objects.all()
    proveedores = Proveedor.objects.all()
    bodegas = Bodega.objects.all()
    return render(request, 'crud/movimiento_form.html', {
        'form': form, 
        'action': 'create',
        'productos': productos,
        'proveedores': proveedores,
        'bodegas': bodegas,
        'module_title': 'Crear Movimiento de Inventario',
        'module_description': 'Registra un nuevo movimiento de inventario.'
    })

@login_required
def movimiento_edit(request, id):
    """Editar movimiento de inventario existente"""
    movimiento = get_object_or_404(MovimientoInventario, id=id)
    
    if request.method == 'POST':
        form = MovimientoInventarioForm(request.POST, instance=movimiento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movimiento de inventario actualizado exitosamente.')
            return redirect('movimientos_list')
        else:
            messages.error(request, 'Error al actualizar el movimiento. Revisa los campos.')
    else:
        form = MovimientoInventarioForm(instance=movimiento)
    
    productos = Producto.objects.all()
    proveedores = Proveedor.objects.all()
    bodegas = Bodega.objects.all()
    return render(request, 'crud/movimiento_form.html', {
        'form': form, 
        'action': 'edit', 
        'movimiento': movimiento,
        'productos': productos,
        'proveedores': proveedores,
        'bodegas': bodegas,
        'module_title': 'Editar Movimiento de Inventario',
        'module_description': 'Modifica la información del movimiento de inventario.'
    })

@login_required
def movimiento_delete(request, id):
    """Eliminar movimiento de inventario"""
    if request.method == 'POST':
        movimiento = get_object_or_404(MovimientoInventario, id=id)
        movimiento.delete()
        messages.success(request, 'Movimiento de inventario eliminado exitosamente.')
        return JsonResponse({'success': True, 'message': 'Movimiento de inventario eliminado exitosamente.'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

# ==================== PEDIDOS CLIENTE CRUD ====================

@login_required
def cliente_pedidos_list(request):
    """Lista de pedidos del cliente actual"""
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
    
    search = request.GET.get('search', '')
    estado_filter = request.GET.get('estado', '')
    
    if search:
        pedidos = pedidos.filter(
            Q(id__icontains=search) | 
            Q(direccion_envio__icontains=search)
        )
    
    if estado_filter:
        pedidos = pedidos.filter(estado=estado_filter)
    
    paginator = Paginator(pedidos, 10)
    page_number = request.GET.get('page')
    pedidos = paginator.get_page(page_number)
    
    context = {
        'pedidos': pedidos,
        'search': search,
        'estado_filter': estado_filter,
        'cliente': cliente
    }
    return render(request, 'crud/cliente_pedidos_list.html', context)

@login_required
def cliente_pedido_create(request):
    """Crear nuevo pedido para el cliente actual"""
    if not verificar_cargo(request.user, ['CLIENTE', 'ADMIN']):
        return redirect('login')
    
    # Buscar el cliente asociado al usuario actual
    try:
        cliente = Cliente.objects.get(email=request.user.email)
    except Cliente.DoesNotExist:
        # Si no existe el cliente, crear uno automáticamente
        cliente = Cliente.objects.create(
            nombre=request.user.nombre or request.user.usuario,
            email=request.user.email,
            telefono=request.user.telefono
        )
    
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.cliente = cliente
            pedido.save()
            messages.success(request, 'Pedido creado exitosamente.')
            return redirect('cliente_pedidos_list')
        else:
            messages.error(request, 'Error al crear el pedido. Revisa los campos.')
    else:
        form = PedidoForm()
    
    # Obtener todos los productos disponibles
    productos = Producto.objects.all()
    return render(request, 'crud/cliente_pedido_form.html', {
        'form': form, 
        'action': 'create',
        'productos': productos,
        'cliente': cliente,
        'module_title': 'Crear Nuevo Pedido',
        'module_description': 'Selecciona los productos y completa la información de envío.'
    })

@login_required
def cliente_pedido_edit(request, id):
    """Editar pedido del cliente actual"""
    if not verificar_cargo(request.user, ['CLIENTE', 'ADMIN']):
        return redirect('login')
    
    # Buscar el cliente asociado al usuario actual
    try:
        cliente = Cliente.objects.get(email=request.user.email)
    except Cliente.DoesNotExist:
        return redirect('cliente_pedidos_list')
    
    pedido = get_object_or_404(Pedido, id=id, cliente=cliente)
    
    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pedido actualizado exitosamente.')
            return redirect('cliente_pedidos_list')
        else:
            messages.error(request, 'Error al actualizar el pedido. Revisa los campos.')
    else:
        form = PedidoForm(instance=pedido)
    
    # Obtener todos los productos disponibles
    productos = Producto.objects.all()
    return render(request, 'crud/cliente_pedido_form.html', {
        'form': form, 
        'action': 'edit', 
        'pedido': pedido,
        'productos': productos,
        'cliente': cliente,
        'module_title': 'Editar Mi Pedido',
        'module_description': 'Modifica los productos y la información de envío.'
    })

@login_required
def cliente_pedido_delete(request, id):
    """Eliminar pedido del cliente actual"""
    if not verificar_cargo(request.user, ['CLIENTE', 'ADMIN']):
        return redirect('login')
    
    # Buscar el cliente asociado al usuario actual
    try:
        cliente = Cliente.objects.get(email=request.user.email)
    except Cliente.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Cliente no encontrado.'})
    
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=id, cliente=cliente)
        pedido.delete()
        messages.success(request, 'Pedido eliminado exitosamente.')
        return JsonResponse({'success': True, 'message': 'Pedido eliminado exitosamente.'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})
