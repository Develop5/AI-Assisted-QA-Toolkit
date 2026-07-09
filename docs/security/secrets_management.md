# Secrets Management Policy

## 1. Forbidden Practices
- Storing secrets in code
- Storing secrets in Docker images
- Logging secrets
- Hardcoding API keys

## 2. Mandatory Requirements
- Use secret vaults (Azure Key Vault, AWS Secrets Manager)
- Rotate secrets every 90 days
- Use environment variables for runtime injection

## 3. QA Responsibilities
- Validate secrets are not exposed in logs
- Validate secrets are not stored in config files
- Validate rotation procedures

## 4. Best Practices
- Use least privilege access
- Use encrypted storage
