import pytest
from fastapi.testclient import TestClient
import copy
import sys
from pathlib import Path

# Add src to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """Fixture to provide a TestClient for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Fixture to reset activities to initial state before each test"""
    # Store original state
    original_activities = copy.deepcopy(activities)
    
    yield
    
    # Reset after test
    activities.clear()
    activities.update(original_activities)
