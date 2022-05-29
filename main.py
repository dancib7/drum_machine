import pygame
from pygame import mixer
from utils import *

if __name__ == '__main__':
    pygame.init()
    
    active_length = 0
    active_beat = 0
    
    # sounds
    '''
    hi_hat = mixer.Sound('sounds\kit2\hi hat.wav')
    snare = mixer.Sound('sounds\kit2\snare.wav')
    kick = mixer.Sound('sounds\kit2\kick.wav')
    crash = mixer.Sound('sounds\kit2\crash.wav')
    clap = mixer.Sound('sounds\kit2\clap.wav')
    tom = mixer.Sound("sounds\kit2\\tom.wav")
    '''
    instruments = {
        'hi_hat': mixer.Sound('sounds\hi hat.wav'),
        'snare': mixer.Sound('sounds\snare.wav'),
        'kick': mixer.Sound('sounds\kick.wav'),
        'crash': mixer.Sound('sounds\crash.wav'),
        'clap': mixer.Sound('sounds\clap.wav'),
        'tom': mixer.Sound("sounds\\tom.wav"),
    }
    instruments_enum = ['hi_hat', 'snare', 'kick', 'crash', 'clap', 'tom']
    instruments['instruments_enum'] = instruments_enum[:]
    nb_instruments = len(instruments_enum)
    # initialize with default
    bpm = BPM_DEFAULT
    nb_beats = NB_BEATS_DEFAULT
    # initiate necessary stuff from pygame
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption('The Beat Maker')
    label_font = pygame.font.Font('Roboto-Bold.ttf', 32)
    medium_font = pygame.font.Font('Roboto-Bold.ttf', 24)
    timer = pygame.time.Clock()
    pygame.mixer.set_num_channels(nb_instruments * 3)
    # initiate necessary variables
    beat_changed = True
    playing = True
    clicked = [[-1 for _ in range(nb_beats)] for _ in range(nb_instruments)]
    active_list = [1 for _ in range(nb_instruments)]
    save_menu = False
    load_menu = False
    saved_beats = []
    with open('saved_beats.txt', 'r') as f:
        for line in f:
            saved_beats.append(line)
    beat_name = ''
    typing = False
    index = 100    
    
    run = True
    while run:
        timer.tick(FPS)
        screen.fill(COLORS['black'])
        boxes = draw_grid(screen, clicked, active_beat, active_list, label_font, instruments_enum, nb_instruments, nb_beats)
        # drawing lower menu
        play_pause = pygame.draw.rect(screen, COLORS['gray'], [50, HEIGHT - 150, 200, 100], 0, 5)
        play_text = label_font.render('Play/Pause', True, COLORS['white'])
        screen.blit(play_text, (70, HEIGHT - 130))
        play_text2 = medium_font.render('Playing' if playing else 'Paused', True, COLORS['dark_gray'])
        screen.blit(play_text2, (70, HEIGHT - 100))
        # nb_beats per minute buttons
        bpm_rect = pygame.draw.rect(screen, COLORS['gray'], [300, HEIGHT - 150, 200, 100], 5, 5)
        bpm_text = medium_font.render('Beats Per Minute', True, COLORS['white'])
        screen.blit(bpm_text, (308, HEIGHT - 130))
        bpm_text2 = label_font.render(f'{bpm}', True, COLORS['white'])
        screen.blit(bpm_text2, (370, HEIGHT - 100))
        bpm_add_rect = pygame.draw.rect(screen, COLORS['gray'], [510, HEIGHT - 150, 48, 48], 0, 5)
        bpm_sub_rect = pygame.draw.rect(screen, COLORS['gray'], [510, HEIGHT - 100, 48, 48], 0, 5)
        add_text = medium_font.render('+5', True, COLORS['white'])
        screen.blit(add_text, (520, HEIGHT - 140))
        sub_text = medium_font.render('-5', True, COLORS['white'])
        screen.blit(sub_text, (520, HEIGHT - 90))
        # nb_beats per loop buttons
        beats_rect = pygame.draw.rect(screen, COLORS['gray'], [600, HEIGHT - 150, 200, 100], 5, 5)
        beats_text = medium_font.render('Beats In Loop', True, COLORS['white'])
        screen.blit(beats_text, (612, HEIGHT - 130))
        beats_text2 = label_font.render(f'{nb_beats}', True, COLORS['white'])
        screen.blit(beats_text2, (670, HEIGHT - 100))
        beats_add_rect = pygame.draw.rect(screen, COLORS['gray'], [810, HEIGHT - 150, 48, 48], 0, 5)
        beats_sub_rect = pygame.draw.rect(screen, COLORS['gray'], [810, HEIGHT - 100, 48, 48], 0, 5)
        add_text2 = medium_font.render('+1', True, COLORS['white'])
        screen.blit(add_text2, (820, HEIGHT - 140))
        sub_text2 = medium_font.render('-1', True, COLORS['white'])
        screen.blit(sub_text2, (820, HEIGHT - 90))
        # clear board button
        clear = pygame.draw.rect(screen, COLORS['gray'], [1150, HEIGHT - 150, 200, 100], 0, 5)
        play_text = label_font.render('Clear Board', True, COLORS['white'])
        screen.blit(play_text, (1160, HEIGHT - 130))
        # save and load buttons
        save_button = pygame.draw.rect(screen, COLORS['gray'], [900, HEIGHT - 150, 200, 48], 0, 5)
        save_text = label_font.render('Save Beat', True, COLORS['white'])
        screen.blit(save_text, (920, HEIGHT - 140))
        load_button = pygame.draw.rect(screen, COLORS['gray'], [900, HEIGHT - 98, 200, 48], 0, 5)
        load_text = label_font.render('Load Beat', True, COLORS['white'])
        screen.blit(load_text, (920, HEIGHT - 90))
        # instrument rectangles
        instrument_rects = [pygame.rect.Rect((0, i * 100), (200, 100)) for i in range(nb_instruments)]
        if beat_changed:
            play_notes(clicked, active_beat, active_list, instruments)
            beat_changed = False
        if save_menu:
            exit_button, saving_button, beat_name, entry_rect = draw_save_menu(screen, beat_name, typing, label_font)
        elif load_menu:
            exit_button, loading_button, entry_rect, delete_button, loaded_information = draw_load_menu(screen, index, label_font, medium_font, saved_beats)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and not save_menu and not load_menu:
                for i in range(len(boxes)):
                    if boxes[i][0].collidepoint(event.pos):
                        coords = boxes[i][1]
                        clicked[coords[1]][coords[0]] *= -1
            if event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu:
                if play_pause.collidepoint(event.pos) and playing:
                    playing = False
                elif play_pause.collidepoint(event.pos) and not playing:
                    playing = True
                    active_beat = 0
                    active_length = 0
                if beats_add_rect.collidepoint(event.pos):
                    nb_beats += 1
                    for i in range(len(clicked)):
                        clicked[i].append(-1)
                elif beats_sub_rect.collidepoint(event.pos):
                    nb_beats -= 1
                    for i in range(len(clicked)):
                        clicked[i].pop(-1)
                if bpm_add_rect.collidepoint(event.pos):
                    bpm += 5
                elif bpm_sub_rect.collidepoint(event.pos):
                    bpm -= 5
                if clear.collidepoint(event.pos):
                    clicked = [[-1 for _ in range(nb_beats)] for _ in range(nb_instruments)]
                for i in range(len(instrument_rects)):
                    if instrument_rects[i].collidepoint(event.pos):
                        active_list[i] *= -1
                if save_button.collidepoint(event.pos):
                    save_menu = True
                if load_button.collidepoint(event.pos):
                    load_menu = True
                    playing = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if exit_button.collidepoint(event.pos):
                    save_menu = False
                    load_menu = False
                    playing = True
                    typing = False
                    beat_name = ''
                if entry_rect.collidepoint(event.pos):
                    if save_menu:
                        if typing:
                            typing = False
                        else:
                            typing = True
                    if load_menu:
                        index = (event.pos[1] - 100) // 50
                if save_menu:
                    if saving_button.collidepoint(event.pos):
                        with open('saved_beats.txt', 'w') as f:
                            saved_beats.append(f'\nname: {beat_name}, nb_beats: {nb_beats}, bpm: {bpm}, selected: {clicked}')
                            for i in range(len(saved_beats)):
                                f.write(str(saved_beats[i]))
                        save_menu = False
                        load_menu = False
                        playing = True
                        typing = False
                        beat_name = ''
                if load_menu:
                    if delete_button.collidepoint(event.pos):
                        if 0 <= index < len(saved_beats):
                            saved_beats.pop(index)
                    if loading_button.collidepoint(event.pos):
                        if 0 <= index < len(saved_beats):
                            nb_beats = loaded_information[0]
                            bpm = loaded_information[1]
                            clicked = loaded_information[2]
                            index = 100
                            save_menu = False
                            load_menu = False
                            playing = True
                            typing = False
            if event.type == pygame.TEXTINPUT and typing:
                beat_name += event.text
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and len(beat_name) > 0:
                    beat_name = beat_name[:-1]
    
        beat_length = (FPS * 60) // bpm
    
        if playing:
            if active_length < beat_length:
                active_length += 1
            else:
                active_length = 0
                if active_beat < nb_beats - 1:
                    active_beat += 1
                    beat_changed = True
                else:
                    active_beat = 0
                    beat_changed = True
    
        pygame.display.flip()
    
    with open('saved_beats.txt', 'w') as f:
        for i in range(len(saved_beats)):
            f.write(str(saved_beats[i]))
            
    pygame.quit()
