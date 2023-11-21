import struct
import codecs
import math
import os
import time

class Registros:
    def __init__(self,tipo,nombre,tamaño,clusterInicial,hfCreacion,hfModif,espLibre,registro):
        self.tipo = tipo
        self.nombre = nombre
        self.tamaño = tamaño
        self.clusterInicial = clusterInicial
        self.hfCreacion = hfCreacion
        self.hfModif = hfModif
        self.espLibre = espLibre
        self.registro = registro

sector = 256
#variables a copiar
clusterCop = 0
tamCop = 0

#Variable para llevar la cuenta de los directorios activos
listaDir = []

def superbloque():
    #variables globales
    global numClusterB
    global numClusterD
    global numClusterT
    with open('fiunamfs.img','rb') as f:
        entrada = 0
        #unpack requiere un buffer de 4 bytes
        while entrada < 64:
            if (entrada == 0):
                #Leemos los 8 bytes correspondientes al
                #nombre del administrador de archivos          
                f_contents = f.read(8)
                #Le quitamos los caracteres extras
                nombreSA = str(f_contents)
                nombreSA = nombreSA.replace('b','')
                nombreSA = nombreSA.replace("'","")
                #Validamos
                if (nombreSA == 'FiUnamFS'): 
                    #print("sistema de archivos correcto")
                    print("Nombre de sistema de archivos: "+nombreSA)
                else:
                    print("Error de sistema de archivos") 
                entrada += 8
                print(f_contents)
            if (entrada == 10):
                #Leemos los 4 bytes correspondientes a
                #la versión 
                f_contents = f.read(4)
                #Le quitamos los caracteres extras
                nombreV = str(f_contents)
                nombreV = nombreV.replace('b','')
                nombreV = nombreV.replace("'","")
                #Validamos
                if (nombreV == '24.1'):
                    #print("versión correcta")
                    print("versión: "+nombreV)
                else:
                    print("Error de versión")     
                print(f_contents)
                entrada += 4
            if (entrada == 20):
                #Leemos los 19 bytes correspondientes a
                #la atiqueta del volumen
                f_contents = f.read(19)
                entrada += 19
                print(f_contents)
            if (entrada == 40):
                #Leemos los 4 bytes correspondientes a
                #el número del cluster en bytes
                f_contents = f.read(4)
                #Desempaquetamos
                numClusterB = struct.unpack('<I', f_contents)
                print(f_contents)
                print(numClusterB)
                entrada += 4
                
            if (entrada == 45):
                #Leemos los 4 bytes correspondientes a
                #el número de clusters que mide el directorio
                f_contents = f.read(4)
                #Desempaquetamos
                numClusterD = struct.unpack('<I', f_contents)
                print(f_contents)
                print(numClusterD)
                entrada += 4
            if (entrada == 50):
                #Leemos los 4 bytes correspondientes a
                #el número de clusters que mide la unidad completa
                f_contents = f.read(4)
                #Desempaquetamos               
                numClusterT = struct.unpack('<I', f_contents)
                print(f_contents)
                print(numClusterT)
                entrada += 4
            else:
                #Avanzamos el cursor 1 posición si no
                #entró a ninguna otra condición
                f_contents = f.read(1)
                #Avanzamos el contador 1 posición
                entrada += 1
    
    print("Fin")

#Checa el contendido del directorio, si es un directorio activo,
#lo guarda en la lista recibida
def directorio(entrada,listaDir):
    #global listaDir
    #Lee el contenido de un directorio
    contador = 0
    #Abrimos disco
    with open('fiunamfs.img','rb') as f:
        #Sabemos que el directorio esta en los clusters 1-4
        #Por lo tanto empieza en 256 * 4 = cada cluster * 1
        #  y se le suma 64 por cada entrada
        #inicio = cadaCluster*1 + 64*entrada
        inicio = (2048 * 1) + (64 * entrada)
        f_contents = f.read(inicio)
        while contador < 64:
            if(contador == 0):
                #Leemos el byte correspondiente a
                #el tipo de archivo
                f_contents = f.read(1)
                tipoArchivo = int.from_bytes(f_contents,byteorder='little')
                #Validación
                if (tipoArchivo == 45):
                    #print("entrada normal")                   
                    #print(tipoArchivo)
                    listaDir.append(entrada)
                elif(tipoArchivo == 47):
                    pass
                    #print("entrada vacía")                   
                    #print(tipoArchivo)
                else:
                    pass
                    #print("Tipo de archivo desconocido")                  
                #print(f_contents)
                #print(tipoArchivo)
                contador += 1
            if(contador == 1):
                #Leemos los 15 bytes correspondientes a
                #el nombre del archivo
                f_contents = f.read(15)
                #print(f_contents)
                contador += 15
            if(contador == 16):
                #Leemos los 3 bytes correspondiente a
                #el tamaño del archivo en bytes
                f_contents = f.read(3)
                #Ajustamos la entrada para calcular
                #print(f_contents)
                #print(int.from_bytes(f_contents,byteorder='little'))
                #print(tipoArchivo)
                contador += 3
            if(contador == 20):
                #Leemos los 3 bytes correspondiente a
                #el cluster inicial
                f_contents = f.read(3)
                #print(f_contents)
                #print(int.from_bytes(f_contents,byteorder='little'))
                #print(tipoArchivo)
                contador += 3
            if(contador == 24):
                #Leemos los 14 bytes correspondiente a
                #la hora y fecha de creación del archivo
                f_contents = f.read(14)
                #print(f_contents)
                contador += 14
            if(contador == 38):
                #Leemos los 14 bytes correspondiente a
                #la hora y fecha de la última modificación del archivo
                f_contents = f.read(14)
                #print(f_contents)
                contador += 14
            if(contador == 52):
                #Leemos los 12 bytes correspondiente a
                #el espacio no utilizado
                f_contents = f.read(12)
                #print(f_contents)
                contador += 12
            else:
                f_contents = f.read(1)
                contador += 1

#Crea objetos de los registros en la lista que pases
def directorioLLenar(entrada,listaDir):
    #Lee el contenido de un directorio
    contador = 0
    #Abrimos disco
    with open('fiunamfs.img','rb') as f:
        #Sabemos que el directorio esta en los clusters 1-4
        #Por lo tanto empieza en 256 * 4 = cada cluster * 1
        #  y se le suma 64 por cada entrada
        #inicio = cadaCluster*1 + 64*entrada
        inicio = (2048 * 1) + (64 * entrada)
        f_contents = f.read(inicio)
        while contador < 64:
            if(contador == 0):
                #Leemos el byte correspondiente a
                #el tipo de archivo
                f_contents = f.read(1)
                tipoArchivo = int.from_bytes(f_contents,byteorder='little')                   
                contador += 1
            if(contador == 1):
                #Leemos los 15 bytes correspondientes a
                #el nombre del archivo
                nombreArchivo = f.read(15)
                #print(f_contents)
                contador += 15
            if(contador == 16):
                #Leemos los 3 bytes correspondiente a
                #el tamaño del archivo en bytes
                f_contents = f.read(3)
                tamañoBytes = int.from_bytes(f_contents,byteorder='little')
                contador += 3
            if(contador == 20):
                #Leemos los 3 bytes correspondiente a
                #el cluster inicial
                f_contents = f.read(3)
                clusterInicial = int.from_bytes(f_contents,byteorder='little')
                #print(tipoArchivo)
                contador += 3
            if(contador == 24):
                #Leemos los 14 bytes correspondiente a
                #la hora y fecha de creación del archivo
                fhCreacion = f.read(14)
                #print(f_contents)
                contador += 14
            if(contador == 38):
                #Leemos los 14 bytes correspondiente a
                #la hora y fecha de la última modificación del archivo
                fhModif = f.read(14)
                #print(f_contents)
                contador += 14
            if(contador == 52):
                #Leemos los 12 bytes correspondiente a
                #el espacio no utilizado
                espLibre = f.read(12)
                #print(f_contents)
                contador += 12
            else:
                f_contents = f.read(1)
                contador += 1

        #Creamos objeto con los datos extraidos
        registro = Registros(tipoArchivo,nombreArchivo,tamañoBytes,clusterInicial,fhCreacion,fhModif,espLibre,entrada)
        listaDir.append(registro)


#Función que imprime los datos del registro ingresado
def printDirectorio(entrada):
    global listaDir
    #Lee el contenido de un directorio
    contador = 0
    #Abrimos disco
    with open('fiunamfs.img','rb') as f:
        #Sabemos que el directorio esta en los clusters 1-4
        #Por lo tanto empieza en 256 * 4 = cada cluster * 1
        #  y se le suma 64 por cada entrada
        #inicio = cadaCluster*1 + 64*entrada
        inicio = (2048 * 1) + (64 * entrada)
        f_contents = f.read(inicio)
        while contador < 64:
            if(contador == 0):
                #Leemos el byte correspondiente a
                #el tipo de archivo
                f_contents = f.read(1)
                tipoArchivo = int.from_bytes(f_contents,byteorder='little')
                #Validación
                if (tipoArchivo == 45):
                    print("entrada normal: "+str(tipoArchivo))                   
                                      
                elif(tipoArchivo == 47):                   
                    print("entrada vacía")                   
                    
                else:                   
                    print("Tipo de archivo desconocido")                  
                print(f_contents)
                
                contador += 1
            if(contador == 1):
                #Leemos los 15 bytes correspondientes a
                #el nombre del archivo
                f_contents = f.read(15)
                print(f_contents)
                contador += 15
            if(contador == 16):
                #Leemos los 3 bytes correspondiente a
                #el tamaño del archivo en bytes
                f_contents = f.read(3)
                #Ajustamos la entrada para calcular
                print(f_contents)
                print(int.from_bytes(f_contents,byteorder='little'))
                
                contador += 3
            if(contador == 20):
                #Leemos los 3 bytes correspondiente a
                #el cluster inicial
                f_contents = f.read(3)
                print(f_contents)
                print(int.from_bytes(f_contents,byteorder='little'))
                
                contador += 3
            if(contador == 24):
                #Leemos los 14 bytes correspondiente a
                #la hora y fecha de creación del archivo
                f_contents = f.read(14)
                print(f_contents)
                contador += 14
            if(contador == 38):
                #Leemos los 14 bytes correspondiente a
                #la hora y fecha de la última modificación del archivo
                f_contents = f.read(14)
                print(f_contents)
                contador += 14
            if(contador == 52):
                #Leemos los 12 bytes correspondiente a
                #el espacio no utilizado
                f_contents = f.read(12)
                print(f_contents)
                contador += 12
            else:
                f_contents = f.read(1)
                contador += 1           

#Lista los dorectorios activos
def listadoDir():
    global listaDir
    #Ubicamos al directorio
    #cadaCluster = sector * 4
    #Checamos el contenido del directorio
    #Gracias al superbloque sabemos cuantos clusters mide el directorio
    #Si mide 4 y cada uno mide 2048, el directorio mide 8192.
    #Si luego dividimos 6114 / 64 = 128 obtenemos el número de espacios de directorios
    
    #Obtenemos todos los directorios ocupados
    for i in range (128):
        directorio(i,listaDir)
    print(listaDir)
    #Recorremos la lista generado con los números de los directorios ocupados
    for j in (listaDir):
        printDirectorio(j)


def copiar(dir,archivo):
    #Obetenemos los datos del directorio al que camos a copiar
    listaCopia = []
    directorioLLenar(dir,listaCopia)
    #Vamos al archivo del directorio
    with open('fiunamfs.img','rb') as rf:
        inicio = (2048 * listaCopia[0].clusterInicial)
        print("Copiando desde el cluster: "+str(listaCopia[0].clusterInicial))
        rf.seek(inicio)
        bytes = rf.read(listaCopia[0].tamaño)
    with open(archivo,'wb') as wf:
        wf.write(bytes)


#Función para eliminar archivos
def eliminar(registro):
    #Bastan con cambiar el tipo de archivo a '47'
    #Primero nos ubicamos en el directorio correcto
    #Cluster * número de cluster + 64(numero de registro)
    inicio = (2048 * 1) + (64 * registro)
    contador = 0
    #Primero verificamos que sea un archivo activo
    with open('fiunamfs.img','rb') as rf:
        f_contents = rf.read(inicio)
        while contador < 1:
            print("Entro: "+str(contador))
            #Leemos el byte correspondiente a
            #el tipo de archivo
            f_contents = rf.read(1)
            tipoArchivo = int.from_bytes(f_contents,byteorder='little')
            #Validación
            print("Eliminar")
            if (tipoArchivo == 45):
                #Confirmamos que es un registro activo
                print("registro activo")
                with open('fiunamfs.img','r+b') as wf:
                    elim = b'/'
                    #regresamos el apuntador a donde estaba
                    wf.seek(inicio)
                    #Eliminamos
                    wf.write(elim)
                    print("Cambiamos valor: ")                                                       
            elif(tipoArchivo == 47):                   
                print("entrada vacía")                                  
            else:                   
                print("Tipo de archivo desconocido")                  
            print(f_contents)
            
            contador += 1


        
def desfragmentar():
    #Agregamos a una lista todos los archivo activos del directorio
    listaAct = []
    for i in range (128):
        directorio(i,listaAct)
    print(listaAct)
    #Obtenemos los objetos
    listaObj = []
    for i in listaAct:
        directorioLLenar(i,listaObj)

    for i in range(len(listaObj)):
        print(listaObj[i].nombre)



    #Ordenar los elementos de la lista según el cluster incial
    listaOrdenada = sorted(listaObj,key=lambda x:x.clusterInicial)


    #Para cada registro activo
    #HAcer la suma de donde empieza y donde termina
    #validar si el siguiente empieza donde termina el último (cluster siguiente)
    #Si no, mover sus datos del directorio (objeto mientras)
    #Y Copiar y pegar el archivo dentro del disco para que cumpla


    #para cada elememento de la lista (registros válidos)
    #los archivos empiezan desde el primer cluster
    primerCluster = 5

 
    for i in listaOrdenada:
        #Si  no empieza en el primer cluster disponible
        if(i.clusterInicial > primerCluster):
            #Modificamos el directorio
            with open('fiunamfs.img','r+b') as wf:
                inicioDir = (2048 * 1)+(64 * i.registro)
                wf.seek(inicioDir)
                contador = 0
                while contador < 64:
                    #Solo cambiamos su cluster inicial
                    if (20 == contador):

                        bytes = primerCluster.to_bytes(3,'little')
                        #f_contents = wf.read(3)
                        wf.write(bytes)
          
                        contador += 3
                    else:
                        wf.read(1)
                        contador += 1

                #Copiar archivo en nueva posición
                contador = 0
                #Ubicación del archivo, el objeto guarda los datos inciales, aunque ya fueron modificados en el disco
                inicioArch = (2048 * i.clusterInicial)
                wf.seek(inicioArch)
                bytesCopia = wf.read(i.tamaño)
                #Pegamos la copia en la nueva posición
                inicioNArch = (2048 * primerCluster)
                wf.seek(inicioNArch)
                wf.write(bytesCopia)

        #Calculamos el lugar inicial para el siguiente archivo
        clustersOcupados = i.tamaño / 2048
        #Redondeamos hacia arriba el número de clusters ocupados para almacenar el archivo
        clustersOcupados = math.ceil(clustersOcupados)
        print("Clusters ocpuados")
        print(clustersOcupados)
        #Se calcula lo que ocupó el archivo anterior y le sumamos 1 para que empiece en el siguiente cluster
        primerCluster = primerCluster + clustersOcupados + 1
        print(primerCluster)
                
                
    
        
         
def obteniendoArchivoAgregarDirectorio(archivoAgregar):


    try:
        #Obteniendo el archivo para agregar al final del directorio
        with open(archivoAgregar, 'rb') as archivo:
            #Almacenando el contenido del archivo
            #contenido = archivo.read()
            #print(contenido)
            #contenidoEnBytes = contenido.encode('utf-8')
            #print(contenidoEnBytes)
            nombreDeArchivoCompleto = archivo.name
            if '.' in nombreDeArchivoCompleto:
            #Almacenando nombre de archivo y extensión en dos varaiables diferentes
                extension = nombreDeArchivoCompleto.split('.')[-1]
                nombreDeArchivo = archivo.name.split('.')[0]
            else:
                extension = "Sin extensión"
            if (len(nombreDeArchivo) < 16 ):
                #Se obtiene fecha y hora de creación de archivo
                fechaCreacion = os.path.getctime(nombreDeArchivoCompleto)
                fecha = time.strftime("%Y%m%d%H%M%S", time.localtime(fechaCreacion))
                #Se obtiene fecha y hora de última modificación
                fechaModificacion = os.path.getmtime(nombreDeArchivoCompleto)
                fechaUlitmaModificacion = time.strftime("%Y%m%d%H%M%S", time.localtime(fechaModificacion))
            
                #Agregamos a una lista todos los archivo activos del directorio
                listaAct = []
                for i in range (128):
                    directorio(i,listaAct)
                #print(listaAct)
                #Obtenemos los objetos de esos archivos activos
                listaObj = []
                for i in listaAct:
                    directorioLLenar(i,listaObj)

                #for i in range(len(listaObj)):
                    #print(listaObj[i].clusterInicial)
                
                #Ordenar los elementos de la lista según la magnitud de su cluster incial
                listaOrdenada = sorted(listaObj,key=lambda x:x.clusterInicial)

                print("----------------contenido ordenado por clusters---------------------")
                for i in range(len(listaOrdenada)):
                    print(listaOrdenada[i].clusterInicial)
                print("-------------------------------fin----------------------------------")
                #Colocamos la nueva información en el directorio
                for i in range(128):
                    # Buscamos el primer lugar disponible del directorio 
                    if i not in listaAct:
                        #Convertimos datos a binario
                        nombreBin = nombreDeArchivo.encode('us-ascii')
                        print(nombreBin)
                        fechaModBin = fechaUlitmaModificacion.encode('us-ascii')
                        print(fechaModBin)                      
                        fechaCreaBin = fecha.encode('us-ascii')
                        print(fechaCreaBin)
                        #Cluster inicial
                        #Sumamos el cluster incial y el tamaño del cluster inicial del directorio que tiene el cluster inicial más grande
                        longitudUltimoArchivo = ((listaOrdenada[-1].clusterInicial)*2048)+(listaOrdenada[-1].tamaño)
                        clusterSiguiente = math.ceil(longitudUltimoArchivo / 2048) + 1                  
                        clusterInicial = clusterSiguiente.to_bytes(3,byteorder = 'little')
                        print("Clusters:")
                        print(clusterSiguiente)
                        print(clusterInicial)
                        #Obtenemos tamaño archivo
                        tamArch = os.path.getsize(archivoAgregar)
                        tamArchBin = tamArch.to_bytes(3,byteorder = 'little')
                        print("Tamaños:")
                        print(tamArch)
                        print(tamArchBin)
                        #Valor maximo de entero que se puede representar en 14 bytes
                        maxValor = (256 ** 3) - 1
                        #Verificamos si es un tamaño válido
                        if(tamArch <= maxValor):
                            #Copiamos toda la información del archivo 
                            archivo.seek(0)
                            contenido = archivo.read()
                            print("Contenido del archivo")
                            print(contenido)
                            #print(contenido)
                            
                            with open('fiunamfs.img','r+b') as wf:
                                inicial = (2048)+(64 * i)
                                wf.seek(inicial)
                                contador = 0
                                #Metemos información al directorio
                                while contador < 52:
                                    if(contador == 0):
                                        #Escribimos el byte correspondiente a
                                        #el tipo de archivo
                                        wf.write(b'-')
                                        contador += 1
                                    if(contador == 1):
                                        #Escribimos los 15 bytes correspondientes a
                                        #el nombre del archivo
                                        wf.write(nombreBin)
                                        #Lo recorremos manueal , por si el nombre ocupa menos espacio que el disponible
                                        wf.seek(inicial + 16)
                                        contador += 15
                                    if(contador == 16):
                                        #Escribimos los 3 bytes correspondiente a
                                        #el tamaño del archivo en bytes
                                        wf.write(tamArchBin)
                                        contador += 3
                                    if(contador == 20):
                                        #Escribimos los 3 bytes correspondiente a
                                        #el cluster inicial
                                        wf.write(clusterInicial)
                                        contador += 3
                                    if(contador == 24):
                                        #Escribimos los 14 bytes correspondiente a
                                        #la hora y fecha de creación del archivo
                                        wf.write(fechaCreaBin)
                                        contador += 14
                                    if(contador == 38):
                                        #Leemos los 14 bytes correspondiente a
                                        #la hora y fecha de la última modificación del archivo
                                        wf.write(fechaModBin)
                                        contador += 14
                                    else:
                                        wf.read(1)
                                        contador += 1
                                #Metemos la información al disco donde indica el directorio
                                ubicArch = (clusterSiguiente * 2048)
                                wf.seek(ubicArch)
                                wf.write(contenido)
                        else:
                            print("Tamaño inválido")
                        break

                #print('Nombre de archivo: ' +nombreDeArchivo)
                #print('Fecha de creación con formato AAAMMDDHHMMSS: ' +fecha)
                #print('Fecha de modificación con formato AAAMMDDHHMMSS: ' +fechaUlitmaModificacion)
                #print('Extensión: ' +extension)
                #print('Contenido: ' + contenido)
                
                #infoArchivo = os.stat(archivoAgregar)
                #creacion = infoArchivo.st_ctime
                #aver = datetime.datetime.utcfromtimestamp(creacion)
                #print('Probando: '  +aver)
            else:
                print("Nombre demsasiado largo")
            

    except FileNotFoundError:
        decisionException()
    else: 
        print('Archivo encontrado')


#Función para ingresar nombre del archivo del que se quiere copiar la información
def usuarioIngresaArchivo():
    archivo = input('Ingresa el nombre de tu archivo con extensión: ')
    obteniendoArchivoAgregarDirectorio(archivo)

#Función para imprimir error cuando suceda
def decisionException():
    print('El archivo no se encuentra dentro del directorio del programa')
    decision = input('¿Desea ingresar intentarlo de nuevo? (y/n) ')
    if (decision == 'y' or decision == 'Y'):
        usuarioIngresaArchivo()
    if (decision == 'n' or decision == 'N'):
        print('Adiós')
    else: 
        print('Input inválido')
        decisionException()








               
            

            
        

#Obtenemos super bloque
#superbloque()
#El superbloque ocupa 2 clusters
#1
#listadoDir()

#printDirectorio(4)

#2
#copiar(4,'archivo.txt')

#3
#usuarioIngresaArchivo()
#listadoDir()

#4
#eliminar(5)

#5
#desfragmentar()

