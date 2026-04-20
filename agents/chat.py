from agents.base import BaseAgent, AgentConfig
from core.message import AgentMessage, TaskType
from models.loader import model_loader
from pydantic import Field
import asyncio


class ChatAgentConfig(AgentConfig):
    name: str = "chat_agent"
    system_prompt: str = """You are a friendly, educational robot companion for children.
Be kind, patient, and encouraging. Use simple language.
Always be safe and appropriate."""


class ChatAgent(BaseAgent):
    def __init__(self, config: ChatAgentConfig):
        super().__init__(config)
        self.system_prompt = config.system_prompt

    async def initialize(self):
        result = model_loader.load_model(
            self.name,
            self.config.model_path
        )
        if result.success:
            self.is_ready = True

    async def process_task(self, message: AgentMessage) -> AgentMessage:
        user_text = message.payload.get("text", "")
        age_group = message.payload.get("age_group", "early")

        prompt = self._build_prompt(user_text, age_group)

        result = await model_loader.generate(
            self.name,
            prompt,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )

        response = AgentMessage(
            from_agent=self.name,
            to_agent=message.from_agent,
            message_type="result",
            task_type=TaskType.CHAT,
            payload={
                "response": result.output or "I'm here to chat!",
                "age_group": age_group
            },
            context=message.context
        )
        return response

    def _build_prompt(self, user_text: str, age_group: str) -> str:
        age_instructions = {
            "toddler": "Use very short sentences (2-5 words). Be gentle.",
            "early": "Use simple sentences. Be encouraging.",
            "school": "Use age-appropriate vocabulary. Be engaging."
        }
        instruction = age_instructions.get(age_group, age_instructions["early"])
        return f"""System: {self.system_prompt}

Age adaptation: {instruction}

User: {user_text}

Robot:"""