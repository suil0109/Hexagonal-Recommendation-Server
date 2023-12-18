from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.domain.models.dto_rec import UserInfo
from src.services.point_service import PointService
from src.composition.api.dependencies import get_point_service
from src.domain.models.exceptions import ErrorResponse, SuccessResponse
from src.domain.models.dto_point import Point, PointDepositBase, PointDeductBase
from src.domain.models.configuration import Status, StatusCode

router = APIRouter()

@router.post("/test")
def test(point: Point):
    return {'test': Status.SUCCESS}

@router.post("/modify") # modification
def modify_point(point: Point, service: PointService = Depends(get_point_service)):
    """
    Returns 0 or 1 : success or fail. when admin request for a point point modification

    Returns:
        id: int
        name: str
        image_url: str
        landing_url: str
    """
    try:
        # tmp = Rec(id=1, name='campaign name 1', image_url='https://image.google.com/image_1.jpg', landing_url='https://landing.google.com/landing_1', weight=2300, target_country='KR', target_gender='M', point=11)
        success = service.modify_point(point)

        if success: 
            return JSONResponse(status_code=StatusCode.OK.value, content=Status.SUCCESS.value)
        else:
            return JSONResponse(status_code=StatusCode.INTERNAL_ERROR.value, content=Status.FAIL.value)
    except Exception as e:
        raise HTTPException(status_code=StatusCode.BAD_REQUEST.value, detail=ErrorResponse(status=Status.FAIL, message=str(e)))


@router.post("/deposit")
def deposit_point(point: PointDepositBase, service: PointService = Depends(get_point_service)):
    """
    Returns a user personalized Recommendation

    Returns:
        id: int
        name: str
        image_url: str
        landing_url: str
    """

    try:
        # tmp1 = Rec(id=2, name='campaign name 1', image_url='https://image.google.com/image_1.jpg', landing_url='https://landing.google.com/landing_1', weight=2300, target_country='KR', target_gender='M', point=11)
        # tmp = RecResponse(id=2, name='campaign name 1', image_url='https://image.google.com/image_1.jpg', landing_url='https://landing.google.com/landing_1')
        # user = User(2,"M","KR")
        success = service.deposit_point(service.create_point_deposit_info(point))

        if success: 
            return JSONResponse(status_code=StatusCode.OK.value, content=Status.SUCCESS.value)
        else:
            return JSONResponse(status_code=StatusCode.INTERNAL_ERROR.value, content=Status.FAIL.value)
    except Exception as e:
        raise HTTPException(status_code=StatusCode.BAD_REQUEST.value, detail=ErrorResponse(status=Status.FAIL, message=str(e)))

@router.post("/deduct")
def deduct_point(point: PointDeductBase, service: PointService = Depends(get_point_service)):
    """
    Returns a user personalized Recommendation

    Returns:
        id: int
        name: str
        image_url: str
        landing_url: str
    """

    try:
        # tmp1 = Rec(id=2, name='campaign name 1', image_url='https://image.google.com/image_1.jpg', landing_url='https://landing.google.com/landing_1', weight=2300, target_country='KR', target_gender='M', point=11)
        # tmp = RecResponse(id=2, name='campaign name 1', image_url='https://image.google.com/image_1.jpg', landing_url='https://landing.google.com/landing_1')
        # point_info = PointInfo(-1,1,'deduct',10)
        # user = User(2,"M","KR")
        # success = service.deduct_point(user, point_info)
        
        success = service.deduct_point(service.create_point_deduct_info(point))

        if success: 
            return JSONResponse(status_code=StatusCode.OK.value, content=Status.SUCCESS.value)
        else:
            return JSONResponse(status_code=StatusCode.INTERNAL_ERROR.value, content=Status.FAIL.value)
    except Exception as e:
        raise HTTPException(status_code=StatusCode.BAD_REQUEST.value, detail=ErrorResponse(status=Status.FAIL, message=str(e)))


@router.post("/history") # post -> get (변경이 없음으로)
def history_point(user: UserInfo, service: PointService = Depends(get_point_service)):
    """
    Returns a user personalized Recommendation

    Returns:
        id: int
        name: str
        image_url: str
        landing_url: str
    """

    try:
        # tmp1 = Rec(id=2, name='campaign name 1', image_url='https://image.google.com/image_1.jpg', landing_url='https://landing.google.com/landing_1', weight=2300, target_country='KR', target_gender='M', point=11)
        # tmp = RecResponse(id=2, name='campaign name 1', image_url='https://image.google.com/image_1.jpg', landing_url='https://landing.google.com/landing_1')
        
        # point_info = PointInfo(-1,1,'deduct',10)
        # user = User(2,"M","KR")
        rec = service.history_point(user)
        return JSONResponse(status_code=StatusCode.OK.value , content=rec)

    
    except Exception as e:
        raise HTTPException(status_code=StatusCode.BAD_REQUEST.value, detail=ErrorResponse(status=Status.FAIL, message=str(e)))



@router.post("/balance") # post -> get (변경이 없음으로)
def balance_point(user: UserInfo, service: PointService = Depends(get_point_service)):
    """
    Returns a user personalized Recommendation

    Returns:
        id: int
        name: str
        image_url: str
        landing_url: str
    """
    try:
        # tmp1 = Rec(id=2, name='campaign name 1', image_url='https://image.google.com/image_1.jpg', landing_url='https://landing.google.com/landing_1', weight=2300, target_country='KR', target_gender='M', point=11)
        # tmp = RecResponse(id=2, name='campaign name 1', image_url='https://image.google.com/image_1.jpg', landing_url='https://landing.google.com/landing_1')
        
        # point_info = PointInfo(-1,1,'deduct',10)
        # user = User(2,"M","KR")
        rec = service.balance_point(user)
        return JSONResponse(status_code=StatusCode.OK.value , content=rec)
    
    except Exception as e:
        raise HTTPException(status_code=StatusCode.BAD_REQUEST.value, detail=ErrorResponse(status=Status.FAIL, message=str(e)))

    