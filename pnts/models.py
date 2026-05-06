from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4


def current_timestamp() -> str:
    return datetime.now().isoformat(timespec="seconds")


@dataclass(slots=True)
class Note:
    date: str
    topic: str
    content: str
    image_paths: list[str] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=current_timestamp)
    updated_at: str = field(default_factory=current_timestamp)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "date": self.date,
            "topic": self.topic,
            "content": self.content,
            "image_paths": list(self.image_paths),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Note":
        return cls(
            id=str(data["id"]),
            date=str(data["date"]),
            topic=str(data.get("topic", "")),
            content=str(data.get("content", "")),
            image_paths=[str(path) for path in data.get("image_paths", [])],
            created_at=str(data.get("created_at", current_timestamp())),
            updated_at=str(data.get("updated_at", current_timestamp())),
        )

