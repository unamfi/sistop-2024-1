import os 
import struct 
from datetime import *
from superblock import *
from  fileEntry import *

def copyfromPC(dirtcopy):
    with open (dirtcopy, "rb") as tcopy:
        #Se comprueba el tamaño del archivo para ver que se pueda agregar al volumen
        fsize = os.path.getsize(dirtcopy)
        if(superblock.newFile(fsize)):
            name = os.path.basename(tcopy)
            if (len(name) <= 14):
            # Se debe asignar espacio en el directorio para los metadatos y en el volumen para el archivo, con ello llenar los setters del file y copiar archivo
            # no se como encontrar a partir de donde puedo escribirr en el directorio o en el volumen