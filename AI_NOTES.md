# AI Notes

I wrote the first draft myself — routes, a global dict for storage, and
validation that looked right but wasn't (`expense.id == ""`, where `id` is
an `int`, so that check could never fire). I used Claude to review it,
catch bugs like that, and help me restructure the parts that needed it.

## AI-generated vs. mine
- **Mine:** initial route design, endpoint choices, decision on what to
  validate (positive amounts, non-blank fields), decision to use dependency
  injection for storage.
- **AI-generated, then reviewed by me:** the `ExpenseStore` class, the full
  test suite (`tests/test_api.py`), the README, and the fix to how
  `/expenses/total` and `/expenses/category/{category}` are routed.

## What I validated and why
- **Dead validation logic** — my `id == ""` / `title == ""` checks were
  unreachable since Pydantic already rejects malformed input before the
  route runs. Replaced with `Field(gt=0)` / `min_length=1` so bad input
  fails fast with a 422 instead of silently passing through.
- **Route collision** — my original design would have treated `total` as
  a category name if someone hit `/expenses/total`. Fixed by giving total
  and category-filter their own sub-paths. I confirmed this with curl
  against both endpoints, not just by reading the code.
- **Shared test state** — the AI's first version reused one global dict
  across all tests, so test order could affect results. Moved storage into
  a class injected per-test via `app.dependency_overrides`, then ran the
  suite in a different order to confirm nothing broke because of it.
- **Silent failure on delete** — checked that `ExpenseStore.delete()`
  returns `None` for a missing id rather than raising, since the 404
  branch in the route depends on that.
- Ran `pytest tests/ -v` on a clean checkout before submitting — 14/14 pass.

## What I didn't use
- A monthly-summary endpoint, suggested as an extra bonus. The brief caps
  bonuses at one, and I'm already claiming Swagger docs (free with
  FastAPI), so I left it out rather than over-scope.
- JSON-file persistence. The brief explicitly allows in-memory storage,
  and adding file I/O would mean handling read/write race conditions that
  weren't part of the ask.