from django import forms
from django.contrib.auth import get_user_model
from catalogo.models import Producto, Categoria
from gestion.models import Cliente, Proveedor, Pedido, Bodega, Turno, MovimientoInventario

Usuario = get_user_model()

# ==================== FORMULARIOS DE USUARIO ====================

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'usuario', 'email', 'nombre', 'apellido', 'telefono', 
            'cargo', 'estado', 'mfa'
        ]
        widgets = {
            'usuario': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de usuario'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'usuario@dominio.com'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el apellido'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56 9 1234 5678'
            }),
            'cargo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'mfa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].required = True
        self.fields['email'].required = True
        self.fields['cargo'].required = True
        self.fields['estado'].required = True

# ==================== FORMULARIOS DE CATEGORÍA ====================

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la categoría'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].required = True

# ==================== FORMULARIOS DE PRODUCTO ====================

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'sku', 'ean_upc', 'nombre', 'descripcion', 'categoria', 'marca', 'modelo',
            'uom_compra', 'uom_venta', 'factor_conversion', 'costo_estandar', 
            'precio_venta', 'impuesto_iva', 'stock_minimo', 'stock_maximo', 
            'punto_reorden', 'perishable', 'control_por_lote', 'control_por_serie',
            'imagen'
        ]
        widgets = {
            'sku': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SKU-0001'
            }),
            'ean_upc': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '1234567890123'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del producto'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select'
            }),
            'marca': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Marca del producto'
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Modelo del producto'
            }),
            'uom_compra': forms.Select(attrs={
                'class': 'form-select'
            }),
            'uom_venta': forms.Select(attrs={
                'class': 'form-select'
            }),
            'factor_conversion': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1'
            }),
            'costo_estandar': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01'
            }),
            'precio_venta': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01'
            }),
            'impuesto_iva': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'stock_minimo': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'stock_maximo': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'punto_reorden': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'perishable': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'control_por_lote': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'control_por_serie': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].required = True
        self.fields['precio_venta'].required = True

# ==================== FORMULARIOS DE PROVEEDOR ====================

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = [
            'rut_nif', 'razon_social', 'nombre_fantasia', 'email', 'telefono',
            'direccion', 'ciudad', 'pais', 'estado'
        ]
        widgets = {
            'rut_nif': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '76.543.210-5'
            }),
            'razon_social': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Proveedor S.A.'
            }),
            'nombre_fantasia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ProveeMax'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'contacto@proveedor.cl'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56 2 2345 6789'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Av. Principal 123'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Santiago'
            }),
            'pais': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Chile'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rut_nif'].required = True
        self.fields['razon_social'].required = True
        self.fields['email'].required = True
        self.fields['estado'].required = True

# ==================== FORMULARIOS DE CLIENTE ====================

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'email', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del cliente'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'cliente@email.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56 9 1234 5678'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].required = True
        self.fields['email'].required = True

# ==================== FORMULARIOS DE PEDIDO ====================

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'productos', 'estado', 'direccion_envio']
        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'form-select'
            }),
            'productos': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'multiple': True
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'direccion_envio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección de envío completa'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].required = True
        self.fields['productos'].required = True
        self.fields['estado'].required = True
        self.fields['direccion_envio'].required = True

# ==================== FORMULARIOS DE BODEGA ====================

class BodegaForm(forms.ModelForm):
    class Meta:
        model = Bodega
        fields = ['nombre', 'ubicacion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'BOD-CENTRAL'
            }),
            'ubicacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Av. Principal 123, Santiago'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].required = True

# ==================== FORMULARIOS DE TURNO ====================

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['trabajador', 'fecha', 'horario_inicio', 'horario_fin']
        widgets = {
            'trabajador': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'horario_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'horario_fin': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['trabajador'].required = True
        self.fields['fecha'].required = True
        self.fields['horario_inicio'].required = True
        self.fields['horario_fin'].required = True

# ==================== FORMULARIOS DE MOVIMIENTO DE INVENTARIO ====================

class MovimientoInventarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ['producto', 'proveedor', 'bodega', 'tipo', 'cantidad', 'lote', 'serie']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
            'bodega': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'lote': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
            'serie': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].required = True
        self.fields['bodega'].required = True
        self.fields['tipo'].required = True
        self.fields['cantidad'].required = True
