# Q4: React Search and Debouncing

A clean, practical React search component implementing:
- Controlled input
- Custom `useDebounce` hook (300ms)
- Native `fetch` with `encodeURIComponent`
- `AbortController` cancellation for outdated/stale requests
- Distinct UI states: initial, loading (`Searching...`), success (user list), empty (`No users found.`), and error

## How to Run
```bash
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

## How to Test on Your Screen
1. Open `http://localhost:5173` in your browser.
2. **Debounce Test**: Type quickly into the search box. Requests are paused until typing stops for 300ms.
3. **Loading State**: While fetching, `Searching...` appears on screen.
4. **Empty Results**: Type a non-existent name like `xyz123` to see `No users found.` on screen.
5. **Clear Query**: Clear the input box to instantly clear results with zero network requests.

## Running Tests
```bash
npm test
```
All 12 Vitest tests pass.
