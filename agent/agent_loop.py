# agent_loop.py
# Purpose: Orchestrates the complete agent cycle: question generation,
# evaluation, scoring, and adaptive decision making.
# Primary Owner: Sabyasachi Hazra

# agent/agent_loop.py

from datetime import datetime

class AgentLoop:

    def __init__(self, question_generator, embedding_engine, scorer, decision_engine, database):

        self.qg = question_generator
        self.embed = embedding_engine
        self.scorer = scorer
        self.decision = decision_engine
        self.db = database


    def run(self, topic, user_answer, mode="normal"):
        """
        Executes one complete agent cycle.
        """

        # 1 Generate Question
        question = self.qg.generate(topic, mode)

        # 2 Convert answer to embedding
        user_vector = self.embed.get_embedding(user_answer)

        # 3 Get reference explanation + embedding
        reference_text = self.qg.generate_reference(topic)
        reference_vector = self.embed.get_embedding(reference_text)

        # 4 Compute similarity metrics
        cross_similarity = self.embed.compute_cross_similarity(user_answer)
        reference_similarity = self.embed.cosine_similarity(
            user_vector, reference_vector
        )

        # 5 Compute stability score
        stability_score = self.scorer.compute(
            cross_similarity=cross_similarity,
            reference_similarity=reference_similarity,
            answer=user_answer
        )

        # 6 Decide next mode
        next_mode = self.decision.evaluate(stability_score)

        # 7 Store session
        self.db.save_session(
            topic=topic,
            score=stability_score,
            timestamp=datetime.now(),
            mode=next_mode
        )

        return {
            "question": question,
            "score": stability_score,
            "next_mode": next_mode
        }