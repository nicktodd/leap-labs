# Demo: Module 5 - Pandas Fundamentals: DataFrames & Series

**Duration:** 18 minutes
**Files:** `pandas_intro_demo.py`
**Prerequisite:** `pip install pandas`

## Part 1: DataFrame and Series (4 min)

Load `shared/trades.csv` with `pd.read_csv()` and show the result. Narration: a `DataFrame` is a
table - rows and columns, like the list-of-dicts from Module 3, but with a name and a type per
column, and a huge library of operations that all understand its shape.

Select a single column (`df["value"]`) and show that its type is a `Series` - a `DataFrame` is,
structurally, a collection of named `Series` sharing an index. `type(df)` vs. `type(df["value"])`
makes this concrete.

## Part 2: Indexing and selection (5 min)

Show three ways to select data, narrating what each is for:

- `df["value"]` - a single column, by name
- `df.iloc[0]` - a single row, by position
- `df.loc[df["side"] == "BUY"]` - rows matching a condition (boolean indexing)

Narration: `.iloc` is position-based (like list indexing), `.loc` is label/condition-based. This
distinction trips people up constantly - call it out explicitly.

## Part 3: Filtering, and the Module 3 comparison (6 min)

Run the pandas equivalent of Module 3's per-instrument value summary:

```python
df.groupby("instrument")["value"].sum()
```

Put this next to Module 3's manual `for` loop with a `dict.get(key, 0.0) + value` accumulator.
Narration: same answer, from twenty lines of manual bookkeeping down to one. This is the payoff
Module 1 set up when it said "this whole demo could be five lines of pandas" - here they are.

Filter before aggregating to show the two compose naturally:

```python
df[df["side"] == "BUY"].groupby("instrument")["value"].sum()
```

## Part 4: What pandas *doesn't* remove (3 min)

Narration, important balance: pandas removes manual bookkeeping, it doesn't remove the need to
understand your data. `df["value"]` being numeric depends on `trades.csv` being clean - Module 6
is entirely about what happens when it isn't.

## Key message

A DataFrame is a table; a Series is one of its columns. `.loc`/`.iloc` select rows; boolean
indexing filters them; `groupby` aggregates them. Together these four operations replace most of
Module 3's manual loops - but only for data that's already in good shape.
