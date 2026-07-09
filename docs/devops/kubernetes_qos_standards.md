# Kubernetes QoS & QA Standards

## 1. Purpose
Defines how QA validates Kubernetes deployments.

## 2. Mandatory Checks
- Pod readiness & liveness probes
- Resource requests & limits
- Autoscaling rules
- Rolling update strategy

## 3. QA Validation
- Validate pods restart gracefully
- Validate zero-downtime deployments
- Validate logs accessible via kubectl
- Validate events for warnings/errors

## 4. Best Practices
- Use ConfigMaps for configuration
- Use Secrets for sensitive data
- Avoid hostPath volumes
