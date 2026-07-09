# Secure Coding Guidelines

## 1. Input Validation
- Validate server-side
- Use allowlists when possible
- Reject malformed data early

## 2. Output Encoding
- HTML encode user content
- Escape special characters
- Avoid unsafe templating engines

## 3. Authentication Rules
- Use modern hashing algorithms
- Enforce MFA for admin accounts
- Use short-lived tokens

## 4. Best Practices
- Avoid global state
- Avoid insecure deserialization
- Avoid direct object references
