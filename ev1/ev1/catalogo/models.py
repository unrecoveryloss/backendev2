from django.db import models
import datetime


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, default=1)
    descripcion = models.CharField(max_length=2500, default= '', blank=True, null=True)
    imagen = models.ImageField(upload_to='uploads/producto/')

    def __str__(self):
        return self.nombre
    
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

class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10)
    correo = models.EmailField(max_length=100)
    clave = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'
    
class Pedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    direccion = models.CharField(max_length=100, default='', blank=True)
    telefono = models.CharField(max_length=20, default='', blank=True)
    fecha = models.DateField(default=datetime.datetime.today)
    estado = models.BooleanField(default=False)

    def __str__(self):
        return str(self.producto)

