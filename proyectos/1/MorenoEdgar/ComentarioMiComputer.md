# Revisión de MiComputer

De acuerdo a la condición establecida, y que realizaré el proyecto de manera individual, el número de fasículo que me corresponde es el 12.

$$\lfloor\frac{(318192950 + 0) \% 100}{4}\rfloor=12$$
# Artículo central: Commodore Vic-20  

En el artículo central se habla de la Commodore Vic-20, lanzada en 1981 por _Commodore Business Machines (CBM)_ y siendo predecesora de la _Personal Electronic Transactor (PET)_.

Lo primero que me llamó la atención de esta computadora, es que esta contiene un chip exclusivo para visualización en pantalla, el cual es el _Video Interface Chip_, que además es el que le da su nombre a la computadora. Este chip tiene la capacidad de visualizar hasta 16 colores, mostrando en pantalla un borde de 8 colores seleccionables, un fondo de 16 colores, y los caracteres que pueden tener un color de 8 seleccionables. Esto a día de hoy no podrá parecer muy impresionante, ya que tenemos interfaces gráficas mucho más complejas y llamativas, además la resolución que manejaba era de $184\times175$ pixeles, lo cual me parece increíblemente poco, pero que en su época seguramente no lo fue.

Sin embargo, no era una computadora perfecta, ya que esta tenía una capacidad de memoria muy limitada, siendo de solo $5 Kb$, con solo $3.5 Kb$ utilizables y con la capacidad de direccionar $32 Kb$ de memoria, parece una cantidad extremadamente limitada, tomando en cuenta que en un procesador relativamente moderno la memoria caché L1, la más pequeña, tienen capacidades cerca de los $512 Kb$, lo cual es considerablemente mayor.  

En la imagen presentada del artículo, noté que en el teclado tiene grabados varios símbolos y caracteres, los cuales parece ser que corresponden a los carácteres gráficos, además de las teclas programables las cuales me son muy familiares con las teclas _Fn_, pero en una posición distinta.

Finalmente, es destacable la cantidad de conexiones que puede tener esta computadora, permitiendo conectar palancas de mando, lápices ópticos, ampliación de memoria, impresoras, e incluso cartuchos de juegos, lo cual seguramente habría sido una característica de mi interés.

# Buffers

Uno de los conceptos más básicos en la computación son los _buffers_, el cual curiosamente está muy vagamente definido para dos sentidos diferentes, pero el que yo siempre he conocido es el término de _buffer_ en memoria.

El concepto de _buffer_ ha estado bastante presente desde que me inicié en el área de la programación, sin embargo pocas veces fue bien explicado, incluso hasta fue un término confuso, sin embargo en este artículo lo explica de una manera bastante clara mediante distintos ejemplos.

En el segundo ejemplo nos menciona el caso de las impresoras, lo cual nos ejemplifica el caso del uso de un _buffer_ para compensar la diferencia de velocidad entre el hardware (la impresora) y el software (la computadora), por lo que se **aparta un espacio en memoria** de la computadora para ir almacenando los carácteres, lo cual será el _buffer de impresión_, esta parte es una buena introducción para los _buffers FIFO_, ya que en el _buffer de impresión_ se van almacenando los caracteres que se irán imprimiendo y posteriormente se envían de uno en uno.

Durante el desarrollo de esta parte me llamó la atención una situación que menciona, ya que recuerdo haberla vivido hace muchos años cuando tenía que realizar un documento en Word, y la computadora se alentaba de vez en cuando, sucedía que cuando normalmente se iba escribiendo de repente dejaba de escribir y luego de unos segundos soltaba todas las letras que se habían escrito, detrás de esto lo que pasaba es que estas pulsasiones de las teclas se iban guardando en el _buffer de digitación avanzada_, que de cierta manera recuerda lo que se iba escribiendo.

Lo que más me llamó la atención de este artículo fue en la parte de _Buffers de memoria en harware_, se menciona que antes las impresoras no permitían que la computadora realizara otra labor mientras se realizaba una impresión, la solución de algunos fabricantes fue ofrecer _buffers de impresión_, que eran cajas que se conectaban entre la computadora y la impresora, las cuales contenían una memoria exclusiva de hasta $16 Kb$ con su propio software, a las cuales se les envía la información de los archivos a imprimir, administrando la cantidad de información que se va enviando a la impresora mediante banderas, indicando si se pueden enviar más datos o hay que esperar a que la impresora se desocupe, y permitiendo además que el ordenador no se mantenga ocupado realizando la impresión.

Finalmente, el artículo explica de una manera clara y sencilla la diferencia entre un _buffer_ y una pila (_stack_), ya que si bien son dos estructuras de datos similares, se diferencian en cómo los datos se ingresan y se recuperan de estos. Esta explicación me pareció bastante buena, ya que sin dar muchos rodeos y mediante una explicación mediante una analogía y también con una sección de código, deja en claro estos dos conceptos.