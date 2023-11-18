import struct
import codecs

def superbloque():
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
                enteros = struct.unpack('<I', f_contents)
                print(f_contents)
                print(enteros)
                entrada += 4
                
            if (entrada == 45):
                #Leemos los 4 bytes correspondientes a
                #el número de clusters que mide el directorio
                f_contents = f.read(4)
                #Desempaquetamos
                enteros = struct.unpack('<I', f_contents)
                print(f_contents)
                print(enteros)
                entrada += 4
            if (entrada == 50):
                #Leemos los 4 bytes correspondientes a
                #el número de clusters que mide la unidad completa
                f_contents = f.read(4)
                #Desempaquetamos
                enteros = struct.unpack('<I', f_contents)
                print(f_contents)
                print(enteros)
                entrada += 4
            else:
                #Avanzamos el cursor 1 posición si no
                #entró a ninguna otra condición
                f_contents = f.read(1)
                #Avanzamos el contador 1 posición
                entrada += 1
    
    #prueba = struct.unpack('<I', )
    print("Fin")
        
    #enteros = struct.unpack('<I' + 'i' * (len(f_contents) // 4), f_contents)

#Llamamos a la función
superbloque()