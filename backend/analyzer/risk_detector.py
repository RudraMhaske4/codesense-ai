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
                recommendations = []
                complexity = function.get("complexity", 1)
                length = function.get("length", 0)
                arguments = function.get("arguments", 0)
                if complexity > 10:
                    reasons.append("High cyclomatic complexity")
                    recommendations.append(
                        "Break the function into smaller functions "
                        "and simplify conditional logic."
                    )
                if length > 50:
                    reasons.append("Long function")
                    recommendations.append(
                        "Split the function into smaller, "
                        "focused functions."
                    )
                if arguments > 5:
                    reasons.append("Too many arguments")
                    recommendations.append(
                        "Group related arguments into a "
                        "configuration object or data class."
                    )
                if not reasons:
                    continue
                severity = (
                    "High" if complexity > 10
                    else "Medium"
                )
                risks.append({
                    "file": result["file"],
                    "function": function["name"],
                    "severity": severity,
                    "complexity": complexity,
                    "length": length,
                    "arguments": arguments,
                    "reasons": reasons,
                    "recommendations": recommendations
                })
        return risks