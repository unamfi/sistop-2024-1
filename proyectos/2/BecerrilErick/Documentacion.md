# Mecanismos de sincronización empleados:

En el código, se utiliza el mecanismo de bloqueo (threading.Lock) para asegurar que la operación de reserva de asientos sea crítica y se evite la condición de carrera cuando varios hilos intentan reservar el mismo asiento simultáneamente. El bloqueo se adquiere alrededor de la sección crítica del código donde se verifica y realiza la reserva del asiento.

# Lógica de operación:

La lógica principal del programa es permitir que múltiples clientes (hilos) intenten reservar asientos en un teatro de 50 asientos. Los clientes ingresan su nombre y el número de asiento deseado en la interfaz gráfica. Luego, se llama a la función reservar_asiento que intenta realizar la reserva. Si el asiento está disponible, se reserva, y si no lo está, se informa al cliente que el asiento ya está ocupado.

# Estado compartido (variables o estructuras globales):

Las variables compartidas incluyen:

* asientos_disponibles: Una lista que contiene los números de asientos disponibles.
* cola_reservas: Una cola utilizada para mantener un registro de los asientos reservados.
* reservas_clientes: Un diccionario que mapea números de asientos a los nombres de los clientes que los reservaron.

# Descripción algorítmica del avance de cada hilo/proceso:

Cada hilo cliente intenta reservar un asiento llamando a la función reserva_asiento. La función intenta adquirir el bloqueo, verifica la disponibilidad del asiento y lo reserva si está disponible. Luego, el asiento se agrega a la cola de reservas y se almacena en el diccionario reservas_clientes.
Descripción de la interacción entre ellos:

La interacción entre los hilos se produce en la función reserva_asiento, donde varios hilos intentan adquirir el bloqueo para realizar una reserva. Solo un hilo a la vez puede realizar la reserva de un asiento, lo que garantiza que no se dupliquen las reservas.
Entorno de desarrollo:

Lenguaje: Python
Versión de Python: 3.11.1  
Bibliotecas adicionales: tkinter y threading (biblioteca estándar de Python).

Sistema operativo/distribución:

Este código se puede ejecutar en diversos sistemas operativos, incluyendo Windows, macOS y distribuciones de Linux, siempre y cuando tenga Python3 



# Prueba de Ejecución Exitosa del Proyecto

* Iniciamos nuestra ventana de Terminal o CMD dependiendo el Sistema Operativo que tengamos 

![](https://github.com/erickmtz97/imgs/blob/main/p21.png) 

* Mandamos llamar a Python3 desde nuestra ventana de comandos 

![](https://github.com/erickmtz97/imgs/blob/main/p22.png) 

* Pegamos nuestro codigo o llamamos al programa con extension .py para poder ejecutarlo. 
(En mi caso pegare todo el codigo para que no haya ningun problema)

![](https://github.com/erickmtz97/imgs/blob/main/p23.png) 

* Una vez pegado, se nos abre la Interfáz Grafica que nos muestra los asientos que tenemos disponibles

![](https://github.com/erickmtz97/imgs/blob/main/p24.png) 

* Posteriormente ponemos nuestro nombre, escribmos el asiento que queremos reservar y presionamos el boton "Reservar Asiento".
(Para la demostracion pondré mi nombre "Erick" y seleccionaré el número 50)

![](https://github.com/erickmtz97/imgs/blob/main/p25.png) 

* Como podemos ver ahora, el asiento 50 ha desaparecido de los asientos disponibles y más abajo aparece la reserva con exito de ese asiento

* Si otra persona quiere reservar el mismo asiento, el programa no lo dejará avanzar hasta que se seleccione un asiento disponible, asi hasta llenar los 50 asientos.
(Agrego otro nombre "Carlos" y reserva el asiento 25)

![](https://github.com/erickmtz97/imgs/blob/main/ps6.png) 
