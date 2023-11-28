import os 
import struct 
from datetime import *
from superblock import *
from  fileEntry import *

def copyfromPC(dirtcopy, route, maxSize, clusSize, entradaArchivos):
    with open (dirtcopy, "rb") as tcopy:
        #Se comprubea que el nombre cumpla con el máximo de carracteres
        name = os.path.basename(dirtcopy)
        size = os.path.getsize(dirtcopy)
        if (len(name) <= 14):
            if(size < maxSize):
                #Revisar que el archivo entre en la unidad, se realiza  al crear una entrada y si no lanza una excepción
                #Obtener fechas y formatearlas
                cdate = ''
                mdate = ''
                newFile = fileEntry(size, name, route, clusSize, maxSize, entradaArchivos, cdate, mdate) #En esta clase se debe realizar toda la asignación en el espacio del directorio, dentro de esta función, en el espacio dde datos
                newFile.setfileonDir(clusSize)
                entradaArchivos.append(newFile)
                with open(dirtcopy, 'rb') as tocopy:
                    #Apartir del cluster inicial del objeto y su tamaño, escribir en datos de fiunam, según lo ya determinado en directorio al crear el objeto