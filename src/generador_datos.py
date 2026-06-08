import numpy as np
import random
import copy
from otelo import Otelo
from agente import NodoMCTS 

class AgenteGeneradorPuro:
    """Un agente MCTS clásico que simula partidas al azar, ideal para generar datos limpios."""
    def __init__(self, color_ia, iteraciones=40):
        self.color_ia = color_ia
        self.iteraciones = iteraciones

    def elegir_movimiento(self, juego):
        raiz = NodoMCTS(copy.deepcopy(juego))
        for _ in range(self.iteraciones):
            nodo = self._seleccion(raiz)
            ganador = self._simulacion(nodo.estado)
            self._retropropagacion(nodo, ganador)
        return raiz.mejor_hijo(c_param=0.0).accion

    def _seleccion(self, nodo):
        while not nodo.estado.es_fin_de_juego():
            if not nodo.es_totalmente_expandido():
                return nodo.expandir()
            else:
                nodo = nodo.mejor_hijo()
        return nodo

    def _simulacion(self, estado):
        estado_simulado = copy.deepcopy(estado)
        while not estado_simulado.es_fin_de_juego():
            movimientos = list(estado_simulado.obtener_movimientos_validos(estado_simulado.turno_actual).keys())
            if movimientos:
                mov = random.choice(movimientos)
                estado_simulado.realizar_movimiento(mov[0], mov[1])
            else:
                estado_simulado.turno_actual = 1 if estado_simulado.turno_actual == 2 else 2
        blancas, negras = estado_simulado.calcular_puntuacion()
        return 1 if blancas > negras else 2 if negras > blancas else 0

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

def generar_partidas(num_partidas, iteraciones_mcts):
    print(f"Iniciando simulación pura de {num_partidas} partidas...")
    agente_blancas = AgenteGeneradorPuro(color_ia=1, iteraciones=iteraciones_mcts)
    agente_negras = AgenteGeneradorPuro(color_ia=2, iteraciones=iteraciones_mcts)
    
    tableros_guardados = []
    etiquetas_guardadas = []
    
    for i in range(num_partidas):
        juego = Otelo()
        historial_partida = [] 
        
        while not juego.es_fin_de_juego():
            movimientos = juego.obtener_movimientos_validos(juego.turno_actual)
            if not movimientos:
                juego.turno_actual = 1 if juego.turno_actual == 2 else 2
                continue
                
            historial_partida.append((np.copy(juego.tablero), juego.turno_actual))
            
            if juego.turno_actual == 1:
                mejor_mov = agente_blancas.elegir_movimiento(juego)
            else:
                mejor_mov = agente_negras.elegir_movimiento(juego)
                
            juego.realizar_movimiento(mejor_mov[0], mejor_mov[1])
            
        blancas, negras = juego.calcular_puntuacion()
        ganador = 1 if blancas > negras else 2 if negras > blancas else 0
            
        for tablero, turno_en_ese_momento in historial_partida:
            tableros_guardados.append(tablero)
            if ganador == 0:
                etiquetas_guardadas.append(0) 
            elif ganador == turno_en_ese_momento:
                etiquetas_guardadas.append(1) 
            else:
                etiquetas_guardadas.append(-1) 
                
        print(f"Partida {i+1}/{num_partidas} completada. Tableros extraídos: {len(historial_partida)}")
                
    X = np.array(tableros_guardados)
    Y = np.array(etiquetas_guardadas)
    np.savez("datos_otelo.npz", tableros=X, etiquetas=Y)
    print(f"\n¡Proceso finalizado! Se han guardado {len(X)} estados en 'datos_otelo.npz'")

if __name__ == "__main__":
    generar_partidas(num_partidas=100, iteraciones_mcts=40)