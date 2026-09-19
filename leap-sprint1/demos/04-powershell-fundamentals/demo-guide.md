# Demo: Module 04 — PowerShell Fundamentals

**Duration:** 10 minutes
**Prerequisite:** Windows machine with PowerShell 7+ (or Windows PowerShell 5.1), the
`sample-workspace/` folder from this demo copied locally, and PostgreSQL installed as a Windows
service (from Module 02 environment setup).

## Part 1: Cmdlet basics and navigation (3 min)

```powershell
Get-Command Get-Process
Get-Help Get-ChildItem -Examples
Get-ChildItem
Set-Location .\sample-workspace
Get-ChildItem -Recurse -Name
```

Narration: PowerShell commands follow a `Verb-Noun` pattern, which makes them guessable —
`Get-Help` and `Get-Command` are how you discover the rest of the vocabulary yourself.
`Get-ChildItem` is the everyday "what's in this folder" cmdlet, same job as `dir`.

## Part 2: The object pipeline (3 min)

```powershell
Get-Process | Where-Object { $_.ProcessName -like "*java*" }
Get-Process | Sort-Object CPU -Descending | Select-Object -First 5
Get-ChildItem -Recurse -File | Measure-Object -Property Length -Sum
```

Narration: this is the single biggest mental shift from bash. A bash pipe passes text between
commands; a PowerShell pipe passes full .NET objects. `Where-Object` filters on real properties
(`ProcessName`, `CPU`) rather than parsing text with regex. `$_` means "the current object in
the pipeline."

## Part 3: Everyday dev-machine tasks (3 min)

```powershell
Get-Service postgresql* | Format-Table -AutoSize
Get-ChildItem Env: | Where-Object Name -like "JAVA*"
$env:JAVA_HOME
Get-Content .\logs\app.log -Tail 5
Select-String -Path .\logs\app.log -Pattern "ERROR"
```

Narration: before starting any Java, Python, or web work today, these are the checks worth
knowing: is the database service running, is `JAVA_HOME` set correctly, and can I quickly find
the error in a log without opening it in an editor. `Select-String` is PowerShell's equivalent
of `grep`.

## Part 4: Creating and editing a file (1 min)

```powershell
New-Item -ItemType File -Path .\notes.txt
Set-Content -Path .\notes.txt -Value "Sprint 1 setup notes"
Add-Content -Path .\notes.txt -Value "PostgreSQL service confirmed running"
Get-Content .\notes.txt
```

Narration: `Set-Content` overwrites, `Add-Content` appends — the same distinction as `>` and `>>`
in bash, just spelled out as cmdlet names.

## Key message

PowerShell is object-oriented where bash is text-oriented, and its verb-noun naming makes it
discoverable. You'll reach for exactly these cmdlets (`Get-Process`, `Get-Service`,
`Get-ChildItem`, `Get-Content`, `Select-String`) whenever you need to check your Windows dev
environment before starting Java, Python, or web work later in the programme.
