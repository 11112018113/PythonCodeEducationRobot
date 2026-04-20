"""Speech-to-Text module using Whisper.cpp for edge deployment."""
import asyncio
from typing import Optional
import subprocess
import os


class SpeechToText:
    def __init__(self, model_path: str = "base"):
        self.model_path = model_path
        self.model_loaded = False

    async def initialize(self):
        self.model_loaded = True

    async def transcribe(self, audio_path: str) -> str:
        if not self.model_loaded:
            await self.initialize()

        if not os.path.exists(audio_path):
            return ""

        result = subprocess.run(
            ["whisper.cpp/main", "-m", f"whisper.cpp/models/ggml-{self.model_path}.bin",
             "-f", audio_path, "--no-timestamps"],
            capture_output=True,
            text=True
        )

        return result.stdout.strip()

    async def listen(self, duration: int = 5) -> str:
        return "Mock: child said hello"

    def is_ready(self) -> bool:
        return self.model_loaded
