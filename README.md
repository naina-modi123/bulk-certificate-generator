# Bulk Certificate Generator

A Python-based backend API that generates certificates in bulk using a predefined PDF template. It supports recipient validation, job status tracking, and certificate downloads.

## Features

- Generate certificates for multiple recipients in a single request.
- Validate recipient names and email addresses.
- Generate personalized PDF certificates.
- Track generation job status and progress.
- Record successful and failed certificate generations.
- Download individual generated certificates.
- Store job and recipient information in a SQLite database.
- Run automated tests using Pytest.

## Technology Stack

- **Language:** Python 3.11
- **Framework:** FastAPI
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **PDF Generation:** ReportLab
- **Testing:** Pytest, HTTPX

## Project Structure

```text
bulk-certificate-generator/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── certificates.py
│   └── jobs.py
├── tests/
│   └── test_main.py
├── generated_certificates/
├── requirements.txt
├── README.md
└── certificates.db
```

## Setup and Installation

### 1. Clone or download the project

Open the project folder in your terminal.

### 2. Create a virtual environment

```powershell
python -m venv venv
```

### 3. Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
python -m pip install email-validator
```

## Run the Application

Start the FastAPI server:

```powershell
python -m uvicorn app.main:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

Open the interactive API documentation:

`http://127.0.0.1:8000/docs`

## API Usage

### 1. Create a certificate generation job

**Endpoint:** `POST /jobs`

Example request:

```json
{
  "recipients": [
    {
      "name": "Aarav Sharma",
      "email": "aarav@example.com"
    },
    {
      "name": "Priya Verma",
      "email": "priya@example.com"
    }
  ],
  "course_name": "Python Programming",
  "event_date": "2026-10-11"
}
```

Example response:

```json
{
  "job_id": 1,
  "status": "pending",
  "total_recipients": 2
}
```

The API processes the recipients and generates a PDF certificate for each successful recipient.

### 2. Check job status

**Endpoint:** `GET /jobs/{job_id}`

Example:

`GET /jobs/1`

The response includes the job status, total recipients, successful and failed counts, and recipient-level results.

### 3. Download a certificate

**Endpoint:** `GET /certificates/{recipient_id}`

Example:

`GET /certificates/1`

A successful request returns the recipient's PDF certificate.

## Testing

Run the automated tests:

```powershell
python -m pytest tests/test_main.py -v
```

## Design Decisions

- **FastAPI:** Provides API endpoints and interactive documentation.
- **SQLite:** Provides relational storage without requiring a separate database server.
- **SQLAlchemy:** Manages database models and queries.
- **ReportLab:** Generates PDF certificates programmatically.
- **Background processing:** Uses FastAPI background tasks to process certificate generation after a job is submitted.
- **Individual failure handling:** Records recipient-level failures so one certificate-generation error does not stop the processing of other recipients.

## Limitations and Future Improvements

- Add more comprehensive tests for validation, job status, certificate retrieval, and individual generation failures.
- Add persistent background workers for larger workloads.
- Add batch downloads of generated certificates.
- Improve certificate design and support configurable certificate fields.
- Add authentication and access control if the API is deployed publicly.

## License

This project was developed as a backend assignment.
=======
# bulk-certificate-generator
>>>>>>> c4b9f912aea0d3901fddebe69885648587dbbbcb
