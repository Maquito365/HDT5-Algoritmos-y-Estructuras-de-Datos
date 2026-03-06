import simpy
import random
import statistics
import matplotlib.pyplot as plt

# Definición de la clase Proceso y Simulacion
class Proceso:
#Constructor de la clase Proceso
    def __init__(self, id_proceso, tiempo_llegada):
        self.id = id_proceso #se guarda el id
        self.memoria =random.randint(1, 10) #es la memoria aleatoria
        self.instrucciones_totales = random.randint(1,10) #n intrucciones aleatorias
        self.instrucciones_restantes = self.instrucciones_totales #n instrucciones restantes
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_salida = 0

class Simulacion:
    #Constructor de la clase Simulacion
    def __init__(self, num_procesos, intervalo):
        self.env = simpy.Environment() #se crea el entorno de simulacion
        self.num_procesos = num_procesos #se guarda el numero de procesos
        self.intervalo = intervalo #se guarda el intervalo de llegada de procesos
        self.RAM = simpy.Container(self.env, capacity= 100, init=100) #se crea la RAM con capacidad de 100
        self.CPU = simpy.Resource(self.env, capacity=1) #se crea la CPU con capacidad de 1
        self.tiempos = []

