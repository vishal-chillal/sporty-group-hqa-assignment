# Test Plan

## Scope

Risk-based coverage of the Single Bet Placement feature across the web UI and REST API. The plan focuses on the core betting journey, financial/business rules, eligibility, validation, and filtering.

## TC-01 — Successful Single-Bet Placement and Receipt

**Priority:** Critical

**Risk rationale:** The primary business journey is placing a valid single bet. Incorrect transaction details or state changes directly affect betting correctness.

### Steps
1. Open the application with a valid user context.
2. Select an upcoming football match.
3. Select one outcome: HOME, DRAW, or AWAY.
4. Verify the selection appears in the Bet Slip.
5. Enter a valid stake within the allowed range and available balance.
6. Verify match, selection, odds, stake, and potential payout in the Bet Slip.
7. Place the bet.
8. Verify successful placement and receipt.
9. Verify receipt details.
10. Verify the balance is reduced by the stake.

### Expected Result
The bet is successfully placed as a single bet. Receipt values are consistent with the Bet Slip and the balance is reduced by the stake.

---

## TC-02 — Insufficient Balance Validation

**Priority:** Critical

**Risk rationale:** Allowing a user to bet more than the available balance can create an invalid financial state and negative account balance.

### Steps
1. Retrieve or observe the current balance.
2. Select a valid upcoming football match and outcome.
3. Enter a stake greater than the available balance but within the maximum stake limit.
4. Attempt to place the bet.
5. Verify the transaction is rejected.
6. Verify the balance remains unchanged.

### Expected Result
The bet is rejected with clear insufficient-balance feedback and no amount is deducted.

---

## TC-03 — Stake Boundary and Input Validation

**Priority:** High

**Risk rationale:** Stake validation protects the core financial transaction from invalid values and boundary-condition defects.

### Steps
1. Enter a stake below the minimum, e.g. €0.01.
2. Verify validation feedback.
3. Enter the minimum valid stake, €1.00.
4. Verify it is accepted.
5. Enter the maximum valid stake, €100.00.
6. Verify it is accepted.
7. Enter €100.01.
8. Verify validation feedback.
9. Verify invalid values cannot be submitted.

### Expected Result
Values below €1.00 and above €100.00 are rejected. €1.00 and €100.00 are accepted. Invalid stake values cannot be submitted.

---

## TC-04 — Upcoming Match Eligibility and Selection Integrity

**Priority:** Critical

**Risk rationale:** Betting must only be available for eligible upcoming/pre-match events. Allowing bets on past events is a core business-rule failure.

### Steps
1. Retrieve the available match list.
2. Identify matches whose kickoff date is in the past.
3. Verify whether past matches are displayed in the UI.
4. Attempt to select a past match.
5. Attempt to place a valid bet on the past match.

### Expected Result
Only upcoming/pre-match football events are displayed and available for betting. Past matches cannot be selected or bet on.

---

## TC-05 — Date and Odds Filtering

**Priority:** High

**Risk rationale:** Incorrect filters can expose the wrong events or prevent users from finding eligible betting opportunities.

### Steps
1. Select a single date containing matches and apply the filter.
2. Verify matches for the selected date are displayed.
3. Select a valid date range containing multiple matches.
4. Verify matches from the selected range are displayed.
5. Apply a valid odds range.
6. Verify matching events are displayed.
7. Set the minimum odds greater than the maximum odds.
8. Apply the filter.

### Expected Result
Valid date and odds filters return matching events. An invalid odds range is rejected with clear validation feedback.

---

## TC-06 — Balance and Reset State Consistency

**Priority:** Critical

**Risk rationale:** Balance is a financial state. Inconsistent reset or currency information can result in incorrect account information and transaction decisions.

### Steps
1. Retrieve the current balance.
2. Place a valid bet.
3. Retrieve the balance again.
4. Verify the stake was deducted.
5. Call the reset-balance endpoint.
6. Record the reset response.
7. Retrieve the balance again.
8. Compare the reset response with the persisted balance.
9. Verify currency consistency across balance and place-bet responses.

### Expected Result
A successful bet deducts the stake. Reset response and persisted balance are consistent. Relevant betting and balance APIs use the specified EUR currency.
