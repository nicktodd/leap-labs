# Module 03 Lab — Linux Fundamentals for Engineers

## Objectives

By the end of this lab you will have:

- Logged into a shared Linux host over SSH
- Navigated the filesystem and inspected file permissions
- Created, copied, moved, and removed files and directories
- Viewed running processes and read/followed a log file
- Edited a file at the command line using `nano`

## Setup

- SSH client (built into Windows Terminal / PowerShell / Git Bash)
- Credentials for the shared Linux training host (provided by your trainer)
- A copy of [`app.log`](../../demos/03-linux-fundamentals/app.log) will already exist on the
  host at `~/sprint1/logs/app.log`

## Connecting with VS Code Remote Development (optional, recommended)

You can complete this lab from a plain SSH terminal (Windows Terminal, PowerShell, Git Bash, or
your terminal of choice). If you'd rather work with a full editor against the remote host — and
you'll want this for later labs that involve writing Dockerfiles and other files directly on the
Linux host — set up VS Code's Remote Development extension now:

1. Install the **Remote Development** extension pack in VS Code (includes **Remote - SSH**).
2. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run **Remote-SSH: Connect to
   Host...**
3. Add a new host using the credentials your trainer gave you, e.g. `ssh
   <username>@<host>`, and connect.
   - **Watch for the password prompt.** VS Code doesn't pop up a normal dialog box for this — it
     reuses the same small input box that the Command Palette itself uses, at the top-centre of
     the window, titled something like `Enter password for '<username>@<host>'`. There's no
     sound and no bold warning; if you're looking at the terminal panel or another app at that
     moment, it's very easy to miss entirely. If the connection seems to hang for more than a
     few seconds after you hit Enter, check the top-centre of the window before assuming
     something's broken.
   - Once authenticated, VS Code opens a **new window** connected to the Linux host — you can
     tell you're in a remote window by the green `SSH: <host>` indicator in the bottom-left
     corner.
4. **Open a folder on the remote host** — this is different from just being connected. Being
   connected (step 3) only gets you an empty remote window; you still need to explicitly open a
   folder that lives on the Linux machine, the same way you'd open a local project folder:
   - Use **File > Open Folder...** (or `Ctrl+K Ctrl+O`), which now shows a folder picker browsing
     the **remote** filesystem, not your local one (your home directory, e.g. `/home/<username>`,
     is a good default).
   - **This step commonly triggers a second password prompt**, in the same easy-to-miss
     top-centre input box as step 3. Opening a folder starts (or reconnects) the VS Code Server
     process on the Linux host, which is a separate authentication step from the initial SSH
     connection — so don't be surprised to be asked again even though you just logged in.
5. Open a terminal inside VS Code (`` Ctrl+` ``) — this terminal runs directly on the Linux host,
   exactly like an SSH session would.

From here on, any file you create or edit in that VS Code window lives on the Linux host itself,
and any terminal commands you run execute there too. This is the pattern you'll reuse in the
Docker labs later in the sprint: connect to your Linux machine, then build and run everything on
it directly.

If a command seems to hang with no output — especially right after connecting or opening a
folder — the most likely cause is a missed password prompt, not a broken connection. Check the
top-centre of the window before troubleshooting anything else.

## Task sheet

Work through each step on the shared Linux host. Keep a note of the command you used for each
step.

1. **Connect and orient yourself**
   - SSH into the host using the credentials provided.
   - Print your current working directory.
   - List the contents of your home directory, including hidden files, in long-listing format.

2. **Create a working area**
   - Create a directory called `sprint1-notes` in your home directory.
   - Inside it, create an empty file called `day1.txt`.
   - Confirm both now exist using a long listing.

3. **Copy, rename, and move**
   - Make a copy of `day1.txt` called `day1-backup.txt`.
   - Rename `day1-backup.txt` to `day1.bak` (hint: this is the same command as moving a file).
   - Move `day1.bak` into a new subdirectory called `archive`.

4. **Permissions**
   - Run a long listing of `day1.txt` and note down the permission string (e.g. `-rw-r--r--`).
   - Change the permissions so that only you can read and write the file, and no one else has
     any access.
   - Re-run the long listing and confirm the permission string changed as expected.

5. **Processes**
   - List all running processes and find any process related to Java.
   - Note the process ID (PID) of one such process.

6. **Logs**
   - Navigate to `~/sprint1/logs/`.
   - View the last 20 lines of `app.log`.
   - Find the single `ERROR` line in the file and note what class and line number it references.
   - Follow the log file live for a few seconds (you won't see new output unless the trainer is
     writing to it, but confirm you know how to stop following it).

7. **Edit at the command line**
   - Open `day1.txt` in `nano`.
   - Add a line summarising one thing you learned about Linux permissions today.
   - Save and exit.
   - Print the file contents to confirm your line was saved.

## Acceptance criteria

- `sprint1-notes/day1.txt` exists, is owned by you, has permissions `-rw-------` (600), and
  contains your one-line summary.
- `sprint1-notes/archive/day1.bak` exists.
- You can state the PID of a Java process and the line number of the `ERROR` in `app.log`
  without looking it up again.

If you finish early, compare notes with a partner: did you use the same commands for step 4?
There's often more than one valid way to do the same thing in Linux.

## Finished early?

Try the extension exercises in [`going-further.md`](going-further.md) — they cover piping,
`grep`, regular expressions, permissions in more depth, and `find`.
