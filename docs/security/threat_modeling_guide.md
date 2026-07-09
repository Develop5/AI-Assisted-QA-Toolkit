# Threat Modeling Guide (STRIDE-Based)

## 1. Purpose
Provides a structured approach to identifying threats early in development.

## 2. STRIDE Categories
- Spoofing
- Tampering
- Repudiation
- Information Disclosure
- Denial of Service
- Elevation of Privilege

## 3. QA Responsibilities
- Validate mitigations exist
- Validate logging for repudiation
- Validate rate limiting for DoS
- Validate access controls for EoP

## 4. Best Practices
- Perform threat modeling every major feature
- Document all assumptions
