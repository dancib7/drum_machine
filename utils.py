import pygame
from constants import *


def draw_grid(screen, clicks, beat, actives, label_font, instruments, nb_insutruments, nb_beats):
    boxes = []
    # draw left and bottom boxes
    _ = pygame.draw.rect(screen, COLORS['gray'], [0, 0, 200, HEIGHT - 200], 5)
    _ = pygame.draw.rect(screen, COLORS['gray'], [0, HEIGHT - 200, WIDTH, 200], 5)
    for i in range(nb_insutruments + 1):
        pygame.draw.line(screen, COLORS['gray'], (0, i * 100), (200, i * 100), 3)
    colors = [COLORS['gray'], COLORS['white'], COLORS['gray']]
    for idx, instrument in enumerate(instruments):
        inst_text = label_font.render(instrument, True, colors[actives[idx]])
        screen.blit(inst_text, (30, 30 + idx * 100))
    for i in range(nb_beats):
        for j in range(nb_insutruments):
            if clicks[j][i] == -1:
                color = COLORS['gray']
            else:
                if actives[j] == 1:
                    color = COLORS['green']
                else:
                    color = COLORS['dark_gray']
            tmp_width = ((WIDTH - 200) // nb_beats)
            rect = pygame.draw.rect(screen, color, [i * tmp_width + 205, (j * 100) + 5, tmp_width - 10, 90], 0, 3)
            pygame.draw.rect(screen, COLORS['gold'], [i * tmp_width + 200, j * 100, tmp_width, 100], 5, 5)
            pygame.draw.rect(screen, COLORS['black'], [i * tmp_width + 200, j * 100, tmp_width, 100], 2, 5)
            boxes.append((rect, (i, j)))
    _ = pygame.draw.rect(screen, COLORS['blue'], [beat * tmp_width + 200, 0, tmp_width, nb_insutruments * 100], 5, 3)
    return boxes


def play_notes(clicked, active_beat, active_list, instruments):
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1 and active_list[i] == 1:
            instruments[instruments['instruments_enum'][i]].play()


def draw_save_menu(screen, beat_name, typing, label_font):
    pygame.draw.rect(screen, COLORS['black'], [0, 0, WIDTH, HEIGHT])
    menu_text = label_font.render('SAVE MENU: Enter a Name for this beat', True, COLORS['white'])
    screen.blit(menu_text, (400, 40))
    exit_btn = pygame.draw.rect(screen, COLORS['gray'], [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5)
    exit_text = label_font.render('Close', True, COLORS['white'])
    screen.blit(exit_text, (WIDTH - 160, HEIGHT - 70))
    saving_btn = pygame.draw.rect(screen, COLORS['gray'], [WIDTH // 2 - 100, HEIGHT * 0.75, 200, 100], 0, 5)
    saving_text = label_font.render('Save Beat', True, COLORS['white'])
    screen.blit(saving_text, (WIDTH // 2 - 70, HEIGHT * 0.75 + 30))
    if typing:
        pygame.draw.rect(screen, COLORS['dark_gray'], [400, 200, 600, 200], 0, 5)
    entry_rect = pygame.draw.rect(screen, COLORS['gray'], [400, 200, 600, 200], 5, 5)
    entry_text = label_font.render(f'{beat_name}', True, COLORS['white'])
    screen.blit(entry_text, (430, 250))
    return exit_btn, saving_btn, beat_name, entry_rect


def draw_load_menu(screen, index, label_font, medium_font, saved_beats):
    loaded_clicked = []
    loaded_beats = 0
    loaded_bpm = 0
    pygame.draw.rect(screen, COLORS['black'], [0, 0, WIDTH, HEIGHT])
    menu_text = label_font.render('LOAD MENU: Select a beat to load in', True, COLORS['white'])
    screen.blit(menu_text, (400, 40))
    exit_btn = pygame.draw.rect(screen, COLORS['gray'], [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5)
    exit_text = label_font.render('Close', True, COLORS['white'])
    screen.blit(exit_text, (WIDTH - 160, HEIGHT - 70))
    loading_btn = pygame.draw.rect(screen, COLORS['gray'], [WIDTH // 2 - 100, HEIGHT * 0.87, 200, 100], 0, 5)
    loading_text = label_font.render('Load Beat', True, COLORS['white'])
    screen.blit(loading_text, (WIDTH // 2 - 70, HEIGHT * 0.87 + 30))
    delete_btn = pygame.draw.rect(screen, COLORS['gray'], [WIDTH // 2 - 400, HEIGHT * 0.87, 200, 100], 0, 5)
    delete_text = label_font.render('Delete Beat', True, COLORS['white'])
    screen.blit(delete_text, (WIDTH // 2 - 385, HEIGHT * 0.87 + 30))
    if 0 <= index < len(saved_beats):
        pygame.draw.rect(screen, COLORS['light_gray'], [190, 100 + index * 50, 1000, 50])
    for beat in range(len(saved_beats)):
        if beat < 10:
            beat_clicked = []
            row_text = medium_font.render(f'{beat + 1}', True, COLORS['white'])
            screen.blit(row_text, (200, 100 + beat * 50))
            name_index_start = saved_beats[beat].index('name: ') + 6
            name_index_end = saved_beats[beat].index(', nb_beats:')
            name_text = medium_font.render(saved_beats[beat][name_index_start:name_index_end], True, COLORS['white'])
            screen.blit(name_text, (240, 100 + beat * 50))
        if 0 <= index < len(saved_beats) and beat == index:
            beats_index_end = saved_beats[beat].index(', bpm:')
            loaded_beats = int(saved_beats[beat][name_index_end + 11:beats_index_end])
            bpm_index_end = saved_beats[beat].index(', selected:')
            loaded_bpm = int(saved_beats[beat][beats_index_end + 6:bpm_index_end])
            loaded_clicks_string = saved_beats[beat][bpm_index_end + 14: -3]
            loaded_clicks_rows = list(loaded_clicks_string.split("], ["))
            for row in range(len(loaded_clicks_rows)):
                loaded_clicks_row = (loaded_clicks_rows[row].split(', '))
                for item in range(len(loaded_clicks_row)):
                    if loaded_clicks_row[item] == '1' or loaded_clicks_row[item] == '-1':
                        loaded_clicks_row[item] = int(loaded_clicks_row[item])
                beat_clicked.append(loaded_clicks_row)
                loaded_clicked = beat_clicked
    loaded_info = [loaded_beats, loaded_bpm, loaded_clicked]
    entry_rect = pygame.draw.rect(screen, COLORS['gray'], [190, 90, 1000, 600], 5, 5)
    return exit_btn, loading_btn, entry_rect, delete_btn, loaded_info