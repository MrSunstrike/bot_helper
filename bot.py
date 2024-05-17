from telebot import TeleBot
from telebot.types import Message, File

from utils import check_and_create_file
from validators import check_number_of_users, is_stt_block_limit, is_gpt_token_limit, is_tts_symbol_limit
from speechkit import speech_to_text, text_to_speech
from yandex_gpt import ask_gpt
from config import LOGS, COUNT_LAST_MSG, BOT_TOKEN, ADMINS_IDS
from database import create_database, add_message, select_n_last_messages
import logging

bot = TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(message: Message) -> None:
    bot.send_message(
        message.from_user.id,
        "Привет, меня зовут Ботя и я буду тебе помогать!\n"
        "Отправь мне свой вопрос текстом или голосом и я тебе отвечу"
        "/help - расскажу подробнее")


@bot.message_handler(commands=["help"])
def help(message: Message) -> None:
    bot.send_message(
        message.from_user.id,
        "Я отвечаю текстом на письменный вопрос и голосом - на голосовой\n"
        "Чтобы проверить, что всё работает используй следующие команды:\n"
        "/tts - проверка работы синтеза голоса (я постараюсь озвучить то, что ты мне отправишь)\n"
        "/stt - проверка работы распознания голоса (я постараюсь разобрать твой войс и отправлю содержимое текстом)"
    )


@bot.message_handler(commands=["debug"])
def debug(message: Message) -> None:
    if message.from_user.id in ADMINS_IDS:
        with open(LOGS, "rb") as file:
            bot.send_document(message.chat.id, file)


@bot.message_handler(commands=["tts"])
def tts_handler(message: Message) -> None:
    user_id: int = message.from_user.id
    bot.send_message(user_id, "Режим проверки: отправь текстовое сообщение, чтобы я его озвучил!")
    bot.register_next_step_handler(message, tts)


def tts(message: Message) -> None:
    try:
        user_id: int = message.from_user.id
        text: str = message.text

        if message.content_type != "text":
            bot.send_message(user_id, "Отправь текстовое сообщение")
            return tts_handler(message)

        status_check_users: bool
        error_message: str

        status_check_users, error_message = check_number_of_users(user_id)

        if not status_check_users:
            bot.send_message(user_id, error_message)
            return

        tts_symbols: int
        error_message: str

        tts_symbols, error_message = is_tts_symbol_limit(user_id, text)

        if not error_message:
            full_user_message = [text, "user_tts", 0, tts_symbols, 0]

            add_message(user_id=user_id, full_message=full_user_message)

            status: bool
            content: str | bytes

            status, content = text_to_speech(text)

            if status:
                bot.send_voice(user_id, content, reply_to_message_id=message.id)
                return

            else:
                error_message = content

        bot.send_message(user_id, error_message)

    except Exception as e:
        logging.error(e)
        bot.send_message(message.from_user.id, "Не получилось ответить")


@bot.message_handler(commands=["stt"])
def stt_handler(message: Message) -> None:
    user_id: int = message.from_user.id
    bot.send_message(user_id, "Режим проверки: отправь голосовое сообщение, чтобы я его распознал!")
    bot.register_next_step_handler(message, stt)


def stt(message: Message) -> None:
    try:
        user_id: int = message.from_user.id

        if not message.voice:
            bot.send_message(user_id, "Отправь голосовое сообщение")
            return stt_handler(message)

        status_check_users: bool
        error_message: str

        status_check_users, error_message = check_number_of_users(user_id)

        if not status_check_users:
            bot.send_message(user_id, error_message)
            return

        stt_blocks: int
        error_message: str

        stt_blocks, error_message = is_stt_block_limit(user_id, message.voice.duration)

        if error_message:
            bot.send_message(user_id, error_message)
            return

        file_id: str = message.voice.file_id
        file_info: File = bot.get_file(file_id)
        file: bytes = bot.download_file(file_info.file_path)

        status_stt: bool
        stt_text: str

        status_stt, stt_text = speech_to_text(file)

        if not status_stt:
            bot.send_message(user_id, stt_text)
            return

        full_user_message = [stt_text, "user_stt", 0, 0, stt_blocks]
        add_message(user_id=user_id, full_message=full_user_message)

        bot.send_message(user_id, stt_text, reply_to_message_id=message.id)

    except Exception as e:
        logging.error(e)
        bot.send_message(message.from_user.id, "Не получилось ответить")


@bot.message_handler(content_types=["voice"])
def handle_voice(message: Message):
    user_id: int = message.from_user.id

    try:
        status_check_users: bool
        error_message: str

        status_check_users, error_message = check_number_of_users(user_id)

        if not status_check_users:
            bot.send_message(user_id, error_message)
            return

        stt_blocks: int

        stt_blocks, error_message = is_stt_block_limit(user_id, message.voice.duration)

        if error_message:
            bot.send_message(user_id, error_message)
            return

        file_id: str = message.voice.file_id
        file_info: File = bot.get_file(file_id)
        file: bytes = bot.download_file(file_info.file_path)

        status_stt: bool
        stt_text: str

        status_stt, stt_text = speech_to_text(file)

        if not status_stt:
            bot.send_message(user_id, stt_text)
            return

        full_user_message = [stt_text, "user", 0, 0, stt_blocks]
        add_message(user_id=user_id, full_message=full_user_message)

        last_messages: list[dict]
        total_spent_tokens: int

        last_messages, total_spent_tokens = select_n_last_messages(user_id, COUNT_LAST_MSG)

        total_gpt_tokens: int

        total_gpt_tokens, error_message = is_gpt_token_limit(last_messages, total_spent_tokens)

        if error_message:
            bot.send_message(user_id, error_message)
            return

        status_gpt: bool
        answer_gpt: str
        tokens_in_answer: int

        status_gpt, answer_gpt, tokens_in_answer = ask_gpt(last_messages)

        if not status_gpt:
            bot.send_message(user_id, answer_gpt)
            return

        total_gpt_tokens += tokens_in_answer

        tts_symbols: int

        tts_symbols, error_message = is_tts_symbol_limit(user_id, answer_gpt)

        full_gpt_message = [answer_gpt, "assistant", total_gpt_tokens, tts_symbols, 0]
        add_message(user_id=user_id, full_message=full_gpt_message)

        if not error_message:
            status: bool
            content: bytes | str

            status, content = text_to_speech(answer_gpt)

            if status:
                bot.send_voice(user_id, content, reply_to_message_id=message.id)
                return

            error_message = content

        bot.send_message(user_id, error_message)
        bot.send_message(user_id, answer_gpt, reply_to_message_id=message.id)

    except Exception as e:
        logging.error(e)
        bot.send_message(message.from_user.id, "Не получилось ответить. Попробуй записать другое сообщение")


@bot.message_handler(content_types=["text"])
def handle_text(message: Message) -> None:
    user_id = message.from_user.id

    try:
        status_check_users: bool
        error_message: str

        status_check_users, error_message = check_number_of_users(user_id)

        if not status_check_users:
            bot.send_message(user_id, error_message)
            return

        full_user_message = [message.text, "user", 0, 0, 0]
        add_message(user_id=user_id, full_message=full_user_message)

        last_messages: list[dict]
        total_spent_tokens: int

        last_messages, total_spent_tokens = select_n_last_messages(user_id, COUNT_LAST_MSG)

        total_gpt_tokens: int

        total_gpt_tokens, error_message = is_gpt_token_limit(last_messages, total_spent_tokens)

        if error_message:
            bot.send_message(user_id, error_message)
            return

        status_gpt: bool
        answer_gpt: str
        tokens_in_answer: int

        status_gpt, answer_gpt, tokens_in_answer = ask_gpt(last_messages)

        if not status_gpt:
            bot.send_message(user_id, answer_gpt)
            return

        total_gpt_tokens += tokens_in_answer

        full_gpt_message = [answer_gpt, "assistant", total_gpt_tokens, 0, 0]
        add_message(user_id=user_id, full_message=full_gpt_message)

        bot.send_message(user_id, answer_gpt, reply_to_message_id=message.id)

    except Exception as e:
        logging.error(e)
        bot.send_message(message.from_user.id, "Не получилось ответить. Попробуй написать другое сообщение")


@bot.message_handler(func=lambda: True)
def handler(message: Message) -> None:
    bot.send_message(message.from_user.id, "Отправь мне голосовое или текстовое сообщение, и я тебе отвечу")


if __name__ == "__main__":
    check_and_create_file(LOGS)
    logging.basicConfig(
        filename=LOGS, level=logging.ERROR,
        format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="w"
    )
    logging.error("Бот перезапущен")
    create_database()
    bot.infinity_polling()
