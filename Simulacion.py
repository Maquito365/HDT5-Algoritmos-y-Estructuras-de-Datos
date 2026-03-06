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

    #Método para generar procesos
    def generar_procesos(self):
        for i in range(self.num_procesos):
            yield self.env.timeout(random.expovariate(1.0 / self.intervalo)) #se espera un tiempo aleatorio entre procesos
            proceso = Proceso(i, self.env.now) #se crea un nuevo proceso
            self.env.process(self.ejecutar_proceso(proceso)) #se ejecuta el proceso
    
    #Método para ejecutar un proceso
    def ejecutar_proceso(self, proceso):
        yield self.RAM.get(proceso.memoria) #se solicita la memoria necesaria para el proceso
        while proceso.instrucciones_restantes > 0:
            with self.CPU.request() as req: #Se solicita la CPU
                yield req
                yield self.env.timeout(1) #se simula el quantum del CPU 1 unidad 3 instru
                proceso.instrucciones_restantes -= 3 #se restan 3 instrucciones por cada ciclo de CPU
                if proceso.instrucciones_restantes < 0:
                    proceso.instrucciones_restantes = 0
                if proceso.instrucciones_restantes == 0:
                    proceso.tiempo_salida = self.env.now
                    self.tiempos.append(proceso.tiempo_salida - proceso.tiempo_llegada) #se guarda el tiempo de respuesta del proceso
                    yield self.RAM.put(proceso.memoria) #se devuelve la memoria al sistema
                    break
                else:
                    numero = random.randint(1,21) 
                    if numero == 1: #si es 1 pasa a waiting
                        yield self.env.timeout(1) #se simula el tiempo de espera en waiting
                    elif numero == 2: #si es 2 pasa a ready
                        pass
        



