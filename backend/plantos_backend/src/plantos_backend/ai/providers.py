"""AI Provider abstractions."""
from __future__ import annotations

from typing import Protocol

from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from plantos_backend.settings import get_settings


class AIProvider(Protocol):
    """Protocol for AI providers."""

    def get_chat_model(self, model_name: str | None = None) -> BaseChatModel:
        """Get a chat model instance."""
        ...


class OpenAIProvider:
    """OpenAI provider implementation."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_chat_model(self, model_name: str | None = None) -> BaseChatModel:
        return ChatOpenAI(
            api_key=self.api_key,
            model=model_name or "gpt-4o",
            temperature=0,
        )


class GeminiProvider:
    """Google Gemini provider implementation."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_chat_model(self, model_name: str | None = None) -> BaseChatModel:
        return ChatGoogleGenerativeAI(
            google_api_key=self.api_key,
            model=model_name or "gemini-1.5-flash",
            temperature=0,
        )


def get_provider(name: str | None = None) -> AIProvider:
    """Factory to get the configured AI provider."""
    settings = get_settings()
    provider_name = (name or settings.default_ai_provider).lower()

    if provider_name == "openai":
        if not settings.openai_api_key:
            raise ValueError("PLANTOS_OPENAI_API_KEY is not set")
        return OpenAIProvider(settings.openai_api_key)
    
    if provider_name == "gemini":
        if not settings.gemini_api_key:
            raise ValueError("PLANTOS_GEMINI_API_KEY is not set")
        return GeminiProvider(settings.gemini_api_key)

    raise ValueError(f"Unknown AI provider: {provider_name}")
