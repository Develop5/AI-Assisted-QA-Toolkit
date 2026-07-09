"""
AI-Assisted Log & Error Analyzer (with DevOps RAG Integration)
--------------------------------------------------------------

This module analyzes logs and errors using an LLM and now includes
DevOps RAG integration to enhance root cause analysis with context
from CI/CD, Kubernetes, observability, container standards, SRE policies,
and deployment strategies.

Author: AI-Assisted QA Lead (in transition)
"""

import os
from dataclasses import dataclass
from typing import Optional

try:
    from openai import OpenAI
except ImportError:
    raise ImportError("Install with: pip install openai")

# Import DevOps RAG engine
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
# Log Analyzer (with DevOps RAG)
# -----------------------------
"""
DevOps RAG Integration — Log Analyzer Enhancement
-------------------------------------------------

This integration extends the AI-Assisted Log Analyzer with DevOps-aware
context using a Retrieval-Augmented Generation (RAG) engine. The Log Analyzer
now retrieves relevant DevOps documentation (CI/CD standards, Kubernetes QoS,
container guidelines, observability rules, deployment strategies, SRE policies,
GitOps standards, load testing rules, incident response playbooks, etc.) and
injects that knowledge directly into the LLM prompt.

What this integration provides
------------------------------
The Log Analyzer becomes significantly more accurate and context-aware by
combining raw logs with DevOps documentation. This allows the system to:

1. Classify logs using DevOps categories such as:
   - Kubernetes
   - CI/CD
   - Containers
   - Observability
   - SRE
   - Deployment strategies
   - GitOps
   - Infrastructure failures

2. Improve severity assessment using DevOps reliability criteria:
   - readiness/liveness probe failures
   - autoscaling issues
   - container health check failures
   - CI/CD pipeline breakages
   - node resource exhaustion
   - rollout instability

3. Produce deeper root cause analysis by leveraging DevOps standards:
   - Kubernetes restart loops
   - image pull failures
   - misconfigured resource limits
   - failing health checks
   - broken deployment strategies
   - container misconfiguration
   - CI/CD missteps or missing gates

4. Generate more actionable next steps aligned with DevOps best practices:
   - validate readiness/liveness probes
   - inspect autoscaling metrics
   - check container registry connectivity
   - verify rollout strategy configuration
   - inspect node resource usage
   - validate pipeline security scans

Example of what this integration enables
----------------------------------------
Given the following log:

    2026-07-09 02:41:12 ERROR kubelet - Failed to pull image: connection timeout
    Back-off pulling image "registry.example.com/app:latest"

The enhanced Log Analyzer can now:
- Identify the category as "kubernetes" or "container"
- Mark severity as "high" or "critical" based on DevOps reliability rules
- Infer a root cause such as:
      "Image pull failure due to registry connectivity or authentication issues"
- Recommend next steps such as:
      "Validate container registry availability, check image tag correctness,
       verify node network connectivity, and inspect Kubernetes event logs"

By using DevOps documentation as context, the Log Analyzer becomes capable of
producing richer, more accurate, and operationally meaningful insights that
align with real-world DevOps and SRE practices.

"""

class LogAnalyzer:
    """
    Analyzes logs and errors using an LLM, enhanced with DevOps RAG context.
    """

    def __init__(self, model: str = "gpt-4o-mini", devops_docs_path: str = "docs/devops/"):
        self.llm = LLMClient(model=model)
        self.rag = QARAGEngine(docs_path=devops_docs_path)

    def analyze(self, raw_logs: str, context: Optional[str] = None) -> LogAnalysisResult:
        # Retrieve DevOps documentation relevant to the logs
        devops_chunks = self.rag.retrieve(raw_logs)

        prompt = self._build_prompt(raw_logs, context, devops_chunks)
        raw_output = self.llm.generate(prompt)
        return self._parse_output(raw_output, devops_chunks_used=len(devops_chunks) > 0)

    def _build_prompt(self, raw_logs: str, context: Optional[str], devops_docs: list) -> str:
        context_block = f"\nContext:\n{context}\n" if context else ""
        devops_block = "\n\n".join(devops_docs)

        return f"""
You are an expert QA + DevOps reliability engineer.

Use the following DevOps documentation to improve your analysis:

--- DevOps Documentation Context ---
{devops_block}
-----------------------------------

Analyze the following logs and return a JSON object with:

- category: high-level category (e.g., 'authentication', 'network', 'database', 'kubernetes', 'ci/cd', 'container')
- severity: one of ['low', 'medium', 'high', 'critical']
- summary: short human-readable summary
- probable_root_cause: likely root cause based on logs + DevOps context
- suggested_next_steps: recommended actions for investigation or fix

Logs:
{raw_logs}
{context_block}

Return ONLY valid JSON.
"""

    def _parse_output(self, raw_output: str, devops_chunks_used: bool) -> LogAnalysisResult:
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
            devops_context_used=devops_chunks_used
        )


# -----------------------------
# Example Usage
# -----------------------------

if __name__ == "__main__":
    sample_logs = """
    2026-07-09 02:41:12 ERROR kubelet - Failed to pull image: connection timeout
    Back-off pulling image "registry.example.com/app:latest"
    """

    analyzer = LogAnalyzer(devops_docs_path="docs/devops/")
    result = analyzer.analyze(sample_logs)

    print("\nLog Analysis Result:\n")
    print(f"Category: {result.category}")
    print(f"Severity: {result.severity}")
    print(f"Summary: {result.summary}")
    print(f"Probable Root Cause: {result.probable_root_cause}")
    print(f"Suggested Next Steps: {result.suggested_next_steps}")
    print(f"DevOps Context Used: {result.devops_context_used}")
