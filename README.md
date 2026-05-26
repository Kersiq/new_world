# Payment Service

Асинхронный микросервис процессинга платежей с эмуляцией внешнего шлюза, retry-механикой через RabbitMQ DLX и доставкой webhook-уведомлений через transactional outbox.

## Стек

- Python 3.12, FastAPI, FastStream (RabbitMQ)
- PostgreSQL 17, SQLAlchemy 2.0 async, Alembic
- APScheduler (cron jobs)
- Dishka (DI)
- Docker Compose

## Архитектура

```
POST /payments          --> outbox (PAYMENT)
scheduler (cron 1 min)  --> publish to payments.new
payment-consumer        --> emulate gateway (2-5s, 90/10) --> update status + outbox (WEBHOOK_DELIVERY)
scheduler (cron 1 min)  --> httpx POST на webhook_url (3 попытки, exp backoff)
```

Retry-механика на стороне RMQ: `payments.new` → DLX → `payments.retry` (TTL) → DLX → `payments.new`. После `max_retries` сообщение уходит в `payments.dlq`.

## Запуск

1. Скопировать пример env-файла и заполнить значения:

   ```bash
   cp .env.example .env
   ```

   Заполнить переменные внутри `.env` (см. таблицу ниже).

2. **Перед первым запуском** включить volume для Postgres и RabbitMQ в `docker-compose.yml` — раскомментировать секции:

   ```yaml
   #volumes:
   #  - ./db_data:/var/lib/postgresql/data
   ```

   и

   ```yaml
   #volumes:
   #  - ./rabbitmq_data:/var/lib/rabbitmq
   ```

   Без этого данные пропадут при пересоздании контейнеров.

3. Поднять стек:

   ```bash
   docker compose up --build
   ```

   Миграции применятся автоматически при старте `backend`.

## Переменные окружения

| Переменная             | Назначение                              |
|------------------------|------------------------------------------|
| `COMPOSE_PROJECT_NAME` | Префикс для имён контейнеров            |
| `DB__HOST`             | Хост Postgres (внутри сети — `postgres`) |
| `DB__PORT`             | Порт Postgres                            |
| `DB__USERNAME`         | Пользователь БД                          |
| `DB__PASSWORD`         | Пароль БД                                |
| `DB__DB_NAME`          | Имя БД                                   |
| `RABBIT__HOST`         | Хост RabbitMQ (внутри сети — `rabbitmq`) |
| `RABBIT__PORT`         | AMQP-порт                                |
| `RABBIT__USERNAME`     | Пользователь RMQ                         |
| `RABBIT__PASSWORD`     | Пароль RMQ                               |
| `RABBIT__VHOST`        | Virtual host RMQ                         |
| `WEB__API_KEY`         | Ключ для заголовка `X-API-Key`           |

## Эндпоинты

- `POST /api/v1/payments` — создать платёж (требует `Idempotency-Key` и `X-API-Key`)
- `GET /api/v1/payments/{id}` — получить статус платежа

## Порты на хосте

- `8080` — backend (FastAPI)
- `5672` — RabbitMQ AMQP
- `15672` — RabbitMQ management UI (`guest`/`guest` по умолчанию)
