from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_job():
    response = client.post(
        "/jobs",
        json={
            "recipients": [
                {"name": "Test User", "email": "test@example.com"}
            ],
            "course_name": "Python",
            "event_date": "2026-10-11"
        }
    )
    assert response.status_code == 200
    assert "job_id" in response.json()


def test_invalid_email():
    response = client.post(
        "/jobs",
        json={
            "recipients": [
                {"name": "Test User", "email": "invalid-email"}
            ],
            "course_name": "Python",
            "event_date": "2026-10-11"
        }
    )
    assert response.status_code == 422


def test_empty_recipients():
    response = client.post(
        "/jobs",
        json={
            "recipients": [],
            "course_name": "Python",
            "event_date": "2026-10-11"
        }
    )
    assert response.status_code == 422
def test_job_status():
    create_response = client.post(
        "/jobs",
        json={
            "recipients": [
                {"name": "Status User", "email": "status@example.com"}
            ],
            "course_name": "Python",
            "event_date": "2026-10-11"
        }
    )

    job_id = create_response.json()["job_id"]
    import time
    time.sleep(1)

    response = client.get(f"/jobs/{job_id}")

    assert response.status_code == 200
    assert response.json()["status"] in ["pending", "processing", "completed"]


def test_job_not_found():
    response = client.get("/jobs/999999")
    assert response.status_code == 404
def test_download_certificate():
    create_response = client.post(
        "/jobs",
        json={
            "recipients": [
                {"name": "Download User", "email": "download@example.com"}
            ],
            "course_name": "Python",
            "event_date": "2026-10-11"
        }
    )

    job_id = create_response.json()["job_id"]

    import time
    time.sleep(2)

    job_response = client.get(f"/jobs/{job_id}")
    recipient_id = job_response.json()["recipients"][0]["id"]

    response = client.get(f"/certificates/{recipient_id}")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
def test_individual_certificate_failure(monkeypatch):
    from app import jobs

    def fail_one_certificate(name, course_name, event_date, recipient_id):
        if name == "Fail User":
            raise Exception("Simulated certificate failure")

        return "generated_certificates/test_certificate.pdf"

    monkeypatch.setattr(
        jobs,
        "generate_certificate",
        fail_one_certificate
    )

    response = client.post(
        "/jobs",
        json={
            "recipients": [
                {"name": "Fail User", "email": "fail@example.com"},
                {"name": "Success User", "email": "success@example.com"}
            ],
            "course_name": "Python",
            "event_date": "2026-10-11"
        }
    )

    assert response.status_code == 200

    job_id = response.json()["job_id"]

    import time
    time.sleep(2)

    job_response = client.get(f"/jobs/{job_id}")
    data = job_response.json()

    assert data["status"] == "completed"
    assert data["successful_count"] == 1
    assert data["failed_count"] == 1