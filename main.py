import pygame
import tkinter
import time

import arklogs as logs  # Модуль для работы с log файлом
import dialogbox  # Модуль для работы с диалоговыми окнами
import gamedesign as gd  # Модуль для отображения игровых элементов
import arkmobs  # Модуль с мобами
from arkplayer import Player  # Игрок
from arkplatform import Platform  # Платформа
import arkconfig as config  # Модуль с настройками игры


def start_settings():
    """Установка начальных настроек"""
    global game_mod, all_mobs_lines, visible_mobs_lines, mobs_matrix, all_points, score, mobs_list, player, platform
    # Режим игры, количество генерируемых рядов с препятствиями
    # game_mod, all_mobs_lines = dialogbox.get_parameters()
    game_mod, all_mobs_lines = 2, 20  # Режим игры, кол-во рядов с мобами
    visible_mobs_lines = min(9, all_mobs_lines)
    mobs_matrix, all_points = arkmobs.generate_mobs_matrix(all_mobs_lines)
    mobs_list = arkmobs.add_mobs(visible_mobs_lines, mobs_matrix)
    score = 0
    time.sleep(0.05)  # Задержка перед возвращением на платформу (в секундах)
    player = Player(platform.rect.centerx)  # Создание игрока


# Открытие лог-файла и запись начальных строчек
log_file = open(config.log_file_name, 'w', encoding='utf-8')
logs.print_def_str(log_file, 0)
logs.print_def_str(log_file, 1)

# ----------------Стандартные настройки---------------
pygame.init()  # Инициализируем PyGame
fps = 90  # Частота обновления
window_size = 650, 700
bg_color = (15, 15, 15)
sc = pygame.display.set_mode(window_size)  # Создаем поверхность окна
sc.fill(bg_color)
pygame.display.set_caption("Arkanoid")  # Название окна
icon = pygame.image.load(r"logo.jpg")  # Загружаем иконку окна
pygame.display.set_icon(icon)  # Устанавливаем иконку окна
clock = pygame.time.Clock()  # Счётчик для поддержания FPS
# ----------------Стандартные настройки---------------

# Само игровое поле
game_field = pygame.Surface((400, 660))
gf_color = (70, 70, 70)
game_field.fill(gf_color)

# Игровой процесс
game = True  # Игра (on/off)
platform = Platform()  # Создание платформы
mobs_matrix = [[], ]
score = best_score = all_points = gameMod = 0
all_mobs_lines = visible_mobs_lines = 0
mobs_list = pygame.sprite.Group()
player = Player(platform.rect.centerx)
start_settings()  # Задание стартовых настроек

# Музыка
pygame.mixer.music.load(r"background.mp3")
pygame.mixer.music.set_volume(0.5)
# pygame.mixer.music.play(-1)

# Вывод стартовой информации в лог-файл

logs.print_start_info(log_file,
                      [game_mod, all_mobs_lines, visible_mobs_lines,
                       mobs_matrix, all_points])

start_time = time.time()  # Начальное время перед игрой

# Невидимое окно tkinter (чтобы открывались диалоговые окна)
tk_window = tkinter.Tk()
tk_window.withdraw()

platform_direction = 0  # Направление движения платформы

logs.print_def_str(log_file, 2)
while True:  # Основной игровой цикл
    for event in pygame.event.get():  # Обработка событий
        if event.type == pygame.QUIT:  # Выход из игры
            logs.print_def_str(log_file, 3)
            log_file.close()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # [r] - Рестарт
                if dialogbox.restart():  # Окно для подтверждения рестарта
                    start_settings()  # Задание стартовых настроек

            if event.key == pygame.K_p:  # [p] - Пауза
                game = not game
                if game:
                    pygame.mixer.music.unpause()  # Пауза фоновой музыки
                else:
                    pygame.mixer.music.pause()  # Продолжение фоновой музыки
            if game:
                # Движение платформы
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    platform_direction = -1
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    platform_direction = 1

                # Активация игрока
                if not player.is_free and event.key == pygame.K_SPACE:
                    player.activation()
        elif event.type == pygame.KEYUP:  # Если все кнопки отпущены
            platform_direction = 0
    platform.set_speed(platform_direction)

    sc.fill(bg_color)  # Обнуление окна
    sc.blit(game_field, (20, 20))  # Отрисовка игрового поля
    if game:
        # Вывод информации об игроке в лог-файл каждые 0,5 секунды (примерно)
        # if abs(time.time() - int(time.time())) < 0.05
        # and int(time.time() - st) % 0.5 == 0:
        # PrintPlayerInfo2LogFile(logFile, player)

        # Список мобов, с которыми столкнулся игрок
        hit_list = pygame.sprite.spritecollide(player, mobs_list, False)
        for mob in hit_list:
            # Нанесение урона этим мобам
            mobs_matrix[mob.coords[0]][mob.coords[1]] -= player.damage
            if mob.hardness - player.damage <= 0:
                score += mob.full_hardness
                mob.hardness = 0
                mob.kill()
                # mobsList.remove(mob)
                # hitList.remove(mob)
            else:
                mob.hardness -= player.damage

        platform.update()  # Обновление координат платформы
        player.update(platform.rect.centerx, platform.rect.left,
                      platform.rect.right, hit_list)

    if game_mod == 1:
        if score == all_points:  # Если включён обычный режим, и убиты все мобы
            logs.print_def_str(log_file, 5)
            game = False
            if dialogbox.finish(True, score):
                # Рестарт
                start_settings()
                logs.print_def_str(log_file, 7)
                logs.print_start_info(log_file,
                                      [game_mod, all_mobs_lines,
                                       visible_mobs_lines,
                                       mobs_matrix, all_points])
                game = True
            else:
                logs.print_def_str(log_file, 4)
                exit()

    if player.lives == 0:  # Если проиграли
        logs.print_def_str(log_file, 6)
        game = False
        if dialogbox.finish(False, score):
            # Рестарт
            start_settings()
            logs.print_def_str(log_file, 7)
            logs.print_start_info(log_file,
                                  [game_mod, all_mobs_lines, visible_mobs_lines,
                                   mobs_matrix, all_points])
            game = True
        else:
            logs.print_def_str(log_file, 4)
            exit()

    # ----------------Отрисовка всех элементов игры---------------
    platform.draw(sc)
    player.draw(sc)
    gd.print_pause(sc, game)
    gd.draw_lives(sc, player.lives)

    if score > best_score:
        best_score = score

    gd.print_score(sc, score)
    gd.print_best_score(sc, best_score)
    gd.draw_thorns(sc)
    arkmobs.draw_mobs(sc, mobs_list)
    # ----------------Отрисовка всех элементов игры---------------

    # pygame.draw.aaline(sc, (255, 255, 255), [20, 190], [420, 190])  # Линия
    pygame.display.update()  # Обновляем дисплей
    clock.tick(fps)

pygame.mixer.music.stop()
