# Práctica 3: ¡Mis archivos evolucionan!

	Práctica creada: 2023.08.31
	Entrega en tiempo: 2023.09.07

**Ojo** Esta práctica se entregará _de la mano_ con el [proyecto
#1](../../proyectos/1/README.md).

## Un proyecto implica avance

En el transcurso del desarrollo de tus proyectos, cada uno de los _objetos_ que
lo constituyen (digamos, por simplicidad, cada uno de los _archivos_) va
registrando avances. Y muchas veces nos produce _ansiedad_ modificar un pedazo
de código, un párrafo de texto o una imagen por el trabajo que le
invertimos... ¿Y si no nos queda bien?

Es por eso que muchas veces nos encontramos con directorios llenos de archivos
que incluyen:

    Proyecto_2.c
	Proyecto_2.atorado.c
	Proyecto_2.con_apuntadores.c
	Proyecto_2.con_arreglos.c
	Proyecto_2.corregido.c
	Proyecto_2.EL_BUENO.c
	Proyecto_2.Final.c
	Proyecto_2.V2.c

¿Cual de estas versiones es verdaderamente **la buena**? Es más... ¿Para qué
tenemos tantas versiones?

Git nos brinda la oportunidad de liberarnos de toda esa molesta historia, y
tener una *verdad única*, ¡y sin perder la historia, manteniendo la capacidad de
volver a cualquier punto en el tiempo!

Les presento como ejemplo el repositorio que uso para control de asistencias del
grupo. Usando el comando que vimos en nuestra práctica anterior:

	$ git log --all --graph --oneline --pretty=format:'%h <%an> %s %Cgreen%d'

(O con el alias que yo establecí, `git lg`, que es equivalente):

![Los *commits* que forman parte de la lista del grupo](./img/git_lg.png)

(adjunté una imagen en vez de copiar únicamente el texto para poder referirme
más fácilmente a las partes; más adelante lo haré únicamente con el texto
copiado)

¡Ojo! El puntito solitario que le indiqué a `git log` (o, en este caso, a
`git lg`, que lo "envuelve" y pasa a `git log`) le indica que me entregue los
resultados relevantes únicamente para el directorio actual, `.`

## ¿Cómo interpretar la historia de Git?

La columna que aparece en rojo tiene el _identificador de cada commit_. Lo que
se nos presenta es una cadena corta (en este caso, de 7 dígitos hexadecimales)
de *la suma SHA1 identificadora* de cada commit. Esta es una abreviación (la
suma completa mide 40 caracteres), pero es suficiente para expresar _sin
ambigüedad_ a cada uno de los commits. (¡Pero no se preocupen! Rara vez las
usamos directamente)

En amarillo, tenemos las ramas locales y remotas (o las _cabezas_) de nuestro
repositorio. Cada rama es, en realidad, sólo el apuntador con un nombre amigable
al humano a un *commit* específico.

Lo demás no es tan relevante para esta práctica, aunque sí es importante en
general. En verde tenemos la fecha, en azul el nombre del autor, y en blanco la
descripción del commit.

## Pónganse los cinturones, ¡que vamos a despegar!

Como paso previo a _viajar en el tiempo_, asegúrense de que no haya tiradero:
Procuren que no haya archivos _tirados_ en el repositorio. Si los hay, pueden
moverlos hacia afuera de éste con las herramientas que más les acomoden. Si hay
cambios en archivos que forman parte de Git, pueden hacer _commit_... ¡Pero
dejen su repositorio en un estado tan limpio como sea posible!

## Y volver, volver. volver...

Puedo volver a un punto en el tiempo con su número de commit. Por ejemplo, si
quiero recuperar mi lista limpia y vacía, puedo volver al commit del 14 de
agosto, _Más adecuaciones para darle la patada inaugural a 2024-1_:

    $ git checkout 044c579
	Note: switching to '044c579'.
	
	You are in 'detached HEAD' state. You can look around, make experimental
	changes and commit them, and you can discard any commits you make in this
	state without impacting any branches by switching back to a branch.
	
	If you want to create a new branch to retain commits you create, you may
	do so (now or later) by using -c with the switch command. Example:
	
	  git switch -c <new-branch-name>

    Or undo this operation with:

      git switch -

    Turn off this advice by setting config variable advice.detachedHead to false

	HEAD is now at 044c579 Más adecuaciones para darle la patada inaugural a 2024-1

Veré únicamente los archivos que existían en ese punto en el tiempo. Si ahora
pido nuevamente `git lg .`, veré que la cabeza anónima de rama sobre la cual
estoy trabajando (`HEAD`) apunta al commit que solicité. Para ver nuevamente la
historia completa del repositorio _en el directorio actual_ tengo que
especificar el switch `--all`:

    ✓ ((HEAD detached at 044c579)*) gwolf@misnenet『33』~/vcs/clase_sistop/semestres/2024-1/lista $ git lg .
	* 044c579 (HEAD) Más adecuaciones para darle la patada inaugural a 2024-1 (Mon Aug 14 18:11:07 2023 -0600 2 weeks ago) <Gunnar Wolf>
    * 3772e39 Preparo la lista para iniciar el semestre 2024-1 (Sun Aug 13 17:04:34 2023 -0600 3 weeks ago) <Gunnar Wolf>
    ✓ ((HEAD detached at 044c579)*) gwolf@misnenet『34』~/vcs/clase_sistop/semestres/2024-1/lista $ git lg --all .
	* 7d4651e (origin/master, origin/HEAD, master) Lista 29/ago (Tue Aug 29 19:48:02 2023 -0600 2 days ago) <Gunnar Wolf>
   * 7e6949b Entregas de la práctica #1 (Mon Aug 28 09:13:10 2023 -0600 3 days ago) <Gunnar Wolf>
   * f67be57 Lista 24/ago (Thu Aug 24 19:44:20 2023 -0600 7 days ago) <Gunnar Wolf>
   * be75006 Actualizo lista con altas y bajas (Wed Aug 23 13:47:09 2023 -0600 8 days ago) <Gunnar Wolf>
   * 63568a8 Agrego correo de alumno por altas/bajas (Tue Aug 22 19:51:38 2023 -0600 9 days ago) <Gunnar Wolf>
   * be49c58 Tomo lista 17 y 22 de agosto (Tue Aug 22 19:50:19 2023 -0600 9 days ago) <Gunnar Wolf>
   * 044c579 (HEAD) Más adecuaciones para darle la patada inaugural a 2024-1 (Mon Aug 14 18:11:07 2023 -0600 2 weeks ago) <Gunnar Wolf>
   * 3772e39 Preparo la lista para iniciar el semestre 2024-1 (Sun Aug 13 17:04:34 2023 -0600 3 weeks ago) <Gunnar Wolf>
   ✓ ((HEAD detached at 044c579)*) gwolf@misnenet『35』~/vcs/clase_sistop/semestres/2024-1/lista $

## ¿Cuál es la diferencia entre dos commits?

**¡UPS!**

El planteamiento de esta práctica todavía no está completo ☹
