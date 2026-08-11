# Starter Codebase — Trade Report Generator

A small, real, currently-working utility: reads `trades.csv`, calculates trade value and fees per
instrument, prints a per-ticker summary, and writes `report.csv`.

It's also the codebase this sprint's refactor mission runs against, from Module 1 through Module
13. Nobody has touched it in a while. It works — that's not in question. What it costs to keep
working, and what it would cost to safely change, is the question this sprint asks.

## Run it

```bash
cd shared/starter-codebase
mvn compile
java -cp target/classes com.neueda.leap.sprint7.legacy.TradeReportGenerator
```

Reads `src/main/resources/trades.csv` by default (or pass a path as the first argument), prints a
summary to the console, and writes `report.csv` to the current directory.

## Run the tests

From Module 11 onward, this codebase has a growing test suite — start with a characterisation
test that locks in current behaviour, then focused unit tests added as each safe refactoring
step makes something newly testable:

```bash
cd shared/starter-codebase
mvn test
```

## Do not fix anything here yet

This codebase is the subject of Module 1's review lab, Module 10's code smell hunt, and Module
11's characterisation-tests-then-refactor exercise. Changing it now would remove the point of
those later modules. If you've spotted something — good, write it down, and hang onto it.
