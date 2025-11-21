from fastapi import HTTPException
from openai import OpenAI

from app.core.config import settings


def get_boson_client() -> OpenAI:
    """Centralized Boson AI client factory"""
    if not settings.BOSON_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="BOSON_API_KEY not configured. Please set it in environment variables."
        )
    return OpenAI(
        api_key=settings.BOSON_API_KEY,
        base_url="https://api.boson.ai/v1"
    )
