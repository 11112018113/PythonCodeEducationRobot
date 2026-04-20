from typing import Dict, List, Optional
from agents.base import BaseAgent


class AgentRegistry:
    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        self._agents[agent.name] = agent

    def unregister(self, name: str) -> None:
        self._agents.pop(name, None)

    def get(self, name: str) -> Optional[BaseAgent]:
        return self._agents.get(name)

    def get_all(self) -> List[BaseAgent]:
        return list(self._agents.values())

    def clear(self) -> None:
        self._agents.clear()


registry = AgentRegistry()