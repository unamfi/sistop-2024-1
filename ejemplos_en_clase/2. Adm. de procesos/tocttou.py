#!/usr/bin/python3
#
# TOCTTOU -- Ilustra la _CONDICIÓN DE CARRERA_ creando un fallo de tipo "Time Of
# Check To Time Of Use"

import sys
import os
import os.path
import time

print("Veamos los permisos de %s" % sys.argv[1])

if not(os.path.exists(sys.argv[1])):
    print("Tu archivo %s no existe" % sys.argv[1])
    exit(0)

# (...)
time.sleep(2)

permisos = os.stat(sys.argv[1])
size = permisos.st_size
if size > 1000:
    print('Es un archivote!')
else:
    print('Es un archivito')
