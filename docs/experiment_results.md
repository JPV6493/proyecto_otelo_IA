# Resultados experimentales

Resultados generados automaticamente con:

```bash
python3 -m othello_ai.experiments --selfplay-games 12 --selfplay-agent uct:12 --epochs 20 --tournament-games 8 --uct-iters 16 --seed 23
```

## Dataset

- Partidas de autojuego: 12
- Agente de autojuego: `uct:12`
- Ejemplos tras simetrias: 5720
- Fichero: `data/processed/selfplay_experiment.npz`

## Entrenamiento

- Modelo: `models/value_net_experiment.npz`
- Capas ocultas: `(64, 32)`
- Epocas: 20
- Loss entrenamiento final: 0.84350
- Loss validacion final: 0.87669

## Torneos

| Agente A | Agente B | Partidas | Victorias A | Victorias B | Empates | Dif. media A | Tiempo (s) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `greedy` | `random` | 8 | 5 | 3 | 0 | 7.50 | 0.2 |
| `heuristic` | `greedy` | 8 | 7 | 1 | 0 | 18.00 | 0.7 |
| `uct:16` | `greedy` | 8 | 6 | 2 | 0 | 9.00 | 24.4 |
| `uct:32` | `uct:16` | 8 | 4 | 3 | 1 | 6.00 | 73.1 |
| `uctnn:models/value_net_experiment.npz:16` | `random` | 8 | 7 | 1 | 0 | 13.00 | 1.6 |
| `uctnn:models/value_net_experiment.npz:16` | `greedy` | 8 | 3 | 4 | 1 | -6.75 | 1.7 |
| `uctnn:models/value_net_experiment.npz:16` | `uct:16` | 8 | 4 | 4 | 0 | -0.25 | 26.0 |

Nota: las partidas alternan el color inicial para reducir el sesgo de mover primero.
