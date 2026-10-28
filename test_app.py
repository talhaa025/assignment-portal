import pytest
import app as portal

@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(portal, "DATA_FILE", str(tmp_path / "data.json"))
    return portal.app.test_client()

GOOD = {"name": "Ali", "reg_no": "FA22-BCS-001",
        "title": "Lab 1", "url": "https://github.com/ali/lab1"}

def test_valid_submission_saved(client):
    r = client.post("/", data=GOOD)
    assert b"Submission saved" in r.data
    assert len(portal.load()) == 1
    assert b"Lab 1" in client.get("/").data

def test_missing_registration_number(client):
    r = client.post("/", data={**GOOD, "reg_no": ""})
    assert b"Registration number is required" in r.data
    assert portal.load() == []

def test_invalid_url_rejected(client):
    r = client.post("/", data={**GOOD, "url": "not-a-url"})
    assert b"Submission URL is invalid" in r.data
    assert portal.load() == []