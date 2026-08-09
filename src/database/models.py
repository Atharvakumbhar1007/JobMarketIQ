"""SQLAlchemy ORM models for JobMarketIQ."""

from sqlalchemy import (
    Column, String, Integer, Numeric, Boolean,
    Text, Date, ForeignKey, UniqueConstraint,
)
from sqlalchemy.orm import relationship
from src.database.db import Base


class Location(Base):
    __tablename__ = "locations"

    location_id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String(100), nullable=False)
    state = Column(String(100))
    country = Column(String(100), default="India")

    jobs = relationship("Job", back_populates="location")

    __table_args__ = (
        UniqueConstraint("city", "country", name="uq_city_country"),
    )

    def __repr__(self):
        return f"<Location city={self.city}>"


class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(String(100), primary_key=True)
    job_title = Column(String(200), nullable=False)
    company = Column(String(200))
    location_id = Column(Integer, ForeignKey("locations.location_id"))
    salary_min = Column(Numeric)
    salary_max = Column(Numeric)
    experience_min = Column(Integer)
    experience_max = Column(Integer)
    employment_type = Column(String(50))
    work_mode = Column(String(20))
    remote = Column(Boolean, default=False)
    description = Column(Text)
    posted_date = Column(Date)

    location = relationship("Location", back_populates="jobs")
    job_skills = relationship("JobSkill", back_populates="job", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Job {self.job_title} @ {self.company}>"


class Skill(Base):
    __tablename__ = "skills"

    skill_id = Column(Integer, primary_key=True, autoincrement=True)
    skill_name = Column(String(100), unique=True, nullable=False)
    category = Column(String(100))
    demand_count = Column(Integer, default=0)

    job_skills = relationship("JobSkill", back_populates="skill")

    def __repr__(self):
        return f"<Skill {self.skill_name} ({self.category})>"


class JobSkill(Base):
    __tablename__ = "job_skills"

    job_id = Column(String(100), ForeignKey("jobs.job_id"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.skill_id"), primary_key=True)

    job = relationship("Job", back_populates="job_skills")
    skill = relationship("Skill", back_populates="job_skills")

    def __repr__(self):
        return f"<JobSkill job={self.job_id} skill={self.skill_id}>"
