from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.schema.trip import STripCreate, STripDetailed, STripValidateDates
from app.services.trip import TripService

router = APIRouter(prefix="/trip", tags=["Trips"])

trip_service_singleton = TripService()


def get_trip_service() -> TripService:
    return trip_service_singleton


@router.get("/{trip_id}", response_model=STripDetailed)
async def get_trip(trip_id: int, trip_service: TripService = Depends(get_trip_service)):
    try:
        return await trip_service.get_trip_with_details(trip_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from None


@router.post("/", response_model=STripDetailed, status_code=status.HTTP_201_CREATED)
async def add_trip(
    trip_data: STripCreate,
    current_user=Depends(get_current_user),
    trip_service: TripService = Depends(get_trip_service),
):
    return await trip_service.add_trip(trip_data, current_user)


@router.put("/{trip_id}", response_model=STripDetailed)
async def update_trip_dates(
    trip_id: int,
    trip_data: STripValidateDates,
    current_user=Depends(get_current_user),
    trip_service: TripService = Depends(get_trip_service),
):
    return await trip_service.update_trip_dates(trip_id, trip_data, current_user)


@router.delete("/{trip_id}", response_model=STripDetailed)
async def delete_trip(
    trip_id: int,
    current_user=Depends(get_current_user),
    trip_service: TripService = Depends(get_trip_service),
):
    return await trip_service.delete_trip(trip_id, current_user)
