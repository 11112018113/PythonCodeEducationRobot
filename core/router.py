from enum import Enum
from dataclasses import dataclass


class Intent(str, Enum):
    CHAT = "chat"
    STORY = "story"
    LEARN = "learn"
    SCHEDULE = "schedule"
    UNKNOWN = "unknown"


INTENT_KEYWORDS = {
    Intent.CHAT: ["hello", "hi", "how", "what", "play", "talk"],
    Intent.STORY: ["story", "tell", "adventure", "dragon", "book"],
    Intent.LEARN: ["math", "count", "what is", "quiz", "learn", "spell"],
    Intent.SCHEDULE: ["remind", "time", "schedule", "bedtime", "routine"],
}


@dataclass
class RoutingResult:
    intent: Intent
    confidence: float
    agent_name: str


class IntentRouter:
    def classify(self, text: str) -> Intent:
        text_lower = text.lower()
        scores = {}
        for intent, keywords in INTENT_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            scores[intent] = score

        if not scores or max(scores.values()) == 0:
            return Intent.CHAT

        return max(scores, key=scores.get)

    def route(self, text: str) -> RoutingResult:
        intent = self.classify(text)
        agent_map = {
            Intent.CHAT: "chat_agent",
            Intent.STORY: "story_agent",
            Intent.LEARN: "learn_agent",
            Intent.SCHEDULE: "schedule_agent",
            Intent.UNKNOWN: "chat_agent",
        }
        return RoutingResult(
            intent=intent,
            confidence=0.8,
            agent_name=agent_map.get(intent, "chat_agent")
        )