import unittest
from backend.analyzer.risk_detector import RiskDetector
class TestRiskDetector(unittest.TestCase):
    def test_detect_high_complexity(self):
        scan_results = [
            {
                "file": "sample.py",
                "functions": [
                    {
                        "name": "complex_function",
                        "complexity": 12,
                        "length": 20,
                        "arguments": 2
                    }
                ]
            }
        ]
        detector = RiskDetector(scan_results)
        risks = detector.analyze()
        self.assertEqual(len(risks), 1)
        self.assertEqual(risks[0]["severity"], "High")
        self.assertIn(
            "High cyclomatic complexity",
            risks[0]["reasons"]
        )
    def test_detect_long_function(self):
        scan_results = [
            {
                "file": "sample.py",
                "functions": [
                    {
                        "name": "long_function",
                        "complexity": 2,
                        "length": 60,
                        "arguments": 2
                    }
                ]
            }
        ]
        detector = RiskDetector(scan_results)
        risks = detector.analyze()
        self.assertEqual(len(risks), 1)
        self.assertIn(
            "Long function",
            risks[0]["reasons"]
        )
    def test_detect_too_many_arguments(self):
        scan_results = [
            {
                "file": "sample.py",
                "functions": [
                    {
                        "name": "many_arguments",
                        "complexity": 2,
                        "length": 10,
                        "arguments": 6
                    }
                ]
            }
        ]
        detector = RiskDetector(scan_results)
        risks = detector.analyze()
        self.assertEqual(len(risks), 1)
        self.assertIn(
            "Too many arguments",
            risks[0]["reasons"]
        )
    def test_no_risks(self):
        scan_results = [
            {
                "file": "sample.py",
                "functions": [
                    {
                        "name": "simple_function",
                        "complexity": 2,
                        "length": 10,
                        "arguments": 2
                    }
                ]
            }
        ]
        detector = RiskDetector(scan_results)
        risks = detector.analyze()
        self.assertEqual(risks, [])
    def test_multiple_risks_in_one_function(self):
        scan_results = [
            {
                "file": "sample.py",
                "functions": [
                    {
                        "name": "risky_function",
                        "complexity": 12,
                        "length": 60,
                        "arguments": 6
                    }
                ]
            }
        ]
        detector = RiskDetector(scan_results)
        risks = detector.analyze()
        self.assertEqual(len(risks), 1)
        self.assertEqual(risks[0]["severity"], "High")
        self.assertEqual(len(risks[0]["reasons"]), 3)
if __name__ == "__main__":
    unittest.main()