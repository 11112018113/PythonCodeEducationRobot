from agents.base import BaseAgent, AgentConfig
from core.message import AgentMessage, MessageType, TaskType
from core.router import IntentRouter, Intent
from core.safety import SafetyFilter
from models.loader import model_loader
from pydantic import Field
from typing import Optional


class CoordinatorConfig(AgentConfig):
    name: str = "coordinator"
    system_prompt: str = """You are the coordinator for a child-friendly
educational robot. Your job is to:
1. Detect the child's age group
2. Route requests to the right agent
3. Ensure safety of all interactions"""


class CoordinatorAgent(BaseAgent):
    def __init__(self, config: CoordinatorConfig):
        super().__init__(config)
        self.router = IntentRouter()
        self.safety = SafetyFilter()

    async def initialize(self):
        result = model_loader.load_model(
            self.name,
            self.config.model_path
        )
        if result.success:
            self.is_ready = True

    async def process_task(self, message: AgentMessage) -> AgentMessage:
        user_text = message.payload.get("text", "")

        safety_result = self.safety.check(user_text)
        if not safety_result.allowed:
            return AgentMessage(
                from_agent=self.name,
                to_agent=message.from_agent,
                message_type=MessageType.ERROR,
                payload={"error": "Content not allowed", "reason": safety_result.reason},
                context=message.context
            )

        routing = self.router.route(user_text)
        target_agent = routing.agent_name
        age_group = self.safety.categorize_age_group(user_text)

        forwarded = AgentMessage(
            from_agent=self.name,
            to_agent=target_agent,
            message_type=MessageType.TASK,
            task_type=TaskType(routing.intent.value),
            payload={
                "text": user_text,
                "age_group": age_group,
                "safety_level": safety_result.safety_level.value
            },
            context=message.context
        )
        return forwarded