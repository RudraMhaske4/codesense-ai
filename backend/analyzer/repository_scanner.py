from pathlib import Path
from backend.analyzer.python_analyzer import PythonAnalyzer
class RepositoryScanner:
    def __init__(self, repository_path):
        self.repository_path = Path(repository_path)
    def find_python_files(self):
        return list(self.repository_path.rglob("*.py"))
    def scan(self):
        python_files = self.find_python_files()
        results = []
        for file_path in python_files:
            try:
                analyzer = PythonAnalyzer(file_path)
                result = analyzer.analyze()
                results.append(result)
            except Exception as error:
                results.append({
                    "file": str(file_path),
                    "error": str(error)
                })
        return results