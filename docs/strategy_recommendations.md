# Strategy and Recommendations

## 1. Automation Strategy

The assignment requires two focused automated tests:

1. One critical end-to-end UI journey using Selenium WebDriver and Pytest.
2. One API validation or business-rule test using Python `requests`.

The framework intentionally stays small and uses Page Objects for the UI, service
objects for API operations, Pytest fixtures for lifecycle management, and Allure
for test reporting. The two tests run in parallel with isolated worker-scoped user
IDs and reset state before and after each test. Failed UI tests automatically
capture a screenshot and browser URL for diagnosis.

## 2. Selected Automated Tests

### UI — Successful Single-Bet Placement

The UI test covers the primary customer journey:

- Open the application with a configured user context.
- Select an upcoming match and outcome.
- Validate the Bet Slip selection.
- Enter a valid stake.
- Validate the stake and potential payout.
- Place the bet.
- Validate the receipt and the persisted balance deduction.

This journey was selected because it crosses the match list, odds selection, Bet
Slip, transaction submission, receipt, and balance state. It provides more useful
regression coverage than testing an isolated UI control.

### API — Reset Balance Consistency

The API test verifies that `POST /api/reset-balance` and `GET /api/balance` agree
on the persisted account state. It also validates the expected reset amount,
success message, and EUR currency.

This test was selected because balance is a core financial state and the manual
execution identified a mismatch between the reset response and the subsequently
persisted balance. API-level coverage exposes this defect without the timing and
rendering overhead of the UI.

The broader API suite should additionally automate insufficient balance, invalid
selection, invalid match, malformed payload, authorization, currency, and stake
validation rules when the assignment scope expands.

## 3. What Is Intentionally Manual

The following remain manual because they are exploratory, visual, or outside the
two-test automation requirement:

- Receipt presentation and home/away team ordering.
- Bet Slip layout, content, and empty-state behavior.
- Date and odds filter combinations.
- Error-modal copy, retry behavior, and close behavior.
- Cross-browser and visual compatibility beyond latest desktop Chrome.
- Exploratory combinations of filters, balance states, and transaction sequences.

These checks are documented in `docs/execution_results.md`, together with their
defects and evidence.

## 4. Important Specification Clarification

The specification contains two minimum-stake values: the business-rules table
states €1.00, while the validation section states €1.01. This should be resolved
by the product owner before expanding automated boundary coverage. Until then,
the chosen value must be stated explicitly in the relevant test and documentation.

The specification also requires EUR consistently across balance and place-bet
responses, upcoming events only, and home-team-first/away-team-second ordering.
These requirements are covered by the manual findings and should become API or
UI regression checks as the product defects are fixed.

## 5. Recommendations for Scaling

### Recommendation 1 — CI/CD and Failure Artifacts

Run API and UI smoke tests in CI after the target environment is available. Keep
automatic screenshots, browser metadata, logs, and Allure attachments for UI
failures. API failures should retain the request correlation ID and response body
in the report.

### Recommendation 2 — Expand API and Integration Coverage

Prioritize server-side checks for insufficient balance, stake boundaries and
precision, invalid selections, unknown matches, authorization, malformed payloads,
currency consistency, past-event eligibility, and duplicate/in-progress bets.
Use isolated user data or a supported reset mechanism for repeatable execution.

### Recommendation 3 — Establish a Single Contract

Resolve the specification discrepancies and make the API contract authoritative.
Contract and business-rule tests should enforce response schemas, status codes,
currency, balance transitions, and match eligibility before the UI suite is
expanded.

## 6. Framework Principles

- Keep the Page Object and API service layers small and focused.
- Keep environment-specific values in configuration or environment variables.
- Use setup and teardown to restore test state.
- Keep tests independent and safe to run in parallel.
- Keep assertions close to the business behavior being verified.
- Avoid adding abstractions that are not needed by the current assignment.
