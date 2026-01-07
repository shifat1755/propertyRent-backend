from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.sql import func

from app.infrastructure.data.models.property_model import Amenity, Property
from app.presentation.schemas.property_schema import PropertyBase


class PropertyRepository:
    def __init__(self, db: Session):
        self.db = db

    async def add_property(self, property: PropertyBase) -> Property:
        amenity_objects = []
        for amenity_name in property.amenities:
            amenity = (
                await self.db.execute(
                    select(Amenity).where(Amenity.name == amenity_name)
                )
            ).scalar_one_or_none()

            if not amenity:
                amenity = Amenity(name=amenity_name)
                self.db.add(amenity)
                await self.db.flush()  # Ensures amenity.id is available
            amenity_objects.append(amenity)

        db_property = Property(
            posted_by=property.posted_by,
            title=property.title,
            description=property.description,
            address=property.address,
            city=property.city,
            state=property.state,
            zip_code=property.zip_code,
            country=property.country,
            price=property.price,
            property_type=property.property_type,
            status=property.status,
            bedrooms=property.bedrooms,
            bathrooms=property.bathrooms,
            area_sqft=property.area_sqft,
            lot_size_sqft=property.lot_size_sqft,
            parking_spaces=property.parking_spaces,
            heating_type=property.heating_type,
            cooling_type=property.cooling_type,
            amenities=amenity_objects,
            year_built=property.year_built,
            image_urls=property.image_urls,
            updated_at=func.now(),
        )
        try:
            self.db.add(db_property)
            await self.db.commit()
            # Re-fetch with amenities eagerly loaded
            result = await self.db.execute(
                select(Property)
                .options(selectinload(Property.amenities))
                .where(Property.id == db_property.id)
            )
            property_with_amenities = result.scalar_one()
            return property_with_amenities
        except Exception as e:
            self.db.rollback()
            raise e

    async def get_properties_by_user(self, user_id: int) -> list[Property]:
        stmt = (
            select(Property)
            .options(selectinload(Property.amenities))
            .where(Property.posted_by == user_id)
        )
        res = await self.db.execute(stmt)
        return res.scalars().all()

    async def get_all_properties(self) -> list[Property]:
        stmt = select(Property).options(selectinload(Property.amenities))
        res = await self.db.execute(stmt)
        return res.scalars().all()
