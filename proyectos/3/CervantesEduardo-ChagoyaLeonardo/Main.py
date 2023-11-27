import os 
import threading
from superblock import *

opciones ={'ls':1,
            'cptPC':2,
            'cpfPC':3,
            'del':4,
            'help': 5,
            'exit':6}

def presentacion():
    exit = False;
    print("\t\t\t\t\t---Bienvenido a Mini-SysF---")
    print('Ejecute alguno de los comandos explicados en el archivo de texto para usar el sistema, si no los conoces, escribe  \'help\'')

    super_bloque = superblock("fiunamfs.img")

    while(exit == False):
        opcion = input('\n\t\\User >')
        try:
            if opciones[opcion] == 1:
                print("Decidiste listar")
            
            elif opciones[opcion] == 2:
                print("Decidiste copiar a PC")

            elif opciones[opcion] == 3:
                print("Decidiste copiar de PC")

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