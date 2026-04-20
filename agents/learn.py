"""Learn Agent - Math, reading, and science exercises with adaptive difficulty."""
from agents.base import BaseAgent, AgentConfig
from core.message import AgentMessage, MessageType, TaskType
from pydantic import Field
from typing import Optional, Dict, List
import random


class LearnAgentConfig(AgentConfig):
    name: str = "learn_agent"
    system_prompt: str = """You are a patient, encouraging teacher for children.
Make learning fun with games and positive reinforcement.
Adapt difficulty based on the child's performance."""


class LearnAgent(BaseAgent):
    """Agent for educational exercises."""

    def __init__(self, config: LearnAgentConfig):
        super().__init__(config)
        self.progress: Dict[str, int] = {}
        self.current_quiz: Optional[Dict] = None

    async def initialize(self):
        from models.loader import model_loader
        result = model_loader.load_model(self.name, self.config.model_path)
        if result.success:
            self.is_ready = True

    async def process_task(self, message: AgentMessage) -> AgentMessage:
        payload = message.payload
        subject = payload.get("subject", "math")
        age_group = payload.get("age_group", "early")
        difficulty = payload.get("difficulty", 1)
        action = payload.get("action", "new")

        if action == "answer":
            return await self._check_answer(message)
        elif action == "hint":
            return await self._give_hint()
        else:
            return await self._generate_exercise(subject, age_group, difficulty)

    async def _generate_exercise(self, subject: str, age_group: str, difficulty: int) -> AgentMessage:
        """Generate a new exercise."""
        if subject == "math":
            exercise = self._math_exercise(age_group, difficulty)
        elif subject == "reading":
            exercise = self._reading_exercise(age_group, difficulty)
        elif subject == "science":
            exercise = self._science_exercise(age_group, difficulty)
        else:
            exercise = self._math_exercise(age_group, difficulty)

        self.current_quiz = exercise

        return AgentMessage(
            from_agent=self.name,
            to_agent=message.from_agent,
            message_type=MessageType.RESPONSE,
            payload={
                "exercise": exercise,
                "subject": subject,
                "difficulty": difficulty,
            },
            context=message.context,
        )

    def _math_exercise(self, age_group: str, difficulty: int) -> Dict:
        """Generate math exercise."""
        if difficulty == 1:
            a, b = random.randint(1, 5), random.randint(1, 5)
            op = "+"
            answer = a + b
            question = f"What is {a} + {b}?"
        elif difficulty == 2:
            a, b = random.randint(1, 10), random.randint(1, 10)
            op = "+"
            answer = a + b
            question = f"What is {a} + {b}?"
        else:
            a, b = random.randint(5, 20), random.randint(5, 20)
            if a < b:
                a, b = b, a
            op = "-"
            answer = a - b
            question = f"What is {a} - {b}?"

        choices = [answer, answer + 1, answer - 1, answer + 2]
        random.shuffle(choices)
        choices = choices[:4]
        if answer not in choices:
            choices[0] = answer

        return {
            "type": "math",
            "question": question,
            "answer": answer,
            "choices": choices,
            "hint": f"Try counting {op} {a} and {b}",
        }

    def _reading_exercise(self, age_group: str, difficulty: int) -> Dict:
        """Generate reading exercise."""
        words = {
            1: ["cat", "dog", "sun", "hat", "cup"],
            2: ["happy", "green", "jump", "blue", "fish"],
            3: ["beautiful", "wonderful", "adventure", "delicious"],
        }
        word_list = words.get(difficulty, words[2])

        target_word = random.choice(word_list)
        sounds = {"cat": "k", "dog": "d", "sun": "s", "hat": "h", "cup": "k"}

        return {
            "type": "reading",
            "question": f"What sound does '{target_word}' start with?",
            "answer": sounds.get(target_word, "t"),
            "choices": ["k", "d", "t", "s"],
            "hint": f"The word '{target_word}' starts with...",
        }

    def _science_exercise(self, age_group: str, difficulty: int) -> Dict:
        """Generate science exercise."""
        topics = [
            {"q": "What do plants need to grow?", "a": "sunlight", "choices": ["sunlight", "candy", "phones", "games"]},
            {"q": "What type of animal is a dog?", "a": "mammal", "choices": ["mammal", "reptile", "fish", "bird"]},
            {"q": "What season comes after summer?", "a": "fall", "choices": ["fall", "winter", "spring", "summer"]},
        ]
        topic = random.choice(topics)
        return {
            "type": "science",
            "question": topic["q"],
            "answer": topic["a"],
            "choices": topic["choices"],
            "hint": "Think about what you learned before!",
        }

    async def _check_answer(self, message: AgentMessage) -> AgentMessage:
        """Check user's answer."""
        if not self.current_quiz:
            return AgentMessage(
                from_agent=self.name,
                to_agent=message.from_agent,
                message_type=MessageType.ERROR,
                payload={"error": "No active exercise"},
            )

        user_answer = message.payload.get("answer", "")
        correct = user_answer == self.current_quiz["answer"]

        if correct:
            feedback = self._positive_feedback()
        else:
            feedback = self._encouragement()

        return AgentMessage(
            from_agent=self.name,
            to_agent=message.from_agent,
            message_type=MessageType.RESPONSE,
            payload={
                "correct": correct,
                "feedback": feedback,
                "correct_answer": self.current_quiz["answer"],
            },
        )

    async def _give_hint(self) -> AgentMessage:
        """Give a hint for current exercise."""
        if not self.current_quiz:
            return AgentMessage(
                from_agent=self.name,
                to_agent=message.from_agent,
                message_type=MessageType.ERROR,
                payload={"error": "No active exercise"},
            )

        return AgentMessage(
            from_agent=self.name,
            to_agent=message.from_agent,
            message_type=MessageType.RESPONSE,
            payload={"hint": self.current_quiz.get("hint", "Try your best!")},
        )

    def _positive_feedback(self) -> str:
        feedbacks = [
            "Great job! You're amazing! 🌟",
            "You did it! So smart! 🎉",
            "Perfect! Keep it up! ⭐",
            "Excellent work! You're a star! 🌈",
        ]
        return random.choice(feedbacks)

    def _encouragement(self) -> str:
        encouragements = [
            "Good try! Let's try another one! 💪",
            "Almost! Keep thinking! 🧠",
            "Nice effort! You'll get it! 🌱",
            "That's okay! Learning is fun! 📚",
        ]
        return random.choice(encouragements)