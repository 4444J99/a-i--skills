from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class SecretPattern:
    name: str
    regex: re.Pattern[str]


PATTERNS = [
    SecretPattern(
        name="private-key-block",
        regex=re.compile(r"-----BEGIN (?:RSA|EC|DSA|OPENSSH|PRIVATE) KEY-----"),
    ),
    SecretPattern(
        name="aws-access-key-id",
        regex=re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b"),
    ),
    SecretPattern(
        name="aws-secret-access-key",
        regex=re.compile(
            r"(?i)\baws_secret_access_key\b\s*[:=]\s*['\"]?[A-Za-z0-9/+=]{40}"
        ),
    ),
    SecretPattern(
        name="github-token",
        regex=re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36}\b"),
    ),
    SecretPattern(
        name="gitlab-token",
        regex=re.compile(r"\bglpat-[0-9A-Za-z\-_]{20,}\b"),
    ),
    SecretPattern(
        name="slack-token",
        regex=re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{10,}\b"),
    ),
    SecretPattern(
        name="google-api-key",
        regex=re.compile(r"\bAIza[0-9A-Za-z\-_]{35}\b"),
    ),
    SecretPattern(
        name="stripe-live-key",
        regex=re.compile(r"\bsk_live_[0-9a-zA-Z]{24}\b"),
    ),
    SecretPattern(
        name="jwt",
        regex=re.compile(
            r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"
        ),
    ),
    SecretPattern(
        name="generic-credential-assignment",
        regex=re.compile(
            r"(?i)\b(api[_-]?key|secret|token|password)\b\s*[:=]\s*['\"]?[A-Za-z0-9_\-\/+=]{16,}"
        ),
    ),
]

ALLOWLIST = [
    re.compile(r"(?i)redacted"),
    re.compile(r"(?i)<redacted>"),
    re.compile(r"(?i)placeholder"),
    re.compile(r"(?i)example"),
    re.compile(r"(?i)dummy"),
    re.compile(r"(?i)fake"),
    re.compile(r"\b(x{4,}|\*{4,})\b"),
]
