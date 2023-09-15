#!/usr/bin/python3

# De algún lugar se supone que obtuve la siguiente cadena
cadena = 'Tengo mucho texto que enviar... ¡Qué flojera! Bueno, pero vamos a enviarlo completo...'

dev = open('/tmp/salida', 'w') # Supóngase que esto abre un archivo real
bytes = bytearray(cadena, 'utf-8')
for byte in bytes:
    dev.write(chr(byte))

### Raspberry → 115200,N,8,1
### Cisco → 38400,N,8,1 ó 9600,N,8,1

## Cada escritura de caracter me tomaría 1/9600 segundo
## (mas señalización -- 1 bit por cada 8)
