from src.http_client import get_stream, Client
from src.utils.io import IO
from src.services.user_service import UserService
from src.services.catalog_service import CatalogService

REPORT_ENDPOINT = "/reports"

class ReportService:
    def __init__(self):
        self.user_service = UserService()
        self.catalog_service = CatalogService()
        self.io = IO()

    # def generate_report(self):
    #     users = self.user_service.get_users()
    #     catalog = self.catalog_service.fetch_all_catalog_pages()
    #     return {
    #         "users": users,
    #         "catalog": catalog
    #     }

    def download_daily_report(self, base_url: str, dest_path: str = "report.txt") -> None:
        url = f"{base_url}{REPORT_ENDPOINT}/daily"
        stream = get_stream(url)
        self.io.save_stream(stream, dest_path)
        # print(stream)

    def download_with_client(self, base_url: str, dest_path: str) -> None:
        client = Client(base_url=base_url)
        try:
            stream = client.get_stream(REPORT_ENDPOINT)
            self.io.save_stream(stream, dest_path)
            # print(stream)
        finally:
            client.close()