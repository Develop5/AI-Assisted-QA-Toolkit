"""
Security RAG Integration — Regression Optimizer Enhancement
-----------------------------------------------------------

This integration extends the Regression Optimizer with security-aware
context using a Retrieval-Augmented Generation (RAG) engine. The optimizer
now retrieves relevant security documentation (AppSec standards, DevSecOps
pipeline rules, API security standards, IAM governance, secrets management,
SAST/DAST policies, SBOM rules, and security risk matrices) and injects that
knowledge directly into the LLM prompt.

What this integration provides
------------------------------
By combining test metadata with security documentation, the Regression
Optimizer becomes capable of:

1. Identifying security-critical tests that must remain in regression.
2. Detecting missing security coverage (e.g., authentication, authorization,
   rate limiting, secrets rotation, dependency vulnerabilities).
3. Prioritizing tests based on security risk factors such as exploitability,
   exposure, and privilege escalation potential.
4. Recommending new security-focused regression tests.
5. Producing regression decisions aligned with AppSec and DevSecOps standards.

Example
-------
Given test metadata related to authentication or API endpoints, the optimizer
can now:
- classify tests as "security-critical"
- recommend keeping them in regression
- suggest additional tests such as:
      "Add a test validating token expiration"
      "Add a test validating RBAC enforcement"
      "Add a test validating rate limiting on sensitive endpoints"

This makes the regression suite more robust and aligned with real-world
security practices.
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
    security_context_used: bool


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


class RegressionOptimizer:
    """
    Optimizes regression suites using LLM + Security RAG context.
    """

    def __init__(self, model: str = "gpt-4o-mini", security_docs_path: str = "docs/security/"):
        self.llm = LLMClient(model=model)
        self.rag = QARAGEngine(docs_path=security_docs_path)

    def optimize(self, tests: List[TestMetadata]) -> RegressionRecommendation:
        metadata_text = "\n".join(
            f"{t.id}: {t.title} | tags={t.tags} | component={t.component}"
            for t in tests
        )

        security_chunks = self.rag.retrieve(metadata_text)

        prompt = self._build_prompt(metadata_text, security_chunks)
        raw_output = self.llm.generate(prompt)

        return self._parse_output(raw_output, security_chunks_used=len(security_chunks) > 0)

    def _build_prompt(self, metadata: str, security_docs: List[str]) -> str:
        docs_block = "\n\n".join(security_docs)

        return f"""
You are an expert QA + Security engineer.

Use the following Security documentation to guide regression optimization:

--- Security Documentation Context ---
{docs_block}
-------------------------------------

Test metadata:
{metadata}

Return JSON with:
- tests_to_keep
- tests_to_remove
- tests_to_review
- suggested_new_tests
- summary
"""

    def _parse_output(self, raw_output: str, security_chunks_used: bool) -> RegressionRecommendation:
        import json
        data = json.loads(raw_output)

        return RegressionRecommendation(
            tests_to_keep=data.get("tests_to_keep", []),
            tests_to_remove=data.get("tests_to_remove", []),
            tests_to_review=data.get("tests_to_review", []),
            suggested_new_tests=data.get("suggested_new_tests", []),
            summary=data.get("summary", ""),
            security_context_used=security_chunks_used
        )
