# Restaurante Casa de Toño

## Descripción

Día a día el restaurante Casa de Toño recibe grandes cantidades de gente en sus establecimientos. Aquellos que han comido en dicho lugar conocen muy bien la fila de esperar que llega a existir a ciertas horas. En estas horas, la gente va llegando y conforme se desocupa un lugar para el tamaño del grupo, pasa dicho grupo al establecimiento. En ningún punto meten gente que cuando no hay cupo disponible, y pueden llegar a meter a un grupo que llegó después que otro dependiendo el tamaño de este.

Con esto en mente, se intentará simular el programa que se encarga de mostrar los turnos que tocan en pantalla considerando la cola de espera, así como el tamaño de grupo en cuestión.

## Elementos de concurrencia

En este caso se observa lo siguiente:

1. El restaurante cuenta con un tamaño específico de mesas para un tamaño específico de grupo. Por ello, la primera consideración es que no puede entrar gente si todas las mesas están ocupadas.

2. Se tiene un tamaño de grupo asignado por mesa, por lo mismo, para el restaurante es importante optimizar la asignación de mesas dependiendo de este factor, es decir, no puede asignar una mesa de cuatro personas a una persona. 

3. Se tiene que observar que, aunque pueda pasar que un grupo de 4 que llegó después que una persona pase primero, si hay otros grupos de 4 esperando, estos deberán de pasar primero que aquel que llegó último, es decir, hay un orden en cómo llegan las personas en los diferentes grupos.
