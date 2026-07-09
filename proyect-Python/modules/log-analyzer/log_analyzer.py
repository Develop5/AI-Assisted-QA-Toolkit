"""
AI-Assisted Log & Error Analyzer
--------------------------------

This module provides a functional implementation of an AI-powered
log and error analyzer. It takes raw logs or error messages as input
and produces structured insights using an LLM backend.

The design is intentionally simple and extensible so it can evolve
into more advanced versions (RAG, embeddings-based clustering, multi-model support).

Extended Description
--------------------
This module performs the following functions:

- It reads raw logs, stack traces, or error messages as plain text.
- It builds an optimized prompt to classify, summarize, and analyze the issues.
- It sends the prompt to an LLM backend (OpenAI) to generate insights.
- It returns structured analysis including category, severity, and suggested root cause.
- It includes an executable example demonstrating how the module works.
- It is fully functional: if you have your OPENAI_API_KEY set in the environment,
  you can run it immediately.

Author: AI-Assisted QA Lead (in transition)
"""

import os
from dataclasses import dataclass
from typing import Optional

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
class LogAnalysisResult:
    category: str
    severity: str
    summary: str
    probable_root_cause: str
    suggested_next_steps: str


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
            temperature=0.1,
        )
        return response.choices[0].message.content


# -----------------------------
# Log Analyzer
# -----------------------------

class LogAnalyzer:
    """
    Analyzes logs and errors using an LLM to provide structured insights.
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        self.llm = LLMClient(model=model)

    def analyze(self, raw_logs: str, context: Optional[str] = None) -> LogAnalysisResult:
        prompt = self._build_prompt(raw_logs, context)
        raw_output = self.llm.generate(prompt)
        return self._parse_output(raw_output)

    def _build_prompt(self, raw_logs: str, context: Optional[str]) -> str:
        context_block = f"\nContext:\n{context}\n" if context else ""
        return f"""
You are an expert QA and reliability engineer.

Analyze the following logs and errors and return a JSON object with the following fields:
- category: high-level category (e.g., 'authentication', 'network', 'database', 'frontend', 'configuration')
- severity: one of ['low', 'medium', 'high', 'critical']
- summary: short human-readable summary of the issue
- probable_root_cause: likely root cause based on the logs
- suggested_next_steps: recommended actions for investigation or fix

Logs:
{raw_logs}
{context_block}

Return ONLY valid JSON, no explanations.
"""

    def _parse_output(self, raw_output: str) -> LogAnalysisResult:
        import json

        try:
            data = json.loads(raw_output)
        except json.JSONDecodeError:
            raise ValueError("LLM returned invalid JSON. Raw output:\n" + raw_output)

        return LogAnalysisResult(
            category=data.get("category", "unknown"),
            severity=data.get("severity", "medium"),
            summary=data.get("summary", ""),
            probable_root_cause=data.get("probable_root_cause", ""),
            suggested_next_steps=data.get("suggested_next_steps", ""),
        )


# -----------------------------
# Example Usage
# -----------------------------

if __name__ == "__main__":
    sample_logs = """
    2026-07-09 02:41:12 ERROR AuthService - Login failed for user test@example.com
    java.sql.SQLNonTransientConnectionException: Could not connect to database
        at com.example.auth.AuthService.login(AuthService.java:87)
        Caused by: java.net.ConnectException: Connection timed out
    """

    analyzer = LogAnalyzer()
    result = analyzer.analyze(sample_logs)

    print("\nLog Analysis Result:\n")
    print(f"Category: {result.category}")
    print(f"Severity: {result.severity}")
    print(f"Summary: {result.summary}")
    print(f"Probable Root Cause: {result.probable_root_cause}")
    print(f"Suggested Next Steps: {result.suggested_next_steps}")
