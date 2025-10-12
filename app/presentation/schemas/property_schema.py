from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.infrastructure.data.models.property_model import PropertyStatus, PropertyType


# Base schema
class PropertyBase(BaseModel):
    title: str
    description: str | None = None
    address: str
    city: str
    state: str
    zip_code: str
    country: str
    price: float
    property_type: PropertyType
    status: PropertyStatus = PropertyStatus.AVAILABLE
    bedrooms: int | None = None
    bathrooms: float | None = None
    area_sqft: float | None = None
    lot_size_sqft: float | None = None
    parking_spaces: int | None = None
    heating_type: str | None = None
    cooling_type: str | None = None
    amenities: list[str] | None = None
    year_built: int | None = None
    image_urls: list[str] | None = None
    posted_by: int | None = None  # User ID of the agent posting the property

    model_config = ConfigDict(
        extra="forbid",
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "title": "Beautiful Family Home",
                "description": "A lovely 3-bedroom family home located in the suburbs.",
                "address": "123 Main St",
                "city": "Springfield",
                "state": "IL",
                "zip_code": "62704",
                "country": "USA",
                "price": 250000.00,
                "property_type": "house",
                "status": "available",
                "bedrooms": 3,
                "bathrooms": 2.5,
                "area_sqft": 2000.0,
                "lot_size_sqft": 5000.0,
                "year_built": 1995,
                "parking_spaces": 2,
                "heating_type": "central",
                "cooling_type": "central",
                "amenities": ["pool", "garage", "garden"],
                "image_urls": [
                    "http://example.com/image1.jpg",
                    "http://example.com/image2.jpg",
                ],
            }
        },
    )


class PropertyResponse(PropertyBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    is_featured: bool | None = None
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "id": 1,
                **PropertyBase.model_config["json_schema_extra"].get("example", {}),
                "created_at": "2025-01-01T12:00:00Z",
                "updated_at": "2025-01-02T12:00:00Z",
                "is_featured": False,
            }
        },
    )
