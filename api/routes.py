from fastapi import (
    APIRouter,
    UploadFile,
    File,
    BackgroundTasks,
    HTTPException
)

from api.schemas import (
    ScoreRequest,
    ShortlistRequest,
    ParseRequest
)

from service.ats_service import ATSService

from utils.job_store import (
    create_job,
    update_job,
    get_job
)

from utils.logger import logger

import os
import shutil

router = APIRouter()

ats_service = ATSService()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ----------------------------
# Background Job
# ----------------------------
def run_scoring_job(job_id, request):
    try:
        logger.info(f"Started async scoring job : {job_id}")

        result = ats_service.calculate_score(
            skills_score=request.skills_score,
            experience_score=request.experience_score,
            education_score=request.education_score,
            semantic_score=request.semantic_score,
        )

        update_job(job_id, result)

        logger.info(f"Completed async scoring job : {job_id}")

    except Exception as e:
        logger.error(f"Async Job Error : {str(e)}")


# ----------------------------
# Upload Resume
# ----------------------------
@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    try:

        logger.info(f"Uploading Resume : {file.filename}")

        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"Resume Saved : {file_path}")

        return {
            "success": True,
            "filename": file.filename,
            "path": file_path
        }

    except Exception as e:

        logger.error(f"Upload Error : {str(e)}")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ----------------------------
# Parse Resume
# ----------------------------
@router.post("/parse")
def parse_resume(request: ParseRequest):

    try:

        logger.info(f"Parsing Resume : {request.file_path}")

        result = ats_service.parse_resume(
            request.file_path
        )

        logger.info("Resume Parsed Successfully")

        return {
            "success": True,
            "data": result
        }

    except Exception as e:

        logger.error(f"Parse Error : {str(e)}")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ----------------------------
# ATS Score
# ----------------------------
@router.post("/score")
def calculate_score(request: ScoreRequest):

    try:

        logger.info("ATS Score API Called")

        result = ats_service.calculate_score(
            skills_score=request.skills_score,
            experience_score=request.experience_score,
            education_score=request.education_score,
            semantic_score=request.semantic_score,
        )

        logger.info("ATS Score Generated Successfully")

        return {
            "success": True,
            "data": result
        }

    except Exception as e:

        logger.error(f"Score Error : {str(e)}")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ----------------------------
# Shortlist Candidate
# ----------------------------
@router.post("/shortlist")
def shortlist(request: ShortlistRequest):

    try:

        logger.info(
            f"Shortlist Check : {request.overall_score}"
        )

        result = ats_service.shortlist(
            overall_score=request.overall_score,
            threshold=request.threshold
        )

        logger.info("Shortlist Completed")

        return {
            "success": True,
            "data": result
        }

    except Exception as e:

        logger.error(f"Shortlist Error : {str(e)}")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ----------------------------
# Async Score
# ----------------------------
@router.post("/score-async")
def score_async(
    request: ScoreRequest,
    background_tasks: BackgroundTasks
):

    try:

        job_id = create_job()

        logger.info(
            f"Created Async Job : {job_id}"
        )

        background_tasks.add_task(
            run_scoring_job,
            job_id,
            request
        )

        return {
            "success": True,
            "job_id": job_id,
            "status": "Processing"
        }

    except Exception as e:

        logger.error(f"Async Error : {str(e)}")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ----------------------------
# Job Status
# ----------------------------
@router.get("/job/{job_id}")
def job_status(job_id: str):

    try:

        logger.info(f"Checking Job : {job_id}")

        job = get_job(job_id)

        if not job:
            raise HTTPException(
                status_code=404,
                detail="Job Not Found"
            )

        return {
            "success": True,
            "data": job
        }

    except HTTPException:
        raise

    except Exception as e:

        logger.error(f"Job Status Error : {str(e)}")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )