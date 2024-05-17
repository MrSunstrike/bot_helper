import logging

from config import LOGS, MAX_USERS, MAX_USER_STT_BLOCKS, MAX_USER_GPT_TOKENS, MAX_USER_TTS_SYMBOLS
from database import count_users, count_all_limits
from yandex_gpt import count_gpt_tokens


logging.basicConfig(
    filename=LOGS, level=logging.ERROR,
    format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="w"
)


def check_number_of_users(user_id: int) -> tuple[bool, str]:
    count: int = count_users(user_id)

    if count is None:
        return False, "Ошибка при работе с БД"

    if count >= MAX_USERS:
        return False, "Превышено максимальное количество пользователей"

    return True, ""


def is_gpt_token_limit(messages, total_spent_tokens) -> tuple[int, str]:
    all_tokens: int = count_gpt_tokens(messages) + total_spent_tokens

    if all_tokens > MAX_USER_GPT_TOKENS:
        return 0, f"Превышен общий лимит GPT токенов {MAX_USER_GPT_TOKENS}"

    return all_tokens, ""


def is_stt_block_limit(user_id: int, duration: int) -> tuple[int, str]:
    audio_blocks: int = -(-duration // 15)
    all_blocks: int = count_all_limits(user_id, "stt_blocks") + audio_blocks

    if duration >= 30:
        return 0, "SpeechKit STT работает с голосовыми сообщениями меньше 30 секунд"

    if all_blocks > MAX_USER_STT_BLOCKS:
        return 0, f"Превышен общий лимит SpeechKit STT {MAX_USER_STT_BLOCKS}"

    return audio_blocks, ""


def is_tts_symbol_limit(user_id: int, text: str) -> tuple[int, str]:
    text_symbols: int = len(text)
    all_symbols: int = count_all_limits(user_id, "tts_symbols") + text_symbols

    if all_symbols > MAX_USER_TTS_SYMBOLS:
        return 0, f"Превышен общий лимит SpeechKit TTS {MAX_USER_TTS_SYMBOLS}"

    return text_symbols, ""
