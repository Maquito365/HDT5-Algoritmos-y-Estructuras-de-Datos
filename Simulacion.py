# -*- coding: utf-8 -*-
# =============================================================================
# Simulación de Procesos en un Sistema Operativo de Tiempo Compartido
# Usando SimPy (Discrete Event Simulation)
# =============================================================================
# Universidad del Valle de Guatemala
# Programación - Semestre 3
# Marco Antonio Soloj - 25701
# =============================================================================
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
    def __init__(self, num_procesos, intervalo, memoria_ram=100,velocidad_cpu=3, num_cpus=1):
        self.env = simpy.Environment() #se crea el entorno de simulacion
        self.num_procesos = num_procesos #se guarda el numero de procesos
        self.intervalo = intervalo #se guarda el intervalo de llegada de procesos
        self.RAM = simpy.Container(self.env, capacity=memoria_ram, init= memoria_ram) #se crea la RAM con capacidad 
        self.CPU = simpy.Resource(self.env, capacity=num_cpus) #se crea la CPU con capacidad de 1
        self.velocidad_cpu = velocidad_cpu #se guarda la velocidad de la CPU
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
                proceso.instrucciones_restantes -= self.velocidad_cpu #se restan 3 instrucciones por cada ciclo de CPU
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
    def correr(self):
        self.env.process(self.generar_procesos()) #se inicia la generación de procesos
        self.env.run()
    
    def estadisticas(self):
        promedio = statistics.mean(self.tiempos)
        if len(self.tiempos) > 1:
            desviacion = statistics.stdev(self.tiempos)
        else:
            desviacion = 0
        return promedio, desviacion
    
# ==========================================
# ESCENARIO BASE - RAM 100 - CPU normal
# ==========================================
#Simulaciones para intervalos de 10 y N procesos
procesos = [25,50,100,150,200] #diferentes cantidades de procesos a simular
promedios = []
desviaciones = []
for n in procesos:
    random.seed(42) #se fija la semilla para reproducibilidad
    sim = Simulacion(n,10,) #se crea una instancia de la simulacion con n procesos y un intervalo de 10
    sim.correr() #se corre la simulacion
    promedio, desviacion = sim.estadisticas() #se obtienen las estadísticas de la
    promedios.append(promedio)
    desviaciones.append(desviacion)
    print(f"Procesos: {n}, Promedio: {promedio:.2f}, Desviación: {desviacion:.2f}")

# Gráfica de los resultados
plt.plot(procesos, promedios)
plt.xlabel('Número de Procesos')
plt.ylabel('Tiempo Promedio ')
plt.title('Tiempo Promedio de Respuesta vs Número de Procesos')
plt.grid(True)
plt.show()    

#Simulaciones para intervalos de 5 y N procesos
promedios_5 = []
desviaciones_5 = []
for n in procesos:
    random.seed(42) #se fija la semilla para reproducibilidad
    sim = Simulacion(n,5) #se crea una instancia de la simulacion con n procesos y un intervalo de 5
    sim.correr() #se corre la simulacion
    promedio, desviacion = sim.estadisticas() #se obtienen las estadísticas de la
    promedios_5.append(promedio)
    desviaciones_5.append(desviacion)
    print(f"Procesos: {n}, Promedio: {promedio:.2f}, Desviación: {desviacion:.2f}")

plt.plot(procesos, promedios_5)
plt.xlabel("Número de procesos")
plt.ylabel("Tiempo promedio en el sistema")
plt.title("Procesos vs Tiempo Promedio (Intervalo 5)")
plt.grid(True)
plt.show()

#Simulaciones para intervalos de 1 y N procesos
promedios_1 = []
desviaciones_1 = []
for n in procesos:
    random.seed(42) #se fija la semilla para reproducibilidad
    sim = Simulacion(n,1) #se crea una instancia de la simulacion con n procesos y un intervalo de 1
    sim.correr() #se corre la simulacion
    promedio, desviacion = sim.estadisticas() #se obtienen las estadísticas de la
    promedios_1.append(promedio)
    desviaciones_1.append(desviacion)
    print(f"Procesos: {n}, Promedio: {promedio:.2f}, Desviación: {desviacion:.2f}")

plt.plot(procesos, promedios_1)
plt.xlabel("Número de procesos")
plt.ylabel("Tiempo promedio en el sistema")
plt.title("Procesos vs Tiempo Promedio (Intervalo 1)")
plt.grid(True)
plt.show()

# ==========================================
# ESCENARIO RAM 200
# ==========================================
promedios_10 = []
desviaciones_10 = []
for n in procesos:
    random.seed(42) #se fija la semilla para reproducibilidad
    sim = Simulacion(n,10,memoria_ram=200) #se crea una instancia de la simulacion con n procesos y un intervalo de 10
    sim.correr() #se corre la simulacion
    promedio, desviacion = sim.estadisticas() #se obtienen las estadísticas de la
    promedios_10.append(promedio)
    desviaciones_10.append(desviacion)
    print(f"Procesos: {n}, Promedio: {promedio:.2f}, Desviación: {desviacion:.2f}")

plt.plot(procesos, promedios_10)
plt.xlabel("Número de procesos")
plt.ylabel("Tiempo promedio en el sistema")
plt.title("Procesos vs Tiempo Promedio (Intervalo 10) - RAM 200")
plt.grid(True)
plt.show()

promedios_5 = []
desviaciones_5 = []
for n in procesos:
    random.seed(42) #se fija la semilla para reproducibilidad
    sim = Simulacion(n,5,memoria_ram=200) #se crea una instancia de la simulacion con n procesos y un intervalo de 5
    sim.correr() #se corre la simulacion
    promedio, desviacion = sim.estadisticas() #se obtienen las estadísticas de la
    promedios_5.append(promedio)
    desviaciones_5.append(desviacion)
    print(f"Procesos: {n}, Promedio: {promedio:.2f}, Desviación: {desviacion:.2f}")

plt.plot(procesos, promedios_5)
plt.xlabel("Número de procesos")
plt.ylabel("Tiempo promedio en el sistema")
plt.title("Procesos vs Tiempo Promedio (Intervalo 5) - RAM 200")
plt.grid(True)
plt.show()

promedios_1 = []
desviaciones_1 = []
for n in procesos:
    random.seed(42) #se fija la semilla para reproducibilidad
    sim = Simulacion(n,1,memoria_ram=200) #se crea una instancia de la simulacion con n procesos y un intervalo de 1
    sim.correr() #se corre la simulacion
    promedio, desviacion = sim.estadisticas() #se obtienen las estadísticas de la
    promedios_1.append(promedio)
    desviaciones_1.append(desviacion)
    print(f"Procesos: {n}, Promedio: {promedio:.2f}, Desviación: {desviacion:.2f}")

plt.plot(procesos, promedios_1)
plt.xlabel("Número de procesos")
plt.ylabel("Tiempo promedio en el sistema")
plt.title("Procesos vs Tiempo Promedio (Intervalo 1) - RAM 200")
plt.grid(True)
plt.show()

# ==========================================
# ESCENARIO RAM 100 y CPU rápida de 6 
# ==========================================
promedios_10 = []
desviaciones_10 = []
for n in procesos:
    random.seed(42) #se fija la semilla para reproducibilidad
    sim = Simulacion(n,10,memoria_ram=100,velocidad_cpu=6) #se crea una instancia de la simulacion con n procesos y un intervalo de 10
    sim.correr() #se corre la simulacion
    promedio, desviacion = sim.estadisticas() #se obtienen las estadísticas de la
    promedios_10.append(promedio)
    desviaciones_10.append(desviacion)
    print(f"Procesos: {n}, Promedio: {promedio:.2f}, Desviación: {desviacion:.2f}")

plt.plot(procesos, promedios_10)
plt.xlabel("Número de procesos")
plt.ylabel("Tiempo promedio en el sistema")
plt.title("Procesos vs Tiempo Promedio (Intervalo 10) - RAM 100 y CPU rápida")
plt.grid(True)
plt.show()

promedios_5 = []
desviaciones_5 = []
for n in procesos:
    random.seed(42) #se fija la semilla para reproducibilidad
    sim = Simulacion(n,5,memoria_ram=100,velocidad_cpu=6) #se crea una instancia de la simulacion con n procesos y un intervalo de 5
    sim.correr() #se corre la simulacion
    promedio, desviacion = sim.estadisticas() #se obtienen las estadísticas de la
    promedios_5.append(promedio)
    desviaciones_5.append(desviacion)
    print(f"Procesos: {n}, Promedio: {promedio:.2f}, Desviación: {desviacion:.2f}")

plt.plot(procesos, promedios_5)
plt.xlabel("Número de procesos")
plt.ylabel("Tiempo promedio en el sistema")
plt.title("Procesos vs Tiempo Promedio (Intervalo 5) - RAM 100 y CPU rápida")
plt.grid(True)
plt.show()

promedios_1 = []
desviaciones_1 = []
for n in procesos:
    random.seed(42) #se fija la semilla para reproducibilidad
    sim = Simulacion(n,1,memoria_ram=100,velocidad_cpu=6) #se crea una instancia de la simulacion con n procesos y un intervalo de 1
    sim.correr() #se corre la simulacion
    promedio, desviacion = sim.estadisticas() #se obtienen las estadísticas de la
    promedios_1.append(promedio)
    desviaciones_1.append(desviacion)
    print(f"Procesos: {n}, Promedio: {promedio:.2f}, Desviación: {desviacion:.2f}")

plt.plot(procesos, promedios_1)
plt.xlabel("Número de procesos")
plt.ylabel("Tiempo promedio en el sistema")
plt.title("Procesos vs Tiempo Promedio (Intervalo 1) - RAM 100 y CPU rápida")
plt.grid(True)
plt.show()

# ==========================================
# ESCENARIO RAM 100 y CPU normal con 2 CPUs
# ==========================================
promedios_10 = []
desviaciones_10 = []
for n in procesos:
    random.seed(42) #se fija la semilla para reproducibilidad
    sim = Simulacion(n,10,memoria_ram=100,velocidad_cpu=3, num_cpus=2) #se crea una instancia de la simulacion con n procesos y un intervalo de 10
    sim.correr() #se corre la simulacion
    promedio, desviacion = sim.estadisticas() #se obtienen las estadísticas de la
    promedios_10.append(promedio)
    desviaciones_10.append(desviacion)
    print(f"Procesos: {n}, Promedio: {promedio:.2f}, Desviación: {desviacion:.2f}")

plt.plot(procesos, promedios_10)
plt.xlabel("Número de procesos")
plt.ylabel("Tiempo promedio en el sistema")
plt.title("Procesos vs Tiempo Promedio (Intervalo 10) - RAM 100 y CPU normal con 2 CPUs")
plt.grid(True)
plt.show()

promedios_5 = []
desviaciones_5 = []
for n in procesos:
    random.seed(42) #se fija la semilla para reproducibilidad
    sim = Simulacion(n,5,memoria_ram=100,velocidad_cpu=3, num_cpus=2) #se crea una instancia de la simulacion con n procesos y un intervalo de 5
    sim.correr() #se corre la simulacion
    promedio, desviacion = sim.estadisticas() #se obtienen las estadísticas de la
    promedios_5.append(promedio)
    desviaciones_5.append(desviacion)
    print(f"Procesos: {n}, Promedio: {promedio:.2f}, Desviación: {desviacion:.2f}")

plt.plot(procesos, promedios_5)
plt.xlabel("Número de procesos")
plt.ylabel("Tiempo promedio en el sistema")
plt.title("Procesos vs Tiempo Promedio (Intervalo 5) - RAM 100 y CPU normal con 2 CPUs")
plt.grid(True)
plt.show()

promedios_1 = []
desviaciones_1 = []
for n in procesos:
    random.seed(42) #se fija la semilla para reproducibilidad
    sim = Simulacion(n,1,memoria_ram=100,velocidad_cpu=3, num_cpus=2) #se crea una instancia de la simulacion con n procesos y un intervalo de 1
    sim.correr() #se corre la simulacion
    promedio, desviacion = sim.estadisticas() #se obtienen las estadísticas de la
    promedios_1.append(promedio)
    desviaciones_1.append(desviacion)
    print(f"Procesos: {n}, Promedio: {promedio:.2f}, Desviación: {desviacion:.2f}")

plt.plot(procesos, promedios_1)
plt.xlabel("Número de procesos")
plt.ylabel("Tiempo promedio en el sistema")
plt.title("Procesos vs Tiempo Promedio (Intervalo 1) - RAM 100 y CPU normal con 2 CPUs")
plt.grid(True)
plt.show() 

