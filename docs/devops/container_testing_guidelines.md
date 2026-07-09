# Container Testing Guidelines

## 1. Scope
Defines how QA and DevOps teams validate containerized applications.

## 2. Mandatory Checks
- Container builds reproducible
- No root user inside containers
- Health checks implemented
- Resource limits defined

## 3. Testing Strategy
- Validate Dockerfile linting
- Validate image size thresholds
- Validate startup time < 3 seconds
- Validate logs emitted to stdout/stderr

## 4. Best Practices
- Use multi-stage builds
- Avoid copying secrets into images
- Use minimal base images
