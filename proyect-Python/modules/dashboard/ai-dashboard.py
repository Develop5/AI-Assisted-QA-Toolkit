"""
AI-Assisted QA Dashboard (Streamlit)
------------------------------------

This dashboard provides a unified UI for interacting with the modules of the
AI-Assisted-QA-Toolkit. It allows users to:

- Generate test cases from raw requirements
- Generate automated scripts (Playwright/Cypress)
- Analyze logs and errors
- Optimize regression test suites
- Visualize results in a clean, interactive interface

The design is intentionally simple and modular so it can evolve into more
advanced dashboards with authentication, multi-user support, CI/CD integration,
and real-time monitoring.

Author: AI-Assisted QA Lead (in transition)
"""

import streamlit as st
import os

# Import modules from your project
from modules.testcase_generator.generator import TestCaseGenerator
from modules.script_generator.script_generator import ScriptGenerator, TestCase
from modules.log_analyzer.log_analyzer import LogAnalyzer
from modules.regression_optimizer.regression_optimizer import (
    RegressionOptimizer,
    TestMetadata,
)

# -----------------------------
# Streamlit Page Setup
# -----------------------------

st.set_page_config(
    page_title="AI-Assisted QA Dashboard",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI-Assisted QA Dashboard")
st.write("A unified interface for AI-powered Quality Assurance modules.")


# -----------------------------
# Sidebar Navigation
# -----------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to:",
    [
        "Test Case Generator",
        "Script Generator",
        "Log Analyzer",
        "Regression Optimizer",
        "QA Documentation RAG",
        "Security Documentation RAG",
        "DevOps Documentation RAG"
    ]
)



# -----------------------------
# Test Case Generator Page
# -----------------------------

if page == "Test Case Generator":
    st.header("📝 AI Test Case Generator")

    requirements = st.text_area(
        "Enter raw requirements:",
        height=200,
        placeholder="Users must be able to log in using email and password..."
    )

    if st.button("Generate Test Cases"):
        if not requirements.strip():
            st.error("Please enter requirements.")
        else:
            generator = TestCaseGenerator()
            testcases = generator.generate_testcases(requirements)

            st.success("Test cases generated successfully!")
            for tc in testcases:
                st.subheader(f"{tc.id} — {tc.title}")
                st.write("**Steps:**")
                for step in tc.steps:
                    st.write(f"- {step}")
                st.write("**Expected Result:**")
                st.write(tc.expected_result)
                st.markdown("---")


# -----------------------------
# Script Generator Page
# -----------------------------

elif page == "Script Generator":
    st.header("⚙️ AI Script Generator")

    tc_id = st.text_input("Test Case ID")
    tc_title = st.text_input("Title")
    tc_steps = st.text_area("Steps (one per line)")
    tc_expected = st.text_area("Expected Result")

    framework = st.selectbox("Framework", ["playwright", "cypress"])

    if st.button("Generate Script"):
        if not tc_id or not tc_title or not tc_steps.strip():
            st.error("Please fill in all fields.")
        else:
            test_case = TestCase(
                id=tc_id,
                title=tc_title,
                steps=[s.strip() for s in tc_steps.split("\n") if s.strip()],
                expected_result=tc_expected,
            )

            generator = ScriptGenerator(framework=framework)
            script = generator.generate_script(test_case)

            st.success("Script generated successfully!")
            st.code(script, language="python")


# -----------------------------
# Log Analyzer Page
# -----------------------------

elif page == "Log Analyzer":
    st.header("📉 AI Log & Error Analyzer")

    logs = st.text_area(
        "Paste logs or stack traces:",
        height=250,
        placeholder="2026-07-09 ERROR AuthService - Login failed..."
    )

    context = st.text_area(
        "Optional context:",
        height=100,
        placeholder="Authentication module recently updated..."
    )

    if st.button("Analyze Logs"):
        if not logs.strip():
            st.error("Please enter logs.")
        else:
            analyzer = LogAnalyzer()
            result = analyzer.analyze(logs, context)

            st.success("Analysis complete!")

            st.write("### Category")
            st.write(result.category)

            st.write("### Severity")
            st.write(result.severity)

            st.write("### Summary")
            st.write(result.summary)

            st.write("### Probable Root Cause")
            st.write(result.probable_root_cause)

            st.write("### Suggested Next Steps")
            st.write(result.suggested_next_steps)


# -----------------------------
# Regression Optimizer Page
# -----------------------------

elif page == "Regression Optimizer":
    st.header("📊 AI Regression Optimizer")

    st.write("Enter test metadata below:")

    num_tests = st.number_input("Number of tests", min_value=1, max_value=50, value=3)

    tests = []
    for i in range(num_tests):
        st.subheader(f"Test {i+1}")
        id_ = st.text_input(f"ID {i+1}")
        title = st.text_input(f"Title {i+1}")
        tags = st.text_input(f"Tags {i+1} (comma-separated)")
        component = st.text_input(f"Component {i+1}")

        if id_ and title:
            tests.append(
                TestMetadata(
                    id=id_,
                    title=title,
                    tags=[t.strip() for t in tags.split(",") if t.strip()],
                    component=component,
                )
            )

    if st.button("Optimize Regression Suite"):
        if not tests:
            st.error("Please enter at least one valid test.")
        else:
            optimizer = RegressionOptimizer()
            recommendation = optimizer.optimize(tests)

            st.success("Optimization complete!")

            st.write("### Tests to Keep")
            st.write(recommendation.tests_to_keep)

            st.write("### Tests to Remove")
            st.write(recommendation.tests_to_remove)

            st.write("### Tests to Review")
            st.write(recommendation.tests_to_review)

            st.write("### Suggested New Tests")
            for t in recommendation.suggested_new_tests:
                st.write(f"- {t}")

            st.write("### Summary")
            st.write(recommendation.summary)



# -----------------------------
# RAG Documentation Page
# -----------------------------

elif page == "QA Documentation RAG":
    st.header("📚 QA Documentation RAG Assistant")

    st.write(
        "Ask questions about QA standards, automation rules, regression governance, "
        "or any internal documentation indexed by the RAG engine."
    )

    query = st.text_area(
        "Enter your question:",
        height=150,
        placeholder="Example: What are the mandatory fields for a test case?"
    )

    docs_path = st.text_input(
        "Documentation folder:",
        value="docs/qa/",
        help="Folder containing QA documentation files (.md) used by the RAG engine."
    )

    if st.button("Ask RAG"):
        if not query.strip():
            st.error("Please enter a question.")
        else:
            try:
                from modules.rag_docs.rag_docs import QARAGEngine

                rag = QARAGEngine(docs_path=docs_path)
                answer = rag.answer(query)
                retrieved_chunks = rag.retrieve(query)

                st.success("RAG answer generated successfully!")

                st.subheader("📘 Answer")
                st.write(answer)

                st.subheader("📄 Retrieved Documentation Chunks")
                for i, chunk in enumerate(retrieved_chunks, start=1):
                    st.markdown(f"**Chunk {i}:**")
                    st.write(chunk)
                    st.markdown("---")

            except Exception as e:
                st.error(f"Error running RAG engine: {e}")

# -----------------------------
# Security Documentation RAG Page
# -----------------------------

elif page == "Security Documentation RAG":
    st.header("🔐 Security Documentation RAG Assistant")

    st.write(
        "Ask questions about AppSec, DevSecOps, threat modeling, secure coding, "
        "secrets management, SBOM, SAST/DAST, IAM, API security, and more."
    )

    query = st.text_area(
        "Enter your security-related question:",
        height=150,
        placeholder="Example: What are the mandatory controls for API security?"
    )

    security_docs_path = st.text_input(
        "Security documentation folder:",
        value="docs/security/",
        help="Folder containing security documentation files (.md) used by the RAG engine."
    )

    if st.button("Ask Security RAG"):
        if not query.strip():
            st.error("Please enter a question.")
        else:
            try:
                from modules.rag_docs.rag_docs import QARAGEngine

                rag = QARAGEngine(docs_path=security_docs_path)
                answer = rag.answer(query)
                retrieved_chunks = rag.retrieve(query)

                st.success("Security RAG answer generated successfully!")

                st.subheader("🔐 Answer")
                st.write(answer)

                st.subheader("📄 Retrieved Security Documentation Chunks")
                for i, chunk in enumerate(retrieved_chunks, start=1):
                    st.markdown(f"**Chunk {i}:**")
                    st.write(chunk)
                    st.markdown("---")

            except Exception as e:
                st.error(f"Error running Security RAG engine: {e}")


# -----------------------------
# DevOps Documentation RAG Page
# -----------------------------

elif page == "DevOps Documentation RAG":
    st.header("⚙️ DevOps Documentation RAG Assistant")

    st.write(
        "Ask questions about CI/CD, containers, Kubernetes, observability, deployment strategies, "
        "SRE, security pipelines, GitOps, load testing, incident response, and more."
    )

    query = st.text_area(
        "Enter your DevOps-related question:",
        height=150,
        placeholder="Example: What checks must QA validate in a Kubernetes deployment?"
    )

    devops_docs_path = st.text_input(
        "DevOps documentation folder:",
        value="docs/devops/",
        help="Folder containing DevOps documentation files (.md) used by the RAG engine."
    )

    if st.button("Ask DevOps RAG"):
        if not query.strip():
            st.error("Please enter a question.")
        else:
            try:
                from modules.rag_docs.rag_docs import QARAGEngine

                rag = QARAGEngine(docs_path=devops_docs_path)
                answer = rag.answer(query)
                retrieved_chunks = rag.retrieve(query)

                st.success("DevOps RAG answer generated successfully!")

                st.subheader("⚙️ Answer")
                st.write(answer)

                st.subheader("📄 Retrieved DevOps Documentation Chunks")
                for i, chunk in enumerate(retrieved_chunks, start=1):
                    st.markdown(f"**Chunk {i}:**")
                    st.write(chunk)
                    st.markdown("---")

            except Exception as e:
                st.error(f"Error running DevOps RAG engine: {e}")

