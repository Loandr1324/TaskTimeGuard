import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN_BOT
from loguru import logger
import time

"""
Ссылка на документацию по html форматированию сообщения в телеграмм
https://core.telegram.org/bots/api#html-style
"""


class NotifTelegram:
    def __init__(self):
        self.TOKEN = TOKEN_BOT
        self.message = dict.fromkeys(['text', 'keyboard'])
        self.count_msg = 0

    def message_alert(self, task: dict):
        """
        Формируем сообщение для уведомления менеджеров при отмене позиций поставщиком
        :param task:
            Словарь с ключами:
                'task_id': str or int,
                'task_name': str,
                'task_last_start': datetime.datetime(%Y, %m, %d, %H, %M, %S'),
                'time_interval': int,
                'task_delta_interval': int
        return: dict {
            'text': текст сообщения: str
            'keyboard: клавиатура к сообщению: str'
            };
        """
        row1 = "‼️<b>                    ТРЕВОГА                       </b>‼️\n\n"
        row2 = "Превышено время запуска модуля:\n"
        row3 = f'<code>{task["task_name"]}</code>\n'
        row4 = f'Последний запуск модуля: <code>{task["task_last_start"]}</code>\n'
        row5 = f'Интервал между запусками (сек): <code>{task["task_delta_interval"]}</code>\n'
        row6 = f'<b>Допустимый интервал между запусками (сек):</b> <code>{task["time_interval"]}</code>\n'
        self.message['text'] = row1 + row2 + row3 + row4 + row5 + row6

        # Создаём клавиатуру для сообщения
        # self.message['keyboard'] = InlineKeyboardMarkup(inline_keyboard=[
        #     [InlineKeyboardButton(text="Перейти к заказу", url=url_order)],
        # ])

    def send_massage_chat(self, chat_id: str) -> bool:
        """Отправляем полученное сообщение в чат бот"""
        logger.info(chat_id)

        telegram_bot = telepot.Bot(self.TOKEN)
        try:
            telegram_bot.sendMessage(
                chat_id, self.message['text'],
                parse_mode="HTML",
                reply_markup=self.message['keyboard'],
                disable_web_page_preview=True)

            self.count_msg += 1
            if self.count_msg == 19:
                logger.warning(f"Отправлено {self.count_msg} сообщений в телеграм. Делаем паузу 60 сек...")
                time.sleep(60)
                self.count_msg = 0
            return True
        except Exception as e:
            logger.error('Отправка уведомления в телеграм была неудачна. Описание ошибки:')
            logger.error(e)
            return False
