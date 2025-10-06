from django.contrib import admin
from .models import Categoria, Producto, Cargo, Trabajador, Turno, Cliente, Pedido

class ProductoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'precio', 'categoria', 'descripcion']
    search_fields = ['nombre', 'descripcion']
    list_filter = ['categoria']
    ordering = ['id']

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']
    search_fields = ['nombre']
    ordering = ['id']

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'descripcion']
    search_fields = ['nombre']


@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'rut', 'cargo']
    list_filter = ['cargo']
    search_fields = ['nombre', 'rut']

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ['id', 'trabajador', 'fecha', 'horario_inicio', 'horario_fin']
    list_filter = ['fecha', 'trabajador']

class ClienteAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'apellido', 'telefono', 'correo']
    search_fields = ['nombre', 'correo']
    ordering = ['id']

class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'producto', 'cliente', 'cantidad', 'direccion', 'telefono', 'fecha', 'estado']
    search_fields = ['producto', 'cliente']
    ordering = ['id']

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Pedido, PedidoAdmin)



