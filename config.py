from dotenv import load_dotenv
from os import getenv

load_dotenv()

# Лимиты
MAX_USERS = 3
MAX_GPT_TOKENS = 120
MAX_USER_STT_BLOCKS = 10
MAX_USER_TTS_SYMBOLS = 5_000
MAX_USER_GPT_TOKENS = 2_000

# Настройки YaGPT
YAGPT_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
YAGPT_TOKEN_COUNTS_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/tokenizeCompletion"
YAGPT_MODEL = "yandexgpt-lite"
YAGPT_STREAM_CONFIG = False
YAGPT_TEMPERATURE_CONFIG = 0.7
COUNT_LAST_MSG = 4
SYSTEM_PROMPT = [
    {
        "role": "system",
        "text": "Ты дружелюбный помощник по имени Ботя. Отвечай на вопросы дружелюбно и используй в ответах мемы."
    }
]

# Настройки SpeechKit
STT_URL = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize"
STT_TOPIC = "general"

TTS_URL = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"
TTS_VOICE = "ermil"

LANGUAGE = "ru-RU"

# Система
LOGS = "logs/logs.txt"
DB_FILE = "db.sqlite"
IAM_ENDPOINT = "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token"
ADMINS_IDS = [786540182]


# Токены
IAM_TOKEN_PATH = "creds/iam_token.txt"
FOLDER_ID = getenv("FOLDER_ID")
BOT_TOKEN = getenv("BOT_TOKEN")

