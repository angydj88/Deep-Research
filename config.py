"""Configuración centralizada."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # API
    API_KEY = os.getenv("GEMINI_API_KEY", "")
    MODEL = "gemini-3-flash-preview"

    # Generación
    MAX_TOKENS = 8192
    TEMPERATURE = 0.3
    DELAY_BETWEEN_CALLS = 3  # segundos
    MAX_RETRIES = 3

    # App
    VERSION = "5.0"
    REPORTS_DIR = "reports"

    @classmethod
    def validate(cls):
        """Verifica que la configuración sea válida."""
        errors = []
        if not cls.API_KEY:
            errors.append("GEMINI_API_KEY no está configurada")
        if len(cls.API_KEY) < 10:
            errors.append("GEMINI_API_KEY parece inválida")
        return errors
