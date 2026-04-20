"""Schedule Agent - Daily routines, reminders, and time management."""
from agents.base import BaseAgent, AgentConfig
from core.message import AgentMessage, MessageType, TaskType
from pydantic import Field
from typing import Optional, Dict, List
from datetime import datetime, time, timedelta
import json


class ScheduleAgentConfig(AgentConfig):
    name: str = "schedule_agent"
    system_prompt: str = """You are a helpful schedule assistant for children.
Help manage daily routines, remind about activities, and prepare for transitions."""


class ScheduleAgent(BaseAgent):
    def __init__(self, config: ScheduleAgentConfig):
        super().__init__(config)
        self.schedules: Dict[str, List[Dict]] = {}
        self.reminders: List[Dict] = []

    async def initialize(self):
        from models.loader import model_loader
        result = model_loader.load_model(self.name, self.config.model_path)
        if result.success:
            self.is_ready = True

    async def process_task(self, message: AgentMessage) -> AgentMessage:
        payload = message.payload
        action = payload.get("action", "get_schedule")

        if action == "add_reminder":
            return await self._add_reminder(payload)
        elif action == "get_schedule":
            return await self._get_schedule(payload)
        elif action == "check_due":
            return await self._check_due_reminders()
        elif action == "transition_warning":
            return await self._transition_warning(payload)
        else:
            return await self._get_schedule(payload)

    async def _add_reminder(self, payload: Dict) -> AgentMessage:
        reminder_time = payload.get("time", "08:00")
        activity = payload.get("activity", "wake up")
        repeat = payload.get("repeat", "daily")

        reminder = {
            "time": reminder_time,
            "activity": activity,
            "repeat": repeat,
            "enabled": True,
        }
        self.reminders.append(reminder)

        return AgentMessage(
            from_agent=self.name,
            to_agent=message.from_agent,
            message_type=MessageType.RESPONSE,
            payload={
                "response": f"Reminder set for {activity} at {reminder_time}!",
                "reminder": reminder,
            },
            context=message.context,
        )

    async def _get_schedule(self, payload: Dict) -> AgentMessage:
        time_now = datetime.now().strftime("%H:%M")
        schedule = self.reminders if self.reminders else self._default_schedule()

        return AgentMessage(
            from_agent=self.name,
            to_agent=message.from_agent,
            message_type=MessageType.RESPONSE,
            payload={
                "schedule": schedule,
                "current_time": time_now,
            },
            context=message.context,
        )

    async def _check_due_reminders(self) -> AgentMessage:
        time_now = datetime.now()
        current_time = time_now.strftime("%H:%M")
        due = [r for r in self.reminders if r.get("time") == current_time and r.get("enabled")]

        if due:
            response = f"It's time for: {', '.join([r['activity'] for r in due])}!"
        else:
            response = "No reminders right now."

        return AgentMessage(
            from_agent=self.name,
            to_agent=message.from_agent,
            message_type=MessageType.RESPONSE,
            payload={
                "response": response,
                "due_reminders": due,
            },
            context=message.context,
        )

    async def _transition_warning(self, payload: Dict) -> AgentMessage:
        next_activity = payload.get("next_activity", "bedtime")
        minutes = payload.get("minutes", 5)

        response = f"In {minutes} minutes, it will be time for {next_activity}!"

        return AgentMessage(
            from_agent=self.name,
            to_agent=message.from_agent,
            message_type=MessageType.RESPONSE,
            payload={
                "response": response,
                "warning": True,
                "next_activity": next_activity,
            },
            context=message.context,
        )

    def _default_schedule(self) -> List[Dict]:
        return [
            {"time": "07:00", "activity": "wake up", "repeat": "daily"},
            {"time": "08:00", "activity": "breakfast", "repeat": "daily"},
            {"time": "09:00", "activity": "learning time", "repeat": "daily"},
            {"time": "12:00", "activity": "lunch", "repeat": "daily"},
            {"time": "13:00", "activity": "nap time", "repeat": "daily"},
            {"time": "15:00", "activity": "play time", "repeat": "daily"},
            {"time": "18:00", "activity": "dinner", "repeat": "daily"},
            {"time": "20:00", "activity": "bedtime", "repeat": "daily"},
        ]
