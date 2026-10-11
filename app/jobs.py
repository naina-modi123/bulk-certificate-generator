from app.models import GenerationJob, Recipient
from app.certificates import generate_certificate
from app.database import SessionLocal


def process_job(job_id: int):
    db = SessionLocal()

    try:
        job = db.query(GenerationJob).filter(
            GenerationJob.id == job_id
        ).first()

        if not job:
            return

        job.status = "processing"
        db.commit()

        recipients = db.query(Recipient).filter(
            Recipient.job_id == job_id
        ).all()

        for recipient in recipients:
            try:
                recipient.certificate_path = generate_certificate(
                    recipient.name,
                    job.course_name,
                    job.event_date,
                    recipient.id
                )
                recipient.status = "success"
                job.successful_count += 1

            except Exception as exc:
                recipient.status = "failed"
                recipient.error_message = str(exc)
                job.failed_count += 1

            db.commit()

        job.status = "completed"
        db.commit()

    finally:
        db.close()