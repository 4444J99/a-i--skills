---
name: qa-audit
description: Verify claims in a session/PR/transcript against on-disk reality. Produce a verification report (verified / false-positive / false-negative / partial) with explicit owners. STOP at verification — do not execute remediation without explicit approval.
license: MIT
---

# QA Audit

1. Read referenced session transcripts/artifacts fresh from disk
2. Verify each claim against on-disk reality (file exists, content matches, commit landed)
3. Mark each as: verified / false-positive / false-negative / partial
4. Produce remediation list with explicit owners
5. Stop at verification — do NOT execute remediation without explicit approval
