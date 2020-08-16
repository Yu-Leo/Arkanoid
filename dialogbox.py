# Модуль для работы с диалоговыми окнами

import tkinter.messagebox  # Диалоговые окна tkinter
import phrases_ru as phrases  # Файл с фразами, которые используются в игре


def get_parameters():
    """Вопрос пользователю о режиме игры и сложности"""
    input_msg = input(phrases.ask_game_mode)
    game_mod = int(input_msg)
    if game_mod == 1:
        all_mobs_lines = int(input(phrases.ask_difficulty))
    else:
        return
    return game_mod, all_mobs_lines


def finish(is_win, score):
    """Вызов диалогового окна привыигрыше/проигрыше"""
    tkinter.messagebox.showinfo(
        title=phrases.you_win if is_win else phrases.you_lose,
        message=phrases.your_score(score))  # Уведомление о результате игры
    answer = tkinter.messagebox.askyesno(
        title=phrases.you_win if is_win else phrases.you_lose,
        message=phrases.ask_restart)  # Начинать ли игру с начала (True / False)
    return answer

def restart():
    return tkinter.messagebox.askyesno(title=f"Рестарт",
                                                     message="Перезапустить?")