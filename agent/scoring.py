# scoring.py
# Purpose: Computes the Concept Stability Index by combining semantic similarity,
# structural depth checks, and response balance into a weighted heuristic score.
# Primary Owner: Sabyasachi Hazra

# agent/scoring.py

import numpy as np


class StabilityScorer:
    """
    Computes Concept Stability Index using:
    - Semantic similarity
    - Structural depth heuristic
    - Response balance consistency
    """

    def __init__(self):
        self.reasoning_markers = [
            "because", "if", "when",
            "therefore", "so that"
        ]
        self.min_word_threshold = 20


    # -------------------------------
    # Public API
    # -------------------------------

    def compute(self,
                cross_similarity,
                reference_similarity,
                answers_list):
        """
        Returns final stability score (0–100).
        """

        semantic_score = self._semantic_component(
            cross_similarity,
            reference_similarity
        )

        structural_score = self._structural_component(
            answers_list
        )

        balance_score = self._balance_component(
            answers_list
        )

        final_score = (
            0.5 * semantic_score +
            0.3 * structural_score +
            0.2 * balance_score
        )

        return round(final_score, 2)


    # -------------------------------
    # Components
    # -------------------------------

    def _semantic_component(self,
                            cross_similarity,
                            reference_similarity):
        """
        Combines cross-answer and reference similarity.
        Input expected in 0–1 range.
        Output scaled to 0–100.
        """

        semantic = 0.5 * cross_similarity + \
                   0.5 * reference_similarity

        return semantic * 100


    def _structural_component(self, answers_list):
        """
        Evaluates depth heuristics:
        - Minimum word threshold
        - Presence of reasoning markers
        """

        scores = []

        for answer in answers_list:
            words = answer.split()
            word_count = len(words)

            # Word threshold score
            if word_count >= self.min_word_threshold:
                word_score = 1
            else:
                word_score = word_count / self.min_word_threshold

            # Reasoning marker score
            marker_hits = sum(
                marker in answer.lower()
                for marker in self.reasoning_markers
            )

            marker_score = min(marker_hits / 2, 1)

            combined = 0.6 * word_score + 0.4 * marker_score
            scores.append(combined)

        return np.mean(scores) * 100


    def _balance_component(self, answers_list):
        """
        Measures response length consistency.
        Lower variance → higher stability.
        """

        word_counts = [len(a.split()) for a in answers_list]

        if len(word_counts) < 2:
            return 100  # No variance possible

        variance = np.var(word_counts)

        # Normalize variance impact
        normalized = 1 / (1 + variance / 50)

        return normalized * 100