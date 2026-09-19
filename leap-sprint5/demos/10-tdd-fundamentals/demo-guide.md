# Module 10 Demo Guide — TDD Fundamentals

This is a **live-coding** demo. Delete `TickerValidator.java`'s body and
`TickerValidatorTest.java`'s contents before the session (keep a copy to restore afterward, or
just re-type it live — either is fine). Build it back up in front of the group, one
red-green-refactor cycle at a time, exactly in this order. Narrate the three steps out loud every
single time, even once it starts to feel repetitive — the repetition IS the discipline.

## The Cycle, Said Out Loud Every Time

1. **Red** — write ONE new test, for ONE new piece of behaviour. Run it. Watch it fail. Read the
   failure message.
2. **Green** — write the SMALLEST amount of code that makes it pass. Not the smallest *sensible*
   amount — the smallest amount, full stop, even if it looks silly.
3. **Refactor** — with the safety net of passing tests, clean up anything that needs it. Run the
   tests again to confirm nothing broke.

## Cycle 1: The Simplest Possible Case

**Red:**
```java
@Test
void acceptsAStandardTicker() {
    assertTrue(new TickerValidator().isValid("AAPL"));
}
```
Run it — fails, because `isValid` doesn't exist yet (or returns `false`/isn't implemented).

**Green — the smallest thing that passes, even though it looks absurd:**
```java
public boolean isValid(String ticker) {
    return true;
}
```
**Say this explicitly:** "Yes, this is a silly implementation. That's fine — it's honestly the
smallest thing that makes the one test we have pass. We haven't earned the right to write
anything more sophisticated yet, because nothing is asking for it."

**Refactor:** nothing to refactor yet.

## Cycle 2: Forcing a Real Check

**Red:**
```java
@Test
void rejectsAnEmptyString() {
    assertFalse(new TickerValidator().isValid(""));
}
```
Run it — fails, because `isValid` still just returns `true` unconditionally.

**Green:**
```java
public boolean isValid(String ticker) {
    return !ticker.isEmpty();
}
```
Run both tests — both pass.

## Cycle 3: Case Sensitivity

**Red:**
```java
@Test
void rejectsLowercase() {
    assertFalse(new TickerValidator().isValid("aapl"));
}
```
**Green:** add an uppercase check — a loop over characters calling `Character.isUpperCase`.

## Cycle 4: Length

**Red:**
```java
@Test
void rejectsMoreThanFiveLetters() {
    assertFalse(new TickerValidator().isValid("TOOLONG"));
}
```
**Green:** add a length check.

## Cycle 5: Digits

**Red:**
```java
@Test
void rejectsDigits() {
    assertFalse(new TickerValidator().isValid("AAPL1"));
}
```
**Green:** the character loop now also checks `Character.isLetter`.

**Refactor, for real this time:** the character-checking loop and the length check are both
about validating the "base" ticker. This is a natural point to extract a private helper and
name things properly — do this live, and re-run the tests immediately after to prove nothing
broke.

## Cycle 6: The London Suffix

**Red:**
```java
@Test
void acceptsTheLondonSuffix() {
    assertTrue(new TickerValidator().isValid("VOD.L"));
}
```
This one's harder — "VOD.L" is 5 characters, but the `.L` isn't part of the ticker itself. Watch
it fail against the naive length/character check.

**Green:** strip a trailing `.L` before running the existing checks.

**Refactor:** extract `LONDON_SUFFIX` and `MAX_BASE_LENGTH` as named constants (Module 9's clean
code checklist, still applying here).

## Cycle 7 (bonus, if time allows): `null`

**Red:**
```java
@Test
void rejectsNull() {
    assertFalse(new TickerValidator().isValid(null));
}
```
**Green:** a null check at the top of the method.

## Points to Make Explicitly

- **Every single test was written before the code that satisfies it.** Nobody wrote
  `TickerValidator` and then tests to match — the tests are what *drove* each addition to the
  implementation.
- **The implementation only ever does exactly what a test demands.** Notice there's no
  speculative handling for cases nobody's written a test for yet (e.g., tab/whitespace
  characters) — that's not an oversight, it's TDD's discipline against over-building.
- **"Smallest thing that passes" felt uncomfortable in Cycle 1, and that's normal.** Point out
  that the discomfort fades once the pattern of "next test forces the next real behaviour"
  becomes visible.

## Transition to the Lab

Learners now run this exact cycle themselves, from a blank class, building a `FeeBandClassifier`
— see `labs/10-tdd-fundamentals/README.md` for the step list they'll follow.
