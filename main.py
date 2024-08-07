import pygame
pygame.init()


class Button:
    def __init__(self, pos: tuple, size: tuple, sound_drum: list, sound_vocal: list, fx: str) -> None:
        self.pos_x, self.pos_y = pos
        self.size_x, self.size_y = size
        self.sound_drum = sound_drum
        self.sound_vocal = sound_vocal
        self.fx = fx


def main_loop():
    bt = [
        [
            Button((1, 200), (98, 98), [], [], ""),
            Button((101, 200), (98, 98), [], [], ""),
            Button((201, 200), (98, 98), [], [], ""),
            Button((301, 200), (98, 98), [], [], "")
        ],

        [
            Button((1, 300), (98, 98), [], [], ""),
            Button((101, 300), (98, 98), [], [], ""),
            Button((201, 300), (98, 98), [], [], ""),
            Button((301, 300), (98, 98), [], [], "")
        ],

        [
            Button((1, 400), (98, 98), [], [], ""),
            Button((101, 400), (98, 98), [], [], ""),
            Button((201, 400), (98, 98), [], [], ""),
            Button((301, 400), (98, 98), [], [], "")
        ],

        [
            Button((1, 500), (98, 98), [], [], ""),
            Button((101, 500), (98, 98), [], [], ""),
            Button((201, 500), (98, 98), [], [], ""),
            Button((301, 500), (98, 98), [], [], "")
        ]
    ]

    rythm = [[[] for _ in range(4)] for _ in range(4)]

    win = pygame.display.set_mode((401, 701))
    pygame.display.set_caption("Synth")

    clock = pygame.time.Clock()
    run = True
    fps = 60

    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.FINGERDOWN:
                x = event.x * win.get_height() // 100
                y = event.y * win.get_width() // 100
        
        for row in bt:
            for button in row:
                pygame.draw.rect(win, (100, 100, 100), (button.pos_x, button.pos_y, button.size_x, button.size_y))
        for pos_x in range(4): # Button for play, drum, vocal, fx
            pygame.draw.rect(win, (200, 200, 200), (pos_x * 100 + 1, 600, 98, 98))

        pygame.display.update()


if __name__ == "__main__":
    main_loop()
