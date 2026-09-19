# Module 04 — Going Further: Reference Answers

Instructor reference only. Multiple correct command sequences exist; these are one valid path
for each exercise.

```powershell
# 1. Chaining the object pipeline further
Get-ChildItem -Path .\sample-workspace -Recurse -File | Measure-Object

Get-ChildItem -Path .\sample-workspace -Recurse -File |
    Group-Object Extension | Sort-Object Count -Descending

Get-ChildItem -Path .\sample-workspace -Recurse -File |
    Where-Object Length -gt 200 | Sort-Object Length -Descending

# Where-Object { $_.Length -gt 200 } and Where-Object Length -gt 200 are equivalent -
# the second is PowerShell's "simplified syntax" (added in v3.0), which works for a single
# comparison against a property but can't express more complex script-block logic.

# 2. Searching text with Select-String
Select-String -Path .\logs\app.log -Pattern INFO | Measure-Object

# Select-String is case-INsensitive by default (unlike grep, which needs -i), so this
# already matches Info/info with no extra switch. -CaseSensitive would make it stricter.
Select-String -Path .\logs\app.log -Pattern INFO

Select-String -Path .\logs\app.log -Pattern INFO -NotMatch

Get-ChildItem -Path .\sample-workspace -Recurse -File | Select-String -Pattern "app"
# each result object has .Filename, .LineNumber, and .Line properties

# 3. Regular expressions
Select-String -Path .\logs\app.log -Pattern '^\d{4}-\d{2}-\d{2}'
Select-String -Path .\logs\app.log -Pattern 'ERROR|WARN'
Select-String -Path .\logs\app.log -Pattern '\d{4}'
# matches both the year (2026) and the port number (5432) - discuss with class why an
# unanchored pattern picks up more than intended
Select-String -Path .\logs\app.log -Pattern '^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'

(Select-String -Path .\logs\app.log -Pattern '^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}' -AllMatches).Matches.Value

# 4. Permissions in more detail
cd .\sample-workspace
Get-Acl .\notes.txt | Format-List
icacls notes.txt
# (R) = read, (W) = write, (RX) = read & execute, (M) = modify, (F) = full control

# One-sentence contrast (any equivalent phrasing is fine): Windows ACLs let you grant
# different, fine-grained rights to any number of individual users or groups on the same
# file, while a Unix rwx triad only ever expresses three fixed buckets - owner, group, and
# everyone else.

# 5. Finding files with Get-ChildItem
Get-ChildItem -Path .\sample-workspace -Recurse -File

Get-ChildItem -Path .\sample-workspace -Recurse -Filter *.json

Get-ChildItem -Path .\sample-workspace -Recurse -File |
    Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-1) }

Get-ChildItem -Path .\sample-workspace -Recurse -Filter *.txt |
    ForEach-Object { Get-Content $_.FullName | Measure-Object -Line }

# 6. Put it together
Get-ChildItem -Path .\sample-workspace -Recurse -File |
    Where-Object { $_.Extension -in ".txt", ".log" } |
    Select-String -Pattern "error" |
    Measure-Object
```

**Talking points:**

- Exercise 1's last bullet is a good moment to flag that the simplified `Where-Object`
  syntax only covers single-condition filters — as soon as delegates need `-and`/`-or` logic,
  they'll be back to the `{ $_.Property -op value }` script-block form.
- Exercise 2 is designed to surprise delegates coming straight from Module 03: `grep` needs
  `-i` for case-insensitive matching, but `Select-String` is case-insensitive unless told
  otherwise. Worth calling out explicitly since it's the opposite default from bash.
- Exercise 3's third bullet (`\d{4}`) mirrors the ambiguous-match discussion from the Module
  03 answer sheet — same lesson, different shell.
- Exercise 4 is conceptual by design; there's no single Windows equivalent of `chmod 600`, and
  that's the point. If a delegate asks "so what's the ACL equivalent of `600`?" the honest
  answer is "an ACL with only the owner listed, and no inherited entries" — worth a live demo
  with `icacls notes.txt /inheritance:r` if time allows, but not required.
