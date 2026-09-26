# Sporty Group HQA Assignment

Pytest automation for the Single Bet Placement feature. The project contains a
focused Selenium UI smoke test, an API business-rule test, and the manual QA
deliverables required by the assignment.

## Technology

- Python 3.14+
- Pytest
- Selenium WebDriver with desktop Chrome
- `requests` for API testing
- Allure Pytest integration
- `pytest-xdist` for parallel test execution
- Poetry for dependency management

## Project structure

```text
api_services/       API service objects
core/               Configuration, API client, UI client, and logging
ui_pages/           Selenium Page Objects and locators
tests/api/          API tests
tests/ui/           UI tests and UI fixtures
docs/               Test plan, execution results, and strategy
evidence/           Defect evidence
```

## Prerequisites

Install the following before running the suite:

- Python 3.14 or newer
- Poetry
- Latest desktop Google Chrome
- Network access to the test application

Selenium Manager resolves the compatible Chrome driver automatically in most
environments.

## Installation

From the repository root:

```bash
poetry install
```

To enter the Poetry virtual environment:

```bash
poetry shell
```

Alternatively, prefix commands with `poetry run`.

## Configuration

Defaults are defined in `core/config.py` and can be overridden with environment
variables:

| Variable            | Default                                 | Purpose                                    |
| ------------------- | --------------------------------------- | ------------------------------------------ |
| `BASE_URL`          | `https://qae-assignment-tau.vercel.app` | Application base URL                       |
| `USER_ID`           | Assignment candidate user               | Base user ID                               |
| `TEST_USER_ID`      | Value of `USER_ID`                      | Explicit test user ID                      |
| `API_PREFIX`        | `/api`                                  | API path prefix                            |
| `API_TIMEOUT`       | `10`                                    | API timeout in seconds                     |
| `UI_TIMEOUT`        | `10`                                    | Selenium wait timeout in seconds           |
| `INITIAL_BALANCE`   | `125.50`                                | Expected reset balance                     |
| `CURRENCY`          | `EUR`                                   | Expected currency                          |
| `DEFAULT_STAKE`     | `10.00`                                 | UI test stake                              |
| `DEFAULT_SELECTION` | `home`                                  | UI test outcome: `home`, `draw`, or `away` |

Example:

```bash
BASE_URL="https://qae-assignment-tau.vercel.app" \
USER_ID="candidate-7MCypfTSAdl3" \
poetry run pytest
```

`TEST_USER_ID` can be explicitly set when a dedicated test account is available:

```bash
TEST_USER_ID="candidate-7MCypfTSAdl3" poetry run pytest
```

When xdist is active, tests use the configured TEST_USER_ID. The current
assignment contains two tests that can run safely in parallel because their
state changes do not overlap during execution. As the suite grows, additional
state-mutating tests may require isolated users or test data to avoid
cross-test interference.

## Running the tests

The default Pytest configuration runs tests in parallel using pytest-xdist
and automatically determines the worker count and writes Allure results to `allure-results/`.

Run the complete suite:

```bash
poetry run pytest
```

Run only API tests:

```bash
poetry run pytest -m api
```

Run only UI tests:

```bash
poetry run pytest -m ui
```

Run a specific test file:

```bash
poetry run pytest tests/api/test_betting_api.py
poetry run pytest tests/ui/test_match_page.py
```

Run sequentially for debugging or when shared test state must be isolated:

```bash
poetry run pytest -n 1 -s
```

The UI fixture in `tests/ui/conftest.py` resets the worker-scoped balance before
and after each UI test. The API test resets the balance as part of its own
scenario. When using the single test user supplied with the assignment,
state-mutating tests should be run sequentially to avoid shared-state
interference.

## Allure reporting

The test run generates raw results automatically. If the Allure CLI is installed,
open an interactive report with:

```bash
allure serve allure-results
```

To generate a report directory instead:

```bash
allure generate allure-results -o allure-report
```

Generated `allure-results/` and `allure-report/` directories are ignored by Git.

When a UI test fails, the framework also saves a screenshot under
`test-artifacts/screenshots/` and attaches the screenshot and failure URL to the
Allure result. These artifacts are ignored by Git.

## Expected results

The automated tests intentionally assert the requirements identified during
manual execution. Against the currently observed application state, failures may
be expected, including reset-balance inconsistency and incorrect receipt values.
These failures represent product defects documented in
`docs/execution_results.md`; they are not test implementation errors.

## QA deliverables

- [Test plan](docs/test_plan.md)
- [Execution results and bug reports](docs/execution_results.md)
- [Strategy and recommendations](docs/strategy_recommendations.md)

## Scope

The automation intentionally covers one critical UI journey and one API
business-rule check, as required by the assignment. Broader stake validation,
insufficient-balance, filtering, authorization, and contract coverage are
identified as future regression-suite extensions in the strategy document.
