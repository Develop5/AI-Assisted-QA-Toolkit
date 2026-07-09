"""
AI-Assisted Log & Error Analyzer (with DevOps RAG + Security RAG Integration)
-------------------------------------------------------------------------------

This module analyzes logs and errors using an LLM and includes both
DevOps RAG and Security RAG integration to enhance root cause analysis with
comprehensive context from:
- CI/CD, Kubernetes, observability, container standards, SRE policies,
  and deployment strategies (DevOps)
- API security, AppSec, threat modeling, secrets management, SAST/DAST,
  IAM governance, and compliance (Security)

Author: AI-Assisted QA Lead (in transition)
"""

import os
from dataclasses import dataclass
from typing import Optional

try:
    from openai import OpenAI
except ImportError:
    raise ImportError("Install with: pip install openai")

# Import DevOps and Security RAG engines
from modules.rag_docs.rag_docs import QARAGEngine


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
    devops_context_used: bool
    security_context_used: bool


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
            temperature=0.1,
        )
        return response.choices[0].message.content


# -----------------------------
# Log Analyzer (with DevOps RAG + Security RAG)
# -----------------------------
"""
Dual RAG Integration — Log Analyzer Enhancement
-----------------------------------------------

This integration extends the AI-Assisted Log Analyzer with both DevOps and
Security-aware context using dual Retrieval-Augmented Generation (RAG) engines.
The Log Analyzer now retrieves relevant documentation from both knowledge bases
and injects that knowledge directly into the LLM prompt.

What this integration provides
------------------------------
The Log Analyzer becomes significantly more accurate and comprehensive by
combining raw logs with both DevOps and Security documentation. This allows
the system to:

1. Classify logs using integrated categories:
   - Kubernetes, CI/CD, Containers, Observability, SRE, Deployment (DevOps)
   - API Security, AppSec, IAM, Secrets, Threat vectors (Security)

2. Improve severity assessment using combined criteria:
   - DevOps: readiness/liveness probe failures, autoscaling issues, rollout instability
   - Security: authentication failures, unauthorized access, potential breaches,
     vulnerability exploitation, secrets exposure

3. Produce deeper root cause analysis by leveraging both standards:
   - DevOps: Kubernetes restart loops, image pull failures, resource limits
   - Security: misconfigured authentication, insufficient access controls,
     exposed secrets, insecure API endpoints, SAST/DAST scan failures

4. Generate more actionable next steps aligned with best practices:
   - DevOps: validate probes, check container registry, inspect rollout strategy
   - Security: verify IAM policies, scan for vulnerabilities, audit access logs,
     check secrets rotation, validate threat models

Example of what this integration enables
----------------------------------------
Given the following log:

    2026-07-09 02:41:12 ERROR kubelet - Failed to pull image: connection timeout
    Back-off pulling image "registry.example.com/app:latest"
    2026-07-09 02:41:15 WARN auth - Unauthorized access attempt from 192.168.1.100

The enhanced Log Analyzer can now:
- Identify DevOps category as "kubernetes" or "container"
- Identify Security category as "authentication" or "unauthorized_access"
- Mark severity as "high" or "critical" based on combined reliability + security rules
- Infer root causes such as:
      "Image pull failure due to registry connectivity + potential brute force attempt
       on authentication endpoint"
- Recommend next steps such as:
      "Validate container registry availability and check image tag correctness,
       verify node network connectivity, inspect Kubernetes event logs, AND
       audit authentication logs, check IAM policies, enable rate limiting,
       verify secrets are not exposed in logs"

By using both DevOps and Security documentation as context, the Log Analyzer
becomes capable of producing richer, more accurate, and operationally meaningful
insights that align with real-world DevOps + AppSec + SRE practices.

"""

class LogAnalyzer:
    """
    Analyzes logs and errors using an LLM, enhanced with DevOps + Security RAG context.
    """

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        devops_docs_path: str = "docs/devops/",
        security_docs_path: str = "docs/security/"
    ):
        self.llm = LLMClient(model=model)
        self.devops_rag = QARAGEngine(docs_path=devops_docs_path)
        self.security_rag = QARAGEngine(docs_path=security_docs_path)

    def analyze(self, raw_logs: str, context: Optional[str] = None) -> LogAnalysisResult:
        # Retrieve DevOps documentation relevant to the logs
        devops_chunks = self.devops_rag.retrieve(raw_logs)

        # Retrieve Security documentation relevant to the logs
        security_chunks = self.security_rag.retrieve(raw_logs)

        prompt = self._build_prompt(
            raw_logs,
            context,
            devops_chunks,
            security_chunks
        )
        raw_output = self.llm.generate(prompt)
        return self._parse_output(
            raw_output,
            devops_chunks_used=len(devops_chunks) > 0,
            security_chunks_used=len(security_chunks) > 0
        )

    def _build_prompt(
        self,
        raw_logs: str,
        context: Optional[str],
        devops_docs: list,
        security_docs: list
    ) -> str:
        context_block = f"\nContext:\n{context}\n" if context else ""
        devops_block = "\n\n".join(devops_docs) if devops_docs else "[No DevOps documentation retrieved]"
        security_block = "\n\n".join(security_docs) if security_docs else "[No Security documentation retrieved]"

        return f"""
You are an expert QA + DevOps reliability engineer + AppSec specialist.

Use the following documentation to improve your analysis:

--- DevOps Documentation Context ---
{devops_block}
-----------------------------------

--- Security Documentation Context ---
{security_block}
-----------------------------------

Analyze the following logs and return a JSON object with:

- category: high-level category combining DevOps and Security aspects
  (e.g., 'authentication', 'network', 'database', 'kubernetes', 'ci/cd',
   'container', 'api_security', 'secrets', 'unauthorized_access', 'threat')
- severity: one of ['low', 'medium', 'high', 'critical']
- summary: short human-readable summary
- probable_root_cause: likely root cause based on logs + DevOps + Security context
- suggested_next_steps: recommended actions for investigation or fix, addressing
  both operational and security concerns

Logs:
{raw_logs}
{context_block}

Return ONLY valid JSON.
"""

    def _parse_output(
        self,
        raw_output: str,
        devops_chunks_used: bool,
        security_chunks_used: bool
    ) -> LogAnalysisResult:
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
            devops_context_used=devops_chunks_used,
            security_context_used=security_chunks_used
        )


# -----------------------------
# Example Usage
# -----------------------------

if __name__ == "__main__":
    sample_logs = """
    2026-07-09 02:41:12 ERROR kubelet - Failed to pull image: connection timeout
    Back-off pulling image "registry.example.com/app:latest"
    2026-07-09 02:41:15 WARN auth - Unauthorized access attempt from 192.168.1.100
    2026-07-09 02:41:20 ERROR api - Secret exposure detected in logs
    """

    analyzer = LogAnalyzer(
        devops_docs_path="docs/devops/",
        security_docs_path="docs/security/"
    )
    result = analyzer.analyze(sample_logs)

    print("\nLog Analysis Result:\n")
    print(f"Category: {result.category}")
    print(f"Severity: {result.severity}")
    print(f"Summary: {result.summary}")
    print(f"Probable Root Cause: {result.probable_root_cause}")
    print(f"Suggested Next Steps: {result.suggested_next_steps}")
    print(f"DevOps Context Used: {result.devops_context_used}")
    print(f"Security Context Used: {result.security_context_used}")
