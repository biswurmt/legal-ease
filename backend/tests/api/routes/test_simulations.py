"""
Integration tests for Simulation CRUD operations.
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session


def test_create_simulation(client: TestClient, db: Session) -> None:
    """Test creating a new simulation."""
    # First create a case
    case_data = {
        "name": "Simulation Test Case",
        "party_a": "Party A",
        "party_b": "Party B",
        "context": "Context",
        "summary": "Summary"
    }
    case_response = client.post("/api/cases", json=case_data)
    case_id = case_response.json()["id"]

    # Create a simulation
    sim_data = {
        "headline": "Test Simulation",
        "brief": "Test brief",
        "case_id": case_id
    }
    response = client.post("/api/simulations", json=sim_data)
    assert response.status_code == 200
    content = response.json()
    assert content["headline"] == sim_data["headline"]
    assert content["case_id"] == case_id
    assert "id" in content


def test_read_simulations_by_case(client: TestClient, db: Session) -> None:
    """Test reading simulations for a specific case."""
    # Create a case
    case_data = {
        "name": "Case with Sims",
        "party_a": "Party A",
        "party_b": "Party B",
        "context": "Context",
        "summary": "Summary"
    }
    case_response = client.post("/api/cases", json=case_data)
    case_id = case_response.json()["id"]

    # Create simulations
    for i in range(2):
        sim_data = {
            "headline": f"Simulation {i}",
            "brief": f"Brief {i}",
            "case_id": case_id
        }
        client.post("/api/simulations", json=sim_data)

    # Read simulations
    response = client.get(f"/api/simulations/{case_id}")
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) == 2


def test_update_simulation(client: TestClient, db: Session) -> None:
    """Test updating a simulation."""
    # Create case and simulation
    case_data = {
        "name": "Update Sim Case",
        "party_a": "Party A",
        "party_b": "Party B",
        "context": "Context",
        "summary": "Summary"
    }
    case_response = client.post("/api/cases", json=case_data)
    case_id = case_response.json()["id"]

    sim_data = {
        "headline": "Original Headline",
        "brief": "Original Brief",
        "case_id": case_id
    }
    sim_response = client.post("/api/simulations", json=sim_data)
    sim_id = sim_response.json()["id"]

    # Update simulation
    update_data = {
        "headline": "Updated Headline",
        "brief": "Updated Brief"
    }
    response = client.put(f"/api/simulation/{sim_id}", json=update_data)
    assert response.status_code == 200
    content = response.json()
    assert content["headline"] == update_data["headline"]


def test_delete_simulation(client: TestClient, db: Session) -> None:
    """Test deleting a simulation."""
    # Create case and simulation
    case_data = {
        "name": "Delete Sim Case",
        "party_a": "Party A",
        "party_b": "Party B",
        "context": "Context",
        "summary": "Summary"
    }
    case_response = client.post("/api/cases", json=case_data)
    case_id = case_response.json()["id"]

    sim_data = {
        "headline": "Delete Simulation",
        "brief": "Brief",
        "case_id": case_id
    }
    sim_response = client.post("/api/simulations", json=sim_data)
    sim_id = sim_response.json()["id"]

    # Delete simulation
    response = client.delete(f"/api/simulation/{sim_id}")
    assert response.status_code == 200


def test_delete_case_cascades_to_simulations(client: TestClient, db: Session) -> None:
    """Test that deleting a case also deletes its simulations."""
    # Create case and simulation
    case_data = {
        "name": "Cascade Test Case",
        "party_a": "Party A",
        "party_b": "Party B",
        "context": "Context",
        "summary": "Summary"
    }
    case_response = client.post("/api/cases", json=case_data)
    case_id = case_response.json()["id"]

    sim_data = {
        "headline": "Cascade Simulation",
        "brief": "Brief",
        "case_id": case_id
    }
    client.post("/api/simulations", json=sim_data)

    # Delete case
    client.delete(f"/api/case/{case_id}")

    # Verify simulations were deleted
    response = client.get(f"/api/simulations/{case_id}")
    assert response.status_code == 200
    assert len(response.json()) == 0
