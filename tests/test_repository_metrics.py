from backend.analyzer.repository_scanner import RepositoryScanner
from backend.analyzer.repository_metrics import RepositoryMetrics
repository_path = "data/test_repository"
scanner = RepositoryScanner(repository_path)
scan_results = scanner.scan()
metrics = RepositoryMetrics(scan_results)
summary = metrics.calculate()
print("\nRepository Metrics")
print("------------------")
for key, value in summary.items():
    print(f"{key}: {value}")