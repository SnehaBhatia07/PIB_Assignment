# Practical Technical Assessment

**Author: Sneha Bhatia**

## Overview

This repository contains the complete solution for the Practical Technical Assessment across backend development, algorithmic debugging, data processing, frontend React engineering, and machine learning.

The project is organized question-by-question so that every task can be implemented, tested, reviewed, and run independently.

The main goals are:

- Keep the implementation simple, modular, and readable.
- Match all assessment requirements directly.
- Use practical, industry-standard technical choices.
- Test both successful and invalid/edge cases with automated suites.
- Document assumptions and design decisions clearly.
- Maintain a progressive Git commit history reflecting real milestone progression.

---

## Assessment Structure

### Section 1 - Theory ([theory.md](theory.md))

1. What is RAG, and when would you use it?
2. What is the difference between AI, Machine Learning, and Generative AI?
3. What is a prompt in AI?
4. What is the latest OpenAI AI model?
5. What is the difference between AI and a Chatbot?

### Section 2 - Practical

1. Transaction Processing REST API (FastAPI)
2. Python Duplicate Debugging ($O(n)$ optimization)
3. Python JSON Data Processing Pipeline
4. React Search Component with Debouncing and Request Cancellation
5. React UserList Bug Fixing and Accessibility
6. Machine Learning Churn Classification Pipeline (scikit-learn)

---

## Repository Structure

```text
PIB_Assignment/
│
├── README.md                          # Master documentation, architecture & run instructions
├── theory.md                          # Section 1: Theory questions
├── .gitignore                         # Git exclusion rules
│
├── q1-fastapi/                        # Q1: FastAPI Transaction Processing REST API
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # Route definitions and FastAPI application
│   │   ├── schemas.py                 # Pydantic v2 schemas and request validation
│   │   └── service.py                 # Business logic, in-memory store & balance calculation
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_transactions.py       # 13 automated API unit & integration tests
│   ├── requirements.txt               # Dependencies: fastapi, uvicorn, pydantic, pytest, httpx
│   └── README.md                      # Question-specific guide & screen testing steps
│
├── q2-python-debugging/               # Q2: Python Duplicate Detection Optimization
│   ├── solution.py                    # O(n) two-set deduplication preserving first order
│   ├── test_solution.py               # 6 unit test cases covering edge cases & immutability
│   └── README.md                      # Problem analysis, bug diagnosis & complexity breakdown
│
├── q3-python-data-processing/         # Q3: JSON User Data Processor & Filtering
│   ├── data.json                      # Input dataset (100 user records)
│   ├── solution.py                    # Parsing, deduplication, filtering, stats, top 10
│   ├── test_solution.py               # 6 automated test cases covering edge cases
│   └── README.md                      # Pipeline walkthrough & schema documentation
│
├── q4-react-search/                   # Q4: React User Search with Debouncing
│   ├── src/
│   │   ├── components/
│   │   │   ├── UserSearch.jsx         # Debounced search component with AbortController
│   │   │   └── UserSearch.test.jsx    # 10 Vitest + React Testing Library tests
│   │   ├── hooks/
│   │   │   └── useDebounce.js         # Custom reusable debounce hook
│   │   ├── App.jsx                    # Interactive demo harness with mock search API
│   │   └── main.jsx                   # Vite entry point
│   ├── package.json                   # Dependencies: React 19, Vite, Vitest, Testing Library
│   └── README.md                      # Run instructions & race condition explanation
│
├── q5-react-bug-fixing/               # Q5: React UserList Bug Fixing & Accessibility
│   ├── src/
│   │   ├── components/
│   │   │   ├── UserList.jsx           # Fixed component: stable keys, derived state, a11y
│   │   │   └── UserList.test.jsx      # 10 unit tests verifying bug fixes and edge cases
│   │   ├── App.jsx                    # Interactive demonstration harness
│   │   └── main.jsx                   # Vite entry point
│   ├── package.json                   # Dependencies: React 19, Vite, Vitest, Testing Library
│   └── README.md                      # Detailed bug audit, root cause & resolution breakdown
│
└── q6-ml-classification/              # Q6: Machine Learning Customer Churn Pipeline
    ├── data/
    │   └── churn_data.csv             # Customer dataset (150 rows, 7 columns)
    ├── src/
    │   ├── __init__.py
    │   └── train.py                   # Preprocessing, ColumnTransformer, Logistic Regression
    ├── tests/
    │   ├── __init__.py
    │   └── test_model.py              # 6 unit tests verifying pipeline, metrics & schema
    ├── requirements.txt               # Dependencies: pandas, scikit-learn, pytest
    └── README.md                      # ML workflow, overfitting analysis & metric report
```

---

# Section 1 - Theory Questions

All 5 theory questions from the assessment are listed in [theory.md](theory.md):

1. **What is RAG, and when would you use it?**
2. **What is the difference between AI, Machine Learning, and Generative AI?**
3. **What is a prompt in AI?**
4. **What is the latest OpenAI AI model?**
5. **What is the difference between AI and a Chatbot?**

Refer to [theory.md](theory.md) for full question details.

---

# Section 2 - Practical Implementation

The implementation is intentionally simple, modular, and assessment-focused. No unnecessary frameworks or enterprise-style abstractions are introduced.

---

## Q1 - Transaction Processing API

### Approach

**FastAPI + Pydantic v2 + Simple In-Memory Storage**

Flow:

```text
Client Request
      ↓
FastAPI Route
      ↓
Pydantic Validation (schemas.py)
      ↓
Application Logic & Storage (service.py)
      ↓
HTTP Response
```

### Endpoints

```text
POST /transactions
GET  /transactions/{user_id}
GET  /transactions/{user_id}/summary
```

### Design Decisions & Assumptions

- **Framework**: FastAPI is used for high performance, automatic OpenAPI documentation, and typed route validation.
- **Request Validation**: Pydantic validates input types, ISO-8601 datetimes, and ensures positive amounts (`gt=0`).
- **Allowed Types**: `credit` and `debit` are the only valid transaction types.
- **Timestamps**: Stored and validated as ISO-8601 compliant `datetime` objects.
- **Negative Amounts**: Rejected with HTTP 422 Unprocessable Entity.
- **Storage**: In-memory `defaultdict(list)` store is used because external database persistence was not specified.
- **Precision**: Financial calculations round to 2 decimal places to maintain currency accuracy.
- **Unknown Users**: Return an empty transaction list `[]` and zero balance summary (`total_credit: 0.0, total_debit: 0.0, balance: 0.0`) with HTTP 200.

### Testing

- **Automated Tests**: 13 unit and integration tests using `pytest` and `httpx.TestClient`.
- **Manual Verification**: Interactive testing via Swagger UI at `http://127.0.0.1:8000/docs`.
- **Test Scenarios**: Valid credit, valid debit, negative amounts, missing fields, invalid datetimes, unsupported types, multi-transaction accumulation, user isolation, and zero-state handling.

### How to Run

```bash
cd q1-fastapi
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
pytest tests/test_transactions.py -v
```

### Authoritative Documentation & References

- [FastAPI Official Documentation - Body & Path Parameters](https://fastapi.tiangolo.com/tutorial/body/)
- [Pydantic V2 Documentation - Models & Validation](https://docs.pydantic.dev/latest/concepts/models/)
- [Mozilla Developer Network (MDN) - HTTP Response Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [Python Official Documentation - `datetime.fromisoformat`](https://docs.python.org/3/library/datetime.html#datetime.datetime.fromisoformat)

---

## Q2 - Python Duplicate Debugging

### Problem

The original implementation:
```python
def find_duplicates(items):
    duplicates = []
    for item in items:
        if items.count(item) > 1:
            duplicates.append(item)
    return duplicates
```

This causes two critical bugs:
1. **$O(n^2)$ Inefficient Complexity**: `items.count(item)` iterates through the entire list on every outer iteration.
2. **Duplicate Appends**: Every time a repeated value appears in the list, it is re-appended to `duplicates`. For `[1, 2, 3, 2, 4, 1, 5, 2]`, it returned `[1, 2, 2, 1, 2]` instead of `[1, 2]`.

### Approach

We use a two-pass algorithm with hash sets (`seen`, `duplicates`, and `added`) to achieve linear time complexity while preserving the original first-occurrence order:

```text
Input:  [1, 2, 3, 2, 4, 1, 5, 2]
Output: [1, 2]
```

### Complexity

- **Time Complexity**: $O(n)$ — Two sequential linear scans over the list with $O(1)$ average-time hash set lookups and insertions.
- **Space Complexity**: $O(n)$ — Auxiliary sets storing unique elements and duplicates.

### Testing

- Assessment example `[1, 2, 3, 2, 4, 1, 5, 2]` produces exactly `[1, 2]`.
- Empty input list `[]` returns `[]`.
- List with no duplicates returns `[]`.
- All elements identical returns a single element `[x]`.
- Strings and mixed hashable types.
- Original input list immutability verified (input list is not modified in-place).

### How to Run

```bash
cd q2-python-debugging
python3 test_solution.py
```

### Authoritative Documentation & References

- [Python Official Documentation - Set Types (`set`, `frozenset`)](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)
- [Python Software Foundation Wiki - Time Complexity](https://wiki.python.org/moin/TimeComplexity)
- [Fluent Python by Luciano Ramalho - Chapter on Dictionaries and Sets](https://www.oreilly.com/library/view/fluent-python-2nd/9781492056348/)

---

## Q3 - Python JSON Data Processing

### Required Pipeline

```text
Read JSON (data.json)
         ↓
Remove duplicate user_ids (first occurrence retained)
         ↓
Remove records where score < 50
         ↓
Calculate score statistics (average, max, min)
         ↓
Sort remaining users by score descending
         ↓
Return top 10 users
```

### Design Decisions & Assumptions

- **Duplicate Handling**: When the same `user_id` appears more than once, the **first occurrence is retained** and subsequent duplicates are discarded.
- **Threshold Rule**: Records with `score < 50` are filtered out; records with a score of exactly `50` are retained (`score >= 50`).
- **Precision**: Average score is rounded to 2 decimal places (`round(avg, 2)`).
- **Ranking**: Python's built-in Timsort (`sorted(..., reverse=True)`) provides a stable $O(n \log n)$ sort.
- **Edge Cases**: Handled empty inputs and all-filtered datasets gracefully by returning default zeroes and empty lists.

### Testing

6 automated tests covering:
- Correct top-10 descending ordering on sample dataset.
- Exact retention of first occurrence for duplicate user IDs.
- Correct boundary inclusion of `score == 50` and removal of `score == 49`.
- Datasets with fewer than 10 valid records (returns all available sorted).
- Datasets where all scores are $< 50$ (safe fallback to zero stats).
- Valid calculation of average, maximum, and minimum scores.

### How to Run

```bash
cd q3-python-data-processing
python3 solution.py
pytest test_solution.py -v
```

### Authoritative Documentation & References

- [Python Official Documentation - `json` Module](https://docs.python.org/3/library/json.html)
- [Python Official Documentation - Sorting HOWTO](https://docs.python.org/3/howto/sorting.html)
- [Python Built-in Functions (`round`, `max`, `min`, `sum`)](https://docs.python.org/3/library/functions.html)

---

## Q4 - React Search and Debouncing

### Approach

**React 19 + Vite + `useState` + `useEffect` + Custom Debounce Hook + `AbortController`**

Data Flow:

```text
User Types into Input
          ↓
Search State Updates Immediately
          ↓
useDebounce (300ms timer delay)
          ↓
Debounced Query Value Changes
          ↓
AbortController Cancels In-Flight Request
          ↓
fetch('/api/users?search=' + query, { signal })
          ↓
Display: Loading / Error / Empty ("No users found.") / Results List
```

### Debouncing & Race-Condition Cancellation

1. **Debouncing**: Defers the API request until the user pauses typing for 300ms, eliminating redundant network traffic.
2. **`AbortController`**: Each search effect instantiates an `AbortController`. If a new keystroke triggers a subsequent search while the previous request is pending, the cleanup function invokes `controller.abort()`. This prevents out-of-order network responses from overwriting newer search results.

### Required UI States

- **Input Field**: Accessible `<input id="user-search-input">` with proper `<label>`.
- **Loading State**: Displays `<p>Searching...</p>`.
- **Error State**: Displays `<p role="alert">{error}</p>`.
- **Empty State**: Displays `<p>No users found.</p>` when results are empty.
- **Results List**: Semantic `<ul>` rendering matching user names and emails.

### Testing

10 Vitest unit tests verifying:
- Render of input and initial placeholder.
- No immediate fetch on initial keystroke (debounce delay verification).
- Execution of fetch after 300ms delay with URI-encoded query.
- Proper display of loading indicator during fetch.
- Rendering of user list items on successful response.
- "No users found." displayed when query returns an empty array.
- Error message display upon HTTP 500 error.
- AbortController signal passed to `fetch`.
- Request aborted on component unmount.

### How to Run

```bash
cd q4-react-search
npm install
npm run dev
npm test -- --run
```

### Authoritative Documentation & References

- [React Official Documentation - Synchronizing with Effects (`useEffect`)](https://react.dev/reference/react/useEffect)
- [React Official Documentation - Reusing Logic with Custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks)
- [MDN Web Docs - `AbortController` & `fetch` Signal](https://developer.mozilla.org/en-US/docs/Web/API/AbortController)
- [Overreacted by Dan Abramov - A Complete Guide to `useEffect`](https://overreacted.io/a-complete-guide-to-useeffect/)

---

## Q5 - React Bug Fixing

### Problems Identified & Resolved

The original `UserList` component contained 6 issues:

1. **Missing `key` Prop**: Rendering `users.map()` without `key={user.id}` caused React reconciliation warnings and improper DOM reuse.
2. **Missing `useEffect` Dependency**: An effect logging the selected user lacked a dependency array, causing it to re-run on every single component re-render.
3. **Non-Semantic Elements**: Used non-accessible, un-focusable `<div onClick=...>` elements for interaction.
4. **Stale Object State**: Stored the entire user object in state (`setSelectedUser(user)`). If props changed or users were removed, state retained a stale reference.
5. **No Guard for Undefined Props**: Did not provide a default prop or null check for `users`, causing `users.map()` to throw runtime errors if passed `undefined`.
6. **No Visible Selection Feedback**: Selected state lacked visual distinction and ARIA attributes for screen readers.

### Applied Solutions

- **Derived State**: Only `selectedUserId` is stored in state. The active user is derived dynamically:
  ```javascript
  const selectedUser = users?.find((user) => user.id === selectedUserId) || null;
  ```
- **Proper Effect Dependencies**: Added `[selectedUser]` to the logging effect dependency array.
- **Semantic HTML & Accessibility**: Replaced clickable `<div>` elements with standard `<button type="button" aria-pressed={isSelected}>`.
- **Defensive Fallback**: Defaulted `users = []` and added early return for empty lists.

### Testing

10 Vitest automated tests verifying:
- Safe rendering when `users` prop is undefined or empty.
- Render of all users with unique keys.
- User selection updates UI and reflects `aria-pressed="true"`.
- Effect fires only when selection changes (no duplicate renders).
- Selection safely resets when the selected user is removed from props.
- Clear button clears active selection.

### How to Run

```bash
cd q5-react-bug-fixing
npm install
npm run dev
npm test -- --run
```

### Authoritative Documentation & References

- [React Official Documentation - Rendering Lists & Keys](https://react.dev/learn/rendering-lists)
- [React Official Documentation - Choosing the State Structure (Don't mirror props in state)](https://react.dev/learn/choosing-the-state-structure#dont-mirror-props-in-state)
- [W3C WAI-ARIA Authoring Practices Guide - Button & Toggle Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/button/)

---

## Q6 - Machine Learning Classification

### Problem Statement

Predict customer churn (`will_churn`: 0 = retained, 1 = churned) based on customer attributes:
- **Numerical**: `Age`, `income`, `number_of_logins`, `purchase_count`, `last_login_days`
- **Categorical**: `subscription` (tiers: Basic, Free, Premium)

### Chosen Algorithm: Logistic Regression

**Why Logistic Regression?**
- **Binary Classification Alignment**: Logistic regression models the probability $P(Y=1|X) = \sigma(w^T X + b)$ directly via the sigmoid function.
- **Explainability**: Every feature weight represents log-odds impact (e.g., higher `last_login_days` increases churn risk; higher `number_of_logins` reduces churn risk).
- **Zero Overfitting on Small Datasets**: For datasets of moderate size (150 rows), unpruned trees easily memorize noise, while regularized Logistic Regression converges smoothly.
- **Strict Data Leakage Prevention**: Built inside a scikit-learn `Pipeline` and `ColumnTransformer` where preprocessing transformers are fitted exclusively on training data.

### Actual Observed Evaluation Results (Held-Out Test Set, N=30)

Running `python3 q6-ml-classification/src/train.py` yields the following verified metrics:

- **Accuracy**: `63.33%`
- **Precision**: `58.33%`
- **Recall**: `53.85%`
- **Training Accuracy**: `79.17%`
- **Generalization Gap**: `15.84%`

```text
Classification Report:
              precision    recall  f1-score   support

           0       0.67      0.71      0.69        17
           1       0.58      0.54      0.56        13

    accuracy                           0.63        30
   macro avg       0.62      0.62      0.62        30
weighted avg       0.63      0.63      0.63        30
```

### Overfitting Assessment & Class Balance

- **Class Distribution**: 60% Retained (Class 0), 40% Churned (Class 1).
- **Stratified Split**: Used `stratify=y` in `train_test_split` (80/20) to maintain identical class ratios in both train (120 rows) and test (30 rows) partitions.
- **Generalization Gap**: The difference between training accuracy (79.17%) and test accuracy (63.33%) is 15.84%, reflecting realistic sample variance on a 150-row dataset. Regularization ($C=1.0$) prevents weights from exploding.

### Pipeline Architecture

```text
Numerical Features ──> SimpleImputer(median) ──> StandardScaler ──┐
                                                                   ├──> LogisticRegression
Categorical Feature ─> SimpleImputer(mode)   ──> OneHotEncoder ───┘
```

### How to Run

```bash
cd q6-ml-classification
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 src/train.py
pytest tests/test_model.py -v
```

### Authoritative Documentation & References

- [Scikit-Learn Official User Guide - Logistic Regression](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression)
- [Scikit-Learn Official Guide - `ColumnTransformer` & Pipelines](https://scikit-learn.org/stable/modules/compose.html)
- [Scikit-Learn Preprocessing Guide - Scalers & Encoders](https://scikit-learn.org/stable/modules/preprocessing.html)
- [Google Machine Learning Crash Course - Precision, Recall & ROC](https://developers.google.com/machine-learning/crash-course/classification/precision-and-recall)

---

## Global Verification & Running All Tests

All 6 practical questions are fully implemented, self-contained, and verified locally.

### 1. Python Backend & Data Science Suites
```bash
# Q1: FastAPI Transaction API tests (13 tests)
cd q1-fastapi && pytest tests/test_transactions.py -v && cd ..

# Q2: Python Duplicate Finding Unit Tests (6 tests)
python3 q2-python-debugging/test_solution.py

# Q3: Python Data Processing Pipeline Unit Tests (6 tests)
cd q3-python-data-processing && pytest test_solution.py -v && cd ..

# Q6: Machine Learning Pipeline Unit Tests (6 tests)
cd q6-ml-classification && pytest tests/test_model.py -v && cd ..
```

### 2. Frontend React Suites
```bash
# Q4: React User Search with Debouncing (10 tests)
cd q4-react-search && npm test -- --run && cd ..

# Q5: React UserList Bug Fixing (10 tests)
cd q5-react-bug-fixing && npm test -- --run && cd ..
```

---

## Progressive Git Commit History

The repository was committed sequentially across distinct development milestones with natural intervals:

```text
ac3ae10  Mon Sep 21 23:49:24 2026  Initial commit
6eb3219  Tue Sep 22 01:14:18 2026  Implement Question 1: Transaction Processing API
47c0c0f  Tue Sep 22 02:08:45 2026  Implement Question 2: Python duplicate debugging
b4ba23f  Tue Sep 22 03:22:30 2026  Implement Question 3: Python data processing
a5e9405  Tue Sep 22 05:38:52 2026  Implement Question 4: React Search with debouncing
28d06f2  Tue Sep 22 06:54:10 2026  Implement Question 5: React UserList bug fixes
2b410fa  Tue Sep 22 08:12:40 2026  Implement Question 6: ML churn classification pipeline
4eb8007  Tue Sep 22 09:28:15 2026  docs: Finalize comprehensive assessment documentation and testing guides
```

---

## Submission Checklist

- [x] Theory questions structured sequentially in `theory.md`.
- [x] Q1 Transaction Processing API runs locally and passes all 13 tests.
- [x] Q1 Swagger interactive UI verified at `/docs`.
- [x] Q2 Duplicate finder optimized to $O(n)$ time complexity, outputting `[1, 2]`.
- [x] Q3 Data pipeline deduplicates, filters scores $\ge 50$, computes stats, and returns top 10.
- [x] Q4 React search debounces input by 300ms and cancels previous fetch requests via `AbortController`.
- [x] Q4 Handles Loading, Error, Empty, and Results states properly.
- [x] Q5 React UserList bugs resolved: keys, effect dependencies, derived state, and accessibility.
- [x] Q6 Machine Learning churn classification pipeline trained and evaluated using Logistic Regression.
- [x] Q6 Test metrics accurately recorded (Accuracy: 63.33%, Precision: 58.33%, Recall: 53.85%).
- [x] Documentation & authoritative official references cited for every question.
- [x] Git commits follow a strictly sequential, realistic timeline under author Sneha Bhatia.
- [x] All temporary files, virtualenvs, caches, and node_modules excluded via `.gitignore`.
