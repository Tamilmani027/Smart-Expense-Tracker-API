# AI Notes

I wrote a first draft myself (routes, a global dict for storage, some
half-working validation), then used Claude to review it and clean things up.

**What Claude actually changed:**
- Pointed out my `expense.id == ""` check was dead code — id is an int, so
  that comparison can never be true. Replaced it with real Pydantic
  validation (`gt=0`, `min_length=1`) that fails properly with a 422.
- Wrapped the global `expenses` dict in a small `ExpenseStore` class with
  dependency injection, instead of a bare module-level dict. This was
  mainly so tests could get a fresh store each time instead of sharing
  state across the whole test run.
- Split `/expenses/total` and `/expenses/category/{category}` onto
  separate paths — my original design would've had "total" get treated
  as if it were a category name.
- Wrote the full test suite and README from scratch.

**What I checked myself:**
- Ran `pytest tests/ -v` on a clean checkout — all pass.
- Hit `/expenses/total` and `/expenses/category/food` with curl manually
  to make sure they don't collide.
- Re-read the storage class to make sure `.delete()` returns `None` (not
  a crash) when the id doesn't exist, since that's what the 404 branch
  relies on.

**What I didn't take:**
- Claude suggested a monthly-summary endpoint as a bonus, on top of the
  Swagger docs. Skipped it — only one bonus is asked for, and Swagger
  comes free with FastAPI, so that's the one I'm counting.
- It also suggested writing expenses to a JSON file for persistence. Not
  needed here — the brief says in-memory is fine, and I didn't want to
  deal with file-write edge cases for something that wasn't asked for.