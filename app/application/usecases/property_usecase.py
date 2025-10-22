from sqlalchemy.orm import Session

from app.infrastructure.data.models.property_model import Property
from app.infrastructure.repositories.property_repo import PropertyRepository
from app.presentation.schemas.property_schema import PropertyBase


class PropertyUsecase:
    def __init__(self, db: Session):
        self.repo = PropertyRepository(db)

    async def add_property(self, property: PropertyBase) -> Property:
        property.amenities = (
            [amenity.lower() for amenity in property.amenities]
            if len(property.amenities) != 0
            else []
        )
        try:
            res = await self.repo.add_property(property)
            return res
        except Exception as e:
            raise e

    async def get_properties_by_user(self, user_id: int) -> list[Property]:
        try:
            res = await self.repo.get_properties_by_user(user_id)
            return res
        except Exception as e:
            raise e
