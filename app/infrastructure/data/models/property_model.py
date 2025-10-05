import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.infrastructure.data.database import Base


class PropertyType(enum.Enum):
    HOUSE = "house"
    APARTMENT = "apartment"
    CONDO = "condo"
    TOWNHOUSE = "townhouse"
    LAND = "land"
    OTHER = "other"


class PropertyStatus(enum.Enum):
    AVAILABLE = "available"
    SOLD = "sold"
    RENTED = "rented"


class PropertyModel(Base):
    __tablename__ = "properties"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Foreign key to User
    posted_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="properties")  # noqa: F821

    # Property details
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Address
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    zip_code: Mapped[str] = mapped_column(String(20), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)

    # Pricing
    price: Mapped[float] = mapped_column(Float, nullable=False)

    # Property type and status
    property_type: Mapped[PropertyType] = mapped_column(
        SqlEnum(
            PropertyType,
            name="propertytype",
            values_callable=lambda x: [m.value for m in x],
        ),
        nullable=False,
    )
    status: Mapped[PropertyStatus] = mapped_column(
        SqlEnum(
            PropertyStatus,
            name="propertystatus",
            values_callable=lambda x: [m.value for m in x],
        ),
        default=PropertyStatus.AVAILABLE,
        nullable=False,
    )

    # Specifications
    bedrooms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    bathrooms: Mapped[float | None] = mapped_column(Float, nullable=True)
    area_sqft: Mapped[float | None] = mapped_column(Float, nullable=True)
    lot_size_sqft: Mapped[float | None] = mapped_column(Float, nullable=True)
    year_built: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    # Misc
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
