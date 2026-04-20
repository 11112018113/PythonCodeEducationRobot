"""Story Agent - Interactive storytelling with age-appropriate narratives."""
from agents.base import BaseAgent, AgentConfig
from core.message import AgentMessage, MessageType, TaskType
from pydantic import Field
from typing import Optional, List, Dict
import json
import random


class StoryAgentConfig(AgentConfig):
    name: str = "story_agent"
    system_prompt: str = """You are a creative storyteller for children.
Generate engaging, age-appropriate stories with educational themes.
Always use simple language for younger children."""


class StoryAgent(BaseAgent):
    """Agent for generating interactive stories."""

    def __init__(self, config: StoryAgentConfig):
        super().__init__(config)
        self.story_templates = self._load_templates()
        self.current_story: Optional[Dict] = None

    def _load_templates(self) -> Dict:
        """Load story templates by age group."""
        return {
            "toddler": [
                {"theme": "animal", "template": "Once upon a time, there was a {animal} who loved to {action}."},
                {"theme": "bedtime", "template": "The little {animal} was very sleepy. {story}..."},
            ],
            "early": [
                {"theme": "adventure", "template": "One sunny day, {character} discovered a {discovery}. {adventure}"},
                {"theme": "friendship", "template": "{character} made a new friend. Their name was {friend}. {lesson}"},
            ],
            "school": [
                {"theme": "mystery", "template": "The class had a mystery. {clue1} led to {clue2}. {resolution}"},
                {"theme": "science", "template": "Today we learn about {topic}. {experiment}! {discovery}"},
            ],
        }

    async def initialize(self):
        """Initialize the story agent."""
        from models.loader import model_loader
        result = model_loader.load_model(self.name, self.config.model_path)
        if result.success:
            self.is_ready = True

    async def process_task(self, message: AgentMessage) -> AgentMessage:
        """Process storytelling request."""
        payload = message.payload
        age_group = payload.get("age_group", "early")
        topic = payload.get("topic", "adventure")
        interactive = payload.get("interactive", False)
        length = payload.get("length", "medium")
        story = self._generate_story(age_group, topic, length, interactive)

        self.current_story = {
            "age_group": age_group,
            "topic": topic,
            "story": story,
            "interactive": interactive,
        }

        return AgentMessage(
            from_agent=self.name,
            to_agent=message.from_agent,
            message_type=MessageType.RESPONSE,
            payload={
                "story": story,
                "topic": topic,
                "age_group": age_group,
                "interactive": interactive,
                "has_choices": interactive,
            },
            context=message.context,
        )

    def _generate_story(self, age_group: str, topic: str, length: str, interactive: bool) -> str:
        """Generate a story based on parameters."""
        templates = self.story_templates.get(age_group, self.story_templates["early"])

        matching = [t for t in templates if t["theme"] == topic]
        template = random.choice(matching) if matching else random.choice(templates)

        if age_group == "toddler":
            words = 50 if length == "short" else 100
            return self._simple_story(template, words)
        elif age_group == "early":
            words = 100 if length == "short" else 200
            return self._adventure_story(template, words)
        else:
            words = 150 if length == "short" else 300
            return self._complex_story(template, words)

    def _simple_story(self, template: Dict, word_count: int) -> str:
        """Generate simple story for toddlers."""
        animals = ["bear", "rabbit", "cat", "dog", "bird"]
        actions = ["play", "sleep", "eat", "dance", "sing"]

        story = template["template"].format(
            animal=random.choice(animals),
            action=random.choice(actions),
        )
        return story + " The end! 🌟"

    def _adventure_story(self, template: Dict, word_count: int) -> str:
        """Generate adventure story for early childhood."""
        story = template["template"].format(
            character="Lily",
            discovery="mysterious cave",
            adventure="Inside, she found glowing crystals!",
            lesson="They learned to be brave together.",
        )
        return story + " 🌈"

    def _complex_story(self, template: Dict, word_count: int) -> str:
        """Generate complex story for school age."""
        if template["theme"] == "mystery":
            story = template["template"].format(
                clue1="A mysterious footprint",
                clue2="a hidden key",
                resolution="The mystery was solved!",
            )
        else:
            story = template["template"].format(
                topic="plants",
                experiment="We planted a seed and watched it grow",
                discovery="Plants need sunlight and water!",
            )
        return story + " 📚"

    async def handle_interaction(self, choice: str) -> AgentMessage:
        """Handle interactive story choices."""
        if not self.current_story:
            return AgentMessage(
                from_agent=self.name,
                to_agent="coordinator",
                message_type=MessageType.ERROR,
                payload={"error": "No active story"},
            )

        continuation = f"Then, {choice} happened! What will happen next?"

        return AgentMessage(
            from_agent=self.name,
            to_agent="coordinator",
            message_type=MessageType.RESPONSE,
            payload={
                "continuation": continuation,
                "choices": ["explore", "go home", "meet friend"],
            },
        )
