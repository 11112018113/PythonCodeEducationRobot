from dataclasses import dataclass
from typing import Optional, Any
import asyncio


@dataclass
class ModelResult:
    success: bool
    output: Optional[str] = None
    error: Optional[str] = None


class ModelLoader:
    def __init__(self):
        self._loaded_models: dict[str, Any] = {}

    def load_model(self, name: str, model_path: str) -> ModelResult:
        self._loaded_models[name] = {"path": model_path, "ready": True}
        return ModelResult(success=True)

    def is_loaded(self, name: str) -> bool:
        return name in self._loaded_models

    def unload_model(self, name: str):
        self._loaded_models.pop(name, None)

    async def generate(self, model_name: str, prompt: str, **kwargs) -> ModelResult:
        if model_name not in self._loaded_models:
            return ModelResult(success=False, error="Model not loaded")
        return ModelResult(success=True, output="Mock response: " + prompt[:50])


model_loader = ModelLoader()