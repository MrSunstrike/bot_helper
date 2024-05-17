import logging
from http import HTTPStatus

import requests
from creds import get_iam_token
from config import LOGS, FOLDER_ID, STT_TOPIC, LANGUAGE, STT_URL, TTS_VOICE, TTS_URL

logging.basicConfig(
    filename=LOGS, level=logging.ERROR,
    format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="w"
)


def speech_to_text(data: bytes) -> tuple[bool, str]:
    iam_token = get_iam_token()
    params = {
        "topic": STT_TOPIC,
        "folderId": FOLDER_ID,
        "lang": LANGUAGE,
    }
    headers = {
        "Authorization": f"Bearer {iam_token}",
    }

    response = requests.post(url=STT_URL, headers=headers, data=data, params=params)

    decoded_data = response.json()

    if decoded_data.get("error_code") is None:
        return True, decoded_data.get("result")

    else:
        return False, "При запросе в SpeechKit возникла ошибка"


def text_to_speech(text: str) -> tuple[bool, str | bytes]:
    iam_token = get_iam_token()
    headers = {
        "Authorization": f"Bearer {iam_token}",
    }
    data = {
        "text": text,
        "lang": LANGUAGE,
        "voice": TTS_VOICE,
        "folderId": FOLDER_ID,
    }

    response = requests.post(url=TTS_URL, headers=headers, data=data)

    if response.status_code == HTTPStatus.OK:
        return True, response.content

    else:
        return False, "При запросе в SpeechKit возникла ошибка"
