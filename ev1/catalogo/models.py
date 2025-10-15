from django.db import models
import datetime


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Producto(models.Model):

    uom_medidas= [
        ('kg', 'Kilogramo'),
        ('caja', 'Caja'),
        ('uni', 'Unidad'),
    ]

    sku = models.CharField(max_length=50, unique=True, null=True, blank=True)
    ean_upc = models.CharField(max_length=50, unique=True, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, verbose_name='categoria (requerido)', null=True)
    marca = models.CharField(max_length=50, blank=True, null=True)
    modelo = models.CharField(max_length=50, blank=True, null=True)


    uom_compra = models.CharField(max_length=10,choices=uom_medidas,default='un')
    uom_venta = models.CharField(max_length=10,choices=uom_medidas,default='un')
    factor_conversion = models.PositiveIntegerField(null=True, verbose_name="factor de conversion", default=1)
    costo_estandar = models.PositiveIntegerField(null=True, blank=True, default=1)
    precio_venta = models.PositiveIntegerField(default=0)
    impuesto_iva = models.BooleanField(default=True, verbose_name="Aplica IVA (19%)")


    stock_minimo = models.PositiveIntegerField(default=0, verbose_name="Stock Mínimo")
    stock_maximo = models.PositiveIntegerField(blank=True, null=True, verbose_name="Stock Máximo")
    punto_reorden = models.PositiveIntegerField(default=0)
    perishable = models.BooleanField(default=False, verbose_name="Es Perecible")
    control_por_lote = models.BooleanField(default=False, verbose_name="Control por Lote")
    control_por_serie = models.BooleanField(default=False, verbose_name="Control por Serie")
    stock_total = models.PositiveIntegerField(default=0, verbose_name="Stock Total")



    imagen = models.ImageField(upload_to='productos/', null=True, blank=True, verbose_name='Imagen')

    def __str__(self):
        return f"{self.nombre} ({self.sku})"
    
    @property
    def stock_actual(self):
        return self.stock_total

    @property
    def alerta_bajo_stock(self):
        return self.stock_actual <= self.stock_minimo

    @property
    def alerta_por_vencer(self):
        if self.perecible and self.fecha_vencimiento:
            hoy = datetime.datetime.now()
            dias_restantes = (self.fecha_vencimiento - hoy).days
            return dias_restantes <= 7 
        return False


