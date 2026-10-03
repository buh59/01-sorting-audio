import random
import time

from audio import AudioEngine
from sort_algos import (
    bubble_sort,
    exchange_sort,
    heap_sort,
    insertion_sort,
    quick_sort,
    selection_sort,
)
from visualizer_pygame import FastVisualizer

# Config : (Nom, Fonction, Nb Éléments, Steps par frame, Durée note)
ALGOS = {
    "1": ("Quick Sort", quick_sort, 250, 3, 0.005),
    "2": ("Heap Sort", heap_sort, 250, 3, 0.005),
    "3": ("Insertion Sort", insertion_sort, 120, 8, 0.003),
    "4": ("Selection Sort", selection_sort, 100, 10, 0.003),
    "5": ("Bubble Sort", bubble_sort, 100, 12, 0.003),
    "6": ("Exchange Sort", exchange_sort, 100, 12, 0.003),
}


def run_sort(name, algo_func, n_elements, steps_per_frame, tone_duration):
    print(
        f"\n▶ Lancement de {name} ({n_elements} éléments, ratio {steps_per_frame})..."
    )

    data = list(range(1, n_elements + 1))
    random.shuffle(data)
    max_val = max(data)

    audio = AudioEngine()
    viz = FastVisualizer(width=1280, height=720, fps=120)

    step_count = 0
    for current_data, active_indices in algo_func(data):
        step_count += 1

        if step_count % steps_per_frame == 0:
            if active_indices:
                values = [
                    current_data[i] for i in active_indices if i < len(current_data)
                ]
                audio.play_tone(values, max_val, duration=tone_duration)

            viz.update(current_data, active_indices)

    # Affichage final
    viz.update(data)

    # Balayage vert de victoire
    green_set = set()
    for i in range(len(data)):
        green_set.add(i)
        audio.play_tone(data[i], max_val, duration=0.008)  # Retirer le if i % 2 == 0
        viz.update(data, active_indices=(), green_indices=green_set)
        time.sleep(0.005)  # Ajouter un délai

    viz.close()
    audio.close()


def main():
    while True:
        print("\n--- SOUND OF SORTING (ALIENT & GLORP) ---")
        for key, (name, _, n, steps, _) in ALGOS.items():
            print(f"[{key}] {name:<16} (N={n}, steps={steps})")
        print("[Q] Quitter")

        choice = input("\nChoix (1-6) : ").strip().lower()
        if choice == "q":
            break
        if choice not in ALGOS:
            choice = "1"

        name, func, n, steps, duration = ALGOS[choice]
        run_sort(name, func, n, steps, duration)


if __name__ == "__main__":
    main()
