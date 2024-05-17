from http import HTTPStatus

import requests
import logging
from config import LOGS, MAX_GPT_TOKENS, SYSTEM_PROMPT, FOLDER_ID, YAGPT_MODEL, YAGPT_URL, YAGPT_TOKEN_COUNTS_URL, \
    YAGPT_STREAM_CONFIG, YAGPT_TEMPERATURE_CONFIG
from creds import get_iam_token


logging.basicConfig(
    filename=LOGS, level=logging.ERROR,
    format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="w"
)


def count_gpt_tokens(messages: list[dict]):
    iam_token = get_iam_token()

    headers = {
        "Authorization": f"Bearer {iam_token}",
        "Content-Type": "application/json"
    }
    data = {
        "modelUri": f"gpt://{FOLDER_ID}/{YAGPT_MODEL}",
        "messages": messages
    }

    try:
        return len(requests.post(url=YAGPT_TOKEN_COUNTS_URL, json=data, headers=headers).json()["tokens"])

    except Exception as e:
        logging.error(e)
        return 0


def ask_gpt(messages: list[dict[str, str | int]]) -> tuple[bool, str, int]:
    iam_token = get_iam_token()

    headers = {
        "Authorization": f"Bearer {iam_token}",
        "Content-Type": "application/json"
    }
    data = {
        "modelUri": f"gpt://{FOLDER_ID}/{YAGPT_MODEL}",
        "completionOptions": {
            "stream": YAGPT_STREAM_CONFIG,
            "temperature": YAGPT_TEMPERATURE_CONFIG,
            "maxTokens": MAX_GPT_TOKENS
        },
        "messages": SYSTEM_PROMPT + messages
    }

    try:
        response = requests.post(YAGPT_URL, headers=headers, json=data)

        if response.status_code != HTTPStatus.OK:
            return False, f"Ошибка GPT. Статус-код: {response.status_code}", 0

        answer = response.json()["result"]["alternatives"][0]["message"]["text"]

        tokens_in_answer = count_gpt_tokens([{"role": "assistant", "text": answer}])

        return True, answer, tokens_in_answer

    except Exception as e:
        logging.error(e)
        return False, "Ошибка при обращении к GPT",  0
