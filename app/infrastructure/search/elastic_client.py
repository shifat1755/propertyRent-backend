from functools import lru_cache
from typing import AsyncIterator

from elasticsearch import AsyncElasticsearch

from app.config import ElasticsearchConfig


@lru_cache
def _get_client() -> AsyncElasticsearch:
    """Create (and cache) an AsyncElasticsearch client."""
    basic_auth = None
    if ElasticsearchConfig.USERNAME and ElasticsearchConfig.PASSWORD:
        basic_auth = (ElasticsearchConfig.USERNAME, ElasticsearchConfig.PASSWORD)

    return AsyncElasticsearch(
        [ElasticsearchConfig.get_url()],
        basic_auth=basic_auth,
        verify_certs=ElasticsearchConfig.VERIFY_CERTS,
        ca_certs=ElasticsearchConfig.CA_CERT_PATH,
        request_timeout=ElasticsearchConfig.REQUEST_TIMEOUT,
        ssl_show_warn=False,
    )


async def get_es_client() -> AsyncIterator[AsyncElasticsearch]:
    """
    FastAPI dependency that returns a shared AsyncElasticsearch client.

    The client is cached for reuse across requests; FastAPI will handle
    async generator dependencies, so this stays simple.
    """
    client = _get_client()
    try:
        yield client
    finally:
        # Client intentionally kept open; FastAPI shutdown events can close it
        # if needed, but re-creation per request is avoided here.
        pass
