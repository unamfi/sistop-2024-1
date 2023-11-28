import os 
import threading
from superblock import *

route = "fiunamfs.img"

opciones ={'ls':1,
            'cptPC':2,
            'cpfPC':3,
            'del':4,
            'help': 5,
            'exit':6}

def presentacion():
    exit = False;
    global route
    global opciones
    print("\t\t\t\t\t---Bienvenido a Mini-SysF---")
    print('Ejecute alguno de los comandos explicados en el archivo de texto para usar el sistema, si no los conoces, escribe  \'help\'')

    super_bloque = superblock(route) #Objeto super bloque, información vital y control del sistema
    entradaArchivos = [] #Arreglo de fileEntry para tener control de las asignaciones
    print(super_bloque.get_volactualSize())
    

    while(exit == False):
        opcion = input('\n\t\\User >')
        try:
            if opciones[opcion] == 1:
                print("Decidiste listar el directorio fiunam")
            
            elif opciones[opcion] == 2:
                print("Escribe el nombre del arhivo que quieres copiar de fiunam a PC")
                tPC = input('\n\t\\User >')

            elif opciones[opcion] == 3:
                print("Escribe la ruta exacta del archivo en la PC que quieres copiar a fiunam")
                fPC = input('\n\t\\User >')

            elif opciones[opcion] == 4:
                print("Decidiste borrar")
            
            elif opciones[opcion] == 5:
                threading.Thread(target=os.system, args=["Readme.txt"]).start()

            elif opciones[opcion] == 6:
                print("Decidiste salir")
                exit = True
        except KeyError:
                print("El comando no existe, vuelve a intentar")

def main():
    threading.Thread(target=presentacion).start()
    
main()