from django.contrib import admin
from django.utils.html import format_html
from .models import Usuario
from django.http import HttpResponse
import csv

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = [
        'usuario', 'email', 'nombre', 'apellido',
        'telefono', 'cargo', 'estado_coloreado', 'mfa_activado',
        'ultimo_acceso', 'session_count', 'acciones',
    ]
    list_filter = ('cargo', 'estado', 'mfa')
    search_fields = ('usuario', 'email', 'nombre', 'apellido')
    ordering = ('usuario',)
    readonly_fields = ('fecha_creacion', 'ultimo_acceso')

    fieldsets = (
        ('Identificación', {
            'fields': ('usuario', 'email', 'nombre', 'apellido', 'telefono')
        }),
        ('Estado y acceso', {
            'fields': ('cargo', 'estado', 'mfa', 'is_staff', 'ultimo_acceso', 'session_count')
        }),
    )

    actions = ['exportar_a_csv']

    def acciones(self, obj):
        return format_html(
            '<a style="background:#4CAF50;color:white;padding:4px 8px;border-radius:4px;text-decoration:none;margin-right:4px;" href="{}">Editar</a>'
            '<a style="background:#f44336;color:white;padding:4px 8px;border-radius:4px;text-decoration:none;" href="{}">Eliminar</a>',
            f'/admin/accounts/usuario/{obj.id}/change/',
            f'/admin/accounts/usuario/{obj.id}/delete/'
        )
    acciones.short_description = 'Acciones'
    
    def exportar_a_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=usuarios.csv'
        writer = csv.writer(response)
        writer.writerow(['Usuario', 'Email', 'Nombre', 'Apellido', 'Cargo', 'Estado', 'MFA', 'Último acceso'])
        for u in queryset:
            writer.writerow([
                u.usuario,
                u.email,
                u.nombre or '',
                u.apellido or '',
                u.cargo,
                u.estado,
                'Sí' if u.mfa else 'No',
                u.ultimo_acceso.strftime('%Y-%m-%d %H:%M') if u.ultimo_acceso else '-'
            ])
        return response
    exportar_a_csv.short_description = "Exportar a CSV"

    def estado_coloreado(self, obj):
        colores = {
            'ACTIVO': 'success',
            'INACTIVO': 'warning',
            'BLOQUEADO': 'danger'
        }
        color = colores.get(obj.estado, 'secondary')
        return format_html(f'<span class="badge bg-{color}">{obj.estado}</span>')
    estado_coloreado.short_description = 'Estado'

    def mfa_activado(self, obj):
        return format_html(
            '<span class="text-success fw-bold">Sí</span>' if obj.mfa else '<span class="text-muted">No</span>'
        )
    mfa_activado.short_description = 'MFA'

    def ultimo_acceso_formateado(self, obj):
        return obj.ultimo_acceso.strftime('%Y-%m-%d %H:%M') if obj.ultimo_acceso else '-'
    ultimo_acceso_formateado.short_description = 'Último acceso'

    
