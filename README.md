PONG (UDP + PYGAME)

Un juego clásico de Pong multijugador en red desarrollado en Python utilizando Pygame para la interfaz gráfica y Sockets UDP para la comunicación en tiempo real entre el servidor y los clientes.

ARQUITECTURA DEL PROYECTO

1. El Servidor (server.py)
Es el núcleo central del juego. Funciona de manera autónoma utilizando un socket UDP no bloqueante y se encarga de:

* Gestión de Conexiones: Asigna automáticamente hasta 2 jugadores a slots fijos basados en la IP y puerto desde donde se conectan.
* Control de Entradas: Recibe las teclas presionadas por los clientes (W/S para el Jugador 1 y las flechas Arriba/Abajo para el Jugador 2).
* Física y Lógica del Juego: Controla el movimiento de la pelota, los rebotes con las paredes, las colisiones precisas con las paletas (con incremento gradual de velocidad) y la anotación de puntos.
* Broadcast: Envía constantemente el estado actualizado del juego (posiciones de la pelota, paletas y puntajes) a todos los clientes conectados.

2. El Cliente (client.py)
Es la interfaz visual que ejecutan los jugadores. Sus funciones principales son:

* Captura de Inputs: Detecta las pulsaciones de teclado locales (W, S, Flecha Arriba, Flecha Abajo) y las transmite al servidor en formato JSON mediante UDP.
* Sincronización: Recibe periódicamente el estado actual del juego enviado por el servidor de forma asíncrona y no bloqueante.
* Renderizado Gráfico: Dibuja en pantalla (usando Pygame) el fondo, el marcador actual, las dos paletas y la pelota basándose exclusivamente en los datos recibidos del servidor.

CÓMO EJECUTARLO

1. Iniciar el Servidor:
Asegúrate de configurar la IP del servidor en el código y ejecútalo primero con el comando:
python server.py
2. Iniciar los Clientes:
En las computadoras o terminales de los jugadores, asegúrate de apuntar a la IP del servidor y ejecuta el comando:
python client.py
