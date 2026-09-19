# Module 04 Lab — PowerShell Fundamentals

## Objectives

By the end of this lab you will have:

- Used core PowerShell cmdlets to navigate the filesystem
- Used the object pipeline to filter and inspect processes and files
- Checked a Windows service, an environment variable, and a log file
- Created and edited a file at the PowerShell prompt

## Setup

- A Windows machine with PowerShell 7+ (or Windows PowerShell 5.1)
- The [`sample-workspace/`](../../demos/04-powershell-fundamentals/sample-workspace) folder from
  the demo, copied into your own working directory
- PostgreSQL installed and running as a Windows service

## Task sheet

`sample-workspace/` contains three small project folders (`java-app/`, `python-app/`,
`web-app/`) and a `logs/` folder — a rough stand-in for the kind of workspace you'll be using
for Java, Python, and web development later in the programme.

1. **Navigate and orient yourself**
   - Open PowerShell and move into `sample-workspace`.
   - List the top-level contents.
   - List the contents of `java-app` recursively, names only.

2. **Explore with `Get-Command` and `Get-Help`**
   - Use `Get-Command` to check that `Get-ChildItem`, `Get-Content`, and `Get-Process` exist as
     cmdlets on your machine.
   - Use `Get-Help` with `-Examples` on any one of them to see sample usage.

3. **Use the object pipeline**
   - List every running process, then filter it down to anything with `java` in the process
     name.
   - List every file under `sample-workspace`, sort by size, and show only the 5 largest.

4. **Check a Windows service**
   - List any services whose name starts with `postgresql`.
   - Confirm whether the service status is `Running`.

5. **Check an environment variable**
   - List all environment variables that start with `JAVA`.
   - Print the value of `JAVA_HOME` directly.

6. **Read and search a log file**
   - View the last 5 lines of `logs/app.log`.
   - Search the file for the line containing `ERROR` and note the class and line number it
     references.

7. **Create and edit a file**
   - Create a new file called `notes.txt` in `sample-workspace`.
   - Write a line into it summarising the PostgreSQL service status you found in step 4.
   - Append a second line summarising the `ERROR` you found in step 6.
   - Display the file contents to confirm both lines are there.

## Acceptance criteria

- You can state whether the PostgreSQL service is running, without looking it up again.
- You can state the value of `JAVA_HOME` on your machine.
- `sample-workspace/notes.txt` exists and contains two lines matching steps 7.
- You can explain in one sentence how a PowerShell pipeline differs from a bash pipeline.

If you finish early, try piping `Get-ChildItem -Recurse -File` into `Group-Object Extension` to
see a breakdown of file types across all three sample projects.

## Finished early?

Try the extension exercises in [`going-further.md`](going-further.md) — they cover deeper
pipeline chaining, `Select-String`, regular expressions, permissions/ACLs, and `Get-ChildItem`
in more depth.
