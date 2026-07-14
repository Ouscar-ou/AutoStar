# Security Policy

## Private Reporting

Please report security concerns through [GitHub Private Vulnerability Reporting](https://github.com/Ouscar-ou/AutoStar/security/advisories/new).

安全问题请通过 [GitHub Private Vulnerability Reporting](https://github.com/Ouscar-ou/AutoStar/security/advisories/new) 私密提交，不要在公开 Issue 中发布可复现的攻击细节或保密项目数据。

When reporting, include the affected AutoStar version, operating system, reproduction steps, expected behavior, and observed behavior. Share only the minimum project information needed to reproduce the issue.

提交时建议说明 AutoStar 版本、操作系统、复现步骤、预期行为和实际行为，并只提供复现问题所需的最少项目信息。

## Supported Version

Security fixes are provided for the latest official public-preview release. Confirm the package source and run:

```powershell
python starccm_cli.py integrity-check
python starccm_cli.py version
```

If the installation check fails, reinstall from the latest official Release before continuing.

## Project Data

Use sanitized cases and logs for public bug reports. Geometry, simulation files, customer information, and other confidential engineering data should be shared only through an appropriate private channel.
