import pygame
import pygame.midi
pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.midi.init()


def main_loop():
    rythm = [
        [
            [
                [] for _ in range(4)
            ] for _ in range(4)]
            for _ in range(4)
    ]

    win = pygame.display.set_mode((216, 400))
    pygame.display.set_caption("Synth")
    w, h = win.get_size()
    bt_size_x, bt_size_y = w / 4, h * 27 / 200
    bt_start_y = h * 13 / 40

    font = pygame.font.SysFont("Consolas", int(bt_size_y // 4))
    hotbar_inf = [
        font.render("D", True, (0, 0, 0)),
        font.render("V", True, (0, 0, 0)),
        font.render("L", True, (0, 0, 0)),
        font.render("S", True, (0, 0, 0))
    ]
    topbar_inf = [
        font.render("<Bpm", True, (0, 0, 0)),
        font.render("Bpm>", True, (0, 0, 0)),
        font.render("<Vol", True, (0, 0, 0)),
        font.render("Vol>", True, (0, 0, 0))
    ]

    sound = [[pygame.mixer.Sound(f"./drum/{i}{j}.wav") for j in range(4)] for i in range(4)]
    vo_sound = [[pygame.mixer.Sound(f"./vocal/{i}{j}.wav") for j in range(4)] for i in range(4)]

    mode_list = ["Drum", "Vocal", "Load", "Save"]
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
                if i[0] == "v":
                    vo_sound[i[1]][i[2]].play()
                else:
                    sound[i[0]][i[1]].play()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if (event.type == pygame.FINGERDOWN) or (event.type == pygame.MOUSEBUTTONDOWN):
                mouse_pos = pygame.mouse.get_pos()
                x = int(mouse_pos[0] // bt_size_x)
                y = int((mouse_pos[1] - bt_start_y) // bt_size_y)

                if y == 4:
                    if (mode == "Drum") and (mode_list[x] == "Drum"):
                        if not drum_select:
                            for ds in drum_sequence:
                                pth, r, c = ds
                                if pth in rythm[c][r][0]:
                                    rythm[c][r][0].remove(pth)
                                else:
                                    rythm[c][r][0].append(pth)
                            drum_sequence = []
                        drum_select = not drum_select
                    elif (mode == "Vocal") and (mode_list[x] == "Vocal"):
                        vocal_rec_started = not vocal_rec_started
                    elif x == 2:
                        pass # Load
                    elif x == 3:
                        with open("./log.txt", "a", encoding="UTF-8") as f:
                            f.write(f"{rythm}\n")
                            f.close()
                    else:
                        mode = mode_list[x]
                elif y == -1:
                    if x == 0:
                        fps -= 1 / 15
                    elif x == 1:
                        fps += 1 / 15
                    elif x == 2:
                        if mode == "Drum":
                            v = sound[drum_pth[0]][drum_pth[1]].get_volume()
                            if v > 0:
                                sound[drum_pth[0]][drum_pth[1]].set_volume(v - 0.1)
                        elif mode == "Vocal":
                            for vocals_row in vo_sound:
                                for vocal_item in vocals_row:
                                    v = vocal_item.get_volume()
                                    if v > 0:
                                        vocal_item.set_volume(v - 0.1)
                        
                    else:
                        if mode == "Drum":
                            v = sound[drum_pth[0]][drum_pth[1]].get_volume()
                            if v < 1:
                                sound[drum_pth[0]][drum_pth[1]].set_volume(v + 0.1)
                        elif mode == "Vocal":
                            for vocals_row in vo_sound:
                                for vocal_item in vocals_row:
                                    v = vocal_item.get_volume()
                                    if v < 1:
                                        vocal_item.set_volume(v - 0.1)
                elif y >= 0:
                    if mode == "Drum":
                        if not drum_select:
                            drum_sequence.append((drum_pth, x, y))
                        else:
                            drum_pth = y, x
                            sound[y][x].play()
                    elif mode == "Vocal":
                        vo_sound[y][x].play()
                        if vocal_rec_started:
                            rythm[global_col][global_row][global_beat].append(("v", y, x))
        
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
        
        if (mode == "Drum") and not drum_select:
            for r in range(4):
                for c in range(4):
                    if drum_pth in rythm[r][c][0]:
                        pygame.draw.rect(win, (90, 220, 90), (bt_size_x * c + 1, bt_start_y + bt_size_y * r, bt_size_x - 2, bt_size_y - 2))
        pygame.draw.rect(win, (0, 190, 190), (bt_size_x * global_row + 1, bt_start_y + bt_size_y * global_col, bt_size_x - 2, bt_size_y - 2))
        
        bpm = font.render(f"BPM: {round(fps * 15)}", True, (255, 255, 255))
        md = font.render(f"Mode: {mode}", True, (255, 255, 255))
        md_2 = font.render(f"Rec: {vocal_rec_started or (not drum_select)}", True, (255, 255, 255))

        win.blit(bpm, (5, bt_size_y // 4 * 0.2))
        win.blit(md, (5, bt_size_y // 4 * 1.2))
        win.blit(md_2, (5, bt_size_y // 2 * 1.1))

        pygame.display.update()

        cnt += 1
    pygame.midi.quit()


if __name__ == "__main__":
    main_loop()
