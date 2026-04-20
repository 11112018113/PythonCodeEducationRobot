from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    coordinator_model_path: str = "/app/models/coordinator_rkllm"
    chat_model_path: str = "/app/models/chat_rkllm"
    story_model_path: str = "/app/models/story_rkllm"
    learn_model_path: str = "/app/models/learn_rkllm"

    dev_coordinator_model: str = "Qwen/Qwen2.5-1.5B-Instruct-GGUF"
    dev_chat_model: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0-GGUF"
    dev_story_model: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0-GGUF"
    dev_learn_model: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0-GGUF"

    # Runtime settings
    max_tokens: int = 256
    temperature: float = 0.7

    # Safety
    enable_safety_filter: bool = True

    # Age groups
    age_groups: list[str] = ["toddler", "early", "school"]

    # Development mode (use GGUF instead of RKLLM)
    dev_mode: bool = True

    class Config:
        env_prefix = "FAMILYBOT_"


settings = Settings()