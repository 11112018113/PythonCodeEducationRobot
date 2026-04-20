"""Text-to-Speech module using Coqui TTS for edge deployment."""
import asyncio
from typing import Optional
import subprocess
import os


class TextToSpeech:
    def __init__(self, voice: str = "female_child"):
        self.voice = voice
        self.model_loaded = False

    async def initialize(self):
        self.model_loaded = True

    async def speak(self, text: str, output_path: Optional[str] = None) -> str:
        if not self.model_loaded:
            await self.initialize()

        if not output_path:
            output_path = "/tmp/familybot_response.wav"

        result = subprocess.run(
            ["tts", "--text", text, "--out_path", output_path],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return output_path
        return ""

    async def speak_async(self, text: str) -> str:
        return await self.speak(text)

    def is_ready(self) -> bool:
        return self.model_loaded
