import asyncio
from datetime import datetime
import json
import urllib.request  # Import the entire urllib.request module
from urllib.error import URLError, HTTPError

from sqlalchemy import func, update, select
from app.utils import translate
from app.models import TranslationRequest
from sqlmodel.ext.asyncio.session import AsyncSession


def send_webhook_notification(request_id, translated_text, webhook_url: str):
    # Prepare data for the webhook payload
    data = json.dumps(
        {"request_id": request_id, "translated_text": translated_text}
    ).encode("utf-8")

    try:
        with urllib.request.urlopen(webhook_url, data=data) as response:
            response_data = response.read()
            print(
                f"Webhook notification sent successfully (request ID: {request_id}). Response: {response_data.decode()}"
            )

    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"Error sending webhook notification: {e}")


async def translate_in_background(id, rich_text, db: AsyncSession):
    # Simulate translation process (replace with actual API call to Gemini LLM)
    import time

    result = await db.get(TranslationRequest, id)
    print(result)
    if result is None:
        print(f"Translation request with id {id} not found")
        return
    translated_text = translate(
        result.rich_text, result.source_language, result.target_language
    )
    # Simulate translation time (replace with actual translation)
    # translated_text = f"Translation of '{result.rich_text}'"  # Replace with actual translation
    if translated_text["status"] == "error":
        try:
            stmt = (
                update(TranslationRequest)
                .where(TranslationRequest.id == id)
                .values(
                    {
                        TranslationRequest.status: "error",
                        TranslationRequest.translated_text: translated_text[
                            "translated_text"
                        ],
                        TranslationRequest.updated_at: datetime.utcnow(),
                    }
                )
            )
            await db.execute(stmt)
            await db.commit()
            send_webhook_notification(
                result.request_id,
                translated_text["translated_text"],
                result.callback_url,
            )

        # Update the request with translated text and status

        except Exception as e:
            print(f"Error updating translation request: {e}")
    else:
        try:
            stmt = (
                update(TranslationRequest)
                .where(TranslationRequest.id == id)
                .values(
                    {
                        TranslationRequest.status: "complete",
                        TranslationRequest.translated_text: translated_text[
                            "translated_text"
                        ],
                        TranslationRequest.updated_at: datetime.utcnow(),
                        TranslationRequest.token_count: translated_text["token_count"],
                    }
                )
            )
            await db.execute(stmt)
            await db.commit()
            send_webhook_notification(
                result.request_id,
                translated_text["translated_text"],
                result.callback_url,
            )

        # Update the request with translated text and status

        except Exception as e:
            print(f"Error updating translation request: {e}")
