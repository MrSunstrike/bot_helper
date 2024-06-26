
# «Ботя» - бот помощник

## Описание

Ботя - это телеграм-бот, который помогает пользователям, отвечая на их вопросы как текстом, так и голосом. Он может распознавать голосовые сообщения и преобразовывать текстовые сообщения в речь.

## Функциональность

-   **Текстовые сообщения**: Пользователь отправляет текстовое сообщение, и бот отвечает текстом.
-   **Голосовые сообщения**: Пользователь отправляет голосовое сообщение, бот распознает его и отвечает текстом или голосом.
-   **Команды**:
    -   `/start`: Приветственное сообщение и инструкция по использованию.
    -   `/help`: Подробная информация о функциях бота.
    -   `/tts`: Проверка синтеза голоса. Бот озвучивает отправленный текст.
    -   `/stt`: Проверка распознавания речи. Бот преобразует голосовое сообщение в текст.
    -   `/debug`: Только для администраторов. Отправка логов.

## Установка и настройка

### Предварительные требования

-   Python 3.8+
-   Создайте бота в Telegram и получите токен.

### Установка зависимостей

1.  Склонируйте репозиторий:
    
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
    
2.  Установите зависимости:
    
    ```bash
    pip install -r requirements.txt
    ```
    

### Настройка

1.  Создайте файл `.env` в корне проекта и добавьте следующие переменные:
    
    ```env
    BOT_TOKEN=<ваш_токен_бота>
    FOLDER_ID=<ваш_folder_id>
    ```
    
2.  Убедитесь, что в проекте присутствуют следующие файлы и модули:
    -   `utils.py`
    -   `bot.py`
    -   `validators.py`
    -   `speechkit.py`
    -   `yandex_gpt.py`
    -   `config.py`
    -   `creds.py`
    -   `database.py`
    -   `.env`
    -   `logs`
    -   `requirements.txt`

### Запуск

1.  Проверьте наличие и корректность всех необходимых файлов и модулей.
    
2.  Запустите бота:
    
    ```bash    
    python bot.py
    ``` 

## Логирование

Логи записываются в файл, указанный в переменной `LOGS`. Формат логов:

```
%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s
```

## Примеры использования

1.  Отправьте команду `/start`, чтобы начать общение с ботом.
2.  Используйте команду `/help` для получения информации о возможностях бота.
3.  Отправьте текстовое сообщение, чтобы получить ответ в текстовом виде.
4.  Отправьте голосовое сообщение, чтобы получить текстовую расшифровку или ответ в виде голосового сообщения.

## Ссылка в Telegram

Бот зарегистрирован в телеграме: [Ботя](https://t.me/Fivi123123_bot)