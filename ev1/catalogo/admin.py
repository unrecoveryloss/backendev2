from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, Producto

class ProductoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'precio_venta', 'uom_compra', 'categoria', 'descripcion', 'acciones', 'stock_actual', 'alerta_bajo_stock', 'alerta_por_vencer']
    search_fields = ['nombre', 'descripcion']
    list_filter = ['categoria']
    ordering = ['id']
    def acciones(self, obj):
        return format_html(
            '<a style="background:#4CAF50;color:white;padding:4px 8px;border-radius:4px;text-decoration:none;margin-right:4px;" href="{}">Editar</a>'
            '<a style="background:#f44336;color:white;padding:4px 8px;border-radius:4px;text-decoration:none;" href="{}">Eliminar</a>',
            f'/admin/catalogo/producto/{obj.id}/change/',
            f'/admin/catalogo/producto/{obj.id}/delete/'
        )
    acciones.short_description = 'Acciones'

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'acciones']
    search_fields = ['nombre']
    ordering = ['id']
    def acciones(self, obj):
        return format_html(
            '<a style="background:#4CAF50;color:white;padding:4px 8px;border-radius:4px;text-decoration:none;margin-right:4px;" href="{}">Editar</a>'
            '<a style="background:#f44336;color:white;padding:4px 8px;border-radius:4px;text-decoration:none;" href="{}">Eliminar</a>',
            f'/admin/catalogo/categoria/{obj.id}/change/',
            f'/admin/catalogo/categoria/{obj.id}/delete/'
        )
    acciones.short_description = 'Acciones'


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)



