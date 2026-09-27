class QualityScorer:
    def __init__(self, risks):
        self.risks = risks
    def calculate(self):
        score = 100
        high_risks = sum(
            1 for risk in self.risks
            if risk["severity"] == "High"
        )
        medium_risks = sum(
            1 for risk in self.risks
            if risk["severity"] == "Medium"
        )
        score -= high_risks * 15
        score -= medium_risks * 5
        score = max(0, min(100, score))
        if score >= 85:
            rating = "Good"
        elif score >= 60:
            rating = "Moderate"
        else:
            rating = "Needs Improvement"
        return {
            "quality_score": score,
            "rating": rating,
            "high_risks": high_risks,
            "medium_risks": medium_risks
        }