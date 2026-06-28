from __future__ import annotations

import requests

from config.settings import get_settings


class LLMService:
    def __init__(self, base_url: str | None = None, model_name: str | None = None) -> None:
        settings = get_settings()
        self.base_url = (base_url or settings.ollama_base_url).rstrip("/")
        self.model_name = model_name or settings.ollama_model

    def generate(
            self,
            prompt: str,
            *,
            system_prompt: str | None = None,
            temperature: float = 0.2,
            timeout: int = 60
    ) -> str:
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("prompt must be a non-empty string")
        
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
            }
        }

        if system_prompt:
            payload["system"] = system_prompt

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=timeout
        )
        response.raise_for_status()

        data = response.json()
        if not isinstance(data, dict):
            raise RuntimeError("Invalid response from Ollama")

        generated_text = data.get("response", "")
        if not isinstance(generated_text, str):
            raise RuntimeError("Invalid response format from Ollama")
        
        return generated_text