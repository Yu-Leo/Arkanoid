# Модуль для работы с log файлом игры


def print_mobsMatrix(file, mobs_matrix):
    """Вывод сгенерированной матрицы с мобами"""
    for row in mobs_matrix:
        for point in row:
            file.write(str(point) + ' ')
        file.write('\n')


def print_start_info(file, start_info):
    """
    Вывод начальной информации
    info: game_mod, all_mobs_lines, mobs_matrix, all_points
    """
    file.write(f"Режим игры: {start_info[0]}\n")
    file.write(f"Генерируемых рядов: {start_info[1]}\n")
    print_mobsMatrix(file, start_info[2])
    file.write(f"Необходимо очков для победы: {start_info[3]}\n")


def print_player_info(file, player):
    """Вывод информации об игроке в лог-файл"""
    file.write("-" * 20 + "\n")
    file.write("Информация об игроке: \n")
    file.write(" " * 4 + "Координаты: \n")
    file.write(" " * 8 + f"1) Центр: {player.rect.center} \n")
    file.write(" " * 8 + f"2) Левая граница: {player.rect.left} \n")
    file.write(" " * 8 + f"3) Верхняя граница: {player.rect.top} \n")
    file.write(" " * 8 + f"4) Правая граница: {player.rect.right} \n")
    file.write(" " * 8 + f"5) Нижняя граница: {player.rect.bottom} \n")

    file.write(" " * 4 + "Скорость: \n")
    # file.write(" " * 8 + f"1) Дефолтная скорость: {player.dspeed} \n")
    # file.write(" " * 8 + f"2) Максимальная скорость: {player.Speed} \n")
    # file.write(" " * 8 + f"3) Текущая скорость: {player.speed} \n")

    file.write(" " * 4 + "Эффекты: ")
    for i in player.activeEffects:
        file.write(f" {i}")
    file.write("\n")
    file.write(" " * 4 + f"isFree: {player.isFree}\n")
    file.write("-" * 20 + "\n")
    file.write("\n")


def print_message(file, message):
    """Вывод сообщения в лог-файл"""
    file.write(message)


def print_def_str(file, num):
    """
    Вывод одной из страдартных строк
    num - номер страдартной строки
    """
    if num == 0:
        msg = "=" * 7 + "LOG FILE ARKANOID" + "=" * 7
    elif num == 1:
        msg = "-" * 5 + "begin" + "-" * 5
    elif num == 2:
        msg = "-" * 5 + "start" + "-" * 5
    elif num == 3:
        msg = "-" * 5 + "end" + "-" * 5
    elif num == 4:
        msg = "=" * 5 + "EXIT" + "=" * 5
    elif num == 5:
        msg = "WIN"
    elif num == 6:
        msg = "LOSS"
    elif num == 7:
        msg = "RESTART"
    else:
        msg = "!"
    file.write(msg + "\n")
