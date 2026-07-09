# Logging Policy for QA and Automation

## 1. Purpose
Defines how logs must be captured, stored, and analyzed during testing.

## 2. Mandatory Logging
- Navigation events
- API requests and responses
- Console logs
- Network failures
- Assertion failures

## 3. Log Format
Logs must include:
- Timestamp
- Component
- Severity
- Message
- Optional stack trace

## 4. Severity Levels
- INFO: normal execution
- WARNING: unexpected but non-breaking behavior
- ERROR: functional failure
- CRITICAL: system unusable

## 5. Storage Rules
- Logs must be stored per test execution
- Logs must be attached to CI/CD reports
- Logs older than 90 days must be archived

## 6. Best Practices
- Avoid logging sensitive data
- Use structured JSON logs when possible
- Ensure logs are readable and searchable
