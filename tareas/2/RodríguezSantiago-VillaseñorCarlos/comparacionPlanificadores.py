import random
import numpy as np

#Maximo tiempo de llegada
maxLlegada = 10
#Duración máxima procesos
maxT = 10
#lista de la secuencua de procesos
listaProcesos = []
#string con la secuencua de procesos
stringProcesos = ''
#Matrices de cada planificador de procesos simples
#t: tiempo de ejecución. E: Tiempo en espera. T: Tiempo total. P: Penalización
matrizFCFS = np.array([['Proceso', 't', 'nt', 'E', 'T', 'P'],
                       ['A', 0, 0, 0, 0, 0], ['B', 0, 0, 0, 0, 0],
                       ['C', 0, 0, 0, 0, 0], ['D', 0, 0, 0, 0, 0],
                       ['E', 0, 0, 0, 0, 0]])
matrizRR1 = np.array([['Proceso', 't', 'nt', 'E', 'T', 'P'],
                      ['A', 0, 0, 0, 0, 0], ['B', 0, 0, 0, 0, 0],
                      ['C', 0, 0, 0, 0, 0], ['D', 0, 0, 0, 0, 0],
                      ['E', 0, 0, 0, 0, 0]])
matrizRR4 = np.array([['Proceso', 't', 'nt', 'E', 'T', 'P'],
                      ['A', 0, 0, 0, 0, 0], ['B', 0, 0, 0, 0, 0],
                      ['C', 0, 0, 0, 0, 0], ['D', 0, 0, 0, 0, 0],
                      ['E', 0, 0, 0, 0, 0]])
matrizSPN = np.array([['Proceso', 't', 'nt', 'E', 'T', 'P'],
                      ['A', 0, 0, 0, 0, 0], ['B', 0, 0, 0, 0, 0],
                      ['C', 0, 0, 0, 0, 0], ['D', 0, 0, 0, 0, 0],
                      ['E', 0, 0, 0, 0, 0]])

#Valores de cada proceso, garanatizando el orden de llegada A->B->C->D->E
maxLlegadaA = 1
maxLlegadaB = random.randint(maxLlegadaA, maxT)
maxLlegadaC = random.randint(maxLlegadaB, maxT)
maxLlegadaD = random.randint(maxLlegadaC, maxT)
maxLlegadaE = random.randint(maxLlegadaD, maxT)
#proceso: (Llegada, duración)
#Se inicalizan valores aleatorios de duración para cada proceso
#
#Aleatorio

procesos = {
    'A': (maxLlegadaA, random.randint(1, maxT)),
    'B': (maxLlegadaB, random.randint(1, maxT)),
    'C': (maxLlegadaC, random.randint(1, maxT)),
    'D': (maxLlegadaD, random.randint(1, maxT)),
    'E': (maxLlegadaE, random.randint(1, maxT))
}


#Para RR1 y RR4
"""
procesos = {
    'A': (1, 2),
    'B': (5, 4),
    'C': (9, 5),
    'D': (9, 4),
    'E': (10, 4)
}
"""
#Prueba

"""
procesos = {'A': (1, 3), 'B': (2, 5), 'C': (4, 2), 'D': (10, 5), 'E': (13, 5)}
"""

#Tiempo máximo total
tiempoMaxTot = procesos['A'][1] + procesos['B'][1] + procesos['C'][
    1] + procesos['D'][1] + procesos['E'][1]

#print(tiempoMaxTot)
#imprimir valores de procesos
print("Proceso (Llegada, Duración)")
for key, value in procesos.items():
  print(key, value)

for key in procesos.keys():
  cont = procesos[key][1]
  while cont > 0:
    listaProcesos.append(key)
    cont = cont - 1

#Volvemos la lista un string
stringProcesos = ''.join(listaProcesos)

#print(stringProcesos)


#FCFS
def FCFS(procesos):
  indice = 1
  #Inicilizamos datos del diccionario
  #Al inicio nt es es momento en el que iniciar el programa
  for key in procesos.keys():
    matrizFCFS[indice][1] = procesos[key][1]
    matrizFCFS[indice][2] = procesos[key][0]
    indice = indice + 1
  #Inicia programa
  contTick = 0
  #print(matrizFCFS)

  while contTick < tiempoMaxTot:
    #print(contTick)
    #Actualizamos los bloques que van llegando
    if (int(matrizFCFS[1][1]) > 0 and contTick == int(matrizFCFS[1][2])):
      matrizFCFS[1][1] = int(matrizFCFS[1][1]) - 1
      matrizFCFS[1][2] = int(matrizFCFS[1][2]) + 1
      #print(matrizFCFS)
    elif (int(matrizFCFS[2][1]) > 0 and contTick == int(matrizFCFS[2][2])):
      matrizFCFS[2][1] = int(matrizFCFS[2][1]) - 1
      matrizFCFS[2][2] = int(matrizFCFS[2][2]) + 1
      #print(matrizFCFS)
    elif (int(matrizFCFS[3][1]) > 0 and contTick == int(matrizFCFS[3][2])):
      matrizFCFS[3][1] = int(matrizFCFS[3][1]) - 1
      matrizFCFS[3][2] = int(matrizFCFS[3][2]) + 1
      #print(matrizFCFS)
    elif (int(matrizFCFS[4][1]) > 0 and contTick == int(matrizFCFS[4][2])):
      matrizFCFS[4][1] = int(matrizFCFS[4][1]) - 1
      matrizFCFS[4][2] = int(matrizFCFS[4][2]) + 1
      #print(matrizFCFS)
    elif (int(matrizFCFS[5][1]) > 0 and contTick == int(matrizFCFS[5][2])):
      matrizFCFS[5][1] = int(matrizFCFS[5][1]) - 1
      matrizFCFS[5][2] = int(matrizFCFS[5][2]) + 1
      #print(matrizFCFS)

    #Actualizamos tiempo de inicio de los que están esperando
    if (int(matrizFCFS[1][2]) == contTick and int(matrizFCFS[1][1]) > 0):
      matrizFCFS[1][2] = int(matrizFCFS[1][2]) + 1
      #print(matrizFCFS)
    if (int(matrizFCFS[2][2]) == contTick and int(matrizFCFS[2][1]) > 0):
      matrizFCFS[2][2] = int(matrizFCFS[2][2]) + 1
      #print(matrizFCFS)
    if (int(matrizFCFS[3][2]) == contTick and int(matrizFCFS[3][1]) > 0):
      matrizFCFS[3][2] = int(matrizFCFS[3][2]) + 1
      #print(matrizFCFS)
    if (int(matrizFCFS[4][2]) == contTick and int(matrizFCFS[4][1]) > 0):
      matrizFCFS[4][2] = int(matrizFCFS[4][2]) + 1
      #print(matrizFCFS)
    if (int(matrizFCFS[5][2]) == contTick and int(matrizFCFS[5][1]) > 0):
      matrizFCFS[5][2] = int(matrizFCFS[5][2]) + 1
      #print(matrizFCFS)
    #Actualizamos contador global
    contTick = contTick + 1
  #Sacamos los valores faltantes y llenamos la matriz
  # nt = tiempo de finalización
  # T (duración total) = nt(tiempo final) - Llegada
  i = 1
  for key in procesos.keys():
    matrizFCFS[i][4] = int(matrizFCFS[i][2]) - procesos[key][0]
    i = i + 1
  # E(tiempo de espera) = T - t(Duración) - llegada
  j = 1
  for key in procesos.keys():
    matrizFCFS[j][3] = int(matrizFCFS[j][4]) - procesos[key][1]
    #matrizFCFS[j][3] = int(matrizFCFS[j][3]) - procesos[key][0]
    j = j + 1
  #P = T/t
  k = 1
  for key in procesos.keys():
    matrizFCFS[k][5] = int(matrizFCFS[k][4]) / procesos[key][1]
    k = k + 1


#RR1 y RR4
quantum = 1


def RR1(procesos, quantum, matrizRR1):
  #Variables para limitar el numero de ejecuciones
  a = 0
  b = 0
  c = 0
  d = 0
  e = 0

  resultado = []
  indice = 1
  #Inicilizamos datos del diccionario
  for key in procesos.keys():
    matrizRR1[indice][1] = procesos[key][1]
    matrizRR1[indice][2] = procesos[key][0]
    indice = indice + 1
  #Inicializar cola inicial
  colaProcesos = []
  prioridad = '0'
  #matrizRR1[1][1] = int(matrizRR1[1][1]) - 1
  #matrizRR1[1][2] = int(matrizRR1[1][2]) + 1
  #encolarQuantum(procesos,quantum,colaProcesos,'A')
  #incicia programa
  contTick = 0
  #print(matrizRR1)
  while contTick <= tiempoMaxTot + 2:

    #print(contTick)
    try:
      prioridad = colaProcesos.pop(0)
    except:
      prioridad = 'X'
      #print("Cola vacia")
    #print(prioridad)
    #Actualizamos los bloques que van llegando y marcar su tiempo de ejecución
    if (prioridad == 'A'):
      matrizRR1[1][4] = contTick
      #print(matrizRR1)
      #print("----------------------------------")
      #print(colaProcesos)
      resultado.append('A')
    elif (prioridad == 'B'):
      matrizRR1[2][4] = contTick
      #print(matrizRR1)
      #print("----------------------------------")
      #print(colaProcesos)
      resultado.append('B')
    elif (prioridad == 'C'):
      matrizRR1[3][4] = contTick
      #print(matrizRR1)
      #print("----------------------------------")
      #print(colaProcesos)
      resultado.append('C')
    elif (prioridad == 'D'):
      matrizRR1[4][4] = contTick
      #print(matrizRR1)
      #print("----------------------------------")
      #print(colaProcesos)
      resultado.append('D')
    elif (prioridad == 'E'):
      matrizRR1[5][4] = contTick
      #print(matrizRR1)
      #print("----------------------------------")
      #print(colaProcesos)
      resultado.append('E')
    #Calcular proximos movimientos
    #Checar si alguno de los procesos le tocaría entrar el siguiente tick
    #Agregarlo a una lista
    #print("Checamos prox tick")
    temp = contTick + 1
    #print("temp: "+str(temp))
    #Checamos por prioridad
    #print("Por prioridad")
    #Para A
    #print("Proceso: A " )
    #print("Control: "+str(a))
    if (int(matrizRR1[1][2]) == temp and a == 0 and int(matrizRR1[1][1]) > 0):
      a = 1
      b = 0
      c = 0
      d = 0
      e = 0
      for ja in range(0, quantum):
        #print("Prio Valor actual "+ str(matrizRR1[1][1]))
        if (int(matrizRR1[1][1]) > 0):
          colaProcesos.append('A')
          #print("Pila nueva")
          #print(colaProcesos)
          matrizRR1[1][1] = int(matrizRR1[1][1]) - 1
          matrizRR1[1][2] = int(matrizRR1[1][2]) + 1
    #print("Control al salir: "+str(a))

    #Para B
    #print("Proceso: B " )
    #print("Control: "+str(b))
    if (int(matrizRR1[2][2]) == temp and b == 0 and int(matrizRR1[2][1]) > 0):
      a = 0
      b = 1
      c = 0
      d = 0
      e = 0
      for ja in range(0, quantum):
        #print("Prio Valor actual "+ str(matrizRR1[2][1]))
        if (int(matrizRR1[2][1]) > 0):
          colaProcesos.append('B')
          #print("Pila nueva")
          #print(colaProcesos)
          matrizRR1[2][1] = int(matrizRR1[2][1]) - 1
          matrizRR1[2][2] = int(matrizRR1[2][2]) + 1
    #print("Control al salir: "+str(b))

    #Para C
    #print("Proceso: C " )
    #print("Control: "+str(c))
    if (int(matrizRR1[3][2]) == temp and c == 0 and int(matrizRR1[3][1]) > 0):
      a = 0
      b = 0
      c = 1
      d = 0
      e = 0
      for ja in range(0, quantum):
        #print("Prio Valor actual "+ str(matrizRR1[3][1]))
        if (int(matrizRR1[3][1]) > 0):
          colaProcesos.append('C')
          #print("Pila nueva")
          #print(colaProcesos)
          matrizRR1[3][1] = int(matrizRR1[3][1]) - 1
          matrizRR1[3][2] = int(matrizRR1[3][2]) + 1
    #print("Control al salir: "+str(c))

    #Para D
    #print("Proceso: D " )
    #print("Control: "+str(d))
    if (int(matrizRR1[4][2]) == temp and d == 0 and int(matrizRR1[4][1]) > 0):
      a = 0
      b = 0
      c = 0
      d = 1
      e = 0
      for ja in range(0, quantum):
        #print("Prio Valor actual "+ str(matrizRR1[4][1]))
        if (int(matrizRR1[4][1]) > 0):
          colaProcesos.append('D')
          #print("Pila nueva")
          #print(colaProcesos)
          matrizRR1[4][1] = int(matrizRR1[4][1]) - 1
          matrizRR1[4][2] = int(matrizRR1[4][2]) + 1
    #print("Control al salir: "+str(d))

    #Para E
    #print("Proceso: E " )
    #print("Control: "+str(e))
    if (int(matrizRR1[5][2]) == temp and e == 0 and int(matrizRR1[5][1]) > 0):
      a = 0
      b = 0
      c = 0
      d = 0
      e = 1
      for ja in range(0, quantum):
        #print("Prio Valor actual "+ str(matrizRR1[5][1]))
        if (int(matrizRR1[5][1]) > 0):
          colaProcesos.append('E')
          #print("Pila nueva")
          # print(colaProcesos)
          matrizRR1[5][1] = int(matrizRR1[5][1]) - 1
          matrizRR1[5][2] = int(matrizRR1[5][2]) + 1
    #print("Control al salir: "+str(e))

    #Agregar a la cola a todos los procesos pendientes
    i = 1
    for key in procesos.keys():
      temp = contTick + 1
      #print("para " + key)
      # print("con " + matrizRR1[i][2])
      #Hacerlo según prioridad ABCDE
      if (int(matrizRR1[i][2]) == temp):
        #Los proximos 4 disponibles agregarlos a la cola y quitarlos
        for j in range(1, quantum + 1):
          #print("Valor actual "+ str(matrizRR1[i][1]))
          if (int(matrizRR1[i][1]) > 0):
            if (key == 'A'):
              a = 1
              b = 0
              c = 0
              d = 0
              e = 0
            if (key == 'B'):
              a = 0
              b = 1
              c = 0
              d = 0
              e = 0
            if (key == 'C'):
              a = 0
              b = 0
              c = 1
              d = 0
              e = 0
            if (key == 'D'):
              a = 0
              b = 0
              c = 0
              d = 1
              e = 0
            if (key == 'E'):
              a = 0
              b = 0
              c = 0
              d = 0
              e = 1
            colaProcesos.append(key)
            #print("Pila nueva")
            #print(colaProcesos)
            matrizRR1[i][1] = int(matrizRR1[i][1]) - 1
            matrizRR1[i][2] = int(matrizRR1[i][2]) + 1
      i = i + 1

    #Actualizamos contador global
    contTick = contTick + 1
  #Cálculo datos restantes para cada proceso
  #Cambiamos el valor T a t
  m = 1
  for key in procesos.keys():
    matrizRR1[m][1] = int(matrizRR1[m][4]) - procesos[key][0]
    #matrizRR1[m][3] = int(matrizRR1[m][3]) - procesos[key][0]
    m = m + 1  

  #E = T - t -Llegada
  k = 1
  for key in procesos.keys():
    matrizRR1[k][3] = int(matrizRR1[k][1]) - procesos[key][1]
    #matrizRR1[k][3] = int(matrizRR1[k][1]) - procesos[key][0]
    k = k + 1
  #P = T/t
  n = 1
  for key in procesos.keys():
    matrizRR1[n][5] = int(matrizRR1[n][1]) / procesos[key][1]
    n = n + 1
  #Transformamos a string
  stringProcesosRR1 = ''.join(resultado)
  return stringProcesosRR1


#SPN
def SPN(procesos):

  indice = 1
  #Inicilizamos datos del diccionario
  #Al inicio nt es es momento en el que iniciar el programa
  for key in procesos.keys():
    matrizSPN[indice][1] = procesos[key][1]
    matrizSPN[indice][2] = procesos[key][0]
    indice = indice + 1
  #Inicia programa

  #print(matrizSPN)
  contTick = 1
  procesoMasCorto = 'A'
  resultado = []
  while contTick <= tiempoMaxTot + 2:
    #print("------------------------------")
    #print("Tick actual: "+str(contTick))
    #print("------------------------------")
    #Ejecutar el siguiente valor de menor duración
    i = 1
    for key in procesos.keys():
      #Ejecuta el más corto
      if (procesoMasCorto == key and int(matrizSPN[i][1]) > 0):
        #print("Proceso en ejecución: "+key)
        matrizSPN[i][1] = int(matrizSPN[i][1]) - 1
        matrizSPN[i][2] = int(matrizSPN[i][2]) + 1
        #Agregamos a la salida la ejecución
        resultado.append(procesoMasCorto)
        #print("Me quedan: "+matrizSPN[i][1])
        if (int(matrizSPN[i][1]) == 0):
          procesoMasCorto = 'X'
          #print("Transición: "+procesoMasCorto)
        #print(matrizSPN)
      i += 1
    #Recorrer todos los que estan esperando
    j = 1
    for key in procesos.keys():
      if (int(matrizSPN[j][2]) == contTick and int(matrizSPN[j][1]) > 0):
        #print("Recorremos: "+key+" de : "+matrizSPN[j][2])
        matrizSPN[j][2] = int(matrizSPN[j][2]) + 1
        #print("Recorremos: "+key+" hacia : "+matrizSPN[j][2])
      j += 1

    #Evaluar cual sería el siguiente proceso a ejecutar

    if (procesoMasCorto == 'X'):
      k = 1
      siguienteValor = ''
      proxProcesos = []
      #Agregamos a una lista el valor de todos los procesos que van a empezar el siguiente turno
      for key in procesos.keys():
        if (contTick + 1 == int(matrizSPN[k][2]) and int(matrizSPN[k][1]) > 0):
          proxProcesos.append(int(matrizSPN[k][1]))
          #print("Procesos que quieren entrar:")
          #print(proxProcesos)
        k += 1
      #Ordenamos de menor a mayor
      proxProcesos = sorted(proxProcesos)

      #Asignar el valor que corresponda al valor mínimo
      try:
        siguienteValor = proxProcesos.pop(0)
      except:
        print()
      #print(siguienteValor)
      n = 1
      for key in procesos.keys():
        if (siguienteValor == int(matrizSPN[n][1]) and int(matrizSPN[n][2]) == contTick + 1):
          procesoMasCorto = matrizSPN[n][0]
        n += 1
      #print("Siguiente proceso a ejecutar es : "+procesoMasCorto)

    #Actualizamos contador global
    contTick += 1
  #Calculamos datos restantes
  #print(matrizSPN)
  #T = nt = E + t(inicial)
  T = 1
  for key in procesos.keys():
    matrizSPN[T][4] = int(matrizSPN[T][2]) - procesos[key][0]
    T = T + 1
  #E = - Llegada + T - t(inicial)
  E = 1
  for key in procesos.keys():
    matrizSPN[E][3] = int(matrizSPN[E][2]) - procesos[key][1]
    matrizSPN[E][3] = int(matrizSPN[E][3]) - procesos[key][0]
    E = E + 1
  #P = T / t(inicial)
  P = 1
  for key in procesos.keys():
    matrizSPN[P][5] = int(matrizSPN[P][4]) / procesos[key][1]
    P = P + 1

  stringProcesosSPN = ''.join(resultado)
  return stringProcesosSPN


#Ejecuciones

#FCFS
FCFS(procesos)

#RR1
stringProcesosRR1 = ''
quantum = 1
stringProcesosRR1 = RR1(procesos, quantum, matrizRR1)

#RR4
stringProcesosRR4 = ''
quantum = 4
stringProcesosRR4 = RR1(procesos, quantum, matrizRR4)

#SPN
stringProcesosSPN = SPN(procesos)

#Sacar promedios de los resultados

#FCFS
#Promedio de T
sumaTFCFS = 0
for i in range(1, 6):
  sumaTFCFS = sumaTFCFS + int(matrizFCFS[i][4])

promTFCFS = sumaTFCFS / 5

#Promedio de E
sumaEFCFS = 0
for i in range(1, 6):
  sumaEFCFS = sumaEFCFS + int(matrizFCFS[i][3])

promEFCFS = sumaEFCFS / 5

#Promedio de P
sumaPFCFS = 0
for i in range(1, 6):
  sumaPFCFS = sumaPFCFS + float(matrizFCFS[i][5])

promPFCFS = sumaPFCFS / 5

#Impresión FCFS
print("FCFS: T=" + str(promTFCFS) + " E=" + str(promEFCFS) + " P=" +
      str(promPFCFS))
print(stringProcesos)

#RR1
#Promedio de T
sumaTRR1 = 0
for i in range(1, 6):
  sumaTRR1 = sumaTRR1 + int(matrizRR1[i][1])

promTRR1 = sumaTRR1 / 5

#Promedio de E
sumaERR1 = 0
for i in range(1, 6):
  sumaERR1 = sumaERR1 + int(matrizRR1[i][3])

promERR1 = sumaERR1 / 5

#Promedio de P
sumaPRR1 = 0
for i in range(1, 6):
  sumaPRR1 = sumaPRR1 + float(matrizRR1[i][5])

promPRR1 = sumaPRR1 / 5

#Impresión RR1
print("RR1: T=" + str(promTRR1) + " E=" + str(promERR1) + " P=" +
      str(promPRR1))
print(stringProcesosRR1)
#RR4
#Promedio de T
sumaTRR4 = 0
for i in range(1, 6):
  sumaTRR4 = sumaTRR4 + int(matrizRR4[i][1])

promTRR4 = sumaTRR4 / 5

#Promedio de E
sumaERR4 = 0
for i in range(1, 6):
  sumaERR4 = sumaERR4 + int(matrizRR4[i][3])

promERR4 = sumaERR4 / 5

#Promedio de P
sumaPRR4 = 0
for i in range(1, 6):
  sumaPRR4 = sumaPRR4 + float(matrizRR4[i][5])

promPRR4 = sumaPRR4 / 5

#Impresión RR4
print("RR4: T=" + str(promTRR4) + " E=" + str(promERR4) + " P=" +
      str(promPRR4))
print(stringProcesosRR4)

#SPN
#Promedio de T
sumaTSPN = 0
for i in range(1, 6):
  sumaTSPN = sumaTSPN + int(matrizSPN[i][4])

promTSPN = sumaTSPN / 5

#Promedio de E
sumaESPN = 0
for i in range(1, 6):
  sumaESPN = sumaESPN + int(matrizSPN[i][3])

promESPN = sumaESPN / 5

#Promedio de P
sumaPSPN = 0
for i in range(1, 6):
  sumaPSPN = sumaPSPN + float(matrizSPN[i][5])

promPSPN = sumaPSPN / 5

#Impresión FCFS
print("SPN: T=" + str(promTSPN) + " E=" + str(promESPN) + " P=" +
      str(promPSPN))
print(stringProcesosSPN)

"""
print(matrizFCFS)
print(matrizRR1)
print(matrizRR4)
print(matrizSPN)
"""
