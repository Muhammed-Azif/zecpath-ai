# Zecpath AI ATS - Troubleshooting Notes

## 1. Purpose

This document provides troubleshooting guidance for common issues
encountered while developing, running, testing, and maintaining the
Zecpath AI ATS.

The purpose is to help developers quickly identify the source of an
issue and apply the appropriate solution.

---

# 2. Application Does Not Start

### Symptoms

The API fails to start or the terminal displays an import or startup
error.

### Possible Causes

- Incorrect application module
- Missing dependency
- Python virtual environment not activated
- Import error
- Syntax error
- Incorrect project path

### Troubleshooting

Activate the virtual environment:

```bash
venv\Scripts\activate