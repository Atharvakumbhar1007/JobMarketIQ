CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100)
);

CREATE TABLE jobs (
    job_id VARCHAR(100) PRIMARY KEY,
    job_title VARCHAR(200) NOT NULL,
    company VARCHAR(200),
    location_id INTEGER REFERENCES locations(location_id),
    salary_min NUMERIC,
    salary_max NUMERIC,
    experience_min INTEGER,
    experience_max INTEGER,
    employment_type VARCHAR(50),
    remote BOOLEAN,
    description TEXT,
    posted_date DATE
);

CREATE TABLE skills (
    skill_id SERIAL PRIMARY KEY,
    skill_name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(100)
);

CREATE TABLE job_skills (
    job_id VARCHAR(100) REFERENCES jobs(job_id),
    skill_id INTEGER REFERENCES skills(skill_id),
    PRIMARY KEY (job_id, skill_id)
);