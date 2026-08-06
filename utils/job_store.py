import uuid

# In-memory job storage
jobs = {}


def create_job():
    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        "status": "Processing",
        "result": None
    }

    return job_id


def update_job(job_id, result):
    jobs[job_id]["status"] = "Completed"
    jobs[job_id]["result"] = result


def get_job(job_id):
    return jobs.get(job_id)