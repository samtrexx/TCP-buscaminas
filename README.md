Deberá implementarse una aplicación cliente con las siguientes características:
· La aplicación cliente deberá conectarse con la aplicación servidor a través de un socket (la dirección y puerto destino deberán ser proporcionados por el jugador).
·Una vez conectado, el jugador elige la dificultad del juego, puede elegir el nivel:
principiante: tablero de 9 × 9 casillas y 10 minas.
avanzado: tablero de 16 × 16 casillas y 40 minas.
La aplicación cliente envía la elección al jugador y recibe un mensaje de confirmación. En ese momento se imprime un tablero local que sólo sirve para imprimir la información que manda el servidor.
El jugador tendrá la capacidad de descubrir una casilla. La aplicación cliente manda al servidor las coordenadas de la casilla para que el servidor valide su contenido. Espera la respuesta del servidor y actualiza la información del tablero.
En el caso que descubra una casilla que contiene una mina, la aplicación cliente deberá descubrir todas las minas del tablero y notificar al jugador que ha perdido. En el caso que se descubran todas las casillas del tablero, menos las que contienen minas, la aplicación cliente deberá notificar al usuario que ha ganado la partida, y mostrar la duración del juego.
Deberá implementarse una aplicación servidor con las siguientes características:
·la aplicación solicita al usuario especificar la IP y el puerto en el que recibirá solicitudes de conexión usando sockets
· Una vez iniciado el servidor, este recibirá la conexión del jugador.
· En cuanto se conecte un cliente, el servidor recibirá la dificultad que se desea jugar, con base en esta dificultad se generará un tablero que contendrá el número de minas correspondientes a la dificultad colocadas de forma aleatoria dentro del tablero.
El servidor envía un mensaje de confirmación indicando que está listo para recibir y validar cada una de las acciones del jugador(destapar y validar)
El servidor recibe las coordenadas del tiro y valida que la casilla se encuentre libre, si es así manda un mensaje de control tipo “casilla libre”. Si la casilla tiene mina, el servidor manda un mensaje tipo “mina pisada”.
El servidor deberá registrar una marca de tiempo al inicio y al final de la partida para determinar la duración del juego.
Al finalizar la partida, (es decir, cuando todas las minas han sido marcadas, cuando todas las casillas han sido destapadas, excepto las que contienen minas, o cuando se ha destapado una casilla que contiene mina), el servidor deberá informar al jugador si ganó o perdió la partida, así como mostrar un registro del tiempo que duró la partida.

