# Модуль для работы с мобами
import pygame
from random import random

pygame.init()


class Mob(pygame.sprite.Sprite):
    # Настройки (основной цвет, цвет рамки, прочность):
    # (GREEN, 1), (YELLOW, 2), (RED, 3), (BLUE, 4), (PURPLE, 5)
    settings = (
        ((70, 232, 72), (26, 135, 19), 1),
        ((232, 221, 70), (135, 127, 19), 2),
        ((201, 60, 75), (158, 31, 43), 3),
        ((72, 70, 232), (31, 29, 145), 4),
        ((148, 25, 109), (115, 18, 84), 5))

    def __init__(self, matrix_coords, coords, pack):
        pygame.sprite.Sprite.__init__(self)
        self.__full_hardness = Mob.settings[pack][2]  # Начальная прочность
        self.matrix_coords = matrix_coords  # Координаты в матрице с мобами
        self._color, self._grid_color, self.__hardness = Mob.settings[pack]
        self.__image = pygame.Surface((40, 10))
        self.__rect = self.__image.get_rect(topleft=coords)

    @property
    def rect(self):
        return self.__rect

    @property
    def hardness(self):
        return self.__hardness

    @hardness.setter
    def hardness(self, other):
        self.__hardness = other

    @property
    def full_hardness(self):
        return self.__full_hardness

    def draw_mob(self, sc, n):
        """
        Отрисовка с учетом нанесённого удара.
        Эта ф-ция вызывается основной ф-цией отрисовки
        """
        l = self.__rect.width // 4  # Ширина одного сектора
        color = self._color  # Основной цвет моба
        x, y = self.__rect.x, self.__rect.y
        if n == 4:
            for i in range(4):
                pygame.draw.rect(sc, color, (x + i * l, y, l, l))
        elif n == 3:
            pygame.draw.rect(sc, color,
                             (x, y, l, l))
            pygame.draw.rect(sc, color, (x + 2 * l, y, l, l))
            pygame.draw.rect(sc, color, (x + 3 * l, y, l, l))
        elif n == 2:
            pygame.draw.rect(sc, color, (x, y, l, l))
            pygame.draw.rect(sc, color, (x + 3 * l, y, l, l))
        elif n == 1:
            pygame.draw.rect(sc, color, (x, y, l, l))
        for i in range(4):  # Рамочка более тёмного цвета
            pygame.draw.rect(sc, self._grid_color, (x + i * l, y, l, l), 1)

    def is_need_to_draw(self, num):
        """Проверка на то, нужно ли отрисовывать num ячеек"""
        full = self.__full_hardness
        now = self.__hardness
        if num == 4:
            return (full == 5 and now in (4, 5)) or (full != 5 and now == full)
        elif num == 3:
            return (full == 5 and now == 3) or \
                   (full not in (5, 2) and (now == full - 1))
        elif num == 2:
            return (full == 5 and now == 2) or \
                   (full != 5 and (now == full - 2 or full == 2))
        elif num == 1:
            return (full == 5 and now == 1) or (full != 5 and now == full - 3)
        else:
            raise Warning("Ошибка в отрисовке мобов")

    def draw(self, sc):
        """
        Основная ф-ция отрисовки мобов.
        В зависимости от нанесённого удара, вызывает ф-цию с нужными параметрами
        """
        for i in range(4, 0, -1):
            if self.is_need_to_draw(i):
                self.draw_mob(sc, i)

    def __str__(self):
        string = 0
        string += f"Mob {self.matrix_coords}: "
        string += f"full_hardness: {self.__full_hardness}, "
        string += f"hardness: {self.__hardness}"
        return string


def get_one_ceil(points):
    """Получение значения одной ячейки матрицы"""
    a = random()
    for num in range(1, 7):  # Проходим по всем промежуткам
        if points[num - 1] < a <= points[num]:  # Значение соотв. промежутку
            return 0 if num == 6 else num


def generate_mobs_matrix(Nmax):
    """Генерация матрицы с прочностями мобов"""
    all_points = 0  # Кол-во очков, которые необходимо получить, чтобы выиграть
    # Матрица с номерами мобов
    matrix = [[0 for i in range(9)] for j in range(Nmax)]

    # Распределение веросятности создания моба данного цвета (сложности)
    percents = [60, 15, 10, 5, 3]  # green, yellow, red, blue, purple
    points = [
        0,
        percents[0] / 100,
        (sum(percents[0:2])) / 100,
        (sum(percents[0:3])) / 100,
        (sum(percents[0:4])) / 100,
        (sum(percents[0:5])) / 100,
        1]

    # Генецация мобов на основе процентного распределения веросятностей
    for i in range(Nmax):
        for j in range(9):
            matrix[i][j] = get_one_ceil(points)
            all_points += matrix[i][j]
    return matrix, all_points


def add_mob(matrix, i, j, mobs):
    """Добавление одного моба из матрицы (если ячейка не пустая)"""
    if matrix[i][j] != 0:
        mobs.add(Mob(matrix_coords=(i, j),
                     coords=(20 + j * 45, 20 + 15 * i),
                     pack=(matrix[i][j] - 1)))


def add_mobs(lines, matrix):
    """Создание группы мобов по матрице"""
    mobs = pygame.sprite.Group()
    for i in range(lines):
        for j in range(9):
            add_mob(matrix, i, j, mobs)
    return mobs


def draw_mobs(sc, mobs):
    """Отрисовка всех мобов"""
    for mob in mobs:
        mob.draw(sc)
