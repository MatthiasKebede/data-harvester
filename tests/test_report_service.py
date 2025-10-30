import pytest
from src.services.report_service import ReportService

@pytest.fixture
def report_service():
    return ReportService()

def test_generate_report(report_service):
    report = report_service.generate_report()
    assert "users" in report
    assert "catalog" in report