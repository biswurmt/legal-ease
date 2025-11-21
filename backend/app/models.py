from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    A = "A"  # Party A
    B = "B"  # Party B


class Case(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    party_a: str | None = Field(default=None)
    party_b: str | None = Field(default=None)
    context: str | None = Field(default=None)
    summary: str | None = Field(default=None)
    last_modified: datetime = Field(default_factory=datetime.utcnow)


class Simulation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    headline: str
    brief: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    case_id: int = Field(foreign_key="case.id", nullable=False, ondelete="CASCADE")

class Message(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str
    role: MessageRole
    selected: bool = Field(default=False)
    simulation_id: int = Field(foreign_key="simulation.id", nullable=False, ondelete="CASCADE")
    parent_id: int | None = Field(default=None, foreign_key="message.id", nullable=True)

class Bookmark(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    simulation_id: int = Field(foreign_key="simulation.id", nullable=False, ondelete="CASCADE")
    message_id: int = Field(foreign_key="message.id", nullable=False, ondelete="CASCADE")
    name: str = Field(max_length=255)

class Document(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    file_name: str
    file_data: bytes
    case_id: int = Field(foreign_key="case.id", nullable=False, ondelete="CASCADE")
