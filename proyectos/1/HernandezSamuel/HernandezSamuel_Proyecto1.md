UNVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO FACULTAD DE INGENIERÍA Sistemas Operativos. Profesor: Ing. Gunnar Eyal Wolf Iszaevich. Grupo: 06 Alumno: Hernández Hernández Samuel Proyecto 1. 
Revision de MiComputer Número de cuenta: 316060497 Fecha de entrega: 12/09/2023


El proyecto lo realice de manera individual asi que sino calcule mal el fasciculo que me toca es el 24

m = m1 + m2 m = 316060497 + 0 m = 316060497 m % 100 = 316060497 % 100 = 97 f = ⌊97 / 4⌋ f = ⌊24.25⌋ f = 24


Fascículo 24. Research Machines 380Z (Articulo principal).

El artículo presenta el Research Machines 380Z, un microordenador que gano en su época mucha popularidad en escuelas y en el Ministerio de Defensa británico gracias a su sólida 
construcción y potentes gráficos de alta resolución. Aunque no se destacaba por su innovación ni por su competitividad en precio, pero si por su fiabilidad y respaldo. El paquete de 
gráficos de alta resolución (HRG) del 380Z era especialmente destacado, ya que permitía una variedad de resoluciones y colores, pero para aprovechar al máximo esas capacidades, era 
esencial contar con un monitor en color con una interfaz RGB. Además, su sistema contaba con tableros adicionales para el control de disco y comunicaciones. Su teclado era resistente y 
diseñado para soportar un uso intensivo, lo que lo hacía ideal para entornos educativos. El sistema se compone de varios tableros, incluyendo la CPU, RAM y gráficos de alta resolución. 
La fuente de alimentación era robusta y difícil de dañar, lo que aumenta la confiabilidad de la máquina. Por último, el 380Z ofrece diferentes versiones de BASIC y el paquete HRG, 
permitiendo a los usuarios adaptar la memoria según sus necesidades. Además, es compatible con varios lenguajes, incluyendo uno similar al Pascal, lo que lo hacía atractivo tanto para 
educadores como para científicos europeos que requerían cálculos matemáticos complejos. En resumen, el Research Machines 380Z destaca por su solidez y capacidades gráficas, siendo una 
elección popular en entornos educativos y militares.

Fascículo 24. Lenguaje ensamblador (Articulo seleccionado).

El texto trata la temática de cómo representar y trabajar con programas en código de lenguaje máquina. Inicia destacando que los programas en este lenguaje pueden tener diversas 
formas, lo que puede resultar confuso para los principiantes, en esencia, todos los datos almacenados en la memoria de una computadora se reducen en última instancia a números binarios 
de ocho dígitos. Sin embargo, representar estos números en papel resulta poco práctico, ya que ocupan mucho espacio y son propensos a errores de escritura. Para abordar este problema, 
se recurre al sistema numérico hexadecimal, el cual presenta ventajas significativas, ya que permite representar el contenido de un byte como un número de dos dígitos y simplifica la 
representación de direcciones de memoria, que van desde 0 hasta 65535 en decimal y se pueden expresar mediante cuatro dígitos hexadecimales. Cuando se escribe un número hexadecimal en 
papel, se suele iniciar con el símbolo "$" para distinguirlo de los números decimales. Es importante destacar que este símbolo no se incorpora a la memoria de la computadora cuando se 
ingresa el programa, además, cuando un opcode (instrucción de máquina) tiene un operando de dos bytes, estos se ingresan en la máquina en orden inverso, es decir, primero el byte de la 
derecha y luego el de la izquierda. Esto simplifica la ejecución para el procesador, pero puede resultar confuso para los usuarios. Los programas en código de lenguaje máquina se 
imprimen comúnmente en formato hexadecimal, con una larga lista de valores hexadecimales de dos dígitos. Además, se proporciona una dirección de inicio, ya sea en hexadecimal o 
decimal, donde se debe cargar el primer valor hexadecimal. Para realizar esta carga, se utiliza la instrucción "POKE" en el lenguaje de programación BASIC. Es esencial convertir los 
valores hexadecimales a decimal antes de utilizarlos en la instrucción "POKE", ya que en el interior de la máquina se almacenan en formato binario. Para programas en código de máquina 
más extensos, es común utilizar un programa adicional en BASIC llamado "cargador de código máquina". Este programa solicita la dirección de inicio y los valores hexadecimales uno por 
uno. A medida que se ingresan, el programa en BASIC convierte estos valores de hexa a decimal y los coloca en la posición siguiente de la memoria. También es posible leer el dump 
hexadecimal utilizando sentencias "DATA". Una vez que el código máquina se ha cargado, se puede prescindir del programa cargador en BASIC. Es importante cargar el código máquina en una 
ubicación de memoria que no se vea afectada por otros programas en BASIC para evitar que se sobrescriba. Además, se menciona que la mayoría de las computadoras personales tienen 
órdenes en BASIC que permiten cambiar del entorno de BASIC al código máquina a partir de una dirección específica. Esto facilita la ejecución de rutinas de código máquina de alta 
velocidad desde el entorno BASIC. El texto también señala que programar en código de lenguaje máquina presenta desafíos, ya que los errores no generan mensajes de error útiles, y un 
error puede hacer que la máquina no responda, lo que requiere reiniciar y volver a ingresar el programa desde cero. Por lo tanto, se enfatiza la importancia de verificar 
exhaustivamente los programas en papel antes de ingresarlos en la computadora. Finalmente, se menciona la utilidad de los monitores de código de lenguaje máquina y los ensambladores 
para simplificar el proceso de programación en código de máquina, así como la transición al lenguaje ensamblador, que facilita la escritura de programas al permitir el uso de 
mnemotecnia en lugar de valores hexadecimales para los operandos.

