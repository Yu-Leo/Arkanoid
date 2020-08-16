import pygame

pygame.init()
from random import random


class Mob(pygame.sprite.Sprite):
    # Настройки: (GREEN, 1), (YELLOW, 2), (RED, 3), (BLUE, 4), (PURPLE, 5)
    settings = (
        ((70, 232, 72), (26, 135, 19), 1),
        ((232, 221, 70), (135, 127, 19), 2),
        ((201, 60, 75), (158, 31, 43), 3),
        ((72, 70, 232), (31, 29, 145), 4),
        ((148, 25, 109), (115, 18, 84), 5))

    def __init__(self, coords, x, y, pack):
        pygame.sprite.Sprite.__init__(self)
        self.__full_hardness = Mob.settings[pack][2]  # Начальная прочность
        self.coords = coords  # Координаты в матрице с мобами
        self._color, self._grid_color, self.__hardness = Mob.settings[pack]
        self.__image = pygame.Surface((40, 10))
        self.__rect = self.__image.get_rect(topleft=(x, y))

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
        if n == 4:
            for i in range(4):
                pygame.draw.rect(sc, self._color,
                                 (self.__rect.x + i * l, self.__rect.y, l, l))
        elif n == 3:
            pygame.draw.rect(sc, self._color,
                             (self.__rect.x, self.__rect.y, l, l))
            pygame.draw.rect(sc, self._color,
                             (self.__rect.x + 2 * l, self.__rect.y, l, l))
            pygame.draw.rect(sc, self._color,
                             (self.__rect.x + 3 * l, self.__rect.y, l, l))
        elif n == 2:
            pygame.draw.rect(sc, self._color,
                             (self.__rect.x, self.__rect.y, l, l))
            pygame.draw.rect(sc, self._color,
                             (self.__rect.x + 3 * l, self.__rect.y, l, l))
        elif n == 1:
            pygame.draw.rect(sc, self._color,
                             (self.__rect.x, self.__rect.y, l, l))
        for i in range(4):  # Рамочка более тёмного цвета
            pygame.draw.rect(sc, self._grid_color,
                             (self.__rect.x + i * l, self.__rect.y, l, l), 1)

    def draw(self, sc):
        """
        Основная ф-ция отрисовки мобов.
        В зависимости от нанесённого удара, вызывает ф-цию с нужными параметрами
        """

        if (self.__full_hardness == 5 and (
                self.__hardness == 5 or self.__hardness == 4)) or \
                (
                        self.__full_hardness != 5 and self.__hardness == self.__full_hardness):
            self.draw_mob(sc, 4)
        elif (self.__full_hardness == 5 and self.__hardness == 3) or \
                (self.__full_hardness != 5 and (
                        self.__hardness == self.__full_hardness - 1 and self.__full_hardness != 2)):
            self.draw_mob(sc, 3)
        elif (self.__full_hardness == 5 and self.__hardness == 2) or \
                (self.__full_hardness != 5 and (
                        self.__hardness == self.__full_hardness - 2 or self.__full_hardness == 2)):
            self.draw_mob(sc, 2)
        elif (self.__full_hardness == 5 and self.__hardness == 1) or \
                (
                        self.__full_hardness != 5 and self.__hardness == self.__full_hardness - 3):
            self.draw_mob(sc, 1)
        else:
            raise Warning("Ошибка в отрисовке мобов")

    def __str__(self):
        return f'Mob {self._coords}: full_hardness: {self.__full_hardness},' + \
               f' hardness: {self.__hardness}'


def generate_mobs_matrix(Nmax):
    """Генерация матрицы с прочностями мобов"""
    all_points = 0  # Кол-во очков, которые необходимо получить, чтобы выиграть

    # Матрица с номерами мобов
    matrix = [[0 for i in range(9)] for j in range(Nmax)]

    # Распределение веросятности создания моба данного цвета (сложности)
    green = 60  # %
    yellow = 15  # %
    red = 10  # %
    blue = 5  # %
    purple = 3  # %
    points = [
        0,
        green / 100,
        (green + yellow) / 100,
        (green + yellow + red) / 100,
        (green + yellow + red + blue) / 100,
        (green + yellow + red + blue + purple) / 100]

    # Генецация мобов на основе процентного распределения веросятностей
    for i in range(Nmax):
        for j in range(9):
            a = random()
            if points[0] < a <= points[1]:
                matrix[i][j] = 1
            elif points[1] < a <= points[2]:
                matrix[i][j] = 2
            elif points[2] < a <= points[3]:
                matrix[i][j] = 3
            elif points[3] < a <= points[4]:
                matrix[i][j] = 4
            elif points[4] < a <= points[5]:
                matrix[i][j] = 5
            else:
                matrix[i][j] = 0
            all_points += matrix[i][j]
    return matrix, all_points


def add_mobs(lines, matrix):  # Создание группы мобов по матрице
    mobs = pygame.sprite.Group()
    for i in range(lines):
        for j in range(9):
            if matrix[i][j] != 0:
                mobs.add(Mob((i, j), 20 + j * 45, 45 + 15 * lines - i * 20,
                             matrix[i][j] - 1))
    return mobs


def draw_mobs(sc, mobs):
    """Отрисовка всех мобов """
    for mob in mobs:
        mob.draw(sc)
