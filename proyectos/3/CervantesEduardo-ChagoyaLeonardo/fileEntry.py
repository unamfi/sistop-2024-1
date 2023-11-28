import struct 
from math import ceil
from datetime import *
from superblock import *

class fileEntry():
    #Un archivo se inicializa cuando se copia contenido al FiUnam, se iniciliza con casi todos los atributos vacios, solo se comprueba que sea posible copiar el archivo
    def __init__(self,fileSize, name, route, clusSize, maxSize, entradaArchivos, cdate, mdate):
        self.__route = route
        try:
            if (superblock.newFile(fileSize)):
                self.__fileName = name
                self.__fileSize = fileSize #en bytes
                self.__initialCluster = self.__setinitialCluster(fileSize, maxSize, clusSize, entradaArchivos)
                self.__crtDate = cdate
                self.__modDate = mdate
        except withouthSpace as e:
             print(f"Error al intentar añadir archivo: {e.mensaje}")
    
    #Funciones de apoyo al constructor
    def __setinitialCluster(fileSize, maxSize, clusSize, entradaArchivos): #Funcion que asigna espacio en datos al nuevo archivo
        freeClus = ceil(maxSize / clusSize)
        nClus = ceil(fileSize / clusSize)
        #Se recuperará el último cluster asignado para realizar asignación contigua correcta
        try:
            if(freeClus >= nClus):
                if not entradaArchivos:
                    asignClus = 5
                    return asignClus
                else:
                    asignClus = (entradaArchivos[-1].get_fCluster(clusSize) + 1) #del arreglo de entradas se recupera el ultimo cluster que ocupa la ultima y se asigna como primero el siguiente
                    return asignClus
        except withouthSpace as e:
            print(f"Error al intentar añadir archivo: {e.mensaje}")

    def setfileonDir(self,clusSize): #Funcion que crea la entrada en el directorio de fiunam para el nuevo archivo
        with open (self.get_route(), 'rb') as fiunam:
            on = False
            reach = clusSize * 5
            posicion = clusSize + 2
            fiunam.seek(posicion)#para llegar al primer nombre de entrada del directorio y verificar si no esta utilizado
            while(on == False or posicion < reach-63): #Se realiza mientras no se haya guardado en el directorio o mientras haya espacion en el
                posicion += 15
                if (fiunam.read(15).decode('utf-8') != '---------------'): #Si esta utilizado, se realiza un seek al siguiente nombre
                    posicion += 49
                    fiunam.seek(posicion)
                else: #Se guarda la entrada en el directorio, mediante los atributos y pack
                    posicion -= 1
                    #ASIGNARLO Y GUARDARLO AL DIRECTORIO EN FIUNAM
                    coding = 'ascii'
                    fileEntry.__writeCharacters(fiunam, coding , posicion , '-')
                    fileEntry.__writeCharacters(fiunam, coding , posicion + 1 ,self.get_Name())
                    fileEntry.__writelittlendianNumbers(fiunam, posicion + 16, self.get_Size())
                    fileEntry.__writelittlendianNumbers(fiunam, posicion + 20, self.get_iCluster())
                    fileEntry.__writeCharacters(fiunam, coding , posicion + 24  ,self.get_creationDate())
                    fileEntry.__writeCharacters(fiunam, coding , posicion + 38 ,self.get_modificationDate())
                    on == True
    
    def __readCharacters(dirfile, coding, start, end):
        dirfile.seek(start)
        tmp = dirfile.read((end-start)).decode(coding)
        return tmp
    
    def __writeCharacters(dirfile, coding, start, str):
        dirfile.seek(start)
        dirfile.write(str.encode(coding))
    
    def __readlittlendianNumbers(dirfile, start, end):
        dirfile.seek(start) 
        tmp  = struct.unpack('<I', dirfile.read((end - start)))
        return tmp
    
    def __writelittlendianNumbers(dirfile, start, num):
        dirfile.seek(start)
        dirfile.write(struct.pack('<I', num))

    #getters           
    def get_Name(self):
        return self.__fileName
    
    def get_Size(self):
        return self.__fileSize
    
    def get_iCluster(self):
        return self.__initialCluster
    
    def get_fCluster(self, clusSize):
        fCluster = self.get_iCluster() + (ceil(self.get_Size()/ clusSize) - 1)
        return fCluster
    
    def get_creationDate(self):
        return self.__crtDate
    
    def get_modificationDate(self):
        return self.__modDate
    
    def get_route(self):
        return self.__route
    
    #setters, son invocados por las operaciones y modifican los atributos del archivo según la operacion
    def set_Name(self, name):
        return self.__fileName
    
    def set_creationDate(self):
        return self.__crtDate
    
    def set_modificationDate(self):
        return self.__modDate

#Excepciones de apoyo
class withouthSpace(Exception):
    def __init__(self, mensaje="No hay espacio libre en el volumen"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)