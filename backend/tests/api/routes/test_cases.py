"""
Integration tests for Case CRUD operations.
"""
from fastapi.testclient import TestClient
from sqlmodel import Session


def test_create_case(client: TestClient, db: Session) -> None:
    """Test creating a new case."""
    data = {
        "name": "Test Case",
        "party_a": "Party A Inc.",
        "party_b": "Party B LLC",
        "context": "Test context",
        "summary": "Test summary"
    }
    response = client.post("/api/cases", json=data)
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["party_a"] == data["party_a"]
    assert content["party_b"] == data["party_b"]
    assert "id" in content


def test_read_cases(client: TestClient, db: Session) -> None:
    """Test reading all cases."""
    # Create a case first
    data = {
        "name": "Read Test Case",
        "party_a": "Party A",
        "party_b": "Party B",
        "context": "Context",
        "summary": "Summary"
    }
    client.post("/api/cases", json=data)

    # Read all cases
    response = client.get("/api/cases")
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) > 0


def test_read_case_by_id(client: TestClient, db: Session) -> None:
    """Test reading a specific case by ID."""
    # Create a case
    data = {
        "name": "Specific Case",
        "party_a": "Party A",
        "party_b": "Party B",
        "context": "Context",
        "summary": "Summary"
    }
    create_response = client.post("/api/cases", json=data)
    case_id = create_response.json()["id"]

    # Read the case
    response = client.get(f"/api/case/{case_id}")
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == case_id
    assert content["name"] == data["name"]


def test_update_case(client: TestClient, db: Session) -> None:
    """Test updating a case."""
    # Create a case
    data = {
        "name": "Original Name",
        "party_a": "Party A",
        "party_b": "Party B",
        "context": "Original context",
        "summary": "Original summary"
    }
    create_response = client.post("/api/cases", json=data)
    case_id = create_response.json()["id"]

    # Update the case
    update_data = {
        "name": "Updated Name",
        "context": "Updated context"
    }
    response = client.put(f"/api/case/{case_id}", json=update_data)
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == update_data["name"]
    assert content["context"] == update_data["context"]


def test_delete_case(client: TestClient, db: Session) -> None:
    """Test deleting a case."""
    # Create a case
    data = {
        "name": "Delete Test Case",
        "party_a": "Party A",
        "party_b": "Party B",
        "context": "Context",
        "summary": "Summary"
    }
    create_response = client.post("/api/cases", json=data)
    case_id = create_response.json()["id"]

    # Delete the case
    response = client.delete(f"/api/case/{case_id}")
    assert response.status_code == 200

    # Verify deletion
    get_response = client.get(f"/api/case/{case_id}")
    assert get_response.status_code == 404


def test_case_not_found(client: TestClient) -> None:
    """Test reading a non-existent case."""
    response = client.get("/api/case/99999")
    assert response.status_code == 404
