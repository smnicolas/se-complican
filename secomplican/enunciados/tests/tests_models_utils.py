from django.test import TestCase
from enunciados.models import Materia, Cuatrimestre, Parcial, Practica
from enunciados.models_utils import *


def assert_lista_equals(testCase, primera, segunda):
    testCase.assertEquals(len(primera), len(segunda))
    for i, elemento in enumerate(primera):
        testCase.assertEquals(elemento, segunda[i])


class ParcialesDeMateriaOrdenadosTests(TestCase):
    def setUp(self):
        self.materia = Materia(nombre='materia')
        self.materia.save()

    def test_parciales_de_materia_ordenados_sin_materia(self):
        """Debería levantar un ValueError."""
        with self.assertRaises(ValueError):
            parciales_de_materia_ordenados(None)

    def test_parciales_de_materia_ordenados_sin_parciales(self):
        """Debería devolver un diccionario vacío."""
        self.assertEquals(len(parciales_de_materia_ordenados(self.materia)), 0)

    def test_parciales_de_materia_ordenados_con_primeros_parciales_con_igual_anio(self):
        """
        Debería devolver un diccionario con los primeros parciales ordenados
        en la primer posición.
        """
        cuatri1 = Cuatrimestre(anio=2018, numero=Cuatrimestre.VERANO)
        cuatri1.save()
        cuatri2 = Cuatrimestre(anio=2018, numero=Cuatrimestre.PRIMERO)
        cuatri2.save()
        cuatri3 = Cuatrimestre(anio=2018, numero=Cuatrimestre.SEGUNDO)
        cuatri3.save()

        parcial1 = Parcial(materia=self.materia, cuatrimestre=cuatri1, numero=1)
        parcial2 = Parcial(materia=self.materia, cuatrimestre=cuatri2, numero=1)
        parcial3 = Parcial(materia=self.materia, cuatrimestre=cuatri3, numero=1)

        # Los guardamos en desorden
        parcial2.save()
        parcial1.save()
        parcial3.save()

        # Los ordenamos de último a primero
        parciales = [parcial3, parcial2, parcial1]
        ordenados = parciales_de_materia_ordenados(self.materia)
        self.assertEquals(len(ordenados), 1)
        assert_lista_equals(self, ordenados[1], parciales)

    def test_parciales_de_materia_ordenados_con_primeros_parciales_diferente_anio(self):
        """
        Debería devolver el diccionario con los primeros parciales ordenados
        de último año a primero.
        """
        cuatri1 = Cuatrimestre(anio=2018, numero=Cuatrimestre.PRIMERO)
        cuatri1.save()
        cuatri2 = Cuatrimestre(anio=2018, numero=Cuatrimestre.VERANO)
        cuatri2.save()
        cuatri3 = Cuatrimestre(anio=2017, numero=Cuatrimestre.SEGUNDO)
        cuatri3.save()
        cuatri4 = Cuatrimestre(anio=2017, numero=Cuatrimestre.PRIMERO)
        cuatri4.save()

        parcial1 = Parcial(materia=self.materia, cuatrimestre=cuatri1, numero=1)
        parcial2 = Parcial(materia=self.materia, cuatrimestre=cuatri2, numero=1)
        parcial3 = Parcial(materia=self.materia, cuatrimestre=cuatri3, numero=1)
        parcial4 = Parcial(materia=self.materia, cuatrimestre=cuatri4, numero=1)

        # Los guardamos en desorden
        parcial2.save()
        parcial1.save()
        parcial4.save()
        parcial3.save()

        parciales = [parcial1, parcial2, parcial3, parcial4]
        ordenados = parciales_de_materia_ordenados(self.materia)
        self.assertEquals(len(ordenados), 1)
        assert_lista_equals(self, ordenados[1], parciales)

    def test_parciales_de_materia_ordenados_con_parciales_de_numeros_diferentes(self):
        """
        Debería devolver un diccionario con posiciones igual a la cantidad de
        números diferentes.
        """
        cuatri1 = Cuatrimestre(anio=2018, numero=Cuatrimestre.PRIMERO)
        cuatri1.save()
        cuatri2 = Cuatrimestre(anio=2018, numero=Cuatrimestre.VERANO)
        cuatri2.save()
        cuatri3 = Cuatrimestre(anio=2017, numero=Cuatrimestre.SEGUNDO)
        cuatri3.save()
        cuatri4 = Cuatrimestre(anio=2017, numero=Cuatrimestre.PRIMERO)
        cuatri4.save()

        primeros = [
            Parcial(materia=self.materia, cuatrimestre=cuatri1, numero=1),
            Parcial(materia=self.materia, cuatrimestre=cuatri2, numero=1),
        ]

        segundos = [
            Parcial(materia=self.materia, cuatrimestre=cuatri1, numero=2),
            Parcial(materia=self.materia, cuatrimestre=cuatri3, numero=2),
            Parcial(materia=self.materia, cuatrimestre=cuatri4, numero=2),
        ]

        for parcial in primeros:
            parcial.save()

        for parcial in segundos:
            parcial.save()

        ordenados = parciales_de_materia_ordenados(self.materia)
        self.assertEquals(len(ordenados), 2)
        assert_lista_equals(self, ordenados[1], primeros)
        assert_lista_equals(self, ordenados[2], segundos)

    def test_parciales_de_materia_ordenados_con_recuperatorios(self):
        """Debería devolver los recuperatorios antes que los parciales."""
        cuatri1 = Cuatrimestre(anio=2018, numero=Cuatrimestre.PRIMERO)
        cuatri1.save()
        cuatri2 = Cuatrimestre(anio=2018, numero=Cuatrimestre.SEGUNDO)
        cuatri2.save()

        parcial1 = Parcial(materia=self.materia, cuatrimestre=cuatri1, numero=1)
        recu = Parcial(
            materia=self.materia, cuatrimestre=cuatri1, numero=1, recuperatorio=True)
        parcial2 = Parcial(materia=self.materia, cuatrimestre=cuatri2, numero=1)

        parcial1.save()
        parcial2.save()
        recu.save()

        parciales = [parcial2, recu, parcial1]
        ordenados = parciales_de_materia_ordenados(self.materia)
        self.assertEquals(len(ordenados), 1)
        assert_lista_equals(self, ordenados[1], parciales)


class UltimasPracticasOrdenadasTests(TestCase):
    def setUp(self):
        self.materia = Materia(nombre='materia')
        self.materia.save()

    def test_ultimas_practicas_ordenadas_sin_materia(self):
        """Debería levantar un ValueError."""
        with self.assertRaises(ValueError):
            ultimas_practicas_ordenadas(None)

    def test_ultimas_practicas_ordenadas_sin_practicas(self):
        """Debería devolver una lista vacía."""
        self.assertEquals(len(ultimas_practicas_ordenadas(self.materia)), 0)

    def test_ultimas_practicas_ordenadas_con_practicas_de_mismo_cuatrimestre(self):
        """Debería devolver todas las prácticas."""
        cuatri = Cuatrimestre(anio=2018, numero=Cuatrimestre.VERANO)
        cuatri.save()

        practicas = []
        # Creamos 10 prácticas
        for i in range(1, 11):
            practicas.append(Practica(cuatrimestre=cuatri, materia=self.materia, numero=i))

        # Las guardamos en desorden
        for i in range(9, -1, -1):
            practicas[i].save()

        resultado = ultimas_practicas_ordenadas(self.materia)
        assert_lista_equals(self, resultado, practicas)

    def test_ultimas_practicas_ordenadas_con_practicas_de_distinto_cuatrimestre(self):
        """Debería devolver solo las del último cuatrimestre."""
        cuatri1 = Cuatrimestre(anio=2018, numero=Cuatrimestre.VERANO)
        cuatri1.save()
        cuatri2 = Cuatrimestre(anio=2018, numero=Cuatrimestre.SEGUNDO)
        cuatri2.save()

        practicas_viejas = []
        practicas_nuevas = []
        # Creamos 10 prácticas de cada cuatri
        for i in range(1, 11):
            practicas_viejas.append(
                Practica(cuatrimestre=cuatri1, materia=self.materia, numero=i)
            )
            practicas_nuevas.append(
                Practica(cuatrimestre=cuatri2, materia=self.materia, numero=i)
            )

        # Las guardamos en desorden
        for i in range(9, -1, -1):
            practicas_viejas[i].save()
            practicas_nuevas[i].save()

        resultado = ultimas_practicas_ordenadas(self.materia)
        assert_lista_equals(self, resultado, practicas_nuevas)