import argparse
from src.services.report_service import ReportService
from src.utils.io import IO

def main() -> None:
    parser = argparse.ArgumentParser(description="Data Harvester CLI")
    parser.add_argument("--output", type=str, default="report.txt", help="Output file for the report")
    args = parser.parse_args()

    report_service = ReportService()
    report = report_service.generate_report()

    IO.write_file(args.output, str(report))
    print(f"Report written to {args.output}")

if __name__ == "__main__":
    main()