# Execution Results and Bug Reports

## Execution Summary

The top three prioritized scenarios were executed against the application, followed by targeted exploratory checks around the betting flow.

| Test Case | Scenario | Result | Key Finding |
|---|---|---|---|
| TC-01 | Successful single-bet placement and receipt | **Failed** | Receipt payout and team ordering were incorrect; UI balance did not update immediately |
| TC-02 | Insufficient balance validation | **Failed — API / Passed — UI** | UI blocked an over-balance stake, but API allowed a sequence resulting in a negative balance |
| TC-03 | Stake boundary and input validation | **Passed for tested boundaries** | €0.01 and €100.01 were rejected; €1.00 and €100.00 were accepted |

## Exploratory Checks

| Area | Result | Observation |
|---|---|---|
| Single active Bet Slip selection | Passed | Selecting another odd replaces the previous selection |
| Remove All | Passed | Selection is removed and balance remains unchanged |
| Receipt close behavior | Passed | Slip remains empty and the existing date filter remains applied |
| Date filter — single date | Passed | Matches for selected date are displayed |
| Date filter — date range | Passed | Matches within the selected range are displayed |
| Invalid odds range | Failed | Minimum greater than maximum is accepted and produces an empty result instead of validation feedback |
| Past-match eligibility | Failed | Past matches are displayed, selectable, and successfully bettable |
| Normal API balance deduction | Passed | Successful API bet deducts the stake when balance is queried again |
| Place-bet currency | Failed | Place-bet response reports USD while balance/reset responses report EUR |
| Reset balance consistency | Failed | Reset response and subsequent persisted balance did not match |
| Bet Slip available balance | Failed | Required available-balance information is not displayed in the Bet Slip |
| Filtered match count | Observation | UI continues showing 103 matches even when filtered results contain fewer or zero matches |

---

# Bug Reports

## BUG-001 — Incorrect Potential Payout on Receipt

**Severity:** High

### Reproduction Steps
1. Select a match and an outcome.
2. Enter a valid stake.
3. Verify the potential payout in the Bet Slip.
4. Place the bet.
5. Compare the payout shown on the receipt with the Bet Slip calculation.

### Expected
Potential payout should equal `stake × odds` and remain consistent between the Bet Slip and receipt.

### Actual
For the tested bet, the Bet Slip showed the correct calculation, while the receipt displayed an incorrect potential payout. Example: €10 stake × 2.20 odds should produce €22.00, but the receipt displayed €20.00.

### Business Impact
Users receive incorrect financial information about the return associated with their bet.

### Evidence
[Payout slip](../evidence/bug-001-payout-slip.png)

[Payout receipt](../evidence/bug-001-wrong-payout-receipt.png)

---

## BUG-002 — API Allows Betting Beyond Available Balance

**Severity:** Critical

### Reproduction Steps
1. Start with an available balance of €19.
2. Submit a valid bet with a stake of €29 through the API.
3. Observe the response.
4. Query `/api/balance`.

### Expected
The API should reject the transaction because the stake exceeds the available balance. The balance should remain unchanged.

### Actual
The API accepted the bet and the balance became negative.

### Business Impact
Server-side validation can be bypassed, allowing financially invalid bets and a negative account balance.

### API Evidence

Request:
```bash
POST /api/place-bet
{
  "matchId": "mls-lafc-inter-miami-2026-12-28",
  "selection": "HOME",
  "stake": 29,
  "additionalProp1": {}
}
```
Response:
```bash
{
  "message": "Bet placed successfully",
  "matchId": "mls-lafc-inter-miami-2026-12-28",
  "selection": "HOME",
  "stake": 29,
  "odds": 2.2,
  "payout": 63.8,
  "balance": -10,
  "currency": "USD"
}
```

Observed sequence:
```text
Balance before: €19
Stake: €29
Bet response: successful
Balance after: €-10
```

### Evidence
[Negative user balance](../evidence/bug-002-negative-balance.png)

---

## BUG-003 — Reset Balance Response Does Not Match Persisted Balance

**Severity:** High

### Reproduction Steps
1. Call `POST /api/reset-balance`.
2. Record the returned balance.
3. Immediately call `GET /api/balance`.
4. Compare the two balances.

### Expected
The reset response and the persisted balance returned by `/api/balance` should be consistent.

### Actual
Reset returned:
```json
{
  "message": "Balance reset successfully",
  "balance": 125.5,
  "currency": "EUR"
}
```

A subsequent balance request returned:
```json
{
  "balance": 120,
  "currency": "EUR"
}
```

### Business Impact
The account state presented immediately after reset is inconsistent with the persisted balance.


---

## BUG-004 — Place-Bet API Returns Incorrect Currency

**Severity:** High

### Reproduction Steps
1. Call `GET /api/balance`.
2. Place a valid bet using `POST /api/place-bet`.
3. Compare the currency fields.

### Expected
The betting flow should consistently use EUR as specified.

### Actual
`/api/balance` and reset responses return `EUR`, while successful `/api/place-bet` responses return `USD`.

Example:
```json
{
  "message": "Bet placed successfully",
  "stake": 1.1,
  "odds": 4.1,
  "payout": 4.51,
  "balance": 120.2,
  "currency": "USD"
}
```

### Business Impact
Inconsistent currency information can cause ambiguity about the monetary values displayed to the user.


---

## BUG-005 — Kickoff Time Missing From Match Listing

**Severity:** Medium

### Reproduction Steps
1. Open the match listing.
2. Inspect a match entry.
3. Compare the displayed match information with the feature requirement.

### Expected
Each match should display its kickoff date and time.

### Actual
The UI displays the match date but does not display the kickoff time.

### Business Impact
Users lack the specified time information needed to understand when an event starts.

### Evidence
[Match listing with missing kickoff time](../evidence/bug-005-missing-kickoff-time.png)

---

## BUG-006 — Receipt Reverses Home/Away Team Order

**Severity:** Medium

### Reproduction Steps
1. Select a match displayed as `LAFC vs Inter Miami`.
2. Add the selection to the Bet Slip.
3. Place the bet.
4. Compare the match ordering in the Bet Slip and receipt.

### Expected
The home team should remain first and the away team second throughout the flow.

### Actual
Bet Slip:
`LAFC vs Inter Miami`

Receipt:
`Inter Miami vs LAFC`

### Business Impact
The receipt presents the fixture inconsistently and can create ambiguity about the home/away teams associated with the bet.

### Evidence
[Order slip](../evidence/bug-006-team-order-slip.png)

[Order receipt](../evidence/bug-006-team-order-receipt.png)

---

## BUG-007 — UI Balance Does Not Update Immediately After Successful Bet

**Severity:** High

### Reproduction Steps
1. Note the balance displayed in the UI.
2. Place a successful bet.
3. Observe the balance immediately after the success response.
4. Hard refresh the page.

### Expected
The displayed balance should immediately reflect the successful stake deduction.

### Actual
The UI balance remained unchanged immediately after the successful bet. After a hard refresh, the correct persisted balance was displayed.

### Business Impact
The displayed balance is temporarily stale and can mislead the user about available funds.

### Evidence
[Screen recording — UI balance not updated after successful bet](../evidence/bug-007-ui-balance-not-updated.mp4)
---

## BUG-008 — Invalid Odds Filter Range Is Not Rejected

**Severity:** Medium

### Reproduction Steps
1. Set minimum odds to a value greater than maximum odds.
2. Apply the filter.

Example:
- Minimum: 4.45
- Maximum: 2.30

### Expected
The invalid range should be rejected with clear validation feedback.

### Actual
The UI accepts the range and displays an empty result instead of reporting that the range is invalid.

### Business Impact
Users receive no clear explanation that the filter configuration itself is invalid.

### Evidence
[Odds filter](../evidence/bug-008-invalid-odds-filter.png)

---

## BUG-009 — Past Matches Are Displayed and Bettable

**Severity:** High

### Reproduction Steps
1. Retrieve the match list.
2. Identify a match whose kickoff date is in the past.
3. Locate the same match in the UI.
4. Select an outcome.
5. Place a valid bet.

### Expected
Only upcoming/pre-match events should be displayed and available for betting.

### Actual
Past matches are displayed, selectable, and a successful bet can be placed on them.

### Business Impact
Users can place bets on events that should no longer be eligible for betting.

### Evidence
[Past match listing](../evidence/bug-009-past-match.png)

---

## BUG-010 — Available Balance Missing From Bet Slip

**Severity:** Medium

### Reproduction Steps
1. Select an outcome.
2. Open the Bet Slip.
3. Inspect the information displayed in the slip.

### Expected
The Bet Slip should display the available balance along with stake and potential payout.

### Actual
The Bet Slip displays stake and potential payout information but does not display the available balance.

### Business Impact
Users cannot see their current available balance directly in the Bet Slip while preparing a bet.

### Evidence
[Payout slip - Missing balance](../evidence/bug-010-missing-balance.png)

---

## Observation — Filtered Match Count Remains 103

The UI continues to display a `103 matches` count even when a filter produces 3, 4, or 0 visible matches.

This is recorded as an observation rather than a primary defect because the supplied feature specification does not explicitly define a match-count display requirement.
