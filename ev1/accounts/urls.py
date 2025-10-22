from django.urls import path
from .views import (
    login_view, logout_view, CustomPasswordResetView, 
    CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomRegisterView,
    admin_dashboard, supervisor_dashboard, operador_dashboard, cliente_dashboard
)
from .crud_views import (
    # Usuarios CRUD
    usuarios_list, usuario_create, usuario_edit, usuario_delete,
    # Categorías CRUD
    categorias_list, categoria_create, categoria_edit, categoria_delete,
    # Productos CRUD
    productos_list, producto_create, producto_edit, producto_delete,
    # Proveedores CRUD
    proveedores_list, proveedor_create, proveedor_edit, proveedor_delete,
    # Clientes CRUD
    clientes_list, cliente_create, cliente_edit, cliente_delete,
    # Pedidos CRUD
    pedidos_list, pedido_create, pedido_edit, pedido_delete,
    # Bodegas CRUD
    bodegas_list, bodega_create, bodega_edit, bodega_delete,
    # Turnos CRUD
    turnos_list, turno_create, turno_edit, turno_delete,
    # Movimientos CRUD
    movimientos_list, movimiento_create, movimiento_edit, movimiento_delete,
    # Cliente Pedidos CRUD
    cliente_pedidos_list, cliente_pedido_create, cliente_pedido_edit, cliente_pedido_delete,
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('supervisor/dashboard/', supervisor_dashboard, name='supervisor_dashboard'),
    path('operador/dashboard/', operador_dashboard, name='operador_dashboard'),
    path('cliente/dashboard/', cliente_dashboard, name='cliente_dashboard'),
    
    # URLs CRUD - Usuarios
    path('crud/usuarios/', usuarios_list, name='usuarios_list'),
    path('crud/usuarios/create/', usuario_create, name='usuario_create'),
    path('crud/usuarios/edit/<int:id>/', usuario_edit, name='usuario_edit'),
    path('crud/usuarios/delete/<int:id>/', usuario_delete, name='usuario_delete'),
    
    # URLs CRUD - Categorías
    path('crud/categorias/', categorias_list, name='categorias_list'),
    path('crud/categorias/create/', categoria_create, name='categoria_create'),
    path('crud/categorias/edit/<int:id>/', categoria_edit, name='categoria_edit'),
    path('crud/categorias/delete/<int:id>/', categoria_delete, name='categoria_delete'),
    
    # URLs CRUD - Productos
    path('crud/productos/', productos_list, name='productos_list'),
    path('crud/productos/create/', producto_create, name='producto_create'),
    path('crud/productos/edit/<int:id>/', producto_edit, name='producto_edit'),
    path('crud/productos/delete/<int:id>/', producto_delete, name='producto_delete'),
    
    # URLs CRUD - Proveedores
    path('crud/proveedores/', proveedores_list, name='proveedores_list'),
    path('crud/proveedores/create/', proveedor_create, name='proveedor_create'),
    path('crud/proveedores/edit/<int:id>/', proveedor_edit, name='proveedor_edit'),
    path('crud/proveedores/delete/<int:id>/', proveedor_delete, name='proveedor_delete'),
    
    # URLs CRUD - Clientes
    path('crud/clientes/', clientes_list, name='clientes_list'),
    path('crud/clientes/create/', cliente_create, name='cliente_create'),
    path('crud/clientes/edit/<int:id>/', cliente_edit, name='cliente_edit'),
    path('crud/clientes/delete/<int:id>/', cliente_delete, name='cliente_delete'),
    
    # URLs CRUD - Pedidos
    path('crud/pedidos/', pedidos_list, name='pedidos_list'),
    path('crud/pedidos/create/', pedido_create, name='pedido_create'),
    path('crud/pedidos/edit/<int:id>/', pedido_edit, name='pedido_edit'),
    path('crud/pedidos/delete/<int:id>/', pedido_delete, name='pedido_delete'),
    
    # URLs CRUD - Bodegas
    path('crud/bodegas/', bodegas_list, name='bodegas_list'),
    path('crud/bodegas/create/', bodega_create, name='bodega_create'),
    path('crud/bodegas/edit/<int:id>/', bodega_edit, name='bodega_edit'),
    path('crud/bodegas/delete/<int:id>/', bodega_delete, name='bodega_delete'),
    
    # URLs CRUD - Turnos
    path('crud/turnos/', turnos_list, name='turnos_list'),
    path('crud/turnos/create/', turno_create, name='turno_create'),
    path('crud/turnos/edit/<int:id>/', turno_edit, name='turno_edit'),
    path('crud/turnos/delete/<int:id>/', turno_delete, name='turno_delete'),
    
    # URLs CRUD - Movimientos de Inventario
    path('crud/movimientos/', movimientos_list, name='movimientos_list'),
    path('crud/movimientos/create/', movimiento_create, name='movimiento_create'),
    path('crud/movimientos/edit/<int:id>/', movimiento_edit, name='movimiento_edit'),
    path('crud/movimientos/delete/<int:id>/', movimiento_delete, name='movimiento_delete'),
    
    # URLs CRUD - Cliente Pedidos
    path('crud/cliente/pedidos/', cliente_pedidos_list, name='cliente_pedidos_list'),
    path('crud/cliente/pedidos/create/', cliente_pedido_create, name='cliente_pedido_create'),
    path('crud/cliente/pedidos/edit/<int:id>/', cliente_pedido_edit, name='cliente_pedido_edit'),
    path('crud/cliente/pedidos/delete/<int:id>/', cliente_pedido_delete, name='cliente_pedido_delete'),
]
