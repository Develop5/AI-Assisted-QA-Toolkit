# QA Documentation — Automation Standards

## 1. Purpose of This Document
This document defines the standards, conventions, and best practices for building and maintaining automated tests across all QA teams. It ensures consistency, reliability, and long-term maintainability of automation frameworks.

---

## 2. Supported Automation Frameworks
The organization officially supports the following frameworks:

- **Playwright** (primary choice for UI automation)
- **Cypress** (secondary choice for UI automation)
- **PyTest** (API and backend testing)
- **JUnit/TestNG** (Java-based backend testing)

Teams must avoid mixing frameworks within the same project unless explicitly approved.

---

## 3. Automation Principles

### **3.1 Stability First**
Automation must be deterministic and stable. Flaky tests are considered defects and must be fixed or removed.

### **3.2 Maintainability**
Tests must be easy to read, update, and debug. Complex logic should be encapsulated in helper functions or page objects.

### **3.3 Independence**
Each automated test must be fully independent. Tests must not rely on the execution order or shared state.

### **3.4 Fast Feedback**
Automation should provide fast feedback. Long-running tests must be optimized or moved to nightly pipelines.

---

## 4. Selector Strategy

### **4.1 Preferred Selectors**
- `data-testid`
- `aria-label`
- Semantic HTML tags
- Stable IDs

### **4.2 Avoid**
- CSS nth-child selectors
- Dynamic IDs
- Text-based selectors when text is likely to change

---

## 5. Page Object Model (POM)

### **5.1 Requirements**
- Each page must have its own class.
- All selectors must be defined in one place.
- Page methods must represent user actions, not implementation details.

### **5.2 Benefits**
- Reduces duplication
- Improves readability
- Simplifies maintenance

---

## 6. Assertions

### **6.1 Guidelines**
- Assertions must be explicit and tied to the expected result.
- Avoid multiple unrelated assertions in the same test.
- Use descriptive assertion messages.

### **6.2 Types of Assertions**
- UI state validation
- API response validation
- Database state validation (only in integration tests)

---

## 7. Error Handling

### **7.1 Required**
- Capture screenshots on failure
- Capture console logs (UI tests)
- Capture network logs (UI tests)
- Capture API request/response logs (API tests)

### **7.2 Optional**
- Retry logic for known external flakiness (e.g., third-party services)

---

## 8. Test Data Management

### **8.1 Rules**
- Test data must be deterministic.
- Avoid using production data.
- Use factories or fixtures for dynamic data.
- Clean up data after tests when necessary.

---

## 9. CI/CD Integration

### **9.1 Requirements**
- Automation must run on every pull request.
- Critical flows must run on every commit.
- Full regression must run nightly.

### **9.2 Reporting**
- Reports must include:
  - Pass/fail summary
  - Screenshots
  - Logs
  - Duration metrics

---

## 10. Versioning
This document is updated quarterly. Major changes require approval from the QA Automation Lead.
