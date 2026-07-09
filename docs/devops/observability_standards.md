# Observability Standards (QA + DevOps)

## 1. Components
- Logging
- Metrics
- Tracing
- Dashboards
- Alerts

## 2. Mandatory Requirements
- Every service must expose metrics
- Logs must be structured JSON
- Traces must include request IDs
- Dashboards must show error rates, latency, throughput

## 3. QA Responsibilities
- Validate logs during tests
- Validate metrics during load tests
- Validate alerts fire correctly

## 4. Best Practices
- Use OpenTelemetry
- Use consistent naming conventions
