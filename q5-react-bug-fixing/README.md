# Q5: React Bug Fixing

A corrected and optimized implementation of `UserList` addressing all bugs identified in the original assessment code:
- Added missing unique `key` prop using `user.id`.
- Added dependency array `[selectedUser]` to `useEffect` to prevent log spamming on every render.
- Converted duplicated state into derived state by tracking `selectedUserId` and computing `selectedUser` directly from `users`.
- Automatically handles user removal and updates without stale state or manual synchronization.
- Converted non-semantic `<div onClick>` elements to accessible `<button>` components with `aria-pressed`.
- Added defensive prop fallback for `users = []`.

## How to Run
```bash
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

## How to Test on Your Screen
1. Open `http://localhost:5173` in your browser.
2. **Selecting a User**: Click on any user (e.g. `Alice`). Notice the button gets highlighted and `Selected: Alice` appears below.
3. **Clearing Selection**: Click the **Clear** button. The selection highlight clears.
4. **Automatic Stale-State Protection**: Select `Alice`, then click **Remove Alice (ID 1)** on screen. Alice disappears and selection resets cleanly without errors.

## Running Tests
```bash
npm test
```
All 8 Vitest tests pass.
