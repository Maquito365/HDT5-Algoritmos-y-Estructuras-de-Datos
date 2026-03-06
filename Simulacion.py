import simpy
import random
import statistics
import matplotlib.pyplot as plt

# Definición de la clase Proceso y Simulacion
class Proceso:
#Constructor de la clase Proceso
    def __init__(self, id_proceso, tiempo_llegada):
        self.id = id_proceso #se guarda el id
        self.memoria =random.randint(1, 10)
        self.instrucciones_totales = random.randint(1,10)
        self.instrucciones_restantes = self.instrucciones_totales
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_salida = 0
class Simulacion:
    pass