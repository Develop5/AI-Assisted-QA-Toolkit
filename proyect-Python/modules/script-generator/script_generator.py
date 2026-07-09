"""
Security RAG Integration — Script Generator Enhancement
-------------------------------------------------------

This integration extends the Script Generator with security-aware context
using a Retrieval-Augmented Generation (RAG) engine. The generator now
retrieves relevant security documentation (AppSec standards, API security
rules, secure coding guidelines, secrets management policies, SAST/DAST
standards, IAM governance, and more) and injects that knowledge directly
into the LLM prompt.

What this integration provides
------------------------------
By combining test case steps with security documentation, the Script Generator
becomes capable of:

1. Producing automated scripts that follow secure coding practices.
2. Adding security validations such as:
   - authentication checks
   - authorization enforcement
   - rate limiting validation
   - secure input handling
   - token expiration checks
3. Avoiding insecure automation patterns (e.g., logging secrets).
4. Generating scripts aligned with AppSec and DevSecOps standards.

Example
-------
Given a test case involving login or API calls, the generator can now:
- add assertions validating token integrity
- avoid logging sensitive data
- enforce secure selectors
- validate error messages do not leak information

This results in more secure and production-ready automated scripts.
"""

import os
from dataclasses import dataclass
from typing import List

try:
    from openai import OpenAI
except ImportError:
    raise ImportError("Install with: pip install openai")

from modules.rag_docs.rag_docs import QARAGEngine


@dataclass
class TestCase:
    id: str
    title: str
    steps: List[str]
    expected_result: str


class LLMClient:
    def __init__(self, model: str = "gpt-4o-mini"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY missing.")
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return response.choices[0].message.content


class ScriptGenerator:
    """
    Generates Playwright/Cypress scripts using LLM + Security RAG context.
    """

    def __init__(self, framework: str = "playwright", model: str = "gpt-4o-mini", security_docs_path: str = "docs/security/"):
        self.framework = framework
        self.llm = LLMClient(model=model)
        self.rag = QARAGEngine(docs_path=security_docs_path)

    def generate_script(self, test_case: TestCase) -> str:
        tc_text = f"{test_case.id}: {test_case.title}\nSteps: {test_case.steps}\nExpected: {test_case.expected_result}"

        security_chunks = self.rag.retrieve(tc_text)

        prompt = self._build_prompt(test_case, security_chunks)
        return self.llm.generate(prompt)

    def _build_prompt(self, test_case: TestCase, security_docs: List[str]) -> str:
        docs_block = "\n\n".join(security_docs)

        return f"""
You are an expert QA Automation + Security engineer.

Use the following Security documentation to guide script generation:

--- Security Documentation Context ---
{docs_block}
-------------------------------------

Framework: {self.framework}

Generate a secure automated script for this test case:

ID: {test_case.id}
Title: {test_case.title}
Steps: {test_case.steps}
Expected Result: {test_case.expected_result}

Ensure the script:
- follows secure coding guidelines
- avoids logging sensitive data
- validates authentication/authorization when relevant
- handles errors securely
- uses stable selectors
"""

