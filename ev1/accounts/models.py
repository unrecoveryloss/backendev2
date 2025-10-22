from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class UsuarioManager(BaseUserManager):
    def create_user(self, usuario, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El correo electrónico es obligatorio.")
        email = self.normalize_email(email)
        user = self.model(usuario=usuario, email=email, **extra_fields)
        user.set_password(password)  # se guarda de forma segura (hash)
        user.save(using=self._db)
        return user

    def create_superuser(self, usuario, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('cargo', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError("El superusuario debe tener is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("El superusuario debe tener is_superuser=True.")

        return self.create_user(usuario, email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    CARGO_OPCIONES = [
        ('ADMIN', 'Administrador'),
        ('SUPERVISOR', 'Supervisor'),
        ('OPERADOR', 'Operador'),
        ('CLIENTE', 'Cliente')
    ]

    ESTADO_OPCIONES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('BLOQUEADO', 'Bloqueado'),
    ]

    usuario = models.CharField(max_length=50, unique=True, verbose_name='Usuario')
    email = models.EmailField(unique=True, verbose_name='Correo electrónico')
    nombre = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nombre')
    apellido = models.CharField(max_length=100, blank=True, null=True, verbose_name='Apellido')
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name='Teléfono')
    cargo = models.CharField(max_length=15, choices=CARGO_OPCIONES, default='OPERADOR', verbose_name='Cargo')
    estado = models.CharField(max_length=15, choices=ESTADO_OPCIONES, default='ACTIVO', verbose_name='Estado')
    mfa = models.BooleanField(default=False, verbose_name='MFA habilitado')
    ultimo_acceso = models.DateTimeField(blank=True, null=True, verbose_name='Último acceso')
    ip_sesion = models.GenericIPAddressField(blank=True, null=True, verbose_name='IP de sesión')
    session_count = models.PositiveIntegerField(default=0, verbose_name='Número de sesiones')
    fecha_creacion = models.DateTimeField(default=timezone.now, verbose_name='Fecha de creación')

    is_staff = models.BooleanField(default=False, verbose_name='Es parte del staff')
    is_active = models.BooleanField(default=True, verbose_name='Está activo')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuarios_personalizados',
        blank=True,
        help_text='Grupos a los que pertenece este usuario.',
        verbose_name='Grupos'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuarios_con_permisos',
        blank=True,
        help_text='Permisos específicos para este usuario.',
        verbose_name='Permisos de usuario'
    )

    objects = UsuarioManager()

    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.usuario} ({self.cargo})"
    
    def save(self, *args, **kwargs):
        # Actualizar último acceso al guardar
        if self.pk:  # Solo si ya existe el usuario
            self.ultimo_acceso = timezone.now()
        super().save(*args, **kwargs)