import struct
import codecs


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

#Misma función que directorio, pero no guarda datos en una lista, y
#Nos da los datos que queremos copiar en las variables globales 
def directorioCopiar(entrada):
    global clusterCop
    global tamCop
    #Lee el contenido de un directorio
    contador = 0
    #Abrimos disco
    with open('fiunamfs.img','rb') as f:
        #Sabemos que el directorio esta en los clusters 1-4
        #Por lo tanto empieza en 2048 = cada cluster * 1
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
                    pass
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
                tamCop= int.from_bytes(f_contents,byteorder='little')
                #print(int.from_bytes(f_contents,byteorder='little'))
                #print(tipoArchivo)
                contador += 3
            if(contador == 20):
                #Leemos los 3 bytes correspondiente a
                #el cluster inicial
                f_contents = f.read(3)
                #print(f_contents)
                clusterCop = int.from_bytes(f_contents,byteorder='little')
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
    #Si mide 4 y cada uno mide 1024, el directorio mide 4096.
    #Si le agregamos el espacio que ocupa el superbloque 4096 + 2048 = 6114.
    #Si luego dividimos 6114 / 64 = 96 obtenemos el número de espacios de directorios
    
    #Obtenemos todos los directorios ocupados
    for i in range (96):
        directorio(i,listaDir)
    #Recorremos la lista generado con los números de los directorios ocupados
    for j in (listaDir):
        printDirectorio(j)

def copiar(dir,archivo):
    #Inicializamos las varibales globales
    #  con los datos del directorio ingresado
    directorioCopiar(dir)
    print("Copiar")
    print(clusterCop)
    print(tamCop)
    resultado = ''
    #El contador va a empezar en el cluster indicado por clusterCop
    #multiplicado por sector * 4. A eso le sumamos el superbloque
    contador = (clusterCop * (2048)) 
    print("empieza en: "+str(contador))
    contadorFinal = contador + tamCop
    print("termina en :"+str(contadorFinal))
    #Metemos todo el contenido del archivo en una variable 
    with open('fiunamfs.img','rb') as f:
        f.read(contador)
        while contador < contadorFinal:
            if(contador + 10000 < contadorFinal):
                f_contents = f.read(10000)
                temp = str(f_contents)
                resultado = resultado + temp
                contador += 10000
            elif(contador + 5000 < contadorFinal ):
                f_contents = f.read(5000)
                temp = str(f_contents)
                resultado = resultado + temp
                contador += 5000
            elif(contador + 2000 < contadorFinal ):
                f_contents = f.read(2000)
                temp = str(f_contents)
                resultado = resultado + temp
                contador += 2000
            elif(contador + 1000 < contadorFinal ):
                f_contents = f.read(1000)
                temp = str(f_contents)
                resultado = resultado + temp
                contador += 1000
            elif(contador + 500 < contadorFinal ):
                f_contents = f.read(500)
                temp = str(f_contents)
                resultado = resultado + temp
                contador += 500
            elif(contador + 50 < contadorFinal ):
                f_contents = f.read(50)
                temp = str(f_contents)
                resultado = resultado + temp
                contador += 50
            elif(contador + 15 < contadorFinal ):
                f_contents = f.read(15)
                temp = str(f_contents)
                resultado = resultado + temp
                contador += 15
            elif(contador + 5 < contadorFinal ):
                f_contents = f.read(5)
                temp = str(f_contents)
                resultado = resultado + temp
                contador += 5
            else:
                f_contents = f.read(1)
                temp = str(f_contents)
                resultado = resultado + temp
                contador += 1
    with open(archivo,"w") as file:
        file.write(resultado)
    #print(resultado)

    #El cluster inicial 

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
    for i in range (96):
        directorio(i,listaAct)
    print(listaAct)
            
            
        

#Obtenemos super bloque
#superbloque()
#El superbloque ocupa 2 clusters
#listadoDir()

desfragmentar()

printDirectorio()

#copiar(5,'archivo.txt')

#eliminar(5)



