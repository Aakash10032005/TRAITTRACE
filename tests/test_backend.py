import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from backend.main import app
from backend.graph_engine import TraitGraphManager
from backend.router import DEFAULT_PERSONA
from backend.config import settings

# Override API key for test environment so we don't trigger the placeholder ValueError
settings.GROQ_API_KEY = "test_key_override"

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_graph():
    # Clear graph before/after each test to keep tests isolated
    manager = TraitGraphManager()
    manager.clear()
    yield
    manager.clear()

def test_graph_manager_path_creation():
    manager = TraitGraphManager()
    session_id = "test-session-uuid"

    # Add traits
    manager.add_session_trait(session_id, "Minimalist", "swipe", "aesthetic")
    manager.add_session_trait(session_id, "Premium", "select", "pricing")

    # Assert nodes are added correctly
    snapshot = manager.get_graph_snapshot()
    node_ids = [n["id"] for n in snapshot["nodes"]]
    assert session_id in node_ids
    assert "Minimalist" in node_ids
    assert "Premium" in node_ids

    # Verify edge data
    links = snapshot["links"]
    assert len(links) == 2
    assert any(l["source"] == session_id and l["target"] == "Minimalist" for l in links)
    assert any(l["source"] == session_id and l["target"] == "Premium" for l in links)

    # Verify path summary string
    path_summary = manager.get_session_path_as_string(session_id)
    assert "test-session-uuid" in path_summary
    assert "Minimalist" in path_summary
    assert "Premium" in path_summary
    assert "aesthetic" in path_summary
    assert "pricing" in path_summary

@patch("groq.Groq")
def test_interact_endpoint_success(mock_groq_class):
    # Mock Groq client completions response
    mock_groq_instance = MagicMock()
    mock_groq_class.return_value = mock_groq_instance
    
    mock_completion = MagicMock()
    mock_completion.choices = [
        MagicMock(message=MagicMock(content='{"persona": "Sleek Executive", "hero_title": "Less is More", "hero_subtitle": "Subtle premium styles for modern setups.", "recommended_product_id": "prod_premium_minimal"}'))
    ]
    mock_groq_instance.chat.completions.create.return_value = mock_completion

    response = client.post("/api/interact", json={
        "session_id": "session-xyz",
        "interaction_type": "swipe",
        "value": "Minimalist"
    })

    assert response.status_code == 200
    res_data = response.json()
    assert res_data["session_id"] == "session-xyz"
    assert res_data["persona"] == "Sleek Executive"
    assert res_data["hero_title"] == "Less is More"
    assert res_data["recommended_product_id"] == "prod_premium_minimal"

    # Ensure graph snapshot has the nodes
    assert len(res_data["graph_snapshot"]["nodes"]) == 2

@patch("groq.Groq")
def test_interact_endpoint_groq_failure_fallback(mock_groq_class):
    # Mock Groq client throwing an error (e.g. invalid API key, network timeout)
    mock_groq_instance = MagicMock()
    mock_groq_class.return_value = mock_groq_instance
    mock_groq_instance.chat.completions.create.side_effect = Exception("Groq rate limit or API key error")

    response = client.post("/api/interact", json={
        "session_id": "session-error-test",
        "interaction_type": "swipe",
        "value": "Bold & Vibrant"
    })

    # The server should recover and return the default fallback persona seamlessly
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["persona"] == DEFAULT_PERSONA["persona"]
    assert res_data["hero_title"] == DEFAULT_PERSONA["hero_title"]
    assert res_data["recommended_product_id"] == DEFAULT_PERSONA["recommended_product_id"]
    assert len(res_data["graph_snapshot"]["nodes"]) == 2

@patch("groq.Groq")
def test_interact_endpoint_invalid_json_fallback(mock_groq_class):
    # Mock Groq returning unparsable non-JSON data
    mock_groq_instance = MagicMock()
    mock_groq_class.return_value = mock_groq_instance
    
    mock_completion = MagicMock()
    mock_completion.choices = [
        MagicMock(message=MagicMock(content="Here is the output: this is not a valid JSON structure!"))
    ]
    mock_groq_instance.chat.completions.create.return_value = mock_completion

    response = client.post("/api/interact", json={
        "session_id": "session-bad-json",
        "interaction_type": "select",
        "value": "Eco-Friendly"
    })

    assert response.status_code == 200
    res_data = response.json()
    assert res_data["persona"] == DEFAULT_PERSONA["persona"]
    assert res_data["hero_title"] == DEFAULT_PERSONA["hero_title"]
