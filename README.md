# Code Standards

- Follow PEP 8 Python coding standards.
- Use meaningful variable, function, and class names.
- Write modular and reusable code.
- Keep functions small and focused on a single task.
- Add comments where necessary.
- Use logging instead of print() for application events.

# Documentation Format

Each module should include:
- Purpose of the module
- Functions and classes
- Input parameters
- Return values
- Example usage

Example:

```python
def calculate_score(score):
    """
    Calculate the final ATS score.

    Args:
        score (int): Candidate's raw score.

    Returns:
        int: Final ATS score.
    """
    return score
```

## Project Structure

- `data/` – Stores datasets and resumes
- `parsers/` – Resume parsing modules
- `ats_engine/` – ATS scoring logic
- `screening_ai/` – AI screening modules
- `interview_ai/` – AI interview functionality
- `scoring/` – Candidate scoring logic
- `utils/` – Utility and logging functions
- `tests/` – Test scripts 