# SBOM (Software Bill of Materials) Policy

## 1. Purpose
Ensures full visibility into software dependencies.

## 2. Mandatory Requirements
- Every build must generate an SBOM
- SBOM must include transitive dependencies
- SBOM must be stored with artifacts

## 3. QA Responsibilities
- Validate SBOM completeness
- Validate no banned libraries exist
- Validate vulnerability scanning

## 4. Best Practices
- Use CycloneDX or SPDX formats
