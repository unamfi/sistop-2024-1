import struct 
from datetime import *
from superblock import *

class fileEntry():
    #Un archivo se inicializa cuando se copia contenido al FiUnam, se iniciliza con casi todos los atributos vacios, solo se comprueba que sea posible copiar el archivo
    def __init__(self, route, fileSize):

        self.__route = route
        try:
            if (superblock.newFile(fileSize)):
                self.__fileName = ''
                self.__fileSize = 0
                self.__initialCluster = 0
                self.__crtDate = ''
                self.__modDate = ''
        except withouthSpace as e:
             print(f"Error al intentar añadir archivo: {e.mensaje}")

#getters           
    def get_Name(self):
        return self.__fileName
    
    def get_Size(self):
        return self.__fileSize
    
    def get_creationDate(self):
        return self.__crtDate
    
    def get_modificationDate(self):
        return self.__modDate
    
    def set_Name(self, name, spblock):
        return self.__fileName

#setters, son invocados por las operaciones y modifican los atributos del archivo según la operacion. Dentro de estos debe hacerse las asignaciones de espacio para el FiUnam 
#El guardar los datos en el volumen en este punto, implica pasarlos a llitleEndian
    def set_Size(self):
        return self.__fileSize
    
    def set_creationDate(self):
        return self.__crtDate
    
    def set_modificationDate(self):
        return self.__modDate

#Funciones de apoyo    
    def __readCharacters(dirfile, coding, start, end):
        dirfile.seek(start)
        tmp = dirfile.read((end-start)).decode(coding)
        return tmp
    
    def __readlittlendianNumbers(dirfile, start, end):
        dirfile.seek(start) 
        tmp  = struct.unpack('<I', dirfile.read((end - start)))
        return tmp

#Excepciones de apoyo
class withouthSpace(Exception):
    def __init__(self, mensaje="No hay espacio libre en el volumen"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)