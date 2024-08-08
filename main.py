import tkinter
from tkinter import messagebox

import pygame
pygame.init()
pygame.mixer.init()


class Button:
    def __init__(self, pos: tuple, size: tuple, sound_drum: list, sound_vocal: list, fx: str) -> None:
        self.pos_x, self.pos_y = pos
        self.size_x, self.size_y = size
        self.sound_drum = sound_drum
        self.sound_vocal = sound_vocal
        self.fx = fx


def main_loop():
    rythm = [
        [
            [
                [] for _ in range(4)
            ] for _ in range(4)]
            for _ in range(4)
    ]

    win = pygame.display.set_mode((216, 400)) #1080, 2000
    pygame.display.set_caption("Synth")
    w, h = win.get_size()
    bt_size_x, bt_size_y = w / 4, h * 27 / 200
    bt_start_y = h * 13 / 40

    sound = [[pygame.mixer.Sound(f"./drum/{i}{j}.wav") for j in range(4)] for i in range(4)]
    
    mode_list = ["Drum", "Vocal", "FX"]
    mode = "Drum"

    drum_select = True
    drum_pth = (0, 0)
    drum_sequence = []
    vocal_rec_started = False

    clock = pygame.time.Clock()
    run = True
    fps = 20
    cnt = 0

    while run:
        clock.tick(fps)
        win.fill((0, 0, 0))
        global_col, global_row, global_beat = (cnt // 16) % 4, (cnt // 4) % 4, cnt % 4
        s_source = rythm[global_col][global_row][global_beat]
        if len(s_source) > 0:
            for i in s_source:
                sound[i[0]][i[1]].play(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if (event.type == pygame.FINGERDOWN) or (event.type == pygame.MOUSEBUTTONDOWN):
                mouse_pos = pygame.mouse.get_pos()
                x = int(mouse_pos[0] // bt_size_x)
                y = int((mouse_pos[1] - bt_start_y) // bt_size_y)

                if (y == 4) and (x < 4):
                    if mode == "Drum":
                        if not drum_select:
                            for ds in drum_sequence:
                                pth, r, c = ds
                                if pth in rythm[c][r][0]:
                                    rythm[c][r][0].remove(pth)
                                else:
                                    rythm[c][r][0].append(pth)
                            drum_sequence = []
                        drum_select = not drum_select
                    elif mode == "Vocal":
                        vocal_rec_started = not vocal_rec_started
                    else:
                        mode = mode_list[x]
                elif mode == "Drum":
                    if not drum_select:
                        drum_sequence.append((drum_pth, x, y))
                    else:
                        drum_pth = y, x
                        sound[y][x].play()
                elif mode == "Vocal":
                    pass
                elif mode == "FX":
                    pass
        
        for row in range(5):
            for col in range(4):
                if row < 4:
                    pygame.draw.rect(win, (100, 100, 100), (bt_size_x * col + 1, bt_start_y + bt_size_y * row, bt_size_x - 2, bt_size_y - 2))
                else:
                    pygame.draw.rect(win, (200, 200, 200), (bt_size_x * col + 1, bt_start_y + bt_size_y * row, bt_size_x - 2, bt_size_y - 2))
        
        if (mode == "Drum") and not drum_select:
            for r in range(4):
                for c in range(4):
                    if drum_pth in rythm[r][c][0]:
                        pygame.draw.rect(win, (90, 220, 90), (bt_size_x * c + 1, bt_start_y + bt_size_y * r, bt_size_x - 2, bt_size_y - 2))
        pygame.draw.rect(win, (0, 190, 190), (bt_size_x * global_row + 1, bt_start_y + bt_size_y * global_col, bt_size_x - 2, bt_size_y - 2))
        
        pygame.display.update()

        cnt += 1
    
    tkinter.Tk().wm_withdraw()
    w = messagebox.askquestion("Save?", "Save rythm?")
    if w == "yes":
        with open("./log.txt", "a", encoding="UTF-8") as f:
            f.write(f"{rythm}\n")
            f.close()


if __name__ == "__main__":
    main_loop()
