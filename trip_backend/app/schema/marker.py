from pydantic import BaseModel

from app.utils.wkb_to_list import wkb_to_list


class SMarker(BaseModel):
    id: int
    name: str | None
    location: list

    class Config:
        from_attributes = True

    @staticmethod
    def from_orm_marker(marker):
        return SMarker(
            id=marker.id,
            name=marker.name,
            location=wkb_to_list(marker.location),
        )
