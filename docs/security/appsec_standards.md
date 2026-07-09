# Application Security (AppSec) Standards

## 1. Purpose
Defines the mandatory security practices for application development and QA validation.

## 2. Mandatory Controls
- Input validation on all user inputs
- Output encoding for UI rendering
- Strong authentication and session management
- Secure password storage (bcrypt, Argon2)
- Rate limiting on sensitive endpoints

## 3. QA Responsibilities
- Validate input sanitization
- Validate session expiration
- Validate error messages do not leak information
- Validate password reset flows

## 4. Best Practices
- Use secure frameworks
- Avoid custom crypto
- Enforce HTTPS everywhere
