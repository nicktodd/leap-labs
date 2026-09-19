# Module 03 Lab — Reference Answers

Instructor reference only. Multiple correct command sequences exist; this is one valid path.

```bash
# 1. Connect and orient
ssh trainee01@leap-linux-01.internal
pwd
ls -la

# 2. Create a working area
mkdir sprint1-notes
touch sprint1-notes/day1.txt
ls -la sprint1-notes

# 3. Copy, rename, move
cp sprint1-notes/day1.txt sprint1-notes/day1-backup.txt
mv sprint1-notes/day1-backup.txt sprint1-notes/day1.bak
mkdir sprint1-notes/archive
mv sprint1-notes/day1.bak sprint1-notes/archive/

# 4. Permissions
ls -l sprint1-notes/day1.txt      # -rw-r--r--
chmod 600 sprint1-notes/day1.txt
ls -l sprint1-notes/day1.txt      # -rw-------

# 5. Processes
ps aux | grep java
# note the PID from the second column

# 6. Logs
cd ~/sprint1/logs
tail -n 20 app.log
grep -n ERROR app.log             # AccountController.java:42
tail -f app.log                   # Ctrl+C to stop

# 7. Edit at the command line
nano sprint1-notes/day1.txt
# type a line, Ctrl+O, Enter, Ctrl+X
cat sprint1-notes/day1.txt
```

**Expected `ERROR` finding:** `AccountController.getBalance(AccountController.java:42)` —
`NullPointerException` because `account` is null.
