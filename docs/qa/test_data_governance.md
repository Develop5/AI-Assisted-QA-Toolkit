# Test Data Governance

## 1. Principles
- Deterministic
- Reproducible
- Isolated
- Non-production

## 2. Allowed Data Sources
- Synthetic data
- Factories
- Fixtures
- Mock services

## 3. Forbidden Data
- Production data
- Sensitive personal data
- Real customer accounts

## 4. Data Reset Rules
- Tests must clean up after execution
- Database snapshots must be versioned
- API mocks must be deterministic

## 5. Best Practices
- Use UUIDs for dynamic data
- Avoid random values unless controlled
- Document all required test data
