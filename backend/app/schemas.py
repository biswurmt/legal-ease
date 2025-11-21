from datetime import datetime

from pydantic import BaseModel

from app.models import Message


# Audio and Legal API Response Models
class AudioResponse(BaseModel):
    message: str
    audio_data: bytes | None = None  # Base64 encoded audio

class ContextResponse(BaseModel):
    context: str

# Tree Generation Response Models
class TreeNode(BaseModel):
    speaker: str
    line: str
    level: int
    reflects_personality: str
    responses: list['TreeNode'] = []

class ScenariosTreeResponse(BaseModel):
    scenarios_tree: TreeNode

class TreeResponse(BaseModel):
    tree_id: int | None = None
    case_id: int
    simulation_goal: str
    scenarios_tree: TreeNode
    error: str | None = None
    raw_response: str | None = None

class ModelRequest(BaseModel):
    question: str

class ConversationTurn(BaseModel):
    party: str
    statement: str

class ConversationResponse(BaseModel):
    conversation: list[ConversationTurn]

def map_role_to_party(role: str) -> str:
    role = role.lower()
    if role == "user":
        return "Party A"
    elif role == "assistant":
        return "Party B"
    elif role == "system":
        return "System"
    else:
        return "Unknown"

def messages_to_conversation(messages: list[Message]) -> ConversationResponse:
    conversation_turns = [
        ConversationTurn(
            party=msg.role,
            statement=msg.content
        )
        for msg in messages
    ]
    return ConversationResponse(conversation=conversation_turns)


class CaseWithTreeCount(BaseModel):
    id: int
    name: str
    party_a: str | None
    party_b: str | None
    context: str | None
    summary: str | None
    last_modified: datetime
    scenario_count: int


class SimulationCreate(BaseModel):
    headline: str
    brief: str
    case_id: int


class SimulationResponse(BaseModel):
    id: int
    headline: str
    brief: str
    created_at: datetime
    case_id: int


class BookmarkCreate(BaseModel):
    simulation_id: int
    message_id: int
    name: str


class BookmarkResponse(BaseModel):
    id: int
    simulation_id: int
    message_id: int
    name: str
