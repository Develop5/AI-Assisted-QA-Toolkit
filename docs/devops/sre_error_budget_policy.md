# SRE Error Budget Policy

## 1. Purpose
Defines how QA and DevOps collaborate on reliability targets.

## 2. Error Budget
- Based on SLOs (e.g., 99.9% uptime)
- Budget consumed by incidents, downtime, failures

## 3. QA Responsibilities
- Validate reliability during load tests
- Validate recovery procedures
- Validate failover mechanisms

## 4. DevOps Responsibilities
- Monitor SLOs
- Track error budget consumption
- Trigger release freeze if budget exhausted
