import math
import random
import copy
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # Ocultar advertencias de sistema de TensorFlow
import tensorflow as tf
from otelo import Otelo

class NodoMCTS:
    def __init__(self, estado_juego, padre=None, accion=None):
        self.estado = estado_juego
        self.padre = padre
        self.accion = accion 
        self.hijos = []
        self.visitas = 0
        self.recompensa = 0.0
        
        self.movimientos_intento = list(self.estado.obtener_movimientos_validos(self.estado.turno_actual).keys())
        
        if not self.movimientos_intento and not self.estado.es_fin_de_juego():
            self.movimientos_intento = [(-1, -1)] 

    def es_totalmente_expandido(self):
        return len(self.movimientos_intento) == 0

    def expandir(self):
        accion = self.movimientos_intento.pop()
        nuevo_estado = copy.deepcopy(self.estado)
        
        if accion == (-1, -1):
            nuevo_estado.turno_actual = 1 if nuevo_estado.turno_actual == 2 else 2
        else:
            nuevo_estado.realizar_movimiento(accion[0], accion[1])
            
        nuevo_hijo = NodoMCTS(nuevo_estado, padre=self, accion=accion)
        self.hijos.append(nuevo_hijo)
        return nuevo_hijo

    def mejor_hijo(self, c_param=1.414):
        mejor_valor = -float('inf')
        mejores_hijos = []
        
        for hijo in self.hijos:
            if hijo.visitas == 0:
                valor_ucb = float('inf')
            else:
                explotacion = hijo.recompensa / hijo.visitas
                exploracion = c_param * math.sqrt(math.log(self.visitas) / hijo.visitas)
                valor_ucb = explotacion + exploracion
            
            if valor_ucb > mejor_valor:
                mejor_valor = valor_ucb
                mejores_hijos = [hijo]
            elif valor_ucb == mejor_valor:
                mejores_hijos.append(hijo)
                
        return random.choice(mejores_hijos)


class AgenteOtelo:
    def __init__(self, color_ia, iteraciones=50):
        self.color_ia = color_ia
        self.iteraciones = iteraciones
        # Cargamos el "cerebro" (Red Neuronal) en la memoria al iniciar el agente
        self.modelo = tf.keras.models.load_model("modelo_otelo.keras")

    def elegir_movimiento(self, juego):
        raiz = NodoMCTS(copy.deepcopy(juego))
        
        for _ in range(self.iteraciones):
            nodo = self._seleccion(raiz)
            ganador = self._simulacion(nodo.estado)
            self._retropropagacion(nodo, ganador)
            
        mejor_movimiento = raiz.mejor_hijo(c_param=0.0).accion
        return mejor_movimiento

    def _seleccion(self, nodo):
        while not nodo.estado.es_fin_de_juego():
            if not nodo.es_totalmente_expandido():
                return nodo.expandir()
            else:
                nodo = nodo.mejor_hijo()
        return nodo

    def _simulacion(self, estado):
        """
        3. Simulation (Default Policy): Sustituida por Deep Learning.
        En lugar de jugar al azar hasta el final, la IA evalúa el tablero.
        """
        # Si el juego ya ha terminado de verdad, devolvemos el ganador real
        if estado.es_fin_de_juego():
            blancas, negras = estado.calcular_puntuacion()
            if blancas > negras: return 1
            elif negras > blancas: return 2
            else: return 0
            
        # Transformamos la matriz del tablero al formato que espera TensorFlow
        tablero_entrada = np.expand_dims(estado.tablero, axis=0)
        
        # Le pedimos a la red que prediga la probabilidad de victoria [-1, 1]
        prediccion = self.modelo.predict(tablero_entrada, verbose=0)[0][0]
        
        jugador_actual = estado.turno_actual
        oponente = 1 if jugador_actual == 2 else 2
        
        # Si la predicción es positiva, la IA cree que ganará el jugador actual
        if prediccion > 0:
            return jugador_actual
        else:
            return oponente

    def _retropropagacion(self, nodo, ganador):
        while nodo is not None:
            nodo.visitas += 1
            if ganador != 0:
                if nodo.padre is not None:
                    jugador_que_movio = nodo.padre.estado.turno_actual
                    if jugador_que_movio == ganador:
                        nodo.recompensa += 1
                    else:
                        nodo.recompensa -= 1
            nodo = nodo.padre


# =====================================================================
# BLOQUE DE PRUEBA
# =====================================================================
if __name__ == "__main__":
    juego = Otelo()
    # La IA usa su red neuronal recién entrenada
    ia = AgenteOtelo(color_ia=1, iteraciones=50) 
    
    print("Bienvenido a Otelo MCTS + Deep Learning. Tú (Negras/N) vs IA (Blancas/B).")
    
    while not juego.es_fin_de_juego():
        juego.imprimir_tablero()
        movimientos = juego.obtener_movimientos_validos(juego.turno_actual)
        
        if not movimientos:
            print(f"\nEl jugador {'Negras (N)' if juego.turno_actual == 2 else 'Blancas (B)'} pasa turno.")
            juego.turno_actual = 1 if juego.turno_actual == 2 else 2
            continue

        if juego.turno_actual == 2:
            print("\nTus movimientos válidos:")
            for coord in movimientos.keys():
                print(f"- {coord[0]} {coord[1]}")
                
            try:
                entrada = input("Fila y columna (ej: 2 3) o 'q' para salir: ")
                if entrada.lower() == 'q': break
                fila, col = map(int, entrada.split())
                
                if (fila, col) in movimientos:
                    juego.realizar_movimiento(fila, col)
                else:
                    print("\n[!] Movimiento inválido.")
            except ValueError:
                print("\n[!] Entrada incorrecta.")
        else:
            print("\nLa IA está consultando su Red Neuronal...")
            mejor_mov = ia.elegir_movimiento(juego)
            print(f"La IA coloca ficha en la fila {mejor_mov[0]}, columna {mejor_mov[1]}")
            juego.realizar_movimiento(mejor_mov[0], mejor_mov[1])

    if juego.es_fin_de_juego():
        juego.imprimir_tablero()
        blancas, negras = juego.calcular_puntuacion()
        print("\n=== FIN DE LA PARTIDA ===")
        print(f"Puntuación - IA (Blancas): {blancas} | Tú (Negras): {negras}")