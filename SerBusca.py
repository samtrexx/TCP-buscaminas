import socket
import random
import pickle
import time

def generar_tablero(dificultad):
    filas, columnas, minas = (9, 9, 10) if dificultad == 'principiante' else (16, 16, 40)
    tablero = [['_' for _ in range(columnas)] for _ in range(filas)]
    minas_pos = set()

    while len(minas_pos) < minas:
        mina_fila = random.randint(0, filas - 1)
        mina_columna = random.randint(0, columnas - 1)
        minas_pos.add((mina_fila, mina_columna))

    return tablero, minas_pos

def manejar_cliente(conexion, direccion):
    print(f"Conexión desde {direccion}")
    dificultad = conexion.recv(1024).decode()
    
    # Generar el tablero según la dificultad
    tablero, minas_pos = generar_tablero(dificultad)
    conexion.send("Tablero listo. Comienza el juego.".encode())
    
    inicio = time.time()

    while True:
        # Recibir coordenadas del jugador
        fila, columna = pickle.loads(conexion.recv(4096))
        
        if (fila, columna) in minas_pos:
            # Revelar todas las minas
            for mina_fila, mina_columna in minas_pos:
                tablero[mina_fila][mina_columna] = "1"
            
            # Enviar mensaje de que se pisó una mina y luego enviar el tablero completo
            conexion.send("mina pisada".encode())
            conexion.send(pickle.dumps(tablero))  # Enviar tablero con todas las minas reveladas

            fin = time.time()
            duracion = fin - inicio  
            conexion.send(pickle.dumps(duracion))
        
            break  # Terminar el juego

        else:
            conexion.send("casilla libre".encode())
            # Actualizar el tablero (mostrar la casilla descubierta)
            tablero[fila][columna] = "0"
            conexion.send(pickle.dumps(tablero))  # Enviar el tablero actualizado

        # Verificar si ha ganado
        if all(tablero[fila][columna] != '_' for fila in range(len(tablero)) for columna in range(len(tablero[0])) if (fila, columna) not in minas_pos):
            conexion.send("ganaste".encode())
            break

    # Calcular y enviar la duración al final del juego
    fin = time.time()
    duracion = fin - inicio
    print(f"Duración del juego: {duracion:.2f} segundos")
    conexion.send(pickle.dumps(duracion))
    conexion.close()

def iniciar_servidor():
    # ip = input("Introduce la IP en la que recibir solicitudes: ")
    # puerto = int(input("Introduce el puerto: "))
    ip = "192.168.1.72"
    puerto = 54321

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((ip, puerto))
    servidor.listen(1)
    print("Esperando conexiones...")

    while True:
        conexion, direccion = servidor.accept()
        manejar_cliente(conexion, direccion)

if __name__ == "__main__":
    iniciar_servidor()
