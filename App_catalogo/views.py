# catalogo/views.py
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.generic import TemplateView
from .datos import LIBROS, buscar_libro

# Ejercicio 1: Respuesta simple
def hola_mundo(request):
    return HttpResponse("Hola desde Django")

# Ejercicio 2: Ruta con parámetro entero
def calcular_cuadrado(request, numero):
    resultado = numero ** 2
    return HttpResponse(f"El cuadrado de {numero} es {resultado}")

# Ejercicio 3: Vista basada en clase para contacto
class ContactoView(TemplateView):
    template_name = "App_catalogo/contacto.html"

class AcercaView(TemplateView):
    template_name = "App_catalogo/acerca.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["version"] = "1.0"
        return contexto

# Ejercicio 4: Actualizar la vista inicio para calcular disponibles y prestados
def inicio(request):
    disponibles = sum(1 for libro in LIBROS if libro["disponible"])
    prestados = len(LIBROS) - disponibles
    contexto = {
        "nombre_sitio": "Catálogo ADSO",
        "total": len(LIBROS),
        "disponibles": disponibles,
        "prestados": prestados
    }
    return render(request, "App_catalogo/inicio.html", contexto)

def lista_libros(request):
    genero = request.GET.get("genero", "").strip()
    libros = LIBROS
    if genero:
        libros = [libro for libro in LIBROS if libro["genero"] == genero]
    return render(
        request,
        "App_catalogo/lista.html",
        {"libros": libros, "genero": genero},
    )

def detalle_libro(request, libro_id):
    libro = buscar_libro(libro_id)
    if libro is None:
        raise Http404("No se encontró el libro solicitado.")
    return render(request, "App_catalogo/detalle.html", {"libro": libro})

# Ejercicio 5: Listado de autores sin repetir y conteo de libros
def lista_autores(request):
    autores_unicos = sorted(list(set(libro["autor"] for libro in LIBROS)))
    conteo_autores = []
    for autor in autores_unicos:
        cantidad = sum(1 for libro in LIBROS if libro["autor"] == autor)
        conteo_autores.append({"autor": autor, "total": cantidad})
    return render(request, "App_catalogo/autores.html", {"autores": conteo_autores})

# Ejercicio 6: Formulario con POST para sugerir libros
def sugerir_libro(request):
    mensaje = ""
    if request.method == "POST":
        titulo = request.POST.get("titulo", "").strip()
        if titulo:
            mensaje = f"Gracias, tendremos en cuenta: {titulo}"
        else:
            mensaje = "Escribe un título"
    return render(request, "App_catalogo/sugerir.html", {"mensaje": mensaje})

def buscar(request):
    query = request.GET.get("q", "").strip()
    resultados = [
        libro for libro in LIBROS
        if query.casefold() in libro["titulo"].casefold()
    ]
    return render(
        request,
        "App_catalogo/buscar.html",
        {
            "query": query,
            "busco": "q" in request.GET,
            "resultados": resultados,
        },
    )