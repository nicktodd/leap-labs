# Module 03 — Going Further: Reference Answers

Instructor reference only. Multiple correct command sequences exist; these are one valid path
for each exercise.

```bash
# 1. Piping and chaining commands
cd ~/sprint1/logs
wc -l app.log
ls -la ~ | sort -k5 -n
ls ~/sprint1/logs | grep '.log' | wc -l

false && echo "this won't print"     # nothing prints: && only runs the next command if the first succeeded
false; echo "this will print"        # always prints: ; just runs the next command regardless

# 2. Searching text with grep
grep -c INFO app.log
grep -i info app.log
grep -v INFO app.log
grep -A 2 WARN app.log
grep -r Linux ~/sprint1-notes

# 3. Regular expressions
grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}' app.log
grep -E 'ERROR|WARN' app.log
grep -E '[0-9]{4}' app.log            # matches the 8080 port number (also matches the year - discuss with class)
grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}' app.log

# 4. Permissions in more detail
cd ~/sprint1-notes
touch shared-notes.txt
chmod g+rw shared-notes.txt
ls -l shared-notes.txt                # -rw-rw-r--

chmod o-x,g-x,u-x . 2>/dev/null || chmod -x .   # remove execute for everyone on sprint1-notes
ls sprint1-notes                      # "Permission denied" - the x bit controls traversal/access
                                       # into a directory, not whether it can be listed from outside
chmod +x .                            # restore execute before continuing

umask                                 # e.g. 0022
touch umask-test.txt
ls -l umask-test.txt                  # -rw-r--r-- (666 minus the 022 mask)

# 5. Finding files with find
find ~/sprint1-notes
find ~/sprint1-notes -type f -name "*.txt"
find ~/sprint1-notes -type f -mtime -1
find ~/sprint1-notes -type f -name "*.txt" -exec chmod 600 {} \;

# 6. Put it together
find ~/sprint1-notes -type f -name "*.txt" -exec grep -il permissions {} \; | wc -l
# or, equivalently:
find ~/sprint1-notes -type f -name "*.txt" | xargs grep -il permissions | wc -l
```

**Talking points:**

- Exercise 3's third bullet is deliberately ambiguous: `[0-9]{4}` matches both the year at the
  start of the timestamp and the `8080` port number later in the line. Use it to prompt a
  discussion about why regex patterns need to be anchored (`^`, `$`) or bounded to avoid
  unintended matches.
- Exercise 4's directory-permissions bullet is the one delegates most often get wrong first
  try — expect some to be surprised that removing `x` (not `r`) is what blocks access into a
  directory. Confirm they restore `+x` before moving on to exercise 5, or `find`/`grep` against
  `sprint1-notes` will fail with permission errors.
- `umask` values vary by host/distro default; the expected result is whatever `666 - umask`
  works out to for a new file (directories use `777` as the starting point instead).
