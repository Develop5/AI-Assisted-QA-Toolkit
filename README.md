# 🎯 AI-Assisted-QA-Toolkit

A practical, modular toolkit for integrating **Generative AI** into **Quality Assurance** workflows.  
This repository is part of a professional transition from *QA Lead Automation* to *AI‑Assisted QA Lead*, showcasing real tools, frameworks, and examples that demonstrate how AI can enhance QA produc[...] 

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active%20Development-yellow)

---

## 🚀 Project Goals

- Integrate AI into key QA activities: test case generation, log analysis, regression optimization, and intelligent prioritization
- Provide real, production-ready tools for modern QA teams
- Serve as a technical portfolio for senior roles (>€90k/year) in Spain and Europe
- Demonstrate technical leadership in adopting AI within the QA lifecycle

---

## 🧩 Core Modules

| Module | Purpose | Path |
|--------|---------|------|
| **AI Test Case Generator** | Transforms requirements into structured test cases (Gherkin, JSON, Markdown) | `proyect-Python/modules/testcase-generator/` |
| **AI Test Script Generator** | Generates automated test scripts (Playwright/Cypress) from requirements | `proyect-Python/modules/script-generator/` |
| **AI Log & Error Analyzer** | Analyzes logs, errors, and failures with automatic classification & root cause analysis | `proyect-Python/modules/log-analyzer/` |
| **Regression Optimizer** | Detects duplicate tests, identifies obsolete tests, and recommends risk-based test suites | `proyect-Python/modules/regression-optimizer/` |
| **RAG Documents Integration** | Retrieval-Augmented Generation for documentation-driven QA insights | `proyect-Python/modules/rag-docs/` |
| **QA Dashboard** | Interactive Streamlit dashboard with execution status and AI-generated insights | `proyect-Python/modules/dashboard/` |

---

## 📁 Repository Structure

Below is an updated, clearer view of the repository layout reflecting the current project organization. Paths are relative to the repository root.

´´´text
AI-Assisted-QA-Toolkit/
│
├── 📄 README.md                    # This file
├── 📄 LICENSE.md                   # MIT License
├── 📄 CODE_OF_CONDUCT.md           # Community guidelines
├── 📄 CONTRIBUTING.md              # Contribution guidelines
├── 📄 .gitignore                   # Git ignore rules
│
├── 📋 architecture.md              # Technical architecture and design
├── 📋 roadmap.md                   # Development roadmap
│
├── 📂 proyect-Python/
│   └── modules/
│       ├── testcase-generator/     # AI test case generation (LLM-based)
│       ├── script-generator/       # Automated script generation (Playwright/Cypress)
│       ├── log-analyzer/           # Log and error analysis
│       ├── regression-optimizer/   # Regression suite optimization
│       ├── rag-docs/               # RAG-based documentation integration
│       └── dashboard/              # Streamlit interactive dashboard
│
├── 📂 docs/
│   └── qa/
│       └── test_case_standards.md  # QA testing standards and best practices
│
└── 📂 whitepapers/
    └── whitepaper1.md             # Research and technical documentation

Notes:
- The top-level `proyect-Python/` directory contains the working Python modules for the toolkit. The spelling "proyect" mirrors the existing folder name in the repository to avoid confusion; if you'd like it renamed to `project-Python/` or `project-python/`, I can open a PR to rename the folder and update references.
- Each module is intentionally self-contained and includes its own README, examples, and unit tests where applicable.

---

## 📚 Documentation

- **[Architecture](./architecture.md)** - Technical design and component relationships
- **[Roadmap](./roadmap.md)** - Development timeline and planned features
- **[QA Standards](./docs/qa/test_case_standards.md)** - Testing best practices and guidelines
- **[Whitepapers](./whitepapers/)** - Research and in-depth technical documentation

´´´
---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or poetry
- API keys for LLM providers (OpenAI, etc.)

### Installation

```bash
# Clone the repository
git clone https://github.com/Develop5/AI-Assisted-QA-Toolkit.git
cd AI-Assisted-QA-Toolkit

# Install dependencies
pip install -r requirements.txt

# Or using poetry
poetry install
```

### Running the Dashboard

```bash
cd proyect-Python/modules/dashboard
streamlit run app.py
```

---

## 📚 Usage Examples

### Generate Test Cases
```python
from proyect_Python.modules.testcase_generator import TestCaseGenerator

generator = TestCaseGenerator()
test_cases = generator.generate_from_requirements("sample_requirements.md")
```

### Analyze Logs
```python
from proyect_Python.modules.log_analyzer import LogAnalyzer

analyzer = LogAnalyzer()
insights = analyzer.analyze("execution.log")
```

### Optimize Regression Suite
```python
from proyect_Python.modules.regression_optimizer import RegressionOptimizer

optimizer = RegressionOptimizer()
optimized_suite = optimizer.analyze_test_suite("test_suite.json")
```

---

## 🤝 Contributing

Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on:
- Reporting issues
- Submitting feature requests
- Creating pull requests
- Code style and standards

---

## 📜 License

This project is licensed under the [MIT License](./LICENSE.md).

---

## 👨‍💻 Author

**Develop5** - QA Lead | AI/ML Integration Specialist

---

## 🔗 Related Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Playwright Documentation](https://playwright.dev)
- [Cypress Documentation](https://docs.cypress.io)
- [Streamlit Documentation](https://docs.streamlit.io)

---

## 📞 Support & Questions

For issues, feature requests, or questions, please open an issue in the [Issues](https://github.com/Develop5/AI-Assisted-QA-Toolkit/issues) section.
