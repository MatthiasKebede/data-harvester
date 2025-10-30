import pytest
from src.services.catalog_service import CatalogService

@pytest.fixture
def catalog_service():
    return CatalogService()

def test_fetch_catalog_page(catalog_service):
    page = catalog_service.fetch_catalog_page(1)
    assert page is not None

def test_fetch_all_catalog_pages(catalog_service):
    pages = catalog_service.fetch_all_catalog_pages()
    assert len(pages) == 2