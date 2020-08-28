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
    global game_mod, all_mobs_lines, mobs_matrix
    global all_points, score, mobs_list, player, platform
    # Режим игры, количество генерируемых рядов с препятствиями
    # game_mod, all_mobs_lines = dialogbox.get_parameters()
    game_mod, all_mobs_lines = 1, 10  # Режим игры, кол-во рядов с мобами
    mobs_matrix, all_points = arkmobs.generate_mobs_matrix(all_mobs_lines)
    mobs_list = arkmobs.add_mobs(all_mobs_lines, mobs_matrix)
    score = 0
    time.sleep(0.05)  # Задержка перед возвращением на платформу (в секундах)
    player = Player(platform.rect.centerx)  # Создание игрока


def finish(is_win):
    """Выполняется при завершении игры (проигрыше или убийстве всех мобов)"""
    global game
    logs.print_def_str(log_file, (5 if is_win else 6))
    game = False  # Пауза на время открытия диалоговых окон
    # Если пользователь не хочет начинать сначала
    if not dialogbox.finish(is_win, score):
        logs.print_def_str(log_file, 4)
        exit()
    # Рестарт
    start_settings()
    logs.print_def_str(log_file, 7)
    logs.print_start_info(log_file,
                          [game_mod, all_mobs_lines,
                           mobs_matrix, all_points])
    game = True  # продолжение игры


def check_quit(event_type):
    """Выход из игры при нажатии крестика"""
    if event_type == pygame.QUIT:
        logs.print_def_str(log_file, 3)
        log_file.close()
        exit()


def get_direction(key):
    """
    Возвращение номера направления в зависимости от состояния кнопок,
    используемых для управления платформой
    """
    left = (pygame.K_a, pygame.K_LEFT)  # Кнопки для движения влево
    right = (pygame.K_d, pygame.K_RIGHT)  # Кнопки для движения вправо
    if key in left:
        return -1
    elif key in right:
        return 1
    return 0


def check_restart(key):
    """Перезапуск игры при нажатии [r]"""
    # нажатие [r] и "да" в окне для подтверждения рестарта
    if key == pygame.K_r and dialogbox.restart():
        start_settings()


def check_activation(key):
    """Активация игрока при нажатии [SPACE], если игра запущена"""
    if not player.is_free and key == pygame.K_SPACE:
        player.activation()


# Открытие лог-файла и запись начальных строчек
log_file = open(config.log_file_name, 'w', encoding='utf-8')
logs.print_def_str(log_file, 0)
logs.print_def_str(log_file, 1)

# ---------------------------Стандартные настройки------------------------------
pygame.init()  # Инициализируем PyGame
sc = pygame.display.set_mode(config.win_size)  # Создаем поверхность окна
pygame.display.set_caption("Arkanoid by Yu-Leo")  # Название окна
icon = pygame.image.load(r"logo.jpg")  # Загружаем иконку окна
pygame.display.set_icon(icon)  # Устанавливаем иконку окна
clock = pygame.time.Clock()  # Счётчик для поддержания FPS
# ---------------------------Стандартные настройки------------------------------

# Само игровое поле
game_field = pygame.Surface(config.gf_size)
gf_color = config.gf_color
game_field.fill(gf_color)

# Игровой процесс
game = True  # Игра (on/off)
platform = Platform()  # Создание платформы
mobs_matrix = [[], ]
score = best_score = all_points = gameMod = all_mobs_lines = 0
mobs_list = pygame.sprite.Group()
player = Player(platform.rect.centerx)
start_settings()  # Задание стартовых настроек

# Вывод стартовой информации в лог-файл
logs.print_start_info(log_file,
                      [game_mod, all_mobs_lines,
                       mobs_matrix, all_points])

# Невидимое окно tkinter (чтобы открывались диалоговые окна)
tk_window = tkinter.Tk()
tk_window.withdraw()

platform_direction = 0  # Направление движения платформы
logs.print_def_str(log_file, 2)
while True:  # Основной игровой цикл
    for event in pygame.event.get():  # Обработка событий
        check_quit(event.type)  # Проверка на нажание крестика

        if event.type == pygame.KEYDOWN:
            check_restart(event.key)  # Проверка кнопки [r]

            if event.key == pygame.K_p:  # [p] - Пауза
                game = not game

            if game:
                # Изменение направления движения платформы
                platform_direction = get_direction(event.key)

                check_activation(event.key)  # Проверка кнопки [SPACE]
        elif event.type == pygame.KEYUP:  # Если все кнопки отпущены
            platform_direction = 0

    # Изменение направления движения платформы
    platform.set_speed(platform_direction)

    sc.fill(config.bg_color)  # Обнуление окна
    sc.blit(game_field, config.gf_topleft)  # Отрисовка игрового поля
    if game:
        # Список мобов, с которыми столкнулся игрок
        hit_list = pygame.sprite.spritecollide(player, mobs_list, False)
        platform.update()  # Обновление координат платформы
        player.update(platform.rect, collision_with_mobs=(len(hit_list) > 0))
        for mob in hit_list:
            # Нанесение урона этим мобам
            mobs_matrix[mob.matrix_coords[0]][mob.matrix_coords[1]] \
                -= player.damage
            if mob.hardness - player.damage <= 0:
                score += mob.full_hardness
                mob.hardness = 0
                mob.kill()
            else:
                mob.hardness -= player.damage

    # Если включён обычный режим, и убиты все мобы
    if game_mod == 1 and score == all_points:
        finish(is_win=False)

    if player.lives == 0:  # Если проиграли
        finish(is_win=False)

    # -----------------------Отрисовка всех элементов игры----------------------
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
    # -----------------------Отрисовка всех элементов игры----------------------

    # pygame.draw.aaline(sc, (255, 255, 255), [20, 190], [420, 190])  # Линия

    pygame.display.update()  # Обновляем дисплей
    clock.tick(config.fps)
