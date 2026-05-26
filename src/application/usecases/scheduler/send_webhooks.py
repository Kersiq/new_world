import asyncio
import logging
from datetime import datetime, timedelta, UTC

import httpx

from src.application.interfaces.outbox_table import IOutboxRepo
from src.core.enums import OutboxEventTypes
from src.entities.outbox_table import OutboxEntity

logger = logging.getLogger(__name__)

MAX_ATTEMPTS = 3
HTTP_TIMEOUT_S = 5.0


class SendWebhooksUseCase:
    def __init__(self, outbox_repo: IOutboxRepo) -> None:
        self.outbox_repo = outbox_repo

    async def execute(self) -> None:
        pending = await self.outbox_repo.get_pending(OutboxEventTypes.WEBHOOK_DELIVERY)
        if not pending:
            logger.info("No pending webhook deliveries")
            return

        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT_S) as client:
            sent_ids: list[int] = []
            for task in pending:
                ok, error = await self._deliver(client, task)
                if ok:
                    sent_ids.append(task.id)
                    continue
                next_attempt = task.attempts + 1
                if next_attempt >= MAX_ATTEMPTS:
                    await self.outbox_repo.mark_as_failed(task.id, error)
                    logger.warning("Webhook %s exhausted retries: %s", task.id, error)
                else:
                    backoff_s = 2 ** next_attempt
                    next_retry_at = datetime.now(UTC) + timedelta(seconds=backoff_s)
                    await self.outbox_repo.increment_attempt(task.id, error, next_retry_at)
                    logger.info(
                        "Webhook %s failed, retry %s in %ss: %s",
                        task.id, next_attempt, backoff_s, error,
                    )

        if sent_ids:
            await self.outbox_repo.mark_as_sent(sent_ids)
            logger.info("Delivered %s webhooks", len(sent_ids))

    @staticmethod
    async def _deliver(client: httpx.AsyncClient, task: OutboxEntity) -> tuple[bool, str]:
        url = task.payload.get("webhook_url")
        if not url:
            return False, "missing webhook_url in payload"
        body = {
            "payment_id": task.payload.get("payment_id"),
            "status": task.payload.get("status"),
            "processed_at": task.payload.get("processed_at"),
        }
        try:
            response = await client.post(url, json=body)
            if 200 <= response.status_code < 300:
                return True, ""
            return False, f"http {response.status_code}: {response.text[:200]}"
        except httpx.HTTPError as e:
            return False, f"{type(e).__name__}: {e}"
        except asyncio.CancelledError:
            raise
        except Exception as e:
            return False, f"unexpected {type(e).__name__}: {e}"
