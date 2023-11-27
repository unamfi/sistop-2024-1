import struct 

class superblock():
    def __init__(self, route):
    #Para inicializar el superbloque, se recuperará la información del bloque que se encuentra en fiunamfs.img
        self.__route = route

        with open(self.__route, 'rb') as fiunam:
        #Especifiaciones del super bloque
            self.__name = superblock.__readCharacters(fiunam, 'utf-8', 0, 8)
            self.__version = superblock.__readCharacters(fiunam, 'utf-8', 10, 14)
            self.__volumeLabel = superblock.__readCharacters(fiunam, 'utf-8', 20, 39)
            self.__clusterSize = superblock.__readlittlendianNumbers(fiunam, 40, 44)
            self.__dirSize = superblock.__readlittlendianNumbers(fiunam, 45, 49)
            self.__cuSize = superblock.__readlittlendianNumbers(fiunam, 50, 54)
        #Variables del super bloque que permiten controlar las operaciones en la unidad
            self.__volactualSize = ((self.get_unitnumClusters()-5) * self.get_clusterSize())
            self.__diractualSize = (self.get_dirnumClusters() * self.get_clusterSize()) 

    #Funciones de apoyo para el constructor
    def __readCharacters(dirfile, coding, start, end):
        dirfile.seek(start)
        tmp = dirfile.read((end-start)).decode(coding)
        return tmp
    
    def __readlittlendianNumbers(dirfile, start, end):
        dirfile.seek(start) 
        tmp  = struct.unpack('<I', dirfile.read((end - start)))
        return tmp

#getters           
    def get_name(self):
        return self.__name
    
    def get_version(self):
        return self.__version
    
    def get_label(self):
        return self.__volumeLabel
    
    def get_clusterSize(self):
        return self.__clusterSize
    
    def get_dirnumClusters(self):
        return self.__dirSize
    
    def get_unitnumClusters(self):
        return self.__cuSize
    
    def get_actualdirSize(self):
        return self.__diractualSize
    
    def get_volactualSize(self):
        return self.__volactualSize
#setters
#Insertar setters que modifiquen el directorio y el espacio en el volumen cada que se mueven o eliminan archivos

#Metodos para operaciones y archivos
    def newFile(self, fileSize):
        if (self.get_volactualSize()  >=  fileSize):
            self.__diractualSize-= 64
            self.__volactualSize-= fileSize
            return True
        else:
            return False