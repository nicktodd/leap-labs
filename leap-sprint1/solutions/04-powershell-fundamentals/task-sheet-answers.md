# Module 04 Lab — Reference Answers

Instructor reference only.

```powershell
# 1. Navigate and orient
Set-Location .\sample-workspace
Get-ChildItem
Get-ChildItem .\java-app -Recurse -Name

# 2. Discover cmdlets
Get-Command Get-ChildItem, Get-Content, Get-Process
Get-Help Get-Content -Examples

# 3. Object pipeline
Get-Process | Where-Object { $_.ProcessName -like "*java*" }
Get-ChildItem -Recurse -File | Sort-Object Length -Descending | Select-Object -First 5

# 4. Windows service
Get-Service postgresql* | Format-Table -AutoSize
# Status column should read "Running"

# 5. Environment variable
Get-ChildItem Env: | Where-Object Name -like "JAVA*"
$env:JAVA_HOME

# 6. Log file
Get-Content .\logs\app.log -Tail 5
Select-String -Path .\logs\app.log -Pattern "ERROR"
# AccountController.getBalance(AccountController.java:42)

# 7. Create and edit a file
New-Item -ItemType File -Path .\notes.txt
Set-Content -Path .\notes.txt -Value "PostgreSQL service: Running"
Add-Content -Path .\notes.txt -Value "ERROR found in AccountController.java line 42 (NullPointerException)"
Get-Content .\notes.txt
```

**Expected `ERROR` finding:** `AccountController.getBalance(AccountController.java:42)` —
`NullPointerException` because `account` is null (same underlying scenario as the Module 03
log, so delegates should recognise the pattern).

**One-sentence pipeline answer (any equivalent phrasing is fine):** a bash pipe passes plain
text between commands, so the receiving command has to parse it; a PowerShell pipe passes
structured .NET objects with real properties, so the receiving cmdlet can filter and sort on
those properties directly.
