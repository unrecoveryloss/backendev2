from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from . models import Producto, Categoria


def inicio(request):
    productos = Producto.objects.all()
    return render(request, 'inicio.html', {'productos':productos})

def acercade(request):
    return render(request, 'acercade.html', {})

def producto(request,pk):
    producto = Producto.objects.get(id=pk)
    return render(request, 'producto.html', {'producto':producto})

def categoria(request,variable):
    variable = variable.replace('-', '')
    try:
        categoria = Categoria.objects.get(nombre=variable)
        productos = Producto.objects.filter(categoria=categoria)
        return render(request, 'categoria.html', {'productos':productos, 'categoria':categoria})
    except:
        messages.success(request, 'Esa categoría no existe')
        return redirect('home')
    