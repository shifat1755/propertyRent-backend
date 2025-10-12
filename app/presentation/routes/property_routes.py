from fastapi import APIRouter, Depends

# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.usecases.property_usecase import PropertyUsecase
from app.infrastructure.data.database import get_db
from app.presentation.routes.dependencies import get_current_user
from app.presentation.schemas.property_schema import PropertyBase, PropertyResponse

propertyRouter = APIRouter()


@propertyRouter.post("/properties/add", response_model=PropertyResponse)
async def add_property(
    property: PropertyBase,
    db: AsyncSession = Depends(get_db),
    sender=Depends(get_current_user),
):
    property.posted_by = int(sender["user_id"])
    usecase = PropertyUsecase(db)
    res = await usecase.add_property(property)
    amenities = [a.name for a in res.amenities] if res.amenities else []
    res.amenities = []
    response = PropertyResponse.model_validate(res)
    response.amenities = amenities
    return response
