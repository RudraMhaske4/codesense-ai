from backend.analyzer.python_analyzer import PythonAnalyzer
analyzer = PythonAnalyzer("data/sample.py")
result = analyzer.analyze()
print(result)