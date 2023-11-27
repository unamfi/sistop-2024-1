from datetime import *

class system_file:
    def __init__(self):
        #Las cantidades se encuentrran en bytes
        self.__route = "fiunamfs.img"
        self.__size = 1440000
        self.__sectors = (self.__size) / 512
        self.__clusterSize = 512 * 4

    def get_Route(self):
        return self.__route
    
    def get_Size(self):
        return self.__size
    
    def get_sectorsNum(self):
        return self.__sectors
    
    def get_clusterSize(self):
        return self.__clusterSize
