import asyncio
from agents.coordinator import CoordinatorAgent, CoordinatorConfig
from agents.chat import ChatAgent, ChatAgentConfig
from agents.story import StoryAgent, StoryAgentConfig
from agents.learn import LearnAgent, LearnAgentConfig
from agents.registry import registry
from core.message import AgentMessage, MessageType
from config.settings import settings


class FamilyBot:
    def __init__(self):
        self.coordinator = CoordinatorAgent(
            CoordinatorConfig(
                name="coordinator",
                model_path=settings.coordinator_model_path,
            )
        )
        self.chat_agent = ChatAgent(
            ChatAgentConfig(
                name="chat_agent",
                model_path=settings.chat_model_path,
            )
        )
        self.story_agent = StoryAgent(
            StoryAgentConfig(
                name="story_agent",
                model_path=settings.story_model_path,
            )
        )
        self.learn_agent = LearnAgent(
            LearnAgentConfig(
                name="learn_agent",
                model_path=settings.learn_model_path,
            )
        )

    async def initialize(self):
        registry.register(self.coordinator)
        registry.register(self.chat_agent)
        registry.register(self.story_agent)
        registry.register(self.learn_agent)
        await self.coordinator.initialize()
        await self.chat_agent.initialize()
        await self.story_agent.initialize()
        await self.learn_agent.initialize()

    async def shutdown(self):
        await self.coordinator.shutdown()
        await self.chat_agent.shutdown()
        await self.story_agent.shutdown()
        await self.learn_agent.shutdown()
        registry.clear()

    async def process_message(self, text: str, session_id: str = "default") -> AgentMessage:
        message = AgentMessage(
            from_agent="user",
            to_agent="coordinator",
            message_type=MessageType.TASK,
            payload={"text": text},
            context={"session_id": session_id}
        )

        routed = await self.coordinator.process_task(message)

        agent = registry.get(routed.to_agent)
        if agent:
            result = await agent.process_task(routed)
            return result

        return AgentMessage(
            from_agent="coordinator",
            to_agent="user",
            message_type=MessageType.ERROR,
            payload={"error": "Agent not found"}
        )


async def main():
    bot = FamilyBot()
    await bot.initialize()
    print("FamilyBot ready! Type 'quit' to exit.")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit']:
            break
        response = await bot.process_message(user_input)
        print(f"Bot: {response.payload.get('response', 'Error')}")
    await bot.shutdown()


if __name__ == "__main__":
    asyncio.run(main())