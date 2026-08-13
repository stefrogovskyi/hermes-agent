---
name: windows-remote-node-access
description: "Configure OpenSSH and remote file access on Windows."
version: 1.0.0
author: Alistair
license: MIT
metadata:
  hermes:
    tags: [windows, ssh, openssh, tailscale, remote-access, acl, lsa]
---

# Windows Remote Node Access & OpenSSH Troubleshooting

## When to Use
Use when configuring or troubleshooting OpenSSH, Tailscale, or remote command execution and file management on Windows 10/11 nodes.

## OpenSSH Server & ACL Requirements

### 1. Administrator vs Standard User Key Storage
- **Administrator Accounts**: OpenSSH for Windows routes Administrator accounts to `C:\ProgramData\ssh\administrators_authorized_keys` by default due to `Match Group administrators` in `sshd_config`.
- **Standard Users**: Standard user accounts read `%h\.ssh\authorized_keys` (`C:\Users\<username>\.ssh\authorized_keys`).
- **Unified Key Storage**: To unify key storage across all accounts, configure:
  `AuthorizedKeysFile C:/ProgramData/ssh/keys/%u_authorized_keys`
  in `C:\ProgramData\ssh\sshd_config`.

### 2. Encoding & Line Ending Hard Invariants
- **ASCII / UTF-8 without BOM**: OpenSSH fails with `check options failure` / `mm_answer_keyverify` if `authorized_keys` contains a UTF-8 BOM (`0xEF 0xBB 0xBF`). Standard PowerShell 5.1 `Out-File -Encoding utf8` writes UTF-8 WITH BOM. Always write pure ASCII / UTF-8 without BOM:
  ```powershell
  [System.IO.File]::WriteAllBytes($path, [System.Text.Encoding]::ASCII.GetBytes("$key`n"))
  ```
- **Unix LF (`0x0A`) Line Endings Only**: Windows CRLF (`\r\n`) line endings cause trailing `\r` (`0x0D`) to be appended to the key comment, causing `sshauthopt_parse` to fail during signature verification. Write pure `\n` line endings without `\r`.

### 3. Windows ACL Permissions (`check_secure_file`)
- OpenSSH's `check_secure_file()` inspects ACLs of the key file, `.ssh` directory, and parent folders up to `C:\Users`.
- Disabling inheritance (`SetAccessRuleProtection($true, $false)`) and granting access strictly to `<username>`, `SYSTEM`, and `Administrators` satisfies ACL checks:
  ```powershell
  icacls $path /inheritance:r /grant "Administrators:F" /grant "SYSTEM:F" /grant "<username>:F"
  ```
- Set `StrictModes no` at the top of `C:\ProgramData\ssh\sshd_config` to bypass strict ACL checks on Windows filesystems.

### 4. Microsoft Accounts vs Local Windows Accounts
- **Microsoft Accounts** (`user@email.com`): Windows LSA S4U token generation fails for publickey authentication without an interactive password, causing `user_key_allowed: check options failure`.
- **Local User Accounts**: Creating a pure local Windows user account (`net user hermes <password> /add`) bypasses Microsoft Account LSA limitations.
- **Profile Initialization**: New local accounts must have their Windows User Profile initialized in `HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList` by executing a process under that credential once:
  ```powershell
  $p = ConvertTo-SecureString "<password>" -AsPlainText -Force
  Start-Process powershell -Credential (New-Object System.Management.Automation.PSCredential("hermes", $p)) -ArgumentList "-Command whoami" -WindowStyle Hidden -Wait
  ```
- **User Rights Assignment**: Ensure the user account or `Users` group is granted `SeNetworkLogonRight` and `SeBatchLogonRight` via `secedit`.
