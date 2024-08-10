import pygame
pygame.init()
pygame.mixer.init()
pygame.font.init()


def main_loop():
    rythm = [[[] for _ in range(4)]for _ in range(4)]

    win = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Synth")
    w, h = win.get_size()
    bt_size_x, bt_size_y = w / 4, h * 27 / 200
    bt_start_y = h * 13 / 40

    font = pygame.font.SysFont("Consolas", int(bt_size_y // 4))
    hotbar_inf = [
        font.render("D", True, (0, 0, 0)),
        font.render("R", True, (0, 0, 0)),
        font.render("C", True, (0, 0, 0)),
        font.render("S", True, (0, 0, 0))
    ]
    topbar_inf = [
        font.render("<Bpm", True, (0, 0, 0)),
        font.render("Bpm>", True, (0, 0, 0)),
        font.render("<Vol", True, (0, 0, 0)),
        font.render("Vol>", True, (0, 0, 0))
    ]

    sound = [[pygame.mixer.Sound(f"./drum/{i}{j}.wav") for j in range(4)] for i in range(4)]
    mode = "Drum"
    rec_start = False

    drum_pth = (0, 0)
    drum_sequence = []

    clock = pygame.time.Clock()
    run = True
    fps = 5
    cnt = 0

    while run:
        clock.tick(fps)
        win.fill((0, 0, 0))
        global_col, global_row = (cnt // 4) % 4, cnt % 4
        s_source = rythm[global_col][global_row]
        for i in s_source:
            sound[i[0]][i[1]].play()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.FINGERDOWN:
                mouse_pos = pygame.mouse.get_pos()
                x = int(mouse_pos[0] // bt_size_x)
                y = int((mouse_pos[1] - bt_start_y) // bt_size_y)

                if y == 4:
                    if x == 0:
                        mode = "Drum"
                        drum_sequence = []
                    if x == 1:
                        mode = "Record"
                        if rec_start:
                            for ds in drum_sequence:
                                pth, r, c = ds
                                if pth in rythm[c][r]:
                                    rythm[c][r].remove(pth)
                                else:
                                    rythm[c][r].append(pth)
                            drum_sequence = []
                        rec_start = not rec_start
                    elif x == 2:
                        for r in rythm:
                            for c in r:
                                c.remove(pth)
                    elif x == 3:
                        with open("./log.txt", "a", encoding="UTF-8") as f:
                            f.write(f"{rythm}\n")
                            f.close()
                elif y == -1:
                    if x == 0:
                        fps -= 1 / 60
                    elif x == 1:
                        fps += 1 / 60
                    elif x == 2:
                        v = sound[drum_pth[0]][drum_pth[1]].get_volume()
                        if v > 0:
                            sound[drum_pth[0]][drum_pth[1]].set_volume(v - 0.1)
                    
                    else:
                        v = sound[drum_pth[0]][drum_pth[1]].get_volume()
                        if v < 1:
                            sound[drum_pth[0]][drum_pth[1]].set_volume(v + 0.1)
            
                elif y >= 0:
                    if mode == "Record":
                        drum_sequence.append((drum_pth, x, y))
                    else:
                        drum_pth = y, x
                        sound[y][x].play()
        
        for row in range(6):
            for col in range(4):
                if row < 4:
                    pygame.draw.rect(win, (100, 100, 100), (bt_size_x * col + 1, bt_start_y + bt_size_y * row, bt_size_x - 2, bt_size_y - 2))
                elif row == 4:
                    pygame.draw.rect(win, (200, 200, 200), (bt_size_x * col + 1, bt_start_y + bt_size_y * row, bt_size_x - 2, bt_size_y - 2))
                    win.blit(hotbar_inf[col], (bt_size_x * col + 1, bt_start_y + bt_size_y * row))
                else:
                    pygame.draw.rect(win, (200, 200, 200), (bt_size_x * col + 1, bt_start_y - bt_size_y, bt_size_x - 2, bt_size_y - 2))
                    win.blit(topbar_inf[col], (bt_size_x * col + 3, bt_start_y - bt_size_y))
        
        if mode == "Record":
            for r in range(4):
                for c in range(4):
                    if drum_pth in rythm[r][c]:
                        pygame.draw.rect(win, (90, 220, 90), (bt_size_x * c + 1, bt_start_y + bt_size_y * r, bt_size_x - 2, bt_size_y - 2))
        pygame.draw.rect(win, (0, 190, 190), (bt_size_x * global_row + 1, bt_start_y + bt_size_y * global_col, bt_size_x - 2, bt_size_y - 2))
        
        bpm = font.render(f"BPM: {round(fps * 60)}", True, (255, 255, 255))
        md = font.render(f"Mode: {mode}", True, (255, 255, 255))
        
        win.blit(bpm, (5, bt_size_y // 4 * 0.2))
        win.blit(md, (5, bt_size_y // 4 * 1.2))

        pygame.display.update()

        cnt += 1


if __name__ == "__main__":
    main_loop()
