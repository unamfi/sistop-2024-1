#! /usr/bin/env python3
# ./Ejercicio1.py
# ## ###############################################################################################
# -*- Programa que modela la interaccion jefe-trabajador empleando sincronizacion con semáforos -*-
# 
# Autores: Carlos Garcés y Patricia Jimenez
# ## ###############################################################################################

from threading import Thread, Semaphore
import time
import random

# Función que representa a un trabajador
def trabajador(id, semaforo, tActivos):
	while True:
		semaforo.acquire()
		tActivos.append(id)
		print("\n Trabajador [%d] atendiendo solicitud..." %id)
		
		# Tiempo de procesamiento de solicitud
		# ...
		time.sleep(random.uniform(2.0, 4.0))
		# ...
		
		tActivos.remove(id)
		print(" Trabajador [%d] libre (durmiendo)." %id)
	#end while
#end def

# Función que representa al jefe
def jefe(semaf, tActivos):
	# Número máximo de trabajadores (hilos) que pueden estar activos al mismo tiempo
	k = 5

	# Creando y lanzando hilos trabajadores
	for i in range(2*k):
		Thread(target=trabajador, args=(i, semaf, tActivos)).start()

	# Esperando solicitud
	while True:
		input("\n Presione una tecla para generar una solicitud...")
		if len(tActivos) < k:
			# Seleccionar un trabajador para atender la solicitud
			semaf.release()
		else:
			print(" Eperando trabajadores...")
			continue
	#end while
#end def 

def main():
	# Semáforo para controlar la cantidad de hilos empleados
	semaf = Semaphore(0)

	tActivos = []
	jefe(semaf, tActivos)

if __name__ == '__main__':
	main()