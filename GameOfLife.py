# -*- coding: utf-8 -*-

import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import Video, display


rules = (2, 3, 3, 3)  # (D, S, R, O)


# Función para construir el modelo

def build_model(rules, alive_probability=0.2, dims=(200, 200), seed=42):
    np.random.seed(seed)
    random.seed(seed)
    status = np.zeros(dims, dtype=bool)
    new_status = np.zeros(dims, dtype=bool)
    
    # Inicializar aleatoriamente algunas células como vivas
    for i in range(dims[0]):
        for j in range(dims[1]):
            if random.random() < alive_probability:
                status[i, j] = True

    return status, new_status, rules

# Inicializar el modelo
status, new_status, rules = build_model(rules)


# Función para contar los vecinos vivos

def alive_neighbors(x, y, status):
    neighbors = [status[i % status.shape[0], j % status.shape[1]] 
                 for i in range(x-1, x+2) for j in range(y-1, y+2) 
                 if (i, j) != (x, y)]
    return sum(neighbors)

# Función para ejecutar un paso del juego
def game_of_life_step(status, new_status, rules):
    D, S, R, O = rules
    for i in range(status.shape[0]):
        for j in range(status.shape[1]):
            n = alive_neighbors(i, j, status)
            if status[i, j]:
                new_status[i, j] = D <= n <= O
            else:
                new_status[i, j] = R <= n <= O
    
    status[:, :] = new_status[:, :]


# Función para ejecutar la simulación y guardar el video

def run_simulation(frames, status, new_status, rules, filename="game_of_life.mp4"):
    fig, ax = plt.subplots()
    mat = ax.matshow(status, cmap=plt.get_cmap("viridis"))
    plt.title("Game of Life, time = 0")  

    def update(frame):
        game_of_life_step(status, new_status, rules)
        mat.set_data(status)
        ax.set_title(f"Game of Life, time = {frame}")  
        return [mat]

    ani = animation.FuncAnimation(fig, update, frames=frames, blit=True)
    
    # Guardar la animación como archivo de video
    ani.save(filename, writer="ffmpeg", fps=10)
    plt.close(fig)  # Cierra la figura después de guardar el video

# Ejecutar la simulación
run_simulation(60, status, new_status, rules)

# Mostrar el video
video = Video("game_of_life.mp4", embed=True)
display(video)


