from dataclasses import dataclass
from enum import Enum
from typing import Optional


class SafetyLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class SafetyResult:
    allowed: bool
    reason: Optional[str] = None
    safety_level: SafetyLevel = SafetyLevel.MEDIUM


class SafetyFilter:
    BLOCKED_TERMS = [
        "harm", "hurt", "danger", "weapon",
    ]

    def check(self, text: str) -> SafetyResult:
        text_lower = text.lower()
        for term in self.BLOCKED_TERMS:
            if term in text_lower:
                return SafetyResult(
                    allowed=False,
                    reason=f"Blocked term: {term}"
                )
        return SafetyResult(allowed=True)

    def categorize_age_group(self, text: str) -> str:
        words = len(text.split())
        if words < 3:
            return "toddler"
        elif words < 8:
            return "early"
        else:
            return "school"

    def adapt_response(self, response: str, age_group: str) -> str:
        return response