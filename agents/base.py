from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import Optional
import asyncio


class AgentConfig(BaseModel):
    name: str
    model_path: str
    max_tokens: int = 256
    temperature: float = 0.7


class BaseAgent(ABC):
    def __init__(self, config: AgentConfig):
        self.config = config
        self.name = config.name
        self._model = None
        self.is_ready = False

    @abstractmethod
    async def process_task(self, message: 'AgentMessage') -> 'AgentMessage':
        pass

    async def initialize(self):
        self.is_ready = True

    async def shutdown(self):
        self.is_ready = False

    def __repr__(self):
        return f"<{self.__class__.__name__} name={self.name} ready={self.is_ready}>"
