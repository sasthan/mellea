"""
Minimal test for the example DRR agent.

This test:
1. Starts a Mellea session
2. Runs the agent with a simple everyday question
3. Ensures that the agent returns a non-empty answer
4. Prints the selected result

"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mellea import start_session
from mellea.helpers.fancy_logger import FancyLogger

from main import generate_candidates
from double_round_robin import double_round_robin

FancyLogger.get_logger().setLevel("WARNING")


def test_full_agent():
    m = start_session()

    query = "What is the capital of France?"

    # Step 1: generate candidates using the agent's logic
    candidates = generate_candidates(query, m)

    # Step 2: run DRR selection
    comparison_prompt = """
    Select which option is more accurate and helpful 
    as an answer to the user's question.
    """

    results = double_round_robin(
        items=candidates,
        comparison_prompt=comparison_prompt,
        m=m,
        context=None
    )

    best_answer, best_score = results[0]

    print("\n=== TEST AGENT RESULT ===\n")
    print(best_answer)
    print(f"\n(score = {best_score})")

    assert isinstance(best_answer, str)
    assert len(best_answer.strip()) > 0
    assert isinstance(best_score, int)


if __name__ == "__main__":
    test_full_agent()
