from fastapi import APIRouter, Depends, HTTPException

from app.repository.trip import TripRepository
from app.schema.trip import STripDetailed
from app.services.trip import TripService

router = APIRouter(prefix="/trip", tags=["Trips"])

trip_service_singleton = TripService(TripRepository())  # Singleton instance


def get_trip_service() -> TripService:
    return trip_service_singleton


@router.get("/{trip_id}", response_model=STripDetailed)
async def get_trip(trip_id: int, trip_service: TripService = Depends(get_trip_service)):
    try:
        return await trip_service.get_trip_with_details(trip_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from None
