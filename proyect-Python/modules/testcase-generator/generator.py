"""
Security RAG Integration — Test Case Generator Enhancement
----------------------------------------------------------

This integration extends the Test Case Generator with security-aware context
using a Retrieval-Augmented Generation (RAG) engine. The generator now retrieves
relevant security documentation (AppSec standards, API security rules, secure
coding guidelines, secrets management policies, IAM governance, SAST/DAST
standards, and more) and injects that knowledge directly into the LLM prompt.

What this integration provides
------------------------------
By combining raw requirements with security documentation, the Test Case
Generator becomes capable of:

1. Producing test cases that include security validations.
2. Detecting missing security requirements such as:
   - authentication
   - authorization
   - rate limiting
   - secrets protection
   - secure input handling
3. Generating additional security-focused test cases.
4. Aligning test cases with AppSec and DevSecOps standards.

Example
-------
Given requirements involving user login or API calls, the generator can now:
- add test cases validating token expiration
- add test cases validating RBAC enforcement
- add negative tests for invalid payloads
- add tests validating secure error messages

This results in more complete and security-aligned test coverage.
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


class TestCaseGenerator:
    """
    Generates test cases using LLM + Security RAG context.
    """

    def __init__(self, model: str = "gpt-4o-mini", security_docs_path: str = "docs/security/"):
        self.llm = LLMClient(model=model)
        self.rag = QARAGEngine(docs_path=security_docs_path)

    def generate_testcases(self, requirements: str) -> List[TestCase]:
        security_chunks = self.rag.retrieve(requirements)

        prompt = self._build_prompt(requirements, security_chunks)
        raw_output = self.llm.generate(prompt)

        return self._parse_output(raw_output)

    def _build_prompt(self, requirements: str, security_docs: List[str]) -> str:
        docs_block = "\n\n".join(security_docs)

        return f"""
You are an expert QA + Security engineer.

Use the following Security documentation to guide test case creation:

--- Security Documentation Context ---
{docs_block}
-------------------------------------

Convert the following requirements into structured test cases.

Requirements:
{requirements}

Return JSON with:
- id
- title
- steps
- expected_result
"""

    def _parse_output(self, raw_output: str) -> List[TestCase]:
        import json
        data = json.loads(raw_output)

        return [
            TestCase(
                id=item.get("id", "TC-UNKNOWN"),
                title=item.get("title", "Untitled"),
                steps=item.get("steps", []),
                expected_result=item.get("expected_result", "")
            )
            for item in data
        ]
