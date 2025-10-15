from django.urls import path
from .views import (
    CustomLoginView, logout_view, CustomPasswordResetView, 
    CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomRegisterView
)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('register/', CustomRegisterView.as_view(), name='register'),
]
