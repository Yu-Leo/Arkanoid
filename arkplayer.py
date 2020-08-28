import pygame
from random import randint  # Случайные целые числа в диапазоне
from time import sleep  # Задержка
import arklogs as logs  # Модуль для работы с log файлом
from arkconfig import log_file_name  # Имя log файла игры

pygame.init()


class Player(pygame.sprite.Sprite):
    # Эффекты: (без эффекта), (красный), (фиолетовый), (голубой)
    effects = (
        (70, 216, 232),
        (207, 70, 70),
        (208, 0, 255),
        (140, 218, 230))

    def __init__(self, pl_x):
        pygame.sprite.Sprite.__init__(self)
        self._color = Player.effects[0]
        self.__radius = 10
        self.__image = pygame.Surface(
            (self.__radius * 2, self.__radius * 2),
            pygame.SRCALPHA)  # Прозрачная поверхность
        self.__rect = self.__image.get_rect(
            centerx=pl_x,
            centery=630 - self.__radius)  # Rect по поверхности
        self.__is_free = False  # Свободно летает / приклеен к платформе
        self.__SPEED = (1.0, 4.0)  # Обычная(без эффектов) скорость (x, y)
        self.__cur_speed = [0.0, 0.0]  # Текущая скорость (x, y)
        # Направление (-1 - вверх / влево, -1 - вниз / вправо, 0 - стоп)
        self.__direction = [0, 0]
        self.__full_lives = 3  # Полное кол-во жизней
        self.__lives = self.__full_lives  # Кол-во жизней в данный момент
        self.__damage = 1  # Урон, который наносит за одно столкновение с мобом

        self.__inf_mod = False  # Шарик отлетает от уровня платформы (чит)

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, arg):
        self.__rect = arg

    @property
    def lives(self):
        return self.__lives

    @property
    def damage(self):
        return self.__damage

    @property
    def is_free(self):
        return self.__is_free

    def draw(self, sc):
        """Отрисовка игрока на поле"""
        sc.blit(self.__image, self.__rect)
        pygame.draw.circle(self.__image, self._color,
                           (self.__radius, self.__radius), self.__radius - 2)

    def set_speed(self, k):
        """Установление скорости в зависимости от коэффициетка k"""
        self.__cur_speed[0] = self.__SPEED[0] * k
        self.__cur_speed[1] = self.__SPEED[1] * k

    def activation(self):
        """Активация игрока"""
        self.__is_free = True
        self.__direction = [-1, -1]
        self.set_speed(1.0)

    def check_platform_hit(self, left, right):
        """Проверка на столкновение с платформой"""
        x_coord = (self.__rect.right >= left and
                   self.__rect.left <= right) or self.__inf_mod
        y_coord = 630 < self.__rect.bottom + self.__cur_speed[1] <= 660
        return x_coord and y_coord

    def update(self, pl_rect, collision_with_mobs):
        """
        Обновление параметров игрока игрока
        1) Если игрок "приклеен" к платформе, перемещается вместе с ней
        2) Столкновения
            1) с вертикальными стенами
            2) с потолком
            3) с платформой
        3) Изменение самих координат
        5) Выход за границу поля (снизу)
        """

        def random_d():
            t = 5  # Случайное изменение координаты
            return randint(-t, t)

        if not self.__is_free:  # Если приклеен к платформе, движ. вместе с ней
            self.__rect.centerx = pl_rect.centerx
            self.__cur_speed = [0, 0]
        else:
            if self.__rect.left <= 20:  # Столкновение с левой стенкой
                self.__rect.left = 21
                self.__direction[0] = -self.__direction[0]
                r = random_d()
                if self.__rect.centery + r > 20:
                    self.__rect.centery += r

                with open(log_file_name, "w") as file:
                    logs.print_message(file, "LEFT \n")

            elif self.__rect.right >= 20 + 400:  # Столкновение с правой стенкой
                self.__rect.right = 419
                self.__direction[0] = -self.__direction[0]
                self.__rect.centery += random_d()

                with open(log_file_name, "w") as file:
                    logs.print_message(file, "RIGHT \n")

            # Столкновение с потолком
            if self.__rect.top <= 20:
                self.__rect.top = 21
                self.__direction[1] = -self.__direction[1]
                self.__rect.centerx += random_d()

                with open(log_file_name, "w") as file:
                    logs.print_message(file, "TOP \n")

            # Столкновение с платформой
            if self.check_platform_hit(pl_rect.left, pl_rect.right):
                self.__rect.bottom = 630
                self.__direction[1] = -self.__direction[1]
                with open(log_file_name, "w") as file:
                    logs.print_message(file, "PLATFORM \n")

            if collision_with_mobs:  # Отражение ирока от моба
                self.__direction[1] = -self.__direction[1]
                self.rect.centerx += randint(-3, 3)
                # Смещение вниз. Избегем повторного удара
                self.rect.centery += 5

            # Изменение координат
            self.__rect.centerx += self.__cur_speed[0] * self.__direction[0]
            self.__rect.centery += self.__cur_speed[1] * self.__direction[1]

            if self.__rect.bottom > 670:  # Вылет за нижн. границу игрового поля
                self.__lives -= 1
                self.__direction = [0, 0]
                # Задержка перед возвращением на платформу (в секундах)
                sleep(0.05)
                self.__rect.center = (pl_rect.centerx, 630 - self.__radius)
                self.__is_free = False
