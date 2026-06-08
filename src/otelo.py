import numpy as np

class Otelo:
    def __init__(self):
        """
        Inicializa el juego de Otelo con el tablero vacío y coloca las fichas iniciales.
        """
        self.tablero = np.zeros((8, 8), dtype=int)
        self.iniciar_tablero()
        self.turno_actual = 2 

    def iniciar_tablero(self):
        """
        Coloca las 4 fichas iniciales en el centro del tablero.
        0: casilla vacía | 1: ficha blanca | 2: ficha negra
        """
        self.tablero[3, 3] = 1
        self.tablero[4, 4] = 1
        self.tablero[3, 4] = 2
        self.tablero[4, 3] = 2

    def imprimir_tablero(self):
        """Muestra el tablero en la consola de forma visual."""
        simbolos = {0: '.', 1: 'B', 2: 'N'}
        print("  0 1 2 3 4 5 6 7")
        for i in range(8):
            fila = [simbolos[casilla] for casilla in self.tablero[i]]
            print(f"{i} " + " ".join(fila))
        print(f"\nTurno actual: {'Negras (N)' if self.turno_actual == 2 else 'Blancas (B)'}")
    
    def es_movimiento_valido(self, fila, col, jugador):
        """Comprueba si un movimiento atrapa fichas rivales."""
        if self.tablero[fila, col] != 0:
            return []

        oponente = 1 if jugador == 2 else 2
        fichas_a_voltear = []
        direcciones = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]

        for d_fila, d_col in direcciones:
            f, c = fila + d_fila, col + d_col
            fichas_potenciales = []

            while 0 <= f < 8 and 0 <= c < 8 and self.tablero[f, c] == oponente:
                fichas_potenciales.append((f, c))
                f += d_fila
                c += d_col

            if fichas_potenciales and 0 <= f < 8 and 0 <= c < 8 and self.tablero[f, c] == jugador:
                fichas_a_voltear.extend(fichas_potenciales)

        return fichas_a_voltear

    def obtener_movimientos_validos(self, jugador):
        """Devuelve un diccionario con todos los movimientos legales."""
        movimientos = {}
        for fila in range(8):
            for col in range(8):
                fichas_volteadas = self.es_movimiento_valido(fila, col, jugador)
                if fichas_volteadas:
                    movimientos[(fila, col)] = fichas_volteadas
        return movimientos

    def realizar_movimiento(self, fila, col):
        """Ejecuta un movimiento, voltea las fichas y pasa turno."""
        jugador = self.turno_actual
        fichas_a_voltear = self.es_movimiento_valido(fila, col, jugador)
        
        if not fichas_a_voltear:
            return False 

        self.tablero[fila, col] = jugador
        for f, c in fichas_a_voltear:
            self.tablero[f, c] = jugador

        self.turno_actual = 1 if jugador == 2 else 2
        return True
    
    def calcular_puntuacion(self):
        """Cuenta las fichas y devuelve (blancas, negras)."""
        blancas = np.sum(self.tablero == 1)
        negras = np.sum(self.tablero == 2)
        return blancas, negras

    def es_fin_de_juego(self):
        """
        Versión sin 'prints' para que la IA no colapse la terminal.
        Comprueba si el juego ha terminado sin modificar el tablero.
        """
        mov_blancas = self.obtener_movimientos_validos(1)
        mov_negras = self.obtener_movimientos_validos(2)
        return not mov_blancas and not mov_negras

########################## Bloque de prueba para jugar en la consola ##########################
if __name__ == "__main__":
    juego = Otelo()
    
    while not juego.es_fin_de_juego():
        juego.imprimir_tablero()
        movimientos = juego.obtener_movimientos_validos(juego.turno_actual)
        
        # Como quitamos el cambio automático en 'es_fin_de_juego', lo manejamos aquí
        if not movimientos:
            print(f"\nEl jugador {'Negras (N)' if juego.turno_actual == 2 else 'Blancas (B)'} no tiene movimientos y pasa el turno.")
            juego.turno_actual = 1 if juego.turno_actual == 2 else 2
            continue
        
        print("\nMovimientos válidos:")
        for coord in movimientos.keys():
            print(f"- Fila {coord[0]}, Columna {coord[1]}")
            
        try:
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

    # Fin del juego restaurado
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