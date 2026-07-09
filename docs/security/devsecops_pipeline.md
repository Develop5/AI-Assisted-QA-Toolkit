# DevSecOps Pipeline Standards

## 1. Pipeline Security Stages
1. Dependency scanning  
2. Static Application Security Testing (SAST)  
3. Secret scanning  
4. Container scanning  
5. Dynamic Application Security Testing (DAST)  
6. Infrastructure-as-Code scanning  

## 2. Mandatory Requirements
- Pipelines must fail on critical vulnerabilities
- All dependencies must be pinned
- Secrets must never appear in logs

## 3. QA Responsibilities
- Validate security tests run in CI/CD
- Validate vulnerabilities are triaged
- Validate fixes before release

## 4. Best Practices
- Shift-left security
- Automate everything
