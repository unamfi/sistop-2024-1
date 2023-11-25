import struct
import math


#Definimos el archivo a evaluar
mainFile = "fiunamfs.img"
img = open(mainFile,"br+")


#Estas funciones nos ayudan a sacar los datos de los archivos
def getData(start, size):
    global img
    img.seek(start)
    return img.read(size)

def unpackData(start, size):
    global img
    img.seek(start)
    dato = img.read(size)
    return struct.unpack('<i', dato)[0]

def unpackDataASCII(start, size):
    global img
    img.seek(start)
    return img.read(size).decode("ascii")


#Definimos las variables correspondientes a los clusters y al tamaño del directorio, así como la lista de los archivos y el almacenamiento del mapa.
sizeCluster= unpackData(40,4) 
dirClusters = unpackData(45,4)
UnClusters = unpackData(50,4)
dirSize = 64
fileList=[]
storageMap = []

#Inicializa el mapeo
def initMap():
    global storageMap
    for x in range(5):
        storageMap.append(1)
    while (len(storageMap) != 720):
        storageMap.append(0)

#Actualiza la informacion en el mapa a partir de la lista de archivos 
def updateMap():
    global storageMap
    global fileList
    for x in range(720):
        storageMap[x]=0
    for x in range(5):
        storageMap[x]=1
    for archivoActual in fileList:
        aux = archivoActual.numClusters
        for j in range(aux):
            storageMap[archivoActual.firstCluster+j] = 1

#Definimos la clase file para que cada archivo leído, obtenga las propiedades de nombre, tamaño, el cluster, la fecha de creación y el tamaño de cluster equitativo.
class file:
    global sizeCluster
    def __init__(self, name, size, firstCluster, date):
        self.name = name.replace(" ","")
        self.size = size
        self.firstCluster = firstCluster
        self.date = date
        self.numClusters = math.ceil(size/sizeCluster)

#Definimos getData y lo ponemos para imprimirlo
def getData(posicion):
    start = 1024 + (posicion * 64)
    if(unpackDataASCII(start+1,14) != "--------------"):
        name = unpackDataASCII(start+1, 14)
        size = unpackData(start+16, 4)
        firstCluster = unpackData(start+20,4)
        date = unpackDataASCII(start+24, 14)
        if(size!=0):
            aux = file(name,size, firstCluster, date)
            return aux
        else:
            return

#Inicializa los archivos con los datos del directorio principal obtenidos
def initFiles():
    global fileList
    sizeDir = int((sizeCluster * dirClusters)/dirSize)
    for x in range(sizeDir):
        res = getData(x)
        if(res != None):
            fileList.append(res)
            updateMap()

#Nos muestra la lista de los archivos dentro del directorio principal
def showDir():
    global fileList
    for x in fileList:
        print(str(x.name)+"        "+str(x.size)+" bytes")






#Obtiene el mapa de la imagen 
initMap()

#Obtiene los archivos almacenados
initFiles()

#Se inicia el menú
print ("Bienvenidx a FIUnamFS")
while(True):
    print("\nOpciones:\n1) Listar los contenidos del directorio\n2) Copiar uno de los archivos de dentro del FiUnamFS hacia tu sistema\n3) Copiar un archivo de tu computadora hacia tu FiUnamFS\n4) Eliminar un archivo del FiUnamFS\n5) Desfragmentar\n6) Salir\n")
    opcion = input("")
    if (opcion == "1"):
        print("El contenido del directorio es \n")
        showDir()
    if (opcion == "2"):
        print("Debo de copiar el archivo desde FIUnamFS a la computadora...\n")
    if (opcion == "3"):
        print("Debo de copiar el archivo de tu computadora hacia FIUnamFS...\n")
    if (opcion == "4"):
        input("Debo de eliminar el archivo...\n")
    if (opcion == "5"):
        input("Debo de desfragmentar...\n")
    if (opcion == "6" ):
        #Para cerrar el programa
        exit()