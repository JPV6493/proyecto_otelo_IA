import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models

def entrenar_modelo():
    print("Cargando datos...")
    # 1. Cargar los datos que generamos en el paso anterior
    datos = np.load("datos_otelo.npz")
    X = datos['tableros']
    Y = datos['etiquetas']

    print(f"Datos cargados: {len(X)} tableros etiquetados listos para estudiar.")

    # 2. Diseñar la arquitectura de la Red Neuronal
    modelo = models.Sequential([
        # Capa de entrada: Aplana la matriz de 8x8 en una fila de 64 números
        layers.Flatten(input_shape=(8, 8)),
        
        # Capas ocultas: Las "neuronas" que procesan la estrategia
        layers.Dense(128, activation='relu'),
        layers.Dense(64, activation='relu'),
        
        # Capa de salida: 1 sola neurona con activación 'tanh'
        # 'tanh' es perfecta porque su salida siempre está entre -1 y 1
        layers.Dense(1, activation='tanh') 
    ])

    # 3. Compilar el modelo
    # Utilizamos el Error Cuadrático Medio (mse) para calcular qué tanto se equivoca
    modelo.compile(optimizer='adam', loss='mse', metrics=['mae'])

    # 4. Entrenar la red (El estudio)
    print("\nIniciando el entrenamiento...")
    # epochs=20 significa que repasará el libro de texto 20 veces.
    # validation_split=0.2 guarda un 20% de los datos como "examen final" para evitar el sobreajuste.
    modelo.fit(X, Y, epochs=20, batch_size=32, validation_split=0.2)

    # 5. Guardar el "cerebro"
    modelo.save("modelo_otelo.keras")
    print("\n¡Entrenamiento completado! Modelo guardado como 'modelo_otelo.keras'")

if __name__ == "__main__":
    entrenar_modelo()