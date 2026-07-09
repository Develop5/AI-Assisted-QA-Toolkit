"""
AI-Assisted Test Case Generator
-------------------------------

This module provides a functional implementation of an AI-powered
test case generator. It takes raw requirements as input and produces
structured test cases using an LLM backend.

The design is intentionally simple and extensible so it can evolve
into more advanced versions (RAG, domain fine-tuning, multi-model support).

Extended Description
--------------------
This module performs the following functions:

- It reads raw requirements provided as plain text.
- It builds an optimized prompt designed to extract structured test cases.
- It sends the prompt to an LLM backend (OpenAI) to generate the test cases.
- It returns the test cases in structured JSON format.
- It converts the JSON output into Python objects using the TestCase dataclass.
- It includes an executable example demonstrating how the module works.
- It is fully functional: if you have your OPENAI_API_KEY set in the environment,
  you can run it immediately.

Author: AI-Assisted QA Lead
"""


import os
from typing import List, Dict
from dataclasses import dataclass

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
class TestCase:
    id: str
    title: str
    steps: List[str]
    expected_result: str


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
# Test Case Generator
# -----------------------------

class TestCaseGenerator:
    """
    Generates structured test cases from raw requirements using an LLM.
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        self.llm = LLMClient(model=model)

    def generate_testcases(self, requirements: str) -> List[TestCase]:
        prompt = self._build_prompt(requirements)
        raw_output = self.llm.generate(prompt)
        return self._parse_output(raw_output)

    def _build_prompt(self, requirements: str) -> str:
        return f"""
You are an expert QA engineer. Convert the following requirements into
structured test cases. Use the following JSON format:

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
    generator = TestCaseGenerator()

    requirements_text = """
    Users must be able to log in using email and password.
    If credentials are invalid, an error message must be displayed.
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
