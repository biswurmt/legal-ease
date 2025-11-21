"""
Integration tests for Bookmark operations.
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session


def create_test_environment(client: TestClient) -> tuple[int, int, int]:
    """Helper to create case, simulation, and message."""
    # Create case
    case_data = {
        "name": "Bookmark Test Case",
        "party_a": "Party A",
        "party_b": "Party B",
        "context": "Context",
        "summary": "Summary"
    }
    case_response = client.post("/api/cases", json=case_data)
    case_id = case_response.json()["id"]

    # Create simulation
    sim_data = {
        "headline": "Test Simulation",
        "brief": "Brief",
        "case_id": case_id
    }
    sim_response = client.post("/api/simulations", json=sim_data)
    sim_id = sim_response.json()["id"]

    # Create message
    message_data = {
        "content": "Test message",
        "role": "A",
        "simulation_id": sim_id,
        "parent_id": None,
        "selected": True
    }
    msg_response = client.post("/api/message", json=message_data)
    msg_id = msg_response.json()["id"]

    return case_id, sim_id, msg_id


def test_create_bookmark(client: TestClient, db: Session) -> None:
    """Test creating a bookmark."""
    _, sim_id, msg_id = create_test_environment(client)

    bookmark_data = {
        "simulation_id": sim_id,
        "message_id": msg_id,
        "name": "Important Point"
    }
    response = client.post("/api/bookmarks", json=bookmark_data)
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == bookmark_data["name"]
    assert content["simulation_id"] == sim_id
    assert content["message_id"] == msg_id
    assert "id" in content


def test_get_bookmarks_by_simulation(client: TestClient, db: Session) -> None:
    """Test retrieving bookmarks for a simulation."""
    _, sim_id, msg_id = create_test_environment(client)

    # Create multiple bookmarks
    for i in range(3):
        bookmark_data = {
            "simulation_id": sim_id,
            "message_id": msg_id,
            "name": f"Bookmark {i}"
        }
        client.post("/api/bookmarks", json=bookmark_data)

    # Get bookmarks
    response = client.get(f"/api/bookmarks/{sim_id}")
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) == 3


def test_delete_bookmark(client: TestClient, db: Session) -> None:
    """Test deleting a bookmark."""
    _, sim_id, msg_id = create_test_environment(client)

    # Create bookmark
    bookmark_data = {
        "simulation_id": sim_id,
        "message_id": msg_id,
        "name": "Delete Test"
    }
    create_response = client.post("/api/bookmarks", json=bookmark_data)
    bookmark_id = create_response.json()["id"]

    # Delete bookmark
    response = client.delete(f"/api/bookmark/{bookmark_id}")
    assert response.status_code == 200

    # Verify deletion
    get_response = client.get(f"/api/bookmarks/{sim_id}")
    assert len(get_response.json()) == 0


def test_bookmark_cascade_on_simulation_delete(client: TestClient, db: Session) -> None:
    """Test that bookmarks are deleted when simulation is deleted."""
    case_id, sim_id, msg_id = create_test_environment(client)

    # Create bookmark
    bookmark_data = {
        "simulation_id": sim_id,
        "message_id": msg_id,
        "name": "Cascade Test"
    }
    client.post("/api/bookmarks", json=bookmark_data)

    # Delete simulation
    client.delete(f"/api/simulation/{sim_id}")

    # Verify bookmarks were deleted (endpoint should return empty or 404)
    response = client.get(f"/api/bookmarks/{sim_id}")
    # Either empty list or 404 is acceptable
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        assert len(response.json()) == 0
