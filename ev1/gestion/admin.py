from django.contrib import admin
from django.utils.html import format_html
from .models import Cliente, Pedido, Cargo, Trabajador, Turno, MovimientoInventario, Proveedor, Bodega

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'acciones')
    search_fields = ('nombre', 'email')
    def acciones(self, obj):
        return format_html(
            '<a style="background:#4CAF50;color:white;padding:4px 8px;border-radius:4px;text-decoration:none;margin-right:4px;" href="{}">Editar</a>'
            '<a style="background:#f44336;color:white;padding:4px 8px;border-radius:4px;text-decoration:none;" href="{}">Eliminar</a>',
            f'/admin/gestion/cliente/{obj.id}/change/',
            f'/admin/gestion/cliente/{obj.id}/delete/'
        )
    
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha_pedido', 'estado', 'acciones')
    list_filter = ('estado', 'fecha_pedido')
    search_fields = ('cliente__nombre', 'id')
    date_hierarchy = 'fecha_pedido'
    def acciones(self, obj):
        return format_html(
            '<a style="background:#4CAF50;color:white;padding:4px 8px;border-radius:4px;text-decoration:none;margin-right:4px;" href="{}">Editar</a>'
            '<a style="background:#f44336;color:white;padding:4px 8px;border-radius:4px;text-decoration:none;" href="{}">Eliminar</a>',
            f'/admin/gestion/pedido/{obj.id}/change/',
            f'/admin/gestion/pedido/{obj.id}/change/',
        )
    
@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'tipo', 'producto', 'proveedor', 'bodega', 'cantidad', 'acciones']
    list_filter = ['tipo', 'bodega', 'proveedor']
    search_fields = ['producto__nombre', 'proveedor__nombre', 'bodega__nombre']
    list_per_page = 10
    ordering = ['-fecha']
    actions = ['exportar_excel']
    def acciones(self, obj):
        return format_html(
            '<a style="background:#4CAF50;color:white;padding:4px 8px;border-radius:4px;text-decoration:none;margin-right:4px;" href="{}">Editar</a>'
            '<a style="background:#f44336;color:white;padding:4px 8px;border-radius:4px;text-decoration:none;" href="{}">Eliminar</a>',
            f'/admin/gestion/movimientoinventario/{obj.id}/change/',
            f'/admin/gestion/movimientoinventario/{obj.id}/delete/'
        )

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['rut_nif', 'razon_social', 'email', 'estado', 'acciones']
    search_fields = ['nombre']
    def acciones(self, obj):
        return format_html(
            '<a style="background:#4CAF50;color:white;padding:4px 8px;border-radius:4px;text-decoration:none;margin-right:4px;" href="{}">Editar</a>'
            '<a style="background:#f44336;color:white;padding:4px 8px;border-radius:4px;text-decoration:none;" href="{}">Eliminar</a>',
            f'/admin/gestion/proveedor/{obj.id}/change/',
            f'/admin/gestion/proveedor/{obj.id}/delete/'
        )

@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ubicacion', 'acciones']
    search_fields = ['nombre']
    def acciones(self, obj):
        return format_html(
            '<a style="background:#4CAF50;color:white;padding:4px 8px;border-radius:4px;text-decoration:none;margin-right:4px;" href="{}">Editar</a>'
            '<a style="background:#f44336;color:white;padding:4px 8px;border-radius:4px;text-decoration:none;" href="{}">Eliminar</a>',
            f'/admin/gestion/bodega/{obj.id}/change/',
            f'/admin/gestion/bodega/{obj.id}/delete/'
        )

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'descripcion', 'acciones']
    search_fields = ['nombre']
    def acciones(self, obj):
        return format_html(
            '<a style="background:#4CAF50;color:white;padding:4px 8px;border-radius:4px;text-decoration:none;margin-right:4px;" href="{}">Editar</a>'
            '<a style="background:#f44336;color:white;padding:4px 8px;border-radius:4px;text-decoration:none;" href="{}">Eliminar</a>',
            f'/admin/gestion/cargo/{obj.id}/change/',
            f'/admin/gestion/cargo/{obj.id}/delete/'
        )

@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'rut', 'cargo', 'acciones']
    list_filter = ['cargo']
    search_fields = ['nombre', 'rut']
    def acciones(self, obj):
        return format_html(
            '<a style="background:#4CAF50;color:white;padding:4px 8px;border-radius:4px;text-decoration:none;margin-right:4px;" href="{}">Editar</a>'
            '<a style="background:#f44336;color:white;padding:4px 8px;border-radius:4px;text-decoration:none;" href="{}">Eliminar</a>',
            f'/admin/gestion/trabajador/{obj.id}/change/',
            f'/admin/gestion/trabajador/{obj.id}/delete/'
        )

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ['id', 'trabajador', 'fecha', 'horario_inicio', 'horario_fin', 'acciones']
    list_filter = ['fecha', 'trabajador']
    def acciones(self, obj):
        return format_html(
            '<a style="background:#4CAF50;color:white;padding:4px 8px;border-radius:4px;text-decoration:none;margin-right:4px;" href="{}">Editar</a>'
            '<a style="background:#f44336;color:white;padding:4px 8px;border-radius:4px;text-decoration:none;" href="{}">Eliminar</a>',
            f'/admin/gestion/turno/{obj.id}/change/',
            f'/admin/gestion/turno/{obj.id}/delete/'
        )


admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Pedido, PedidoAdmin)
# Register your models here.
