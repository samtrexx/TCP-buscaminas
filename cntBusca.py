import socket
import pickle

# Función para imprimir el tablero con filas como números y columnas como letras
def imprimir_tablero(tablero):
    columnas = "   " + " ".join([chr(65 + i) for i in range(len(tablero[0]))])  # Imprimir letras para las columnas
    print(columnas)  # Imprimir las letras de las columnas
    for i, fila in enumerate(tablero):
        print(f"{i + 1:<2} " + " ".join(fila))  # Imprimir los números de las filas

# Función para convertir coordenadas en el formato (número, letra) a índices
def convertir_coordenadas(entrada):
    entrada = entrada.strip().replace("(", "").replace(")", "").split(',')
    fila_numero = int(entrada[0].strip())
    columna_letra = entrada[1].strip().upper()
    
    fila = fila_numero - 1  # Restar 1 para convertir a índice basado en 0
    columna = ord(columna_letra) - 65  # Convertir la letra a índice (A=0, B=1, ...)
    return fila, columna

# Función para recibir datos desde el servidor
def recibir_datos(cliente):
    datos = bytearray()  # Usamos un bytearray para acumular los datos
    while True:
        parte = cliente.recv(4096)  # Recibimos hasta 4096 bytes a la vez
        if not parte:
            break  # Si no hay más datos, salimos del bucle
        datos.extend(parte)  # Acumulamos los datos recibidos
    return datos  # Devolvemos todos los datos recibidos

def jugar():
    # Solicitar dirección y puerto del servidor
    ip = input("Introduce la IP del servidor: ")
    puerto = int(input("Introduce el puerto: "))

    # Crear el socket y conectarse al servidor
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((ip, puerto))

    # Elegir la dificultad del juego
    dificultad = input("Elige la dificultad (principiante/avanzado): ").lower()
    cliente.send(dificultad.encode())

    # Recibir confirmación de parte del servidor
    confirmacion = cliente.recv(1024).decode()
    print(confirmacion)

    # Inicializar el tablero vacío según la dificultad
    tablero = [['_' for _ in range(9)] for _ in range(9)] if dificultad == 'principiante' else [['_' for _ in range(16)] for _ in range(16)]
    imprimir_tablero(tablero)

    while True:
        # Ingresar coordenadas en formato (número, letra), por ejemplo (10, f)
        coordenadas = input("Da las coordenadas (número, letra): ")

        # Convertir las coordenadas a índices numéricos
        fila, columna = convertir_coordenadas(coordenadas)

        # Enviar las coordenadas al servidor
        cliente.send(pickle.dumps((fila, columna)))

        # Recibir la respuesta del servidor
        respuesta = cliente.recv(1024).decode()

        if respuesta == "mina pisada":
            # Recibir el tablero completo con todas las minas descubiertas
            datos_tablero = recibir_datos(cliente)
            tablero = pickle.loads(datos_tablero)
            imprimir_tablero(tablero)
            print("¡Has pisado una mina! Todas las minas han sido descubiertas. Has perdido.")   

            # Recibir duración
            datos_duracion = recibir_datos(cliente)
            if datos_duracion:
                duracion = pickle.loads(datos_duracion)
                print(f"Duración del juego: {duracion:.2f} segundos")
            else:
                print("Error: No se recibieron datos de duración.")

            break
        elif respuesta == "casilla libre":
            # Recibir el nuevo estado del tablero
            tablero = pickle.loads(cliente.recv(4096))
            imprimir_tablero(tablero)
        elif respuesta == "ganaste":
            print("¡Felicidades, has ganado!")
            duracion = pickle.loads(cliente.recv(4096))   # Recibir duración
            if duracion > 0:  # Verificar duración
                    print(f"Duración del juego: {duracion:.2f} segundos")
            else:
                    print("Error en la duración.")
            break

    cliente.close()

if __name__ == "__main__":
    jugar()
