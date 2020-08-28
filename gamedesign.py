# Модуль для отображения игровых элементов

import pygame

pygame.init()

font = pygame.font.SysFont("arialblack", 28, 0, 0)  # Основной шрифт
little_font = pygame.font.SysFont("arialblack", 18, 0, 0)  # Мелкий шрифт


def print_pause(sc, game):
    """Отображение активности игры. Если игра на паузе, выводим PAUSE"""
    global font
    if not game:
        text = font.render('PAUSE', 1, (255, 255, 255))
        sc.blit(text, (480, 30))


def print_score(sc, score):
    """Отображение текущего счёта"""
    global font
    text1 = font.render('SCORE:', 1, (255, 255, 255))
    text2 = font.render(str(score), 1, (255, 255, 255))
    sc.blit(text1, (480, 160))
    sc.blit(text2, (480, 200))


def print_best_score(sc, best_score):
    """Отображение лучшего счёта с момента запуска игры"""
    global font
    text1 = font.render('BEST', 1, (255, 255, 255))
    text2 = font.render('SCORE:', 1, (255, 255, 255))
    text3 = font.render(str(best_score), 1, (255, 255, 255))
    sc.blit(text1, (480, 280))
    sc.blit(text2, (480, 320))
    sc.blit(text3, (480, 360))


def draw_lives(sc, lives):
    """
    Отображение оставшихся жизней.
    Жизни отображаются красными кружками
    Если жизней < 3, то на месте остальных видны красные контуры
    Если жизней > 3, то разница, между полным числом жизней и числом 3,
    отображается справа в золотом круге (как бонусные жизни)
    """
    global little_font
    for i in range(3):  # Обводка, которая видна, если жизней нет
        pygame.draw.circle(sc, (230, 32, 45), (490 + i * 40, 100), 9, 1)
    for i in range(min(lives, 3)):  # "Стандартные" 3 жизни
        pygame.draw.circle(sc, (230, 32, 45), (490 + i * 40, 100), 10)

    diff = lives - min(lives, 3)  # Кол-во бонусных жизней
    if diff > 0:
        text1 = little_font.render(str(diff), 1, (0, 0, 0))
        pygame.draw.circle(sc, (217, 214, 46), (490 + 3 * 40, 100), 15)
        sc.blit(text1, (490 + 3 * 40 - 5, 87))


def draw_thorns(sc):
    """Шипы внизу игрового поля"""
    red = (232, 70, 70)
    orange = (232, 113, 70)
    colors = (red, orange)
    x, y = 20, 680
    w, h = 40, 20
    for i in range(10):
        pygame.draw.polygon(sc, colors[i % 2],
                            [[i * w + x, y],
                             [i * w + x + w // 2, y - h],
                             [i * w + x + w, y]])


def draw_platform_line(sc):
    """Отрисовка линии на уровне движения платформы"""
    pygame.draw.aaline(sc, (255, 255, 255), [20, 630], [420, 630])
