from django.urls import path
from . import views 

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('acercade/', views.acercade, name='acercade'),
    path('producto/<int:pk>', views.producto, name='producto'),
    path('categoria/<str:variable>', views.categoria, name='categoria'),

]