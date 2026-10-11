from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.database import Base


class GenerationJob(Base):
    __tablename__ = "generation_jobs"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="pending")
    total_recipients = Column(Integer, default=0)
    course_name = Column(String, nullable=False, default="Course")
    event_date = Column(String, nullable=False, default="")
    successful_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    recipients = relationship(
        "Recipient",
        back_populates="job",
        cascade="all, delete-orphan"
    )


class Recipient(Base):
    __tablename__ = "recipients"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(
        Integer,
        ForeignKey("generation_jobs.id"),
        nullable=False
    )
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    certificate_path = Column(String, nullable=True)
    status = Column(String, default="pending")
    error_message = Column(String, nullable=True)
    issued_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    job = relationship("GenerationJob", back_populates="recipients")