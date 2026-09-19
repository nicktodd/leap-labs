# Demo: Module 03 — Linux Fundamentals for Engineers

**Duration:** 10 minutes
**Prerequisite:** Instructor has SSH access to the shared Linux training host and shares their
screen (or a recorded terminal session) for the class. Delegates watch first, then repeat the
steps themselves in the lab.

## Part 1: Logging in and navigating (3 min)

```bash
ssh trainee01@leap-linux-01.internal
pwd
ls -la
cd /opt/sprint1/app
ls -la
```

Narration: point out `pwd` for "where am I", the difference between `ls` and `ls -la` (hidden
files, permissions, owner, size, timestamp), and that `.` and `..` always exist in every
directory.

## Part 2: File and directory operations, permissions (3 min)

```bash
mkdir notes
touch notes/day1.txt
cp notes/day1.txt notes/day1-backup.txt
mv notes/day1-backup.txt notes/day1.bak
ls -l notes/
chmod 640 notes/day1.txt
ls -l notes/
```

Narration: read a permissions string left to right as owner/group/other, and rwx as
read/write/execute. Relate `chmod 640` back to the `rw-r-----` you just saw. Don't go deep into
octal maths here, just enough that the task sheet makes sense.

## Part 3: Processes and logs (2 min)

```bash
ps aux | grep java
tail -n 20 /opt/sprint1/app/logs/app.log
tail -f /opt/sprint1/app/logs/app.log
```

Narration: `ps aux` lists running processes; `tail -f` follows a log file live, which is how
you'll watch a Jenkins build or a containerised app later in the week. Ctrl+C to stop following.

## Part 4: Command-line editing (2 min)

```bash
nano notes/day1.txt
```

Type a line, save with Ctrl+O, Enter, exit with Ctrl+X. Mention `vim` exists as an alternative
and is worth learning later, but `nano` is enough to be productive from day one.

## Key message

You will SSH into Linux hosts and read logs constantly this programme (Jenkins agents, Docker
hosts, later sprints' cloud VMs) — today's goal is just enough Linux to be self-sufficient, not
mastery.
