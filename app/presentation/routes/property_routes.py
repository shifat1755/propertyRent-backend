from elasticsearch import AsyncElasticsearch
from fastapi import APIRouter, Depends

# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.usecases.property_search_usecase import PropertySearchUsecase
from app.application.usecases.property_usecase import PropertyUsecase
from app.infrastructure.data.database import get_db
from app.infrastructure.search.elastic_client import get_es_client
from app.presentation.routes.dependencies import get_current_user
from app.presentation.schemas.property_schema import (
    PropertyBase,
    PropertyResponse,
    PropertySearchParams,
    PropertySearchResult,
)

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


@propertyRouter.get("/properties/me", response_model=list[PropertyResponse])
async def get_my_properties(
    db: AsyncSession = Depends(get_db),
    sender=Depends(get_current_user),
):
    usecase = PropertyUsecase(db)
    properties = await usecase.get_properties_by_user(int(sender["user_id"]))
    result = []
    for property in properties:
        amenities = [a.name for a in property.amenities] if property.amenities else []
        property.amenities = []
        temp = PropertyResponse.model_validate(property)
        temp.amenities = amenities
        result.append(temp)

    return result


@propertyRouter.get("/properties", response_model=list[PropertyResponse])
async def get_all_properties(
    db: AsyncSession = Depends(get_db),
):
    usecase = PropertyUsecase(db)
    properties = await usecase.get_all_properties()
    result = []
    for property in properties:
        amenities = [a.name for a in property.amenities] if property.amenities else []
        property.amenities = []
        temp = PropertyResponse.model_validate(property)
        temp.amenities = amenities
        result.append(temp)

    return result


@propertyRouter.get(
    "/properties/search",
    response_model=PropertySearchResult,
    summary="Full-text and filtered search for properties",
)
async def search_properties(
    params: PropertySearchParams = Depends(),
    es_client: AsyncElasticsearch = Depends(get_es_client),
):
    search_usecase = PropertySearchUsecase(es_client)
    result = await search_usecase.search(params)
    return result
