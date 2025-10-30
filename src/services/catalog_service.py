from src.http_client import Client

CATALOG_ENDPOINT = "/catalog"

class CatalogService:
    def __init__(self):
        self.client = Client()

    def fetch_catalog_page(self, page_number: int):
        url = f"{self.client.base_url}{CATALOG_ENDPOINT}"
        params = {"page": page_number}
        return self.client.get_json(url, params)

    def fetch_all_catalog_pages(self):
        pages = []
        for page_number in range(1, 3):  # Example: Fetch 2 pages
            pages.append(self.fetch_catalog_page(page_number))
        return pages