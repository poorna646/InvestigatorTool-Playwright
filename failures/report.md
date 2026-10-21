# Failure investigation report

## valid login shows welcome message

**Suggested ticket type:** Infrastructure / environment issue
**Classification:** environment (confidence 0.8)
**Attempts that failed:** 2
**Test file:** login.spec.js, line 3

### Likely cause
The test could not reach the server or network.

### Evidence
- Error message contains 'ERR_CONNECTION'

### Error message
```
Error: page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:3000/
Call log:
  - navigating to "http://localhost:3000/", waiting until "load"
```

### Suggested debugging steps
1. Check that the app/server was running during the test
2. Check CI network access and the base URL

### Similar past bugs
- **BUG-102** (environment, similarity 0.52): All UI tests fail at start: connection refused
  - Past fix: Test server did not start in CI. Added a health check and waited for the server before running tests.
- **BUG-105** (locator, similarity 0.09): Profile page test cannot find save button
  - Past fix: Button text was changed to 'Save changes'. Updated the test to the new button name.
- **BUG-101** (locator, similarity 0.05): Checkout test fails: button not found after UI refactor
  - Past fix: Developers renamed data-testid from checkout-button to pay-button. Updated the test locator.

Memory check: the closest past bug agrees with the classification.

### Attachments
- Screenshot: C:\Users\Admin\Documents\playwright\test-results\login-valid-login-shows-welcome-message-chromium\test-failed-1.png
- Trace: C:\Users\Admin\Documents\playwright\test-results\login-valid-login-shows-welcome-message-chromium\trace.zip

---

## wrong password shows error

**Suggested ticket type:** Infrastructure / environment issue
**Classification:** environment (confidence 0.8)
**Attempts that failed:** 2
**Test file:** login.spec.js, line 11

### Likely cause
The test could not reach the server or network.

### Evidence
- Error message contains 'ERR_CONNECTION'

### Error message
```
Error: page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:3000/
Call log:
  - navigating to "http://localhost:3000/", waiting until "load"
```

### Suggested debugging steps
1. Check that the app/server was running during the test
2. Check CI network access and the base URL

### Similar past bugs
- **BUG-102** (environment, similarity 0.52): All UI tests fail at start: connection refused
  - Past fix: Test server did not start in CI. Added a health check and waited for the server before running tests.
- **BUG-105** (locator, similarity 0.09): Profile page test cannot find save button
  - Past fix: Button text was changed to 'Save changes'. Updated the test to the new button name.
- **BUG-101** (locator, similarity 0.05): Checkout test fails: button not found after UI refactor
  - Past fix: Developers renamed data-testid from checkout-button to pay-button. Updated the test locator.

Memory check: the closest past bug agrees with the classification.

### Attachments
- Screenshot: C:\Users\Admin\Documents\playwright\test-results\login-wrong-password-shows-error-chromium\test-failed-1.png
- Trace: C:\Users\Admin\Documents\playwright\test-results\login-wrong-password-shows-error-chromium\trace.zip

---
