# Data Quality Rules

## Job ID

- Must be unique.
- Must not be null.

## Job Title

- Must not be null.
- Leading/trailing whitespace removed.

## Salary

- Must not be negative.
- Minimum salary cannot exceed maximum salary.

## Experience

- Minimum experience cannot be negative.
- Maximum experience cannot be less than minimum experience.

## Location

- Normalize common aliases.

## Description

- Empty descriptions should be flagged.
- Duplicate descriptions should be investigated.

## Dates

- Posted date must be a valid date.
- Future dates should be flagged.
