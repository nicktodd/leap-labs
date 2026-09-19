# Module 04 — Going Further (Optional)

Finished the core lab already? These extension exercises dig a little deeper into the PowerShell
equivalents of what you covered in Module 03's Linux lab: chaining pipeline commands, searching
text with `Select-String` and regular expressions, inspecting permissions in more detail, and
finding files by criteria other than name.

They build directly on `sample-workspace/` from the core lab, so work through the core lab first
if you haven't already.

There's no acceptance-checking here; work at your own pace, and compare notes with a partner or
your trainer if you get stuck. Answers are in
[`solutions/04-powershell-fundamentals/going-further-answers.md`](../../solutions/04-powershell-fundamentals/going-further-answers.md)
if you want to check your work — try each exercise yourself first.

## 1. Chaining the object pipeline further

Module 03 introduced Unix pipes as plain text passed between commands. PowerShell's pipeline
passes structured objects instead, which is what lets you chain filtering, sorting, and grouping
without any text parsing.

- List every file under `sample-workspace`, recursively, and use `Measure-Object` to count how
  many there are without looking at the list.
- List every file under `sample-workspace`, group them by extension with `Group-Object
  Extension`, and sort the groups by count, largest first.
- Chain three pipeline stages together: list every file recursively, filter to only files larger
  than 200 bytes, and sort by size descending.
- Compare `Where-Object { $_.Length -gt 200 }` with `Where-Object Length -gt 200` (no script
  block). Both work — look up why PowerShell allows the second, shorter form.

## 2. Searching text with Select-String

`Select-String` is PowerShell's equivalent of `grep` — it searches text and, because its output
is an object, you can pipe the results into further cmdlets rather than just printing them.

- Search `logs/app.log` for every line containing `INFO`, and use `Measure-Object` on the result
  to count how many matches there are.
- Search `logs/app.log` for `INFO` case-insensitively, so it would also catch `info` or `Info`
  (check `Select-String`'s default case sensitivity first).
- Search `logs/app.log` for lines that do **not** contain `INFO` — `Select-String` has a
  `-NotMatch` switch for this.
- Search recursively through all of `sample-workspace` for the word `app`, regardless of which
  file it's in, and show which filename each match came from.

## 3. A gentle introduction to regular expressions

`Select-String -Pattern` accepts a full .NET regular expression by default, not just a fixed
string. Try these against `logs/app.log`:

- Match any line that starts with a 4-digit year, e.g. `2026-08-19` — hint: `^` anchors to the
  start of a line, and `\d` matches a single digit.
- Match any line containing either `ERROR` or `WARN` in a single command, using `|` inside the
  pattern to mean "or".
- Match any line containing a port number that is exactly four digits, e.g. `5432`, using `{4}`
  to mean "exactly four repetitions" of a digit.
- Extend the year-matching pattern from the first bullet to match the full timestamp format
  `YYYY-MM-DD HH:MM:SS` at the start of a line.
- On the matches from the timestamp pattern, add `-AllMatches` and inspect `$_.Matches.Value` on
  the result — this is how you pull out just the matched text rather than the whole line.

The same regex syntax you use here works in `grep -E` from Module 03, in most programming
languages, and in VS Code's find-and-replace — it isn't a PowerShell-only skill.

## 4. Permissions in more detail

Windows doesn't use the `rwx`/owner-group-other model from Module 03 — it uses **Access Control
Lists (ACLs)**, where each user or group gets an explicit list of allowed or denied rights.

- Run `Get-Acl notes.txt | Format-List` on the `notes.txt` file inside `sample-workspace` and
  identify the `Owner` and `Access` properties.
- Run `icacls notes.txt` from the same folder and compare its output to what `Get-Acl` showed
  you — same underlying permissions, different presentation.
- Look up what `icacls` output like `(R)`, `(W)`, and `(F)` mean.
- In your own words, write one sentence contrasting this model with the `chmod 600` style
  permissions from Module 03 — what does Windows let you express that a simple `rwx` triad
  cannot?

## 5. Finding files with Get-ChildItem

Module 03 used `find` to locate files by criteria other than name. `Get-ChildItem` with
`-Recurse`, `-Filter`, and `Where-Object` does the same job in PowerShell.

- Use `Get-ChildItem -Recurse` to list every file under `sample-workspace`, then filter down to
  only files (not directories) — check what `-File` does versus filtering on `PSIsContainer`.
- List only the files under `sample-workspace` with a `.json` extension.
- List files under `sample-workspace` that were modified in the last day (`LastWriteTime`).
- Combine `Get-ChildItem -Recurse` with `ForEach-Object` to run a command against every `.txt`
  file found — for example, print each file's line count using `Get-Content ... | Measure-Object
  -Line`.

## 6. Put it together

Write a single pipeline that:

1. Finds every file under `sample-workspace`, recursively.
2. Filters down to only files with a `.txt` or `.log` extension.
3. Searches each one for lines containing the word `error` (case-insensitive) using
   `Select-String`.
4. Counts how many matching lines were found in total.

There's more than one valid way to combine `Get-ChildItem`, `Select-String`, and `Measure-Object`
to do this — if your first attempt works, try to think of a second way.
