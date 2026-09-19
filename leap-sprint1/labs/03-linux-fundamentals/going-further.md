# Module 03 — Going Further (Optional)

Finished the core lab already? These extension exercises dig a little deeper into topics you've
only touched on so far: piping commands together, searching text with `grep` and regular
expressions, permissions in more detail, and finding files by criteria other than name.

They build directly on the files you already created in the task sheet — `sprint1-notes/`,
`sprint1-notes/archive/`, and `~/sprint1/logs/app.log` — so work through the core lab first if
you haven't already.

There's no acceptance-checking here; work at your own pace, and compare notes with a partner or
your trainer if you get stuck. Answers are in
[`solutions/03-linux-fundamentals/going-further-answers.md`](../../solutions/03-linux-fundamentals/going-further-answers.md)
if you want to check your work — try each exercise yourself first.

## 1. Piping and chaining commands

The `|` (pipe) symbol sends the output of one command in as the input to the next, so you can
combine simple commands into something more powerful without writing a script.

- Count how many lines are in `app.log` using `wc -l`, without opening the file.
- List the contents of your home directory and pipe the result into `sort` so it's alphabetical
  (it already is by default with `ls`, so instead pipe `ls -la` into `sort -k5 -n` to sort by
  file size — the fifth column in a long listing).
- Chain three commands together: list the contents of `~/sprint1/logs/`, filter for lines
  containing `.log`, and count how many there are — all in a single line using two pipes.
- Look up what `&&` does versus `;` when running two commands on one line. Run
  `false && echo "this won't print"` and then `false; echo "this will print"` and explain the
  difference in your own words.

## 2. Searching text with grep

- Search `app.log` for every line containing `INFO` and count how many there are, without
  looking at the output — `grep` has a flag for this.
- Search `app.log` for `INFO` but make the match case-insensitive, so it would also catch `info`
  or `Info`.
- Search `app.log` for lines that do **not** contain `INFO` — `grep` has a flag to invert a
  match.
- Search `app.log` for `WARN` and show two lines of context after each match (`grep` has a flag
  for trailing context).
- Search recursively through your entire `sprint1-notes` directory for the word `Linux`,
  regardless of which file it's in.

## 3. A gentle introduction to regular expressions

A regular expression (regex) is a pattern that describes text to match, rather than a fixed
string. `grep -E` (or `egrep`) understands the extended set of regex symbols. Try these against
`app.log`:

- Match any line that starts with a 4-digit year, e.g. `2026-08-18` — hint: `^` anchors to the
  start of a line, and `[0-9]` or `\d` matches a single digit.
- Match any line containing either `ERROR` or `WARN` in a single command, using `|` inside the
  pattern to mean "or".
- Match any line containing a port number that is exactly four digits, e.g. `8080`, using
  `{4}` to mean "exactly four repetitions" of a digit.
- Extend the year-matching pattern from the first bullet to match the full timestamp format
  `YYYY-MM-DD HH:MM:SS` at the start of a line.

Regular expressions come up constantly outside Linux too — in `grep`, in most programming
languages, in log analysis tools, and in text editors like VS Code's find-and-replace.

## 4. Permissions in more detail

The core lab had you set permissions using `chmod 600`. Numeric mode isn't the only way to
change permissions.

- Create a new file called `shared-notes.txt` in `sprint1-notes/`.
- Using **symbolic mode** (not numbers), give the group read-and-write access to the file, e.g.
  `chmod g+rw shared-notes.txt`, and confirm with `ls -l`.
- Remove execute permission from the `sprint1-notes` directory for everyone using symbolic mode,
  then try running `ls sprint1-notes` — what happens, and why? (Hint: the execute bit on a
  directory controls whether you can access things *inside* it, not whether you can list it.)
  Restore execute permission before moving on, or later exercises won't be able to reach your
  files.
- Look up what the three permission characters mean for a **directory** specifically (`r`, `w`,
  `x`) as opposed to a regular file — they don't mean quite the same thing.
- Run `umask` on its own with no arguments. This shows the default permissions mask applied to
  new files. Create a new empty file with `touch` and check its permissions — can you explain
  the number you see in terms of the umask value?

## 5. Finding files with find

`find` searches the filesystem based on criteria you specify, rather than a fixed location like
`ls`.

- Use `find` to list every file under `sprint1-notes/`, recursively, regardless of how deeply
  nested it is.
- Use `find` to locate only files (not directories) under `sprint1-notes/` whose name ends in
  `.txt`.
- Use `find` to locate files under `sprint1-notes/` that were modified in the last day
  (`-mtime` or `-mmin`).
- Use `find` combined with `-exec` to run `chmod 600` on every `.txt` file under
  `sprint1-notes/` in a single command, rather than one `chmod` per file.

## 6. Put it together

Write a single pipeline that:

1. Finds every `.txt` file under `sprint1-notes/`.
2. Searches all of them for lines containing the word `permissions` (case-insensitive).
3. Counts how many matching lines were found in total.

There's more than one valid way to combine `find`, `grep`, and `wc` to do this — if your first
attempt works, try to think of a second way.
