Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'python.exe' -or $_.Name -eq 'pythonw.exe' } | ForEach-Object {
    if ($_.CommandLine -match 'launch_liz' -or $_.CommandLine -match 'liz_loop') {
        Write-Host ($_.ProcessId.ToString() + ' [' + $_.Name + '] :: ' + $_.CommandLine)
    }
}
