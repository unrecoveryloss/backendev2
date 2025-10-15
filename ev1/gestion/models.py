from django.db import models
from catalogo.models import Producto
import datetime

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En Proceso'),
        ('ENVIADO', 'Enviado'),
        ('ENTREGADO', 'Entregado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='PENDIENTE')
    direccion_envio = models.TextField()

    def __str__(self):
        return f"Pedido #{self.id} de {self.cliente.nombre}"


class Bodega(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombre
    

class Proveedor(models.Model):

    rut_nif = models.CharField(max_length=20, unique=True, verbose_name="RUT/NIF")
    razon_social = models.CharField(max_length=255)
    nombre_fantasia = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    telefono = models.CharField(max_length=30, blank=True, null=True)

    direccion = models.CharField(max_length=255, blank=True, null=True)
    ciudad = models.CharField(max_length=128, blank=True, null=True)
    pais = models.CharField(max_length=64, default="Chile")

    ESTADOS = [('ACTIVO', 'Activo'), ('BLOQUEADO', 'Bloqueado')]
    estado = models.CharField(max_length=10, choices=ESTADOS, default='ACTIVO')

    def __str__(self):
        return self.razon_social

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

class MovimientoInventario(models.Model):
    TIPOS_MOVIMIENTO = [
        ('INGRESO', 'Ingreso'),
        ('SALIDA', 'Salida'),
        ('AJUSTE', 'Ajuste'),
        ('DEVOLUCION', 'Devolución'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
    bodega = models.ForeignKey(Bodega, on_delete=models.SET_NULL, blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPOS_MOVIMIENTO)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    lote = models.CharField(max_length=50, blank=True, null=True)
    serie = models.CharField(max_length=50, blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    control_por_lote = models.BooleanField(default=False, verbose_name="Control por Lote")
    control_por_serie = models.BooleanField(default=False, verbose_name="Control por Serie")
    perishable = models.BooleanField(default=False, verbose_name="Es Perecible")


    def __str__(self):
        return f"{self.tipo} de {self.producto.nombre} ({self.cantidad})"


class Cargo(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Trabajador(models.Model):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)  
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name='trabajadores')

    def __str__(self):
        return f"{self.nombre} ({self.cargo.nombre})"
    
    class Meta:
        verbose_name = 'Trabajador'
        verbose_name_plural = 'Trabajadores'


class Turno(models.Model):
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE, related_name='turnos')
    fecha = models.DateField()
    horario_inicio = models.TimeField()
    horario_fin = models.TimeField()

    def __str__(self):
        return f"{self.trabajador.nombre} - {self.fecha} ({self.horario_inicio}-{self.horario_fin})"


