# Author Loik Andrey mail: loikand@mail.ru
from typing import List, Any

from config import FILE_NAME_LOG, TASK_ID_IGNOR
from loguru import logger
import datetime as dt

from services.google_table.google_tb_work import WorkGoogle
from services.telegram.send_teleg import NotifTelegram

# Задаём параметры логирования
logger.add(FILE_NAME_LOG,
           format="{time:DD/MM/YY HH:mm:ss} - {file} - {level} - {message}",
           level="INFO",
           rotation="1 week",
           compression="zip")

wk_g = WorkGoogle()


def notif_alert(list_alert: list[dict]):
    """
    Отправляем уведомления о тревоге в телеграмм
    :param list_alert:
        Список словарей с ключами:
                'task_id': str or int,
                'task_name': str,
                'task_last_start': datetime.datetime(%Y, %m, %d, %H, %M, %S'),
                'time_interval': int,
                'task_delta_interval': int
    """
    notif_telegram = NotifTelegram()

    # Получаем список чатов для отправки уведомлений
    user_notif = wk_g.users_alert_notif()[0]['tel_chat_id']
    user_notif = user_notif.replace(' ', '').split(',')

    logger.info(f"Отправляем уведомления о тревоге в телеграмм пользователям {user_notif}")
    for alert in list_alert:
        # Генерируем текст сообщения
        alert['task_last_start'] = alert['task_last_start'].strftime('%Y-%m-%d %H:%M:%S')
        notif_telegram.message_alert(alert)

        # Отправляем сообщение в чаты телеграмм
        for chat_id in user_notif:
            notif_telegram.send_massage_chat(chat_id)
    return


def check_time_interval(tasks: list[dict]) -> list[dict]:
    """
    Проверяем есть ли нарушения в интервале времени между запусками задачи
    :param tasks:
        Список словарей с ключами:
            'task_id' - str or int
            'task_name',- str,
            'last_start' - datetime.datetime(%Y, %m, %d, %H, %M, %S'),
            'task_interval' - str or int
    :return:
        Список словарей с ключами:
            'task_id': str or int,
            'task_name': str,
            'task_last_start': datetime.datetime(%Y, %m, %d, %H, %M, %S'),
            'time_interval': int,
            'task_delta_interval': int,
    """
    alert: list[dict] = []
    for task in tasks:
        time_interval = int(task['task_interval'])
        task_delta_interval = (dt.datetime.now() - task['last_start']).seconds
        is_working_hours = check_working_hours(task)

        # Проверяем, что скрипт пропустил уже 3 допустимых интервала запуска и сейчас рабочее время этого скрипта
        if (task_delta_interval > time_interval * 3 and is_working_hours
                and task['task_id'] not in TASK_ID_IGNOR):
            logger.info(f"Найдена ошибка в интервале запуска задачи: {task['task_id']}")
            alert += [{
                'task_id': task['task_id'],
                'task_name': task['task_name'],
                'task_last_start': task['last_start'],
                'time_interval': time_interval,
                'task_delta_interval': task_delta_interval,
            }]
    return alert


def check_working_hours(task):
    """
    Проверяем возможность запуска задачи согласно заданного интервала времени.

    Находим задачу по ключу 'task_id' и проверяем прошёл ли заданный интервал 'task_interval'
    Добавлен в словарь ключ возможности запуска задачи `can_run_task`.
        Ключ принимает значение True, если интервал с последнего запуска уже прошёл.
        Ключ принимает значение False, если интервал с последнего запуска ещё не прошёл.
    """
    delta = dt.timedelta(seconds=20)
    date_now = dt.datetime.now()
    time_now = date_now.time()

    # Добавляем delta к старту задачи(погрешность на работу скрипта)
    start_time = (dt.datetime.combine(dt.date(1, 1, 1), task['time_start']) + delta).time()

    # Проверяем возможен ли запуск выполнения задачи в текущее время
    end_time = task['time_finish']
    if start_time < end_time:
        is_working_hours = (start_time <= time_now <= end_time)
    else:
        is_working_hours = (time_now <= end_time or time_now >= start_time)
    return is_working_hours


def monitor_tasks():
    """
    Проверяем регулярность запуска задач
    """
    # Получаем задачи из Google Таблицы
    tasks = wk_g.get_tasks()

    # Проверяем нарушения время запуска задач
    list_alert = check_time_interval(tasks)

    # Отправляем уведомления о тревоге в телеграмм
    if list_alert:
        notif_alert(list_alert)

    # Записываем время выполнения в Google таблицу
    time_end = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    wk_g.set_tasks_last_start(6, time_end)


if __name__ == "__main__":
    logger.info("Начало")
    monitor_tasks()
    logger.info("Работа программы завершена")

