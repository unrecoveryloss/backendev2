from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, UserCreationForm
from django.contrib.auth import get_user_model
Usuario = get_user_model()
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class CustomLoginForm(AuthenticationForm):
    usuario = forms.CharField(
        label="Usuario o correo",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'usuario@dominio.com'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'})
    )

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'usuario@dominio.com'})
    )

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mín. 8 caracteres'})
    )
    new_password2 = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repite tu contraseña'})
    )

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu contraseña'}),
        help_text="Debe tener al menos 8 caracteres, incluir letras, números y un símbolo."
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repite tu contraseña'}),
    )

    class Meta:
        model = Usuario
        fields = ['usuario', 'email', 'password1', 'password2']
        widgets = {
            'usuario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
        }

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        try:
            validate_password(password)
        except ValidationError as e:
            raise ValidationError(e.messages)
        return password