import struct
import codecs


sector = 256

def superbloque():
    #variables globales
    global numClusterB
    global numClusterD
    global numClusterT
    with open('fiunamfs.img','rb') as f:
        entrada = 0
        lista = []
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

def directorio(entrada):
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
                    print("entrada normal")                   
                    print(tipoArchivo)
                    if(tipoArchivo == 47):
                        print("entrada vacía")                   
                        print(tipoArchivo)
                else:
                    print("Tipo de archivo desconocido")                  
                print(f_contents)
                #print(tipoArchivo)
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
                #print(tipoArchivo)
                contador += 3
            if(contador == 20):
                #Leemos los 3 bytes correspondiente a
                #el cluster inicial
                f_contents = f.read(3)
                print(f_contents)
                print(int.from_bytes(f_contents,byteorder='little'))
                #print(tipoArchivo)
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

            
    print("Fin2")


#Obtenemos super bloque
#superbloque()
#Ubicamos al directorio
cadaCluster = sector * 4
#Checamos el contenido del directorio 0
directorio(2)


