# decision.py
# Purpose: Applies rule-based threshold logic to determine adaptive mode
# (normal, deeper_probe, advanced) based on stability score.
# Primary Owner: Sabyasachi Hazra

# agent/decision.py

class DecisionEngine:
    """
    Applies rule-based threshold logic to determine
    adaptive questioning mode based on stability score.
    """

    def __init__(self,
                 low_threshold=40,
                 mid_threshold=70,
                 high_threshold=85):
        
        self.low = low_threshold
        self.mid = mid_threshold
        self.high = high_threshold


    def evaluate(self, stability_score):
        """
        Determines next mode based on stability score.
        """

        if stability_score < self.low:
            return "deeper_probe"

        elif self.low <= stability_score < self.mid:
            return "normal"

        elif self.mid <= stability_score < self.high:
            return "normal"

        else:
            return "advanced"


    def classify_level(self, stability_score):
        """
        Optional: Returns descriptive interpretation.
        Useful for UI display.
        """

        if stability_score < self.low:
            return "Fundamental Misunderstanding"

        elif self.low <= stability_score < self.mid:
            return "Surface-Level Stability"

        elif self.mid <= stability_score < self.high:
            return "Moderate Conceptual Depth"

        else:
            return "Strong Conceptual Stability"