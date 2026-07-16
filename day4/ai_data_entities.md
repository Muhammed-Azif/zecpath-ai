# AI Data Entity Design

## Objective

Design the core data entities used in the AI Job Portal for storing candidate and job information.

---

## Entity 1: Candidate

Description:
Stores all information related to a job seeker.

Fields:
- Candidate ID
- Full Name
- Email
- Phone Number
- Location
- Professional Summary
- Skills
- Education
- Experience
- Projects
- Certifications
- Languages
- Soft Skills

---

## Entity 2: Job

Description:
Stores all information related to a job posting.

Fields:
- Job ID
- Job Title
- Company Name
- Location
- Employment Type
- Experience Required
- Salary Range
- Job Summary
- Required Skills
- Preferred Skills
- Education Required
- Responsibilities
- Requirements
- Benefits
- Posted Date
- Application Deadline
- Contact Email

---

## Entity 3: Skill

Description:
Represents a skill that can be associated with both candidates and jobs.

Fields:
- Skill ID
- Skill Name
- Skill Category
- Skill Level

---

## Entity Relationships

- One Candidate can have multiple Skills.
- One Candidate can have multiple Education records.
- One Candidate can have multiple Experience records.
- One Candidate can work on multiple Projects.
- One Job can require multiple Skills.
- The AI matching system compares Candidate Skills, Experience, and Education with Job Requirements to calculate a match score.

---