# Aprendiendo a jugar a Otelo

Proyecto en Python para la convocatoria de junio: agente de Otelo basado en
Monte Carlo Tree Search con UCT y una red neuronal de valor entrenada por
autojuego.

## Contenido

- `othello_ai/game.py`: reglas completas de Otelo/Reversi.
- `othello_ai/mcts.py`: implementacion propia de MCTS con seleccion UCT.
- `othello_ai/agents.py`: agentes `random`, `greedy`, `heuristic`, `uct` y
  `uctnn`.
- `othello_ai/self_play.py`: generacion de datasets por partidas automaticas.
- `othello_ai/neural.py`: red neuronal de valor implementada con NumPy.
- `othello_ai/train.py`: entrenamiento de la red de valor.
- `othello_ai/tournament.py`: comparativas entre agentes.
- `othello_ai/cli.py`: interfaz de texto para jugar contra la maquina.
- `tests/`: pruebas unitarias con `unittest`.
- `plantilla-trabajo/memoria-otelo.tex`: borrador IEEE de la memoria.

## Requisitos

El codigo solo necesita NumPy.

```bash
python3 -m pip install -r requirements.txt
```

## Pruebas

```bash
python3 -m unittest discover -s tests -v
```

## Jugar contra la maquina

```bash
python3 -m othello_ai.cli --agent uct:300 --human black
```

Coordenadas aceptadas: `d3`, `c4`, etc. Tambien se acepta `fila columna`, por
ejemplo `3 4`.

## Generar datos por autojuego

```bash
python3 -m othello_ai.self_play \
  --games 500 \
  --agent uct:80 \
  --output data/processed/selfplay_uct80_500.npz \
  --seed 11
```

Cada estado se etiqueta con `+1`, `0` o `-1` segun el resultado final desde la
perspectiva del jugador activo. Por defecto se aplican las 8 simetrias del
tablero para aumentar el dataset.

## Entrenar la red de valor

```bash
python3 -m othello_ai.train \
  --dataset data/processed/selfplay_uct80_500.npz \
  --output models/value_net_uct80_500.npz \
  --hidden 128,64 \
  --epochs 40 \
  --batch-size 128 \
  --lr 0.001 \
  --seed 11
```

La red recibe 128 atributos: 64 casillas propias y 64 casillas rivales, siempre
desde la perspectiva del jugador activo. La salida usa `tanh`, por lo que queda
en el rango `[-1, 1]`.

## Torneos

```bash
python3 -m othello_ai.tournament --agent-a uct:100 --agent-b greedy --games 50
python3 -m othello_ai.tournament --agent-a uctnn:models/value_net_uct80_500.npz:100 --agent-b uct:100 --games 50
```

Los jugadores alternan color en cada partida para evitar sesgos por mover
primero.

## Experimento rapido ya validado

Durante la preparacion se comprobo el flujo completo con comandos cortos:

```bash
python3 -m othello_ai.self_play --games 2 --agent uct:8 --output data/processed/demo_selfplay.npz --seed 3
python3 -m othello_ai.train --dataset data/processed/demo_selfplay.npz --output models/demo_value_net.npz --hidden 32 --epochs 3 --batch-size 32 --lr 0.01 --seed 4
python3 -m othello_ai.tournament --agent-a uctnn:models/demo_value_net.npz:8 --agent-b random --games 2 --seed 9
```

Ese experimento solo verifica que el pipeline funciona. Para la memoria conviene
generar datasets y torneos mas grandes.
