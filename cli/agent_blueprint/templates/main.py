"""
Author: IBM Research – Mellea Agent Team
Maintainer: Mellea Agent – IBM Research

Purpose:
Minimal demonstration agent using the Double Round Robin (DRR) engine
for robust pairwise comparison between multiple candidate outputs.

How to run:
-------------------------------------
python main.py "your question"
-------------------------------------

Example:
-------------------------------------
python main.py "Find the most likely root-cause among items."
-------------------------------------

This file shows how to:
1. Start a Mellea session.
2. Generate multiple candidate answers.
3. Use DRR for robust pairwise selection.
4. Print the final chosen result.

This is intentionally minimal for blueprint adoption.
"""

import sys
import os
import typer

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from double_round_robin import double_round_robin
from mellea import start_session
from mellea.helpers.fancy_logger import FancyLogger

FancyLogger.get_logger().setLevel("WARNING")


def generate_candidates(query: str, m):
    prompts = [
        f"Answer concisely:\n{query}",
        f"Provide a helpful explanation:\n{query}",
        f"Explain like I'm 12:\n{query}"
    ]

    candidates = []
    for p in prompts:
        resp = m.instruct(p)
        candidates.append(resp.value)
    return candidates


def run_agent(query: str):
    m = start_session()

    candidates = generate_candidates(query, m)

    comparison_prompt = """
    Select which option is more accurate, helpful, and relevant to the user's query.
    Pick the stronger answer.
    """

    results = double_round_robin(
        items=candidates,
        comparison_prompt=comparison_prompt,
        m=m,
        context=None,
    )

    best_answer, best_score = results[0]

    typer.echo("\n=== FINAL SELECTED ANSWER ===\n")
    typer.echo(best_answer)
    typer.echo(f"\n(score = {best_score})\n")


def cli(query: str = typer.Argument(..., help="User query to evaluate using DRR agent")):
    run_agent(query)


if __name__ == "__main__":
    typer.run(cli)
