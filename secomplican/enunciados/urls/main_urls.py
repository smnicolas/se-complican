from django.urls import include, path, register_converter

from enunciados.url_converters import CarreraConverter, MateriaCarreraConverter
from enunciados.views import index, materias
from enunciados.views.enunciados import crear as crear_enunciado
from enunciados.views.soluciones import editar as editar_solucion
from enunciados.views.soluciones import versiones as versiones_solucion

register_converter(CarreraConverter, 'carrera')
register_converter(MateriaCarreraConverter, 'materiacarrera')

urlpatterns = [
    path('', index.index, name='index'),
    path('<carrera:carrera>/materias/',
         materias.MateriasView.as_view(), name='materias'),

    path(
        'nuevo-ejercicio/',
        crear_enunciado.nuevo_enunciado,
        name='agregar_enunciado'
    ),

    path(
        'soluciones/<int:pk>/editar/',
        editar_solucion.editar_solucion,
        name='editar_solucion'
    ),

    path(
        'soluciones/<int:pk>/versiones/',
        versiones_solucion.VersionesSolucionView.as_view(),
        name='versiones_solucion'
    ),

    path('<materiacarrera:materia_carrera>/',
        include('enunciados.urls.materia_urls', namespace='materia')),
]