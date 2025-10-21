from django.urls import path
from .views import (
    login_view, logout_view, CustomPasswordResetView, 
    CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomRegisterView,
    admin_dashboard, supervisor_dashboard, operador_dashboard, cliente_dashboard
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('supervisor/dashboard/', supervisor_dashboard, name='supervisor_dashboard'),
    path('dashboard/operador/', operador_dashboard, name='operador_dashboard'),
    path('cliente/dashboard/', cliente_dashboard, name='cliente_dashboard'),
]
