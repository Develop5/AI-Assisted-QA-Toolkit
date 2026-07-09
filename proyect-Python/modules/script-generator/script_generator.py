"""
AI-Assisted Test Script Generator
---------------------------------

This module generates automated test scripts (Playwright or Cypress)
from structured test cases using an LLM backend.

It is designed to be the second functional block of the
AI-Assisted-QA-Toolkit.

This module performs the following functions:
- It receives a TestCase object (the same dataclass used in the previous module).
- It builds an optimized prompt for either Playwright or Cypress based on the selected framework.
- It sends the prompt to an LLM backend to generate the automation script.
- It returns a complete, ready-to-use automated test script.
- It includes an executable example demonstrating how to use the module.
- It is fully functional: if you have your OPENAI_API_KEY set in the environment, you can run it immediately.


Author: AI-Assisted QA Lead 
"""

import os
from typing import List
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
# Script Generator
# -----------------------------

class ScriptGenerator:
    """
    Generates Playwright or Cypress scripts from structured test cases.
    """

    def __init__(self, model: str = "gpt-4o-mini", framework: str = "playwright"):
        if framework not in ["playwright", "cypress"]:
            raise ValueError("Framework must be 'playwright' or 'cypress'.")

        self.framework = framework
        self.llm = LLMClient(model=model)

    def generate_script(self, test_case: TestCase) -> str:
        prompt = self._build_prompt(test_case)
        return self.llm.generate(prompt)

    def _build_prompt(self, test_case: TestCase) -> str:
        return f"""
You are an expert QA automation engineer.

Generate a {self.framework} automated test script based on the following test case:

Test Case ID: {test_case.id}
Title: {test_case.title}

Steps:
{self._format_steps(test_case.steps)}

Expected Result:
{test_case.expected_result}

Requirements:
- Use best practices for {self.framework}.
- Use clear selectors.
- Add comments explaining each step.
- Do NOT invent steps; use only the provided ones.
"""

    def _format_steps(self, steps: List[str]) -> str:
        return "\n".join([f"- {step}" for step in steps])


# -----------------------------
# Example Usage
# -----------------------------

if __name__ == "__main__":
    tc = TestCase(
        id="TC-001",
        title="Valid login",
        steps=[
            "Navigate to login page",
            "Enter valid email",
            "Enter valid password",
            "Click login button"
        ],
        expected_result="User is redirected to the dashboard"
    )

    generator = ScriptGenerator(framework="playwright")
    script = generator.generate_script(tc)

    print("\nGenerated Script:\n")
    print(script)
