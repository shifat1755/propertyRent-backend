import json
from typing import Any, Dict, List

from elasticsearch import AsyncElasticsearch

from app.config import ElasticsearchConfig
from app.presentation.schemas.property_schema import (
    PropertyResponse,
    PropertySearchParams,
    PropertySearchResult,
)


class PropertySearchService:
    """Encapsulates Elasticsearch queries for properties."""

    def __init__(self, client: AsyncElasticsearch, index: str | None = None):
        self.client = client
        self.index = index or ElasticsearchConfig.PROPERTY_INDEX

    async def search(self, params: PropertySearchParams) -> PropertySearchResult:
        search_args = self._build_query(params)
        response = await self.client.search(index=self.index, **search_args)
        hits = response.get("hits", {})
        total_obj = hits.get("total", {"value": 0})
        total = total_obj["value"] if isinstance(total_obj, dict) else total_obj

        items: List[PropertyResponse] = []
        for hit in hits.get("hits", []):
            source = hit.get("_source", {})
            normalized = self._normalize_source(source)
            items.append(PropertyResponse.model_validate(normalized))

        return PropertySearchResult(
            items=items,
            total=total,
            page=params.page,
            per_page=params.per_page,
        )

    def _build_query(self, params: PropertySearchParams) -> Dict[str, Any]:
        must: List[Dict[str, Any]] = []
        filters: List[Dict[str, Any]] = []

        if params.q:
            must.append(
                {
                    "multi_match": {
                        "query": params.q,
                        "fields": [
                            "title^3",
                            "description^2",
                            "address",
                            "city",
                            "state",
                            "zip_code",
                            "country",
                        ],
                        "fuzziness": "AUTO",
                        "type": "best_fields",
                    }
                }
            )

        if params.location:
            must.append(
                {
                    "multi_match": {
                        "query": params.location,
                        "fields": ["city", "state", "country", "zip_code"],
                        "type": "phrase",
                    }
                }
            )

        if params.city:
            filters.append({"term": {"city.keyword": params.city}})
        if params.state:
            filters.append({"term": {"state.keyword": params.state}})
        if params.country:
            filters.append({"term": {"country.keyword": params.country}})
        if params.zip_code:
            filters.append({"term": {"zip_code.keyword": params.zip_code}})
        if params.property_type:
            filters.append({"term": {"property_type.keyword": params.property_type}})
        if params.status:
            filters.append({"term": {"status.keyword": params.status}})
        if params.posted_by is not None:
            filters.append({"term": {"posted_by": params.posted_by}})
        if params.is_featured is not None:
            filters.append({"term": {"is_featured": params.is_featured}})

        price_range: Dict[str, Any] = {}
        if params.min_price is not None:
            price_range["gte"] = params.min_price
        if params.max_price is not None:
            price_range["lte"] = params.max_price
        if price_range:
            filters.append({"range": {"price": price_range}})

        bedroom_range: Dict[str, Any] = {}
        if params.min_bedrooms is not None:
            bedroom_range["gte"] = params.min_bedrooms
        if params.max_bedrooms is not None:
            bedroom_range["lte"] = params.max_bedrooms
        if bedroom_range:
            filters.append({"range": {"bedrooms": bedroom_range}})

        bathroom_range: Dict[str, Any] = {}
        if params.min_bathrooms is not None:
            bathroom_range["gte"] = params.min_bathrooms
        if params.max_bathrooms is not None:
            bathroom_range["lte"] = params.max_bathrooms
        if bathroom_range:
            filters.append({"range": {"bathrooms": bathroom_range}})

        area_range: Dict[str, Any] = {}
        if params.min_area is not None:
            area_range["gte"] = params.min_area
        if params.max_area is not None:
            area_range["lte"] = params.max_area
        if area_range:
            filters.append({"range": {"area_sqft": area_range}})

        year_range: Dict[str, Any] = {}
        if params.min_year_built is not None:
            year_range["gte"] = params.min_year_built
        if params.max_year_built is not None:
            year_range["lte"] = params.max_year_built
        if year_range:
            filters.append({"range": {"year_built": year_range}})

        query: Dict[str, Any] = {"bool": {}}
        if must:
            query["bool"]["must"] = must
        if filters:
            query["bool"]["filter"] = filters
        if not must and not filters:
            query = {"match_all": {}}

        sort_field = self._resolve_sort_field(params.sort_by)
        sort_order = "asc" if params.sort_order == "asc" else "desc"
        sort_clause = [{sort_field: {"order": sort_order}}]

        body: Dict[str, Any] = {
            "query": query,
            "from_": (params.page - 1) * params.per_page,
            "size": params.per_page,
            "sort": sort_clause,
            "track_total_hits": True,
        }
        if params.q:
            body["highlight"] = {
                "fields": {"title": {}, "description": {}, "address": {}},
                "fragment_size": 150,
                "number_of_fragments": 1,
            }
        print("Elasticsearch_query_body:", json.dumps(body, indent=2))
        return body

    def _normalize_source(self, source: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize ES source so it fits PropertyResponse."""
        image_urls = source.get("image_urls")
        if isinstance(image_urls, str):
            try:
                image_urls = json.loads(image_urls)
            except json.JSONDecodeError:
                image_urls = [
                    url.strip() for url in image_urls.split(",") if url.strip()
                ]

        posted_by = source.get("posted_by")
        if isinstance(posted_by, str) and posted_by.isdigit():
            posted_by = int(posted_by)

        normalized = {
            **source,
            "image_urls": image_urls,
            "posted_by": posted_by,
        }
        # amenities are not indexed via Logstash; keep it consistent
        normalized.setdefault("amenities", [])
        return normalized

    def _resolve_sort_field(self, sort_by: str | None) -> str:
        allowed = {
            "created_at": "created_at",
            "updated_at": "updated_at",
            "price": "price",
            "area_sqft": "area_sqft",
        }
        if sort_by and sort_by in allowed:
            return allowed[sort_by]
        return "created_at"
