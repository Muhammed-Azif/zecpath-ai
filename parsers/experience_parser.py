"""
Day 10 - Experience Parsing Engine

This module extracts structured work experience from the
'Work Experience' section produced by section_classifier.py.
"""

import re
from datetime import datetime

class ExperienceParser:
    """
    Parses the Work Experience section of a resume.
    """

    def __init__(self):
        # Supported month names
        self.months = {
            "jan": 1, "feb": 2, "mar": 3,
            "apr": 4, "may": 5, "jun": 6,
            "jul": 7, "aug": 8, "sep": 9,
            "oct": 10, "nov": 11, "dec": 12
    
        }
    def parse_dates(self, duration):
        """
        Converts:
            Feb 2025 - Present
        into:
            start_date, end_date, is_current
        """

        parts = duration.split("-")

        if len(parts) != 2:
            return None, None, False

        start = parts[0].strip()
        end = parts[1].strip()

        start_date = self.convert_date(start)

        if end.lower() in ["present", "current"]:
            return start_date, None, True

        end_date = self.convert_date(end)

        return start_date, end_date, False

    def convert_date(self, date_text):
        """
        Converts:
            Feb 2025
        into:
            2025-02
        """

        pieces = date_text.split()

        if len(pieces) != 2:
            return None

        month = pieces[0][:3].lower()
        year = pieces[1]

        if month not in self.months:
            return None

        return f"{year}-{self.months[month]:02d}"

    def calculate_duration(self, start_date, end_date):
        """
        Calculates the duration between two dates in months.

        Example:
            2023-05 → 2025-01
            Returns: 21
        """

        if start_date is None:
            return 0

        # If the job is current, use today's date
        if end_date is None:
            today = datetime.today()
            end_year = today.year
            end_month = today.month
        else:
            end_year, end_month = map(int, end_date.split("-"))

        start_year, start_month = map(int, start_date.split("-"))

        months = (end_year - start_year) * 12
        months += end_month - start_month

        return months + 1



    def parse_experience(self, experience_text):
        """
        Parses the Work Experience section and returns
        structured experience data.
        """

        experiences = []

        job_blocks = experience_text.strip().split("\n\n")

        for block in job_blocks:

            lines = [line.strip() for line in block.split("\n") if line.strip()]

            if len(lines) < 3:
                continue

            title = lines[0]
            company = lines[1]
            duration = lines[2]

            # Parse dates
            start_date, end_date, is_current = self.parse_dates(duration)

            # Calculate duration
            duration_months = self.calculate_duration(
                start_date,
                end_date
            )

            experience = {
                "job_title": title,
                "company": company,
                "start_date": start_date,
                "end_date": end_date,
                "is_current": is_current,
                "duration_months": duration_months
            }

            experiences.append(experience)

        return experiences


    def calculate_total_experience(self, experiences):
        """
        Calculates the total experience from all jobs.
        """

        total_months = 0

        for job in experiences:
            total_months += job["duration_months"]

        years = total_months // 12
        months = total_months % 12

        return {
            "total_months": total_months,
            "years": years,
            "months": months
        }

    def detect_career_gaps(self, experiences):
        """
        Detects employment gaps between jobs.
        """

        if len(experiences) < 2:
            return []

        # Sort jobs by start date
        experiences.sort(key=lambda x: x["start_date"])

        gaps = []

        for i in range(len(experiences) - 1):

            current_job = experiences[i]
            next_job = experiences[i + 1]

            current_end = current_job["end_date"]
            next_start = next_job["start_date"]

            if current_end is None:
                continue

            end_year, end_month = map(int, current_end.split("-"))
            start_year, start_month = map(int, next_start.split("-"))

            end_total = end_year * 12 + end_month
            start_total = start_year * 12 + start_month

            gap = start_total - end_total - 1

            if gap > 0:
                gaps.append({
                    "after_company": current_job["company"],
                    "before_company": next_job["company"],
                    "gap_months": gap
                })

        return gaps

    def detect_overlaps(self, experiences):
        """
        Detect overlapping employment periods.
        """

        if len(experiences) < 2:
            return []

        experiences.sort(key=lambda x: x["start_date"])

        overlaps = []

        for i in range(len(experiences) - 1):

            first = experiences[i]
            second = experiences[i + 1]

            if first["end_date"] is None:
                today = datetime.today()
                first_end = f"{today.year}-{today.month:02d}"
            else:
                first_end = first["end_date"]

            second_start = second["start_date"]

            first_end_month = (
                int(first_end.split("-")[0]) * 12 +
                int(first_end.split("-")[1])
            )

            second_start_month = (
                int(second_start.split("-")[0]) * 12 +
                int(second_start.split("-")[1])
            )

            if second_start_month <= first_end_month:

                overlap = first_end_month - second_start_month + 1

                overlaps.append({
                    "company_1": first["company"],
                    "company_2": second["company"],
                    "overlap_months": overlap
                })

        return overlaps

    def calculate_actual_experience(self, experiences):
        """
        Calculates total experience without double-counting
        overlapping jobs.
        """

        if not experiences:
            return {
                "total_months": 0,
                "years": 0,
                "months": 0
            }

        intervals = []

        for job in experiences:

            start_year, start_month = map(int, job["start_date"].split("-"))

            if job["end_date"] is None:
                today = datetime.today()
                end_year = today.year
                end_month = today.month
            else:
                end_year, end_month = map(int, job["end_date"].split("-"))

            start = start_year * 12 + start_month
            end = end_year * 12 + end_month

            intervals.append((start, end))

        # Sort by start month
        intervals.sort()

        merged = []

        for start, end in intervals:

            if not merged:
                merged.append([start, end])

            else:

                last_start, last_end = merged[-1]

                if start <= last_end + 1:
                    merged[-1][1] = max(last_end, end)

                else:
                    merged.append([start, end])

        total = 0

        for start, end in merged:
            total += end - start + 1

        return {
            "total_months": total,
            "years": total // 12,
            "months": total % 12
        }