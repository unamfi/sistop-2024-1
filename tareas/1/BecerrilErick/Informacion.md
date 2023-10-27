# * El problema que se decidió resolver

Decidí resolver el problema del Elevador, porque se me hizo muy interesante este tipo de situaciones y que al igual que la de los servidores es mucho más probable que ocurra en la realidad. 

# * El lenguaje y entorno en que se desarrolló      
Se resolvió en el lenguaje Python ya que es un lenguaje mucho más facil de leer y de escribirse, tiene demasiadas bibliotecas y que la portabilidad que tiene Python hace que sea compatible con la gran mayoria de los Sistemas Operativos. Y para poder ejecutarlo se recomienda tener instalado alguna version de Python (De preferencia Python3)


# * Estrategia de Sincronización
Se eligió utilizar una cola (Queue) en este código para controlar el acceso de los usuarios al elevador debido a sus propiedades específicas y ventajas en este contexto:

* La cola mantiene un orden de llegada estricto. Los usuarios que llegan primero a la cola serán los primeros en abordar el elevador, lo que garantiza un tratamiento justo y evita situaciones de inanición.

* Usar una cola facilita la sincronización entre los usuarios y el elevador. Cuando un usuario quiere abordar el elevador, simplemente llama a queue.get(), lo que bloquea al usuario hasta que sea su turno. Esto es más simple de implementar que otros patrones de sincronización, como el mutex o el semáforo.

* La cola asegura que un solo usuario aborde el elevador a la vez. Esto evita problemas de acceso simultáneo al elevador que podrían ocurrir con otros enfoques.
* Evita la congestión: Al permitir que los usuarios esperen en cola antes de abordar, evita la congestión en el elevador y garantiza que no haya más usuarios dentro del elevador que su capacidad máxima.

* Utilizar una cola en este programa hace que el código sea más claro y legible, ya que refleja de manera intuitiva la idea de que los usuarios esperan en línea para abordar el elevador.
