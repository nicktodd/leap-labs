# Module 8 Lab — MyBatis in Context: vs JPA/Hibernate

## Objectives

By the end of this lab you will have:

- Compared MyBatis and Spring Data JPA solving the exact same problem
- Formed (and written down) your own judgement on when to reach for each

## Format

This is a short, written discussion — not a coding kata. Work in pairs. You have two real
implementations to work from, not just opinions:

- `demos/07-persistence-with-mybatis/src/main/java/com/fidelity/leap/sprint6/InstrumentMapper.java`
- `demos/08-mybatis-in-context/src/main/java/com/fidelity/leap/sprint6/InstrumentRepository.java`

Run both (one at a time, both on port 8080) and hit `GET /instruments/AAPL` against each. Also
open `Instrument.java` in both projects.

## Questions

Write a short answer (2-4 sentences each) to every question below.

1. **Code volume.** Count the lines actually needed to implement `findByTicker` in each style
   (not counting the class declaration). Which is shorter, and why?

2. **Visibility.** In the MyBatis version, the exact SQL that will run is right there in the
   source. In the JPA version, it isn't — where does it come from instead, and how would you find
   out what SQL actually ran in production?

3. **The `Instrument` class itself.** Module 7's `Instrument` and Module 8's `Instrument` are
   *not* the same kind of object, even though they have the same fields. What's different about
   what happens to a Module 8 `Instrument` after it's loaded, that doesn't happen to a Module 7
   one?

4. **Trade a join.** Sketch (in words, not code) how you'd write "get a client's holdings, joined
   across holdings -> accounts -> instruments" (Module 7's `HoldingMapper`) using Spring Data JPA
   instead. Would it be easier or harder than the MyBatis XML version? What would you need to add
   to `Instrument`/`Holding` that isn't there today?

5. **Your call.** If the mission service were entirely new, would you pick MyBatis, JPA, or
   a mix of both? Justify it in terms of *this specific service* — order processing, holdings,
   transaction history — not persistence technology in the abstract.

## Deliverable

Your five written answers (a shared doc, or on paper, whatever your trainer prefers).

## Acceptance criteria

- All five questions answered, with a specific reason given each time (not just "it depends")
- Question 3 correctly identifies dirty checking / persistence context management as the
  difference, not just "JPA has annotations"
