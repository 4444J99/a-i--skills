# Attack Tree Patterns

Common attack trees for threat modeling analysis.

## Attack Tree Fundamentals

### Structure

```
Goal (Root)
├── OR: Attack Path A
│   ├── AND: Prerequisite 1
│   └── AND: Prerequisite 2
├── OR: Attack Path B
│   └── Single Step
└── OR: Attack Path C
    ├── AND: Step 1
    ├── AND: Step 2
    └── AND: Step 3

OR = Any child achieves goal
AND = All children required
```

### Node Attributes

```
[Attack Step]
├── Probability: Low/Medium/High
├── Difficulty: Easy/Medium/Hard
├── Cost: $Low/$Medium/$High
├── Detectability: Low/Medium/High
└── Mitigated: Yes/No/Partial
```

---

## Account Takeover Attack Tree

```
Goal: Compromise User Account
│
├── OR: Credential Theft
│   ├── OR: Phishing Attack
│   │   ├── AND: Create convincing login page
│   │   ├── AND: Distribute via email/SMS
│   │   └── AND: Victim enters credentials
│   │
│   ├── OR: Credential Stuffing
│   │   ├── AND: Obtain breach database
│   │   └── AND: Automate login attempts
│   │
│   ├── OR: Keylogger/Malware
│   │   ├── AND: Compromise victim device
│   │   └── AND: Capture credentials
│   │
│   └── OR: Social Engineering
│       ├── AND: Contact support
│       └── AND: Convince to reset password
│
├── OR: Session Hijacking
│   ├── OR: XSS Attack
│   │   ├── AND: Find XSS vulnerability
│   │   └── AND: Steal session cookie
│   │
│   ├── OR: Network Sniffing
│   │   ├── AND: Position on network path
│   │   └── AND: Intercept unencrypted session
│   │
│   └── OR: Session Fixation
│       ├── AND: Set session ID before auth
│       └── AND: Victim authenticates
│
├── OR: Password Reset Abuse
│   ├── OR: Email Account Compromise
│   │   ├── AND: Compromise email account
│   │   └── AND: Use password reset
│   │
│   ├── OR: Security Question Bypass
│   │   ├── AND: Research victim's answers
│   │   └── AND: Answer security questions
│   │
│   └── OR: Reset Token Prediction
│       ├── AND: Analyze token generation
│       └── AND: Predict valid token
│
└── OR: Brute Force
    ├── AND: No rate limiting exists
    └── AND: Automate password guessing
```

### Mitigations Map

| Attack Path | Primary Mitigation | Secondary |
|-------------|-------------------|-----------|
| Phishing | Security awareness, MFA | Email filtering |
| Credential stuffing | MFA, breach monitoring | Rate limiting |
| XSS session theft | CSP, HttpOnly cookies | Input validation |
| Password reset abuse | MFA on reset, email verification | Strong tokens |
| Brute force | Rate limiting, lockout | Strong passwords |

---

## Data Exfiltration Attack Tree

```
Goal: Extract Sensitive Data
│
├── OR: SQL Injection
│   ├── AND: Identify injectable parameter
│   ├── AND: Determine database type
│   ├── AND: Extract schema information
│   └── AND: Dump target tables
│
├── OR: API Abuse
│   ├── OR: IDOR Exploitation
│   │   ├── AND: Identify object references
│   │   └── AND: Enumerate other objects
│   │
│   ├── OR: Excessive Data Exposure
│   │   ├── AND: Find verbose endpoint
│   │   └── AND: Extract unneeded fields
│   │
│   └── OR: Broken Function Authorization
│       ├── AND: Discover admin endpoints
│       └── AND: Access without authorization
│
├── OR: File Access
│   ├── OR: Path Traversal
│   │   ├── AND: Find file path input
│   │   └── AND: Traverse to sensitive files
│   │
│   ├── OR: Local File Inclusion
│   │   ├── AND: Find include parameter
│   │   └── AND: Include sensitive file
│   │
│   └── OR: Backup/Log Exposure
│       └── AND: Access unprotected files
│
├── OR: Network Interception
│   ├── AND: Position as MITM
│   └── AND: Decrypt/read traffic
│
└── OR: Insider Threat
    ├── OR: Authorized Access Abuse
    │   └── AND: Exceed access boundaries
    │
    └── OR: Privilege Escalation
        ├── AND: Gain additional privileges
        └── AND: Access restricted data
```

---

## Denial of Service Attack Tree

```
Goal: Make System Unavailable
│
├── OR: Network Layer Attack
│   ├── OR: Volumetric DDoS
│   │   ├── AND: Acquire botnet/amplification
│   │   └── AND: Flood target bandwidth
│   │
│   ├── OR: SYN Flood
│   │   └── AND: Exhaust connection state
│   │
│   └── OR: DNS Amplification
│       ├── AND: Spoof victim IP
│       └── AND: Send queries to open resolvers
│
├── OR: Application Layer Attack
│   ├── OR: Slowloris
│   │   └── AND: Keep connections open slowly
│   │
│   ├── OR: Resource Exhaustion
│   │   ├── AND: Identify expensive operation
│   │   └── AND: Trigger repeatedly
│   │
│   ├── OR: Regex DoS (ReDoS)
│   │   ├── AND: Find vulnerable regex
│   │   └── AND: Submit malicious input
│   │
│   └── OR: XML Bomb
│       ├── AND: Find XML parser
│       └── AND: Submit expanding entity
│
├── OR: Infrastructure Attack
│   ├── OR: Disk Exhaustion
│   │   ├── AND: Find upload endpoint
│   │   └── AND: Upload large files
│   │
│   ├── OR: Memory Exhaustion
│   │   ├── AND: Find memory allocation trigger
│   │   └── AND: Exhaust available memory
│   │
│   └── OR: Connection Pool Exhaustion
│       └── AND: Open connections without closing
│
└── OR: Dependency Attack
    ├── AND: Identify critical dependency
    └── AND: Attack the dependency
```

---

## Privilege Escalation Attack Tree

```
Goal: Gain Administrative Access
│
├── OR: Vertical Escalation
│   ├── OR: Authorization Bypass
│   │   ├── AND: Discover admin endpoint
│   │   └── AND: Access without proper role
│   │
│   ├── OR: Role Manipulation
│   │   ├── AND: Find role assignment mechanism
│   │   └── AND: Modify own role
│   │
│   ├── OR: Default Credentials
│   │   └── AND: Use default admin password
│   │
│   └── OR: Admin Session Hijacking
│       ├── AND: Identify admin user
│       └── AND: Steal admin session
│
├── OR: Horizontal to Vertical
│   ├── AND: Compromise regular user
│   ├── AND: Find privilege escalation bug
│   └── AND: Escalate to admin
│
├── OR: Infrastructure Escalation
│   ├── OR: Container Escape
│   │   ├── AND: Identify container weakness
│   │   └── AND: Break out to host
│   │
│   ├── OR: Kernel Exploit
│   │   ├── AND: Identify vulnerable kernel
│   │   └── AND: Execute privilege escalation exploit
│   │
│   └── OR: Service Misconfiguration
│       ├── AND: Find writable service config
│       └── AND: Modify to run as elevated user
│
└── OR: Trust Relationship Abuse
    ├── AND: Compromise trusted service
    └── AND: Leverage trust for elevated access
```

---

## API Attack Tree

```
Goal: Compromise API
│
├── OR: Authentication Bypass
│   ├── OR: JWT Vulnerabilities
│   │   ├── OR: None Algorithm
│   │   │   └── AND: Modify alg to "none"
│   │   │
│   │   ├── OR: Weak Secret
│   │   │   ├── AND: Brute force secret
│   │   │   └── AND: Forge token
│   │   │
│   │   └── OR: Key Confusion
│   │       └── AND: Use public key as HMAC secret
│   │
│   ├── OR: API Key Exposure
│   │   ├── OR: Find in client code
│   │   ├── OR: Find in repository
│   │   └── OR: Find in logs
│   │
│   └── OR: OAuth Flaws
│       ├── OR: Redirect URI manipulation
│       ├── OR: Missing state validation
│       └── OR: Token leakage
│
├── OR: Authorization Flaws
│   ├── OR: BOLA (IDOR)
│   │   └── AND: Access other users' objects
│   │
│   ├── OR: BFLA
│   │   └── AND: Access unauthorized functions
│   │
│   └── OR: Mass Assignment
│       └── AND: Set privileged fields
│
├── OR: Injection Attacks
│   ├── OR: SQL Injection
│   ├── OR: NoSQL Injection
│   ├── OR: GraphQL Injection
│   └── OR: Command Injection
│
└── OR: Rate Limit Bypass
    ├── OR: Missing rate limits
    ├── OR: Header manipulation (X-Forwarded-For)
    └── OR: Distributed requests
```

---

## Supply Chain Attack Tree

```
Goal: Compromise via Supply Chain
│
├── OR: Dependency Attack
│   ├── OR: Typosquatting
│   │   ├── AND: Create malicious package
│   │   └── AND: Name similar to popular package
│   │
│   ├── OR: Dependency Confusion
│   │   ├── AND: Identify private package names
│   │   └── AND: Publish public package with same name
│   │
│   ├── OR: Compromise Upstream
│   │   ├── AND: Gain maintainer access
│   │   └── AND: Push malicious update
│   │
│   └── OR: Vulnerable Dependency
│       └── AND: Exploit known CVE
│
├── OR: Build Pipeline Attack
│   ├── OR: Compromise CI/CD
│   │   ├── AND: Gain access to CI system
│   │   └── AND: Inject malicious build steps
│   │
│   ├── OR: Artifact Tampering
│   │   ├── AND: Access artifact storage
│   │   └── AND: Replace legitimate artifacts
│   │
│   └── OR: Code Signing Bypass
│       ├── AND: Steal signing keys
│       └── AND: Sign malicious code
│
└── OR: Third-Party Service Attack
    ├── AND: Identify integrated services
    ├── AND: Compromise third-party
    └── AND: Leverage access to target
```

---

## Attack Tree Analysis Template

```markdown
# Attack Tree Analysis: [Goal]

## Tree Diagram
[ASCII or graphical tree]

## Path Analysis

### Path 1: [Name]
- **Steps:** [Number of steps]
- **Difficulty:** [Easy/Medium/Hard]
- **Prerequisites:** [What attacker needs]
- **Detection:** [How we'd detect it]
- **Mitigations:** [Current controls]
- **Residual Risk:** [Low/Medium/High]

### Path 2: [Name]
[Repeat for each significant path]

## Mitigation Priority

| Attack Path | Current State | Recommended Action | Priority |
|-------------|---------------|-------------------|----------|
| [Path] | [Mitigated/Partial/Open] | [Action] | [P1/P2/P3] |

## Summary

**Highest Risk Paths:**
1. [Path] - [Why it's highest risk]
2. [Path]

**Quick Wins:**
1. [Mitigation] - Blocks [N] attack paths

**Long-term Improvements:**
1. [Improvement]
```

---

## Using Attack Trees in Threat Modeling

### Process

1. **Define Goal**
   - What is the attacker trying to achieve?
   - Be specific: "Steal customer credit cards" not "Attack system"

2. **Brainstorm Paths**
   - How could an attacker achieve this goal?
   - Consider different attacker profiles (script kiddie, insider, nation-state)

3. **Decompose Steps**
   - Break down each path into individual steps
   - Identify AND vs OR relationships

4. **Assess Each Path**
   - Difficulty, cost, detectability
   - Current mitigations

5. **Prioritize**
   - Which paths are most likely?
   - Which have highest impact?

6. **Mitigate**
   - Focus on blocking the most critical paths
   - Look for "choke points" that block multiple paths

### Tips

- Start broad, then drill down into likely paths
- Include both technical and non-technical attacks
- Consider insider threats
- Review with diverse team members
- Update trees as system changes
- Focus on realistic attacks, not theoretical
