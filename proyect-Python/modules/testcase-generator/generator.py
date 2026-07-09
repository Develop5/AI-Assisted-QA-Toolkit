"""
AI-Assisted Test Case Generator (with RAG Integration)
------------------------------------------------------

This module provides a functional implementation of an AI-powered
test case generator. It takes raw requirements as input and produces
structured test cases using an LLM backend.

Now enhanced with RAG (Retrieval-Augmented Generation), the generator
retrieves relevant QA documentation and injects it into the prompt,
ensuring that generated test cases follow internal QA standards.

Extended Description
--------------------
This module performs the following functions:

- Reads raw requirements provided as plain text.
- Retrieves relevant QA documentation using the RAG engine.
- Builds an optimized prompt combining requirements + documentation.
- Sends the prompt to an LLM backend (OpenAI) to generate structured test cases.
- Returns test cases in JSON format.
- Converts JSON output into Python objects using the TestCase dataclass.
- Includes an executable example.
- Fully functional: requires OPENAI_API_KEY.

Author: AI-Assisted QA Lead (in transition)
"""

import os
from typing import List
from dataclasses import dataclass

try:
    from openai import OpenAI
except ImportError:
    raise ImportError("Install with: pip install openai")

# Import RAG engine
from modules.rag_docs.rag_docs import QARAGEngine


# -----------------------------
# Data Models
# -----------------------------

@dataclass
class TestCase:
    id: str
    title: str
    steps: List[str]
    expected_result: str


# -----------------------------
# LLM Client Wrapper
# -----------------------------

class LLMClient:
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
# Test Case Generator (with RAG)
# -----------------------------

class TestCaseGenerator:
    """
    Generates structured test cases from raw requirements using an LLM,
    enhanced with RAG-based QA documentation retrieval.
    """

    def __init__(self, model: str = "gpt-4o-mini", docs_path: str = "docs/qa/"):
        self.llm = LLMClient(model=model)
        self.rag = QARAGEngine(docs_path=docs_path)

    def generate_testcases(self, requirements: str) -> List[TestCase]:
        # Retrieve relevant QA documentation
        retrieved_docs = self.rag.retrieve(requirements)

        # Build prompt with documentation context
        prompt = self._build_prompt(requirements, retrieved_docs)

        raw_output = self.llm.generate(prompt)
        return self._parse_output(raw_output)

    def _build_prompt(self, requirements: str, docs: List[str]) -> str:
        docs_context = "\n\n".join(docs)

        return f"""
You are an expert QA engineer. Use the following QA documentation to guide your test case creation:

--- QA Documentation Context ---
{docs_context}
--------------------------------

Convert the following requirements into structured test cases.

Use this JSON format:

[
  {{
    "id": "TC-001",
    "title": "Short descriptive title",
    "steps": ["Step 1", "Step 2", ...],
    "expected_result": "Expected outcome"
  }}
]

Requirements:
{requirements}
"""

    def _parse_output(self, raw_output: str) -> List[TestCase]:
        import json

        try:
            data = json.loads(raw_output)
        except json.JSONDecodeError:
            raise ValueError("LLM returned invalid JSON. Raw output:\n" + raw_output)

        testcases = []
        for item in data:
            tc = TestCase(
                id=item.get("id", "TC-UNKNOWN"),
                title=item.get("title", "Untitled"),
                steps=item.get("steps", []),
                expected_result=item.get("expected_result", ""),
            )
            testcases.append(tc)

        return testcases


# -----------------------------
# Example Usage
# -----------------------------

if __name__ == "__main__":
    generator = TestCaseGenerator(docs_path="docs/qa/")

    requirements_text = """
    Users must be able to reset their password using email verification.
    """

    testcases = generator.generate_testcases(requirements_text)

    print("\nGenerated Test Cases:\n")
    for tc in testcases:
        print(f"ID: {tc.id}")
        print(f"Title: {tc.title}")
        print("Steps:")
        for step in tc.steps:
            print(f"  - {step}")
        print(f"Expected Result: {tc.expected_result}")
        print("-" * 40)
