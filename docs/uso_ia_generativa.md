# Uso de inteligencia artificial generativa

Este documento recoge el uso de inteligencia artificial generativa realizado en
el proyecto, de acuerdo con las condiciones indicadas en el enunciado del
trabajo.

## Sistema utilizado

Se ha utilizado Codex, basado en GPT-5, integrado en el entorno de desarrollo.
El sistema se ha usado como asistente de programacion, revision y documentacion.

No se ha usado IA generativa para sustituir la comprension del trabajo. Los
integrantes deben revisar, ejecutar y entender el codigo antes de la defensa.

## Usos realizados

La IA generativa se ha usado para las siguientes tareas:

- Leer y resumir el enunciado del trabajo.
- Proponer una arquitectura inicial del proyecto.
- Generar una primera version del motor de Otelo.
- Generar una implementacion propia de MCTS con UCT.
- Generar agentes de referencia: aleatorio, voraz, heuristico, UCT y UCTNN.
- Crear scripts para autojuego, entrenamiento, torneos e interfaz de texto.
- Implementar una red neuronal de valor con NumPy.
- Preparar pruebas unitarias.
- Ejecutar experimentos reproducibles.
- Actualizar tablas y resultados de la documentacion.
- Preparar una version inicial de la memoria en LaTeX.

## Prompts principales

Los prompts principales utilizados fueron:

- "Lee el pdf y dime como crees que se podria hacer el mejor proyecto posible".
- "Ejecutalo".
- "Hazlo".
- "Checkea que se cumpla todo lo que pide la convocatoria de junio".
- "Quita el uso de ia generativa del latex y haz un buen documento en el docs".

Ademas de esos prompts principales, se hicieron preguntas de aclaracion sobre el
papel de algunos ficheros, el dataset, el modelo entrenado y el cumplimiento de
los requisitos de la convocatoria.

## Partes generadas o asistidas

El codigo generado con asistencia de IA incluye:

- `othello_ai/game.py`
- `othello_ai/mcts.py`
- `othello_ai/agents.py`
- `othello_ai/neural.py`
- `othello_ai/self_play.py`
- `othello_ai/train.py`
- `othello_ai/tournament.py`
- `othello_ai/cli.py`
- `othello_ai/experiments.py`
- pruebas dentro de `tests/`

La documentacion generada o asistida incluye:

- `README.md`
- `docs/experiment_results.md`
- `docs/experiment_results.json`
- `docs/uso_ia_generativa.md`
- `docs/memoria-otelo.tex`
- `docs/memoria-otelo.pdf`

## Revision humana necesaria

Antes de entregar el trabajo, los integrantes deben comprobar personalmente:

- Que las reglas de Otelo implementadas son correctas.
- Que UCT selecciona movimientos legales.
- Que la red se entrena con los datos generados por autojuego.
- Que el agente UCTNN usa el modelo entrenado para evaluar posiciones.
- Que los resultados de los experimentos se pueden reproducir.
- Que ambos integrantes saben explicar el codigo durante la defensa.

## Limitaciones del uso de IA

La IA generativa puede proponer codigo incorrecto o explicaciones incompletas.
Por ese motivo, el proyecto se ha validado mediante:

- pruebas unitarias;
- ejecucion de partidas automaticas;
- entrenamiento real de la red;
- torneos entre agentes;
- compilacion de la memoria en PDF.

La responsabilidad final sobre el codigo, los resultados y la defensa es de los
autores del trabajo.
