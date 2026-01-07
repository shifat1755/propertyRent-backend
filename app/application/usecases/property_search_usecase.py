from elasticsearch import AsyncElasticsearch

from app.infrastructure.search.property_search_service import PropertySearchService
from app.presentation.schemas.property_schema import (
    PropertySearchParams,
    PropertySearchResult,
)


class PropertySearchUsecase:
    """Coordinates property search via Elasticsearch."""

    def __init__(self, es_client: AsyncElasticsearch):
        self.service = PropertySearchService(es_client)

    async def search(self, params: PropertySearchParams) -> PropertySearchResult:
        return await self.service.search(params)

