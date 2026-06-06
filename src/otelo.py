import numpy as np

class Otelo:
    def __init__(self):
        """
        Inicializa el juego de Otelo con el tablero vacío y coloca las fichas iniciales.
        """
        # Creamos un tablero de 8x8 lleno de ceros (casillas vacías)
        self.tablero = np.zeros((8, 8), dtype=int)
        
        # Colocamos las fichas iniciales
        self.iniciar_tablero()
        
        # El jugador con fichas negras (2) siempre mueve primero
        self.turno_actual = 2 

    def iniciar_tablero(self):
        """
        Coloca las 4 fichas iniciales en el centro del tablero.
        0: casilla vacía
        1: ficha blanca
        2: ficha negra
        """
        # Dos fichas blancas en posiciones opuestas
        self.tablero[3, 3] = 1
        self.tablero[4, 4] = 1
        
        # Dos fichas negras en las otras dos posiciones centrales
        self.tablero[3, 4] = 2
        self.tablero[4, 3] = 2

    def imprimir_tablero(self):
        """
        Muestra el tablero en la consola de forma visual.
        """
        simbolos = {0: '.', 1: 'B', 2: 'N'}
        print("  0 1 2 3 4 5 6 7")
        for i in range(8):
            fila = [simbolos[casilla] for casilla in self.tablero[i]]
            print(f"{i} " + " ".join(fila))
        print(f"\nTurno actual: {'Negras (N)' if self.turno_actual == 2 else 'Blancas (B)'}")
    

    def es_movimiento_valido(self, fila, col, jugador):
        """
        Comprueba si colocar una ficha en (fila, col) es un movimiento válido para el jugador.
        Devuelve una lista con las fichas que se voltearían (lista vacía si es inválido).
        """
        # Regla 1: La casilla debe estar vacía
        if self.tablero[fila, col] != 0:
            return []

        # Determinar el color del oponente
        oponente = 1 if jugador == 2 else 2
        fichas_a_voltear = []

        # Las 8 direcciones posibles: (delta_fila, delta_columna)
        direcciones = [
            (-1, 0), (1, 0), (0, -1), (0, 1),   # Arriba, Abajo, Izquierda, Derecha
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonales
        ]

        for d_fila, d_col in direcciones:
            f, c = fila + d_fila, col + d_col
            fichas_potenciales = []

            # Avanzamos mientras encontremos fichas del oponente
            while 0 <= f < 8 and 0 <= c < 8 and self.tablero[f, c] == oponente:
                fichas_potenciales.append((f, c))
                f += d_fila
                c += d_col

            # Si encontramos fichas del oponente y luego una nuestra, es válido
            if fichas_potenciales and 0 <= f < 8 and 0 <= c < 8 and self.tablero[f, c] == jugador:
                fichas_a_voltear.extend(fichas_potenciales)

        # No está permitido colocar fichas de manera que no se capture ninguna ficha del oponente
        return fichas_a_voltear

    def obtener_movimientos_validos(self, jugador):
        """
        Recorre todo el tablero y devuelve un diccionario con todos los movimientos válidos.
        Las claves son las coordenadas (fila, col) y los valores son las fichas que se voltearían.
        """
        movimientos = {}
        for fila in range(8):
            for col in range(8):
                fichas_volteadas = self.es_movimiento_valido(fila, col, jugador)
                if fichas_volteadas:
                    movimientos[(fila, col)] = fichas_volteadas
        return movimientos

    def realizar_movimiento(self, fila, col):
        """
        Ejecuta un movimiento en el tablero si es válido, voltea las fichas y cambia el turno.
        Devuelve True si se pudo hacer, False si era inválido.
        """
        jugador = self.turno_actual
        fichas_a_voltear = self.es_movimiento_valido(fila, col, jugador)
        
        if not fichas_a_voltear:
            return False  # Movimiento ilegal

        # 1. Colocamos la nueva ficha
        self.tablero[fila, col] = jugador

        # 2. Volteamos las fichas atrapadas
        for f, c in fichas_a_voltear:
            self.tablero[f, c] = jugador

        # 3. Cambiamos el turno al otro jugador
        self.turno_actual = 1 if jugador == 2 else 2
        return True
    

    def calcular_puntuacion(self):
        """
        Cuenta las fichas de cada jugador en el tablero.
        Devuelve una tupla: (fichas_blancas, fichas_negras)
        """
        blancas = np.sum(self.tablero == 1)
        negras = np.sum(self.tablero == 2)
        return blancas, negras

    def es_fin_de_juego(self):
        """
        Comprueba si el juego ha terminado.
        El juego termina cuando ningún jugador tiene movimientos válidos.
        """
        movimientos_actual = self.obtener_movimientos_validos(self.turno_actual)
        
        # Si el jugador actual no tiene movimientos, comprobamos el otro
        if not movimientos_actual:
            otro_jugador = 1 if self.turno_actual == 2 else 2
            movimientos_otro = self.obtener_movimientos_validos(otro_jugador)
            
            # Si el otro tampoco tiene, el juego ha terminado
            if not movimientos_otro:
                return True
                
            # Si el actual no tiene pero el otro sí, el actual debe pasar turno
            print(f"El jugador {'Negras (N)' if self.turno_actual == 2 else 'Blancas (B)'} no tiene movimientos y pasa el turno.")
            self.turno_actual = otro_jugador
            
        return False

########################## Bloque de prueba para jugar en la consola ##########################
if __name__ == "__main__":
    juego = Otelo()
    
    while not juego.es_fin_de_juego():
        juego.imprimir_tablero()
        movimientos = juego.obtener_movimientos_validos(juego.turno_actual)
        
        print("\nMovimientos válidos:")
        for coord in movimientos.keys():
            print(f"- Fila {coord[0]}, Columna {coord[1]}")
            
        try:
            # Pedimos la jugada al usuario
            entrada = input("\nIntroduce fila y columna separadas por espacio (o 'q' para salir): ")
            if entrada.lower() == 'q':
                print("Juego cancelado.")
                break
                
            fila, col = map(int, entrada.split())
            
            if (fila, col) in movimientos:
                juego.realizar_movimiento(fila, col)
            else:
                print("\n[!] Movimiento inválido. Inténtalo de nuevo.")
                
        except ValueError:
            print("\n[!] Por favor, introduce dos números separados por espacio.")

    # Fin del juego
    if juego.es_fin_de_juego():
        juego.imprimir_tablero()
        blancas, negras = juego.calcular_puntuacion()
        print("\n=== FIN DE LA PARTIDA ===")
        print(f"Puntuación - Blancas: {blancas} | Negras: {negras}")
        if blancas > negras:
            print("¡Ganan las Blancas!")
        elif negras > blancas:
            print("¡Ganan las Negras!")
        else:
            print("¡Es un empate!")