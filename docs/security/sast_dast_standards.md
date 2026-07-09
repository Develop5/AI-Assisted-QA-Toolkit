# SAST & DAST Standards

## 1. SAST Requirements
- Must run on every pull request
- Must block merge on critical findings
- Must scan all languages in the repo

## 2. DAST Requirements
- Must run on staging environments
- Must validate authentication flows
- Must detect common OWASP vulnerabilities

## 3. QA Responsibilities
- Validate findings are reproducible
- Validate fixes are effective
- Validate no regressions occur

## 4. Best Practices
- Combine SAST + DAST for full coverage
