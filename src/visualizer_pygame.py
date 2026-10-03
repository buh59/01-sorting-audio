import sys

import pygame


class FastVisualizer:
    def __init__(self, width=1280, height=720, fps=120):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sound of Sorting")
        self.clock = pygame.time.Clock()
        self.fps = fps

    def update(self, data, active_indices=(), green_indices=()):
        # Traitement des événements pour éviter tout gel sous Linux
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.screen.fill((0, 0, 0))

        n = len(data)
        bar_width = self.width / n
        max_val = max(data) if data else 1

        active_set = set(active_indices)
        g_set = set(green_indices) if green_indices else set()

        for idx, val in enumerate(data):
            bar_height = (val / max_val) * (self.height - 40)
            x = idx * bar_width
            y = self.height - bar_height

            if idx in active_set:
                color = (255, 0, 0)
            elif idx in g_set:
                color = (0, 255, 0)
            else:
                color = (255, 255, 255)

            pygame.draw.rect(
                self.screen, color, (x, y, max(1, bar_width - 1), bar_height)
            )

        pygame.display.flip()
        # Maintient le rythme réglé par FPS (ex: 120 étapes par seconde)
        self.clock.tick(self.fps)

    def close(self):
        pygame.time.wait(500)
        pygame.quit()
