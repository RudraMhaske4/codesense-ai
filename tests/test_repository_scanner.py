from backend.analyzer.repository_scanner import RepositoryScanner
repository_path = "data/test_repository"
scanner = RepositoryScanner(repository_path)
results = scanner.scan()
for result in results:
    print(result)