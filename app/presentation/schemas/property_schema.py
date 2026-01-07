from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    FieldValidationInfo,
    field_validator,
)

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


class PropertySearchParams(BaseModel):
    q: str | None = Field(
        default=None, description="Full-text search across title, description, address"
    )
    location: str | None = Field(
        default=None, description="Location keyword (city/state/country/zip)"
    )
    city: str | None = None
    state: str | None = None
    country: str | None = None
    zip_code: str | None = None
    property_type: str | None = Field(
        default=None, description="Matches PropertyType values (e.g. house)"
    )
    status: str | None = Field(
        default=None, description="Matches PropertyStatus values (e.g. available)"
    )
    posted_by: int | None = Field(default=None, description="Owner/agent user id")
    min_price: float | None = Field(default=None, ge=0)
    max_price: float | None = Field(default=None, ge=0)
    min_bedrooms: int | None = Field(default=None, ge=0)
    max_bedrooms: int | None = Field(default=None, ge=0)
    min_bathrooms: float | None = Field(default=None, ge=0)
    max_bathrooms: float | None = Field(default=None, ge=0)
    min_area: float | None = Field(default=None, ge=0, description="area_sqft lower")
    max_area: float | None = Field(default=None, ge=0, description="area_sqft upper")
    min_year_built: int | None = Field(default=None, ge=0)
    max_year_built: int | None = Field(default=None, ge=0)
    is_featured: bool | None = None
    sort_by: str | None = Field(
        default=None, description="created_at, updated_at, price, area_sqft"
    )
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=10, ge=1, le=100)

    model_config = ConfigDict(extra="forbid")

    @field_validator("max_price")
    @classmethod
    def validate_price(cls, v, info: FieldValidationInfo):
        min_value = info.data.get("min_price")
        if v is not None and min_value is not None and v < min_value:
            raise ValueError("max_price cannot be less than min_price")
        return v

    @field_validator("max_bedrooms")
    @classmethod
    def validate_bedrooms(cls, v, info: FieldValidationInfo):
        min_value = info.data.get("min_bedrooms")
        if v is not None and min_value is not None and v < min_value:
            raise ValueError("max_bedrooms cannot be less than min_bedrooms")
        return v

    @field_validator("max_bathrooms")
    @classmethod
    def validate_bathrooms(cls, v, info: FieldValidationInfo):
        min_value = info.data.get("min_bathrooms")
        if v is not None and min_value is not None and v < min_value:
            raise ValueError("max_bathrooms cannot be less than min_bathrooms")
        return v

    @field_validator("max_area")
    @classmethod
    def validate_area(cls, v, info: FieldValidationInfo):
        min_value = info.data.get("min_area")
        if v is not None and min_value is not None and v < min_value:
            raise ValueError("max_area cannot be less than min_area")
        return v

    @field_validator("max_year_built")
    @classmethod
    def validate_year(cls, v, info: FieldValidationInfo):
        min_value = info.data.get("min_year_built")
        if v is not None and min_value is not None and v < min_value:
            raise ValueError("max_year_built cannot be less than min_year_built")
        return v


class PropertySearchResult(BaseModel):
    items: list[PropertyResponse]
    total: int
    page: int
    per_page: int
