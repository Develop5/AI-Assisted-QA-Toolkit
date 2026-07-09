"""
AI-Assisted Regression Optimizer
--------------------------------

This module provides a functional implementation of an AI-powered
regression test suite optimizer. It takes metadata about test cases
and produces recommendations for cleanup, deduplication, and risk-based
prioritization using an LLM backend.

The design is intentionally simple and extensible so it can evolve
into more advanced versions (embeddings-based similarity, historical failure data, multi-model support).

Extended Description
--------------------
This module performs the following functions:

- It reads test suite metadata (IDs, titles, tags, components, etc.).
- It builds an optimized prompt to detect duplicates, obsolete tests, and gaps.
- It sends the prompt to an LLM backend (OpenAI) to generate recommendations.
- It returns structured suggestions for which tests to keep, remove, or add.
- It includes an executable example demonstrating how the module works.
- It is fully functional: if you have your OPENAI_API_KEY set in the environment,
  you can run it immediately.

Author: AI-Assisted QA Lead (in transition)
"""

import os
from dataclasses import dataclass
from typing import List

try:
    from openai import OpenAI
except ImportError:
    raise ImportError(
        "The 'openai' package is required. Install it with: pip install openai"
    )


# -----------------------------
# Data Models
# -----------------------------

@dataclass
class TestMetadata:
    id: str
    title: str
    tags: List[str]
    component: str


@dataclass
class RegressionRecommendation:
    tests_to_keep: List[str]
    tests_to_remove: List[str]
    tests_to_review: List[str]
    suggested_new_tests: List[str]
    summary: str


# -----------------------------
# LLM Client Wrapper
# -----------------------------

class LLMClient:
    """
    Wrapper around the OpenAI client to keep the module decoupled
    from the underlying provider. This allows future replacement
    with Azure OpenAI or local models.
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Environment variable OPENAI_API_KEY is missing.")

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return response.choices[0].message.content


# -----------------------------
# Regression Optimizer
# -----------------------------

class RegressionOptimizer:
    """
    Uses an LLM to analyze test suite metadata and recommend
    regression suite optimizations.
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        self.llm = LLMClient(model=model)

    def optimize(self, tests: List[TestMetadata]) -> RegressionRecommendation:
        prompt = self._build_prompt(tests)
        raw_output = self.llm.generate(prompt)
        return self._parse_output(raw_output)

    def _build_prompt(self, tests: List[TestMetadata]) -> str:
        tests_block = "\n".join(
            [
                f"- ID: {t.id}, Title: {t.title}, Tags: {', '.join(t.tags)}, Component: {t.component}"
                for t in tests
            ]
        )

        return f"""
You are an expert QA lead specializing in regression optimization.

You are given a list of test cases with metadata (ID, title, tags, component).
Analyze them and return a JSON object with the following fields:

- tests_to_keep: list of test IDs that should remain in the regression suite
- tests_to_remove: list of test IDs that are redundant or obsolete
- tests_to_review: list of test IDs that need human review (e.g., unclear, overlapping)
- suggested_new_tests: list of short descriptions of new tests that should be added
- summary: short explanation of the optimization strategy

Test Suite Metadata:
{tests_block}

Return ONLY valid JSON, no explanations.
"""

    def _parse_output(self, raw_output: str) -> RegressionRecommendation:
        import json

        try:
            data = json.loads(raw_output)
        except json.JSONDecodeError:
            raise ValueError("LLM returned invalid JSON. Raw output:\n" + raw_output)

        return RegressionRecommendation(
            tests_to_keep=data.get("tests_to_keep", []),
            tests_to_remove=data.get("tests_to_remove", []),
            tests_to_review=data.get("tests_to_review", []),
            suggested_new_tests=data.get("suggested_new_tests", []),
            summary=data.get("summary", ""),
        )


# -----------------------------
# Example Usage
# -----------------------------

if __name__ == "__main__":
    tests = [
        TestMetadata(
            id="TC-001",
            title="Valid login",
            tags=["smoke", "auth"],
            component="authentication",
        ),
        TestMetadata(
            id="TC-002",
            title="Invalid login - wrong password",
            tags=["regression", "auth"],
            component="authentication",
        ),
        TestMetadata(
            id="TC-003",
            title="Password reset flow",
            tags=["regression", "account"],
            component="account-management",
        ),
        TestMetadata(
            id="TC-004",
            title="Legacy login page",
            tags=["legacy", "auth"],
            component="authentication",
        ),
    ]

    optimizer = RegressionOptimizer()
    recommendation = optimizer.optimize(tests)

    print("\nRegression Optimization Result:\n")
    print(f"Tests to keep: {recommendation.tests_to_keep}")
    print(f"Tests to remove: {recommendation.tests_to_remove}")
    print(f"Tests to review: {recommendation.tests_to_review}")
    print("Suggested new tests:")
    for t in recommendation.suggested_new_tests:
        print(f"  - {t}")
    print(f"\nSummary: {recommendation.summary}")
