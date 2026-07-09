# API Security Standards

## 1. Mandatory Controls
- Authentication required for all sensitive endpoints
- Authorization checks for every resource
- Input validation for all parameters
- Rate limiting for high-risk endpoints

## 2. Forbidden Practices
- Returning stack traces in responses
- Using predictable IDs
- Allowing unauthenticated POST/PUT/DELETE

## 3. QA Responsibilities
- Validate token expiration
- Validate RBAC enforcement
- Validate error handling

## 4. Best Practices
- Use API gateways
- Use JWT with short TTL
