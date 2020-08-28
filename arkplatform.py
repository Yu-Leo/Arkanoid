import pygame
from random import randint

pygame.init()


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.__SIZES = [70, 14]  # Размеры по умолчанию
        self.__sizes = self.__SIZES  # Текущие размеры
        self._color = (70, 216, 232)
        self.__image = pygame.Surface(
            self.__sizes, pygame.SRCALPHA)  # Прозрачная поверхность
        # Генерания с центром на случайной х координате, и на высоте центра 630
        self.__rect = self.__image.get_rect(
            centerx=randint(60, 380),
            centery=630 + self.__sizes[1] // 2)
        self.__max_speed = 7  # Максимальная скорость
        self.__speed = 0  # Текущая скорость

    @property
    def rect(self):
        return self.__rect

    def draw(self, sc):
        """Отрисовка платформы на поле"""
        coords = self.__rect.center
        self.__rect = self.__image.get_rect(center=coords)
        pygame.draw.rect(self.__image, self._color,
                         (0, 0, self.__sizes[0], self.__sizes[1] - 5))
        pygame.draw.rect(self.__image, self._color,
                         (3, 0, self.__sizes[0] - 6, self.__sizes[1]))
        pygame.draw.line(self.__image,
                         (56, 56, 245), (0, 0), (self.__sizes[0], 0), 8)
        sc.blit(self.__image, self.rect.topleft)

    def update(self):
        """Движение платформы"""
        if self.__rect.left >= 20 + self.__max_speed and self.__speed < 0:
            self.rect.x += self.__speed
        if self.__rect.right <= 420 - self.__max_speed and self.__speed > 0:
            self.__rect.x += self.__speed

    def set_speed(self, direction):
        """
        Установка скорости в зависимости от нажатой клавиши
        direction = -1 - двжение влево
        direction = 0 - остановка
        direction = 1 - движение вправо
        """
        self.__speed = direction * self.__max_speed
