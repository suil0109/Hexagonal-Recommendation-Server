from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.services.rec_service import RecService
from src.domain.models.dto_rec import UserInfo
from src.domain.models.configuration import StatusCode
from src.composition.api.dependencies import get_rec_service

router = APIRouter()

@router.post("/")
def test(user: UserInfo):
    return {StatusCode.OK.value}

@router.post("/base")
def get_recs(user: UserInfo,service: RecService = Depends(get_rec_service)):
    """
    Returns a user personalized Recommendation

    Returns:
        id: int
        name: str
        image_url: str
        landing_url: str
    """
    try:
        recs = service.get_recs_for_user(user)
        rec_responses = service.response_recs(recs)

        return JSONResponse(status_code=StatusCode.OK.value, content=rec_responses)
    except Exception as e:
        raise HTTPException(status_code=StatusCode.INTERNAL_ERROR.value, detail=str(e))


@router.post("/ctr")
def get_recs(user: UserInfo, service: RecService = Depends(get_rec_service)):
    """
    Returns a user personalized Recommendation using CTR algorithm

    Returns:
        id: int
        name: str
        image_url: str
        landing_url: str
    """

    try:
        recs = service.get_recs_for_user_with_ctr_prediction(user)
        rec_responses = service.response_recs(recs)
        return JSONResponse(status_code=StatusCode.OK.value, content=rec_responses)
    except Exception as e:
        raise HTTPException(status_code=StatusCode.INTERNAL_ERROR.value, detail=str(e))

