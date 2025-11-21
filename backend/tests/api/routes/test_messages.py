"""
Integration tests for Message and Tree operations.
"""
from fastapi.testclient import TestClient
from sqlmodel import Session


def create_test_case(client: TestClient) -> int:
    """Helper to create a test case."""
    data = {
        "name": "Message Test Case",
        "party_a": "Party A Inc.",
        "party_b": "Party B LLC",
        "context": "Negotiation context",
        "summary": "Contract dispute"
    }
    response = client.post("/api/cases", json=data)
    return response.json()["id"]


def create_test_simulation(client: TestClient, case_id: int) -> int:
    """Helper to create a test simulation."""
    data = {
        "headline": "Test Negotiation",
        "brief": "Opening negotiation",
        "case_id": case_id
    }
    response = client.post("/api/simulations", json=data)
    return response.json()["id"]


def test_create_message(client: TestClient, db: Session) -> None:
    """Test creating a message."""
    case_id = create_test_case(client)
    sim_id = create_test_simulation(client, case_id)

    # Create a message
    message_data = {
        "content": "Test message content",
        "role": "A",
        "simulation_id": sim_id,
        "parent_id": None,
        "selected": True
    }
    response = client.post("/api/message", json=message_data)
    assert response.status_code == 200
    content = response.json()
    assert content["content"] == message_data["content"]
    assert content["role"] == message_data["role"]
    assert "id" in content


def test_get_tree_messages(client: TestClient, db: Session) -> None:
    """Test retrieving all messages in a tree."""
    case_id = create_test_case(client)
    sim_id = create_test_simulation(client, case_id)

    # Create messages
    message1_data = {
        "content": "First message",
        "role": "A",
        "simulation_id": sim_id,
        "parent_id": None,
        "selected": True
    }
    msg1_response = client.post("/api/message", json=message1_data)
    msg1_id = msg1_response.json()["id"]

    message2_data = {
        "content": "Second message",
        "role": "B",
        "simulation_id": sim_id,
        "parent_id": msg1_id,
        "selected": True
    }
    client.post("/api/message", json=message2_data)

    # Get tree messages
    response = client.get(f"/api/trees/{sim_id}/messages")
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) == 2


def test_get_selected_conversation(client: TestClient, db: Session) -> None:
    """Test retrieving selected conversation path."""
    case_id = create_test_case(client)
    sim_id = create_test_simulation(client, case_id)

    # Create a conversation chain
    message1_data = {
        "content": "First message",
        "role": "A",
        "simulation_id": sim_id,
        "parent_id": None,
        "selected": True
    }
    msg1_response = client.post("/api/message", json=message1_data)
    msg1_id = msg1_response.json()["id"]

    message2_data = {
        "content": "Second message",
        "role": "B",
        "simulation_id": sim_id,
        "parent_id": msg1_id,
        "selected": True
    }
    msg2_response = client.post("/api/message", json=message2_data)
    msg2_id = msg2_response.json()["id"]

    # Get conversation
    response = client.get(f"/api/trees/{sim_id}/messages/traversal?message_id={msg2_id}")
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) == 2
    # Should be in order from root to leaf
    assert content[0]["id"] == msg1_id
    assert content[1]["id"] == msg2_id


def test_update_message_selected(client: TestClient, db: Session) -> None:
    """Test updating message selected status."""
    case_id = create_test_case(client)
    sim_id = create_test_simulation(client, case_id)

    # Create message
    message_data = {
        "content": "Test message",
        "role": "A",
        "simulation_id": sim_id,
        "parent_id": None,
        "selected": False
    }
    msg_response = client.post("/api/message", json=message_data)
    msg_id = msg_response.json()["id"]

    # Update selected status
    response = client.patch(f"/api/message/{msg_id}/selected?selected=true")
    assert response.status_code == 200
    content = response.json()
    assert content["selected"] is True


def test_delete_message_with_children(client: TestClient, db: Session) -> None:
    """Test deleting a message and its children."""
    case_id = create_test_case(client)
    sim_id = create_test_simulation(client, case_id)

    # Create parent message
    parent_data = {
        "content": "Parent message",
        "role": "A",
        "simulation_id": sim_id,
        "parent_id": None,
        "selected": True
    }
    parent_response = client.post("/api/message", json=parent_data)
    parent_id = parent_response.json()["id"]

    # Create child message
    child_data = {
        "content": "Child message",
        "role": "B",
        "simulation_id": sim_id,
        "parent_id": parent_id,
        "selected": True
    }
    client.post("/api/message", json=child_data)

    # Delete parent (should cascade)
    response = client.delete(f"/api/message/{parent_id}/with-children")
    assert response.status_code == 200

    # Verify all messages deleted
    tree_response = client.get(f"/api/trees/{sim_id}/messages")
    assert len(tree_response.json()) == 0


def test_get_message_children(client: TestClient, db: Session) -> None:
    """Test getting children of a message."""
    case_id = create_test_case(client)
    sim_id = create_test_simulation(client, case_id)

    # Create parent
    parent_data = {
        "content": "Parent",
        "role": "A",
        "simulation_id": sim_id,
        "parent_id": None,
        "selected": True
    }
    parent_response = client.post("/api/message", json=parent_data)
    parent_id = parent_response.json()["id"]

    # Create multiple children
    for i in range(3):
        child_data = {
            "content": f"Child {i}",
            "role": "B",
            "simulation_id": sim_id,
            "parent_id": parent_id,
            "selected": False
        }
        client.post("/api/message", json=child_data)

    # Get children
    response = client.get(f"/api/message/{parent_id}/children")
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 3
