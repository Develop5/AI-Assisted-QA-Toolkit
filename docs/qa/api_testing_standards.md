# API Testing Standards

## 1. Mandatory Checks
- Status code
- Response body
- Headers
- Schema validation
- Error handling

## 2. Authentication Rules
- Use test accounts
- Rotate tokens regularly
- Avoid storing secrets in code

## 3. Negative Testing
- Invalid payloads
- Missing fields
- Unauthorized access
- Rate limiting

## 4. Performance Testing
- Response time < 300ms for critical APIs
- Load tests must simulate real traffic

## 5. Best Practices
- Use contract testing
- Validate pagination
- Validate idempotency
