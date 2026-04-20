from enum import Enum
from pydantic import BaseModel, Field
from typing import Any, Optional
import uuid


class MessageType(str, Enum):
    TASK = "task"
    RESULT = "result"
    ERROR = "error"
    HEARTBEAT = "heartbeat"


class TaskType(str, Enum):
    CHAT = "chat"
    STORY = "story"
    LEARN = "learn"
    SCHEDULE = "schedule"


class AgentMessage(BaseModel):
    from_agent: str = Field(..., description="Source agent name")
    to_agent: str = Field(..., description="Target agent name")
    message_type: MessageType
    task_type: Optional[TaskType] = None
    payload: dict[str, Any] = Field(default_factory=dict)
    context: dict[str, Any] = Field(default_factory=dict)
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    class Config:
        use_enum_values = True