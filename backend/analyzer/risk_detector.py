class RiskDetector:
    def __init__(self, scan_results):
        self.scan_results = scan_results
    def analyze(self):
        risks = []
        for result in self.scan_results:
            if "error" in result:
                continue
            for function in result.get("functions", []):
                reasons = []
                complexity = function.get("complexity", 1)
                length = function.get("length", 0)
                arguments = function.get("arguments", 0)
                if complexity > 10:
                    reasons.append("High cyclomatic complexity")
                if length > 50:
                    reasons.append("Long function")
                if arguments > 5:
                    reasons.append("Too many arguments")
                if reasons:
                    risks.append({
                        "file": result["file"],
                        "function": function["name"],
                        "risk": (
                            "High" if complexity > 10
                            else "Medium"
                        ),
                        "reasons": reasons
                    })
        return risks