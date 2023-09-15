# Telegram Account Bot

Этот репозиторий содержит Telegram-бота, который продаёт аккаунты. Бот создан с использованием Telegram Bot API и написан на языке Python.

## Функциональность

- Продажа аккаунтов через Telegram
- Приём платежей через различные платёжные шлюзы
- Управление инвентарём
- Предоставление поддержки пользователей через чат
- Генерация отчётов о транзакциях

## Установка

1. Клонируйте репозиторий:

    <pre>git clone https://github.com/wwaannttyy/payments.git<pre>

2. Установите необходимые зависимости:

    <pre>pip install -r requirements.txt<pre>

3. Настройте файл конфигурации:

Переименуйте файл config.example.ini в config.ini и обновите следующие параметры:

- token: Токен Telegram Bot API
- payment_gateway: Токен платёжного шлюза API
- inventory_file: Путь к файлу инвентаря

4. Запустите бота:

    <pre>python bot.py<pre>

## Использование

После запуска бота вы можете взаимодействовать с ним через Telegram. Начните чат с ботом и используйте следующие команды:

- /start - Запустить бота и отобразить доступные команды
- /inventory - Просмотреть доступные аккаунты для продажи
- /buy <account_id> - Купить определенный аккаунт
- /support - Связаться с поддержкой
- /report - Сгенерировать отчёт о транзакциях

## Внесение изменений

Внести изменения всегда можно! Если у вас есть какие-либо идеи или улучшения, не стесняйтесь создавать issue или отправлять pull request.

## Лицензия

Этот проект распространяется под лицензией MIT License.
