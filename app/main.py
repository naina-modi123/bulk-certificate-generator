from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pathlib import Path

from app.database import Base, engine, SessionLocal
from app.models import GenerationJob, Recipient
from app.schemas import CertificateJobRequest
from app.jobs import process_job

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bulk Certificate Generator")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/jobs")
def create_job(
    request: CertificateJobRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    job = GenerationJob(
    status="pending",
    total_recipients=len(request.recipients),
    course_name=request.course_name,
    event_date=request.event_date
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    for recipient_data in request.recipients:
        recipient = Recipient(
            job_id=job.id,
            name=recipient_data.name,
            email=str(recipient_data.email)
        )
        db.add(recipient)

    db.commit()

    background_tasks.add_task(process_job, job.id)
    return {
        "job_id": job.id,
        "status": "pending",
        "total_recipients": len(request.recipients)
    }


@app.get("/jobs/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(GenerationJob).filter(
        GenerationJob.id == job_id
    ).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    recipients = db.query(Recipient).filter(
        Recipient.job_id == job_id
    ).all()

    return {
        "job_id": job.id,
        "status": job.status,
        "total_recipients": job.total_recipients,
        "successful_count": job.successful_count,
        "failed_count": job.failed_count,
        "recipients": [
            {
                "id": r.id,
                "name": r.name,
                "email": r.email,
                "status": r.status,
                "error_message": r.error_message
            }
            for r in recipients
        ]
    }


@app.get("/certificates/{recipient_id}")
def download_certificate(
    recipient_id: int,
    db: Session = Depends(get_db)
):
    recipient = db.query(Recipient).filter(
        Recipient.id == recipient_id
    ).first()

    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")

    if recipient.status != "success" or not recipient.certificate_path:
        raise HTTPException(
            status_code=404,
            detail="Certificate is not available"
        )

    path = Path(recipient.certificate_path)

    if not path.is_file():
        raise HTTPException(status_code=404, detail="Certificate file not found")

    return FileResponse(
        path=str(path),
        media_type="application/pdf",
        filename=f"certificate_{recipient.id}.pdf"
    )