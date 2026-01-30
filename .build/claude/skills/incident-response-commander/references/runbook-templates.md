# Incident Response Runbook Templates

Ready-to-use templates for incident management.

## Incident Declaration Template

```
=====================================
INCIDENT DECLARED
=====================================

Incident ID: INC-[YYYY-MM-DD]-[###]
Severity: SEV-[1/2/3]
Declared by: [Name]
Declared at: [YYYY-MM-DD HH:MM UTC]

IMPACT
------
Service(s) affected: [Service names]
User impact: [Description of user-facing impact]
Business impact: [Revenue, reputation, SLA]
Affected regions: [Geographic or logical regions]

CURRENT STATUS
--------------
[Brief description of what we know]

ACTIONS TAKEN
-------------
1. [First action taken]
2. [Second action taken]

ROLES ASSIGNED
--------------
Incident Commander: [Name]
Communications Lead: [Name]
Operations Lead: [Name]
Subject Matter Experts: [Names]

WAR ROOM
--------
Slack channel: #inc-[date]-[brief-name]
Video call: [Link]
Status page: [Link to status page update]

NEXT UPDATE
-----------
Expected in: [X] minutes
=====================================
```

---

## Status Update Templates

### Internal Status Update

```
=====================================
INCIDENT STATUS UPDATE
=====================================

Incident ID: INC-[YYYY-MM-DD]-[###]
Update #: [N]
Time: [YYYY-MM-DD HH:MM UTC]
Severity: SEV-[1/2/3] [UNCHANGED/UPGRADED/DOWNGRADED]

SUMMARY
-------
[One sentence summary of current state]

IMPACT (Current)
----------------
- Users affected: [Number or percentage]
- Services degraded: [List]
- Geographic impact: [Regions]

TIMELINE (Key Events)
---------------------
[HH:MM] - [Event description]
[HH:MM] - [Event description]
[HH:MM] - [Event description]

CURRENT HYPOTHESIS
------------------
[What we believe is happening and why]

ACTIVE MITIGATIONS
------------------
□ [Mitigation in progress]
□ [Mitigation in progress]
☑ [Mitigation completed]

NEXT STEPS
----------
1. [Action] - Owner: [Name] - ETA: [Time]
2. [Action] - Owner: [Name] - ETA: [Time]

NEXT UPDATE
-----------
In [X] minutes or when significant change occurs.
=====================================
```

### Customer-Facing Status Update

```
[Service Name] - Investigating [Issue Type]

Posted: [YYYY-MM-DD HH:MM UTC]

We are currently investigating reports of [brief,
non-technical description of the issue].

Impact: [User-facing impact in plain language]
- [Specific feature/function affected]
- [Workaround if available]

Our team is actively working on this issue. We will
provide an update in [X] minutes.

We apologize for any inconvenience.
```

### Resolution Update (Customer-Facing)

```
[Service Name] - Resolved

Posted: [YYYY-MM-DD HH:MM UTC]

The issue affecting [brief description] has been
resolved as of [HH:MM UTC].

Duration: [X hours Y minutes]

What happened: [Brief, non-technical explanation]

What we're doing: [Steps to prevent recurrence]

We apologize for the disruption and thank you for
your patience.
```

---

## Severity Level Definitions

### SEV-1: Critical

```
Criteria (any one):
- Complete service outage
- Data breach or security incident
- Revenue-generating features fully unavailable
- >50% of users affected
- Regulatory/compliance impact

Response expectations:
- All hands on deck
- 15-minute status updates
- Executive notification required
- 24/7 coverage until resolved
- Post-mortem within 48 hours
```

### SEV-2: Major

```
Criteria (any one):
- Significant functionality degraded
- 10-50% of users affected
- Major feature unavailable
- Performance severely degraded (>2x latency)
- SLA at risk

Response expectations:
- On-call team engaged
- 30-minute status updates
- Manager notification required
- Business hours+ coverage
- Post-mortem within 1 week
```

### SEV-3: Minor

```
Criteria (any one):
- Minor functionality degraded
- <10% of users affected
- Non-critical feature unavailable
- Workaround available
- No SLA impact

Response expectations:
- On-call engineer
- Hourly status updates
- Team lead notification
- Business hours coverage
- Retrospective as needed
```

---

## Role Definitions

### Incident Commander (IC)

```
Responsibilities:
- Declare and close incidents
- Assign roles and tasks
- Make decisions or escalate
- Manage timeline and updates
- Ensure documentation

NOT responsible for:
- Hands-on debugging
- Writing code fixes
- Customer communication details

Authority:
- Can escalate severity
- Can pull in any resource
- Can authorize emergency changes
- Final decision maker
```

### Communications Lead

```
Responsibilities:
- Draft status updates
- Post to status page
- Handle customer inquiries
- Coordinate with support team
- Manage executive updates

Templates used:
- Internal status updates
- Customer-facing updates
- Executive summaries
```

### Operations Lead

```
Responsibilities:
- Coordinate technical response
- Assign debugging tasks
- Track hypothesis and tests
- Manage rollback decisions
- Document technical timeline

Works closely with:
- Subject matter experts
- On-call engineers
- Platform team
```

---

## Communication Channels

### War Room Setup

```
Channel naming: #inc-YYYYMMDD-brief-description
Example: #inc-20240115-checkout-down

Channel topic:
"SEV-1 | Checkout service outage | IC: @alice |
Ops: @bob | Comms: @carol | Zoom: [link]"

Pinned items:
1. Incident declaration
2. Current status (updated)
3. War room Zoom link
4. Relevant dashboards

Rules:
- Only responders post
- No side conversations
- All actions logged with timestamp
- Questions via thread, not main channel
```

### Escalation Matrix

```
           SEV-3    SEV-2    SEV-1
           ------   ------   ------
On-call      ✓        ✓        ✓
Team Lead    ○        ✓        ✓
Manager      ○        ✓        ✓
Director     ○        ○        ✓
VP           ○        ○        ✓
CTO          ○        ○        ✓
CEO          ○        ○        ✓

✓ = Required notification
○ = Optional/as needed
```

---

## Investigation Checklist

### Initial Triage (First 15 Minutes)

```
□ Confirm the incident is real (not false alarm)
□ Identify affected service(s)
□ Check monitoring dashboards
□ Review recent deployments (last 24h)
□ Check for infrastructure events
□ Determine blast radius
□ Assign severity level
□ Open war room channel
□ Notify stakeholders per escalation matrix
```

### Data Gathering

```
Logs to check:
□ Application logs (errors, warnings)
□ Load balancer logs (5xx, latency)
□ Database logs (slow queries, connections)
□ Infrastructure logs (OOM, disk, network)

Metrics to review:
□ Error rates (by endpoint)
□ Latency (p50, p95, p99)
□ Throughput (requests/sec)
□ Saturation (CPU, memory, disk, network)
□ Downstream dependencies

Questions to ask:
□ What changed recently?
□ When did it start?
□ Is it getting worse or stable?
□ Who is affected?
□ Is there a pattern (region, user type)?
```

### Hypothesis Testing

```
Document each hypothesis:

HYPOTHESIS #[N]
---------------
Theory: [What we think is happening]
Evidence for: [Why we think this]
Evidence against: [Why this might not be it]
Test: [How to verify]
Result: [CONFIRMED/DISPROVEN/INCONCLUSIVE]
```

---

## Mitigation Playbooks

### Rollback Checklist

```
Before rollback:
□ Confirm rollback version exists and is known-good
□ Identify which services need rollback
□ Notify team of rollback plan
□ Prepare monitoring for rollback

During rollback:
□ Execute rollback command/process
□ Monitor error rates
□ Monitor latency
□ Verify service health checks pass

After rollback:
□ Confirm user-facing impact resolved
□ Document rollback in timeline
□ Preserve logs/artifacts from bad version
□ Keep bad version tag for investigation
```

### Emergency Hotfix Checklist

```
□ Hotfix code reviewed (expedited review OK)
□ Hotfix tested (can be abbreviated)
□ Change approved by IC
□ Deployment coordinated in war room
□ Monitoring active during deployment
□ Ready to rollback if hotfix fails

Post-hotfix:
□ Proper PR created with full tests
□ Hotfix merged to main branch
□ Documentation updated
```

### Failover Checklist

```
Before failover:
□ Confirm secondary region is healthy
□ Verify DNS/routing is configured
□ Notify team of failover plan

Execute failover:
□ Shift traffic (gradual if possible)
□ Monitor error rates during shift
□ Monitor latency in new region
□ Verify data consistency

After failover:
□ Confirm primary issue resolved before failback
□ Plan failback during low-traffic window
□ Document failover in incident timeline
```

---

## Incident Close-Out

### Resolution Checklist

```
Before closing incident:
□ User-facing impact fully resolved
□ Error rates returned to baseline
□ Latency returned to baseline
□ No alerts firing
□ On-call confirmed stable
□ Status page updated to "Resolved"
□ Customer communication sent

Documentation:
□ Timeline complete
□ Root cause identified
□ Impact quantified
□ Mitigation documented

Handoff (if applicable):
□ Follow-up owner assigned
□ Context documented
□ Monitoring in place
```

### Incident Summary

```
=====================================
INCIDENT SUMMARY
=====================================

Incident ID: INC-[YYYY-MM-DD]-[###]
Severity: SEV-[1/2/3]

Duration: [Start time] to [End time] ([X hours Y minutes])

Impact:
- Users affected: [Number]
- Transactions lost: [Number/Value]
- SLA impact: [Yes/No, details]

Root cause:
[Brief description of what caused the incident]

Resolution:
[How the incident was resolved]

Action items:
□ [Action item] - Owner: [Name] - Due: [Date]
□ [Action item] - Owner: [Name] - Due: [Date]

Post-mortem scheduled: [Date/time]

=====================================
```
