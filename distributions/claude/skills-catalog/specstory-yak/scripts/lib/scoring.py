"""Scoring and analysis logic for yak shave detection."""

import sys
from dataclasses import asdict
from pathlib import Path
from typing import Optional

from .models import DomainShift, SessionAnalysis
from .parser import (
    parse_date_from_filename,
    extract_title_from_filename,
    extract_session_id,
    extract_messages,
    extract_file_refs,
    extract_tool_calls,
    summarize_message,
    detect_goal,
)


def infer_domain(file_ref: str) -> str:
    """Infer the domain/area from a file reference."""
    ref_lower = file_ref.lower()

    if any(x in ref_lower for x in ["test", "spec", "__test__"]):
        return "testing"
    if any(x in ref_lower for x in ["doc", "readme", "md", "changelog"]):
        return "documentation"
    if any(x in ref_lower for x in ["ci", "github", "workflow", "jenkins", "docker", "k8s"]):
        return "devops"
    if any(x in ref_lower for x in ["config", "env", "settings", "yaml", "json", "toml"]):
        return "configuration"
    if any(x in ref_lower for x in ["ui", "component", "page", "view", "css", "style", "tsx", "jsx"]):
        return "frontend"
    if any(x in ref_lower for x in ["api", "server", "route", "controller", "handler"]):
        return "backend"
    if any(x in ref_lower for x in ["db", "model", "schema", "migration", "sql"]):
        return "database"
    if any(x in ref_lower for x in ["auth", "login", "session", "token"]):
        return "auth"
    if any(x in ref_lower for x in ["script", "bin", "tool", "cli"]):
        return "tooling"

    return "code"


def detect_domain_shifts(file_refs: list[str], messages: list) -> list[DomainShift]:
    """Detect when the session shifted domains based on file references."""
    shifts = []

    if not file_refs:
        return shifts

    # Track domains in order of appearance
    seen_domains = []
    for ref in file_refs:
        domain = infer_domain(ref)
        if not seen_domains or seen_domains[-1] != domain:
            if seen_domains:
                shifts.append(DomainShift(
                    from_domain=seen_domains[-1],
                    to_domain=domain,
                    trigger_line=0,  # Would need more parsing for exact line
                    signal="file_ref_change"
                ))
            seen_domains.append(domain)

    return shifts


def compute_yak_shave_score(analysis: SessionAnalysis) -> tuple[int, dict]:
    """
    Compute yak shave score (0-100) based on various factors.
    Returns (score, breakdown_dict)
    """
    breakdown = {}

    # Factor 1: Domain shifts (40% weight)
    num_shifts = len(analysis.domain_shifts)
    shift_score = min(100, num_shifts * 25)  # Each shift adds 25 points
    breakdown["domain_shifts"] = {"raw": num_shifts, "score": shift_score, "weight": 0.4}

    # Factor 2: Session length vs initial message complexity (20% weight)
    initial_words = len(analysis.initial_message.split())
    total_messages = analysis.user_message_count + analysis.agent_message_count

    # Simple request + long session = high yak shave
    if initial_words < 20 and total_messages > 10:
        length_score = min(100, (total_messages - 10) * 10)
    elif initial_words < 50 and total_messages > 20:
        length_score = min(100, (total_messages - 20) * 5)
    else:
        length_score = 0
    breakdown["length_ratio"] = {"raw": f"{initial_words}w/{total_messages}m", "score": length_score, "weight": 0.2}

    # Factor 3: Tool type cascade (15% weight)
    # Read -> Edit -> Create is more escalation than just Read
    tool_types = set(analysis.tool_calls.keys())
    escalation_levels = {
        "Read": 1, "Grep": 1, "Glob": 1,
        "Edit": 2, "Write": 3,
        "Bash": 3, "shell": 3,
        "WebFetch": 4, "WebSearch": 4,
        "Task": 5,
    }
    max_escalation = max((escalation_levels.get(t, 2) for t in tool_types), default=1)
    tool_score = (max_escalation - 1) * 25
    breakdown["tool_cascade"] = {"raw": list(tool_types), "score": tool_score, "weight": 0.15}

    # Factor 4: File reference diversity (25% weight)
    domains = set(infer_domain(ref) for ref in analysis.file_refs)
    domain_score = min(100, (len(domains) - 1) * 25) if domains else 0
    breakdown["domain_diversity"] = {"raw": list(domains), "score": domain_score, "weight": 0.25}

    # Weighted total
    total = (
        shift_score * 0.4 +
        length_score * 0.2 +
        tool_score * 0.15 +
        domain_score * 0.25
    )

    return int(total), breakdown


def analyze_session(filepath: Path) -> Optional[SessionAnalysis]:
    """Analyze a single specstory session file."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
        return None

    filename = filepath.name
    messages = extract_messages(content)

    if not messages:
        return None

    # Get initial user message
    initial_msg = ""
    for role, _, text in messages:
        if role == "user":
            initial_msg = text
            break

    if not initial_msg:
        return None

    # Count messages by role
    user_count = sum(1 for r, _, _ in messages if r == "user")
    agent_count = sum(1 for r, _, _ in messages if r in ("agent", "assistant"))

    # Extract file refs and tool calls
    file_refs = extract_file_refs(content)
    tool_calls = extract_tool_calls(content)

    # Detect domain shifts
    domain_shifts = detect_domain_shifts(file_refs, messages)

    # Get last message for "ended with"
    last_agent_msg = ""
    for role, _, text in reversed(messages):
        if role in ("agent", "assistant"):
            last_agent_msg = text
            break

    analysis = SessionAnalysis(
        filename=filename,
        session_id=extract_session_id(content),
        timestamp=str(parse_date_from_filename(filename) or "unknown"),
        title=extract_title_from_filename(filename),
        initial_message=initial_msg,
        initial_message_summary=summarize_message(initial_msg),
        detected_goal=detect_goal(initial_msg),
        user_message_count=user_count,
        agent_message_count=agent_count,
        file_refs=file_refs,
        tool_calls=tool_calls,
        domain_shifts=[asdict(s) for s in domain_shifts],
        started_with=summarize_message(initial_msg, 300),
        ended_with=summarize_message(last_agent_msg, 300) if last_agent_msg else "",
    )

    # Compute score
    score, breakdown = compute_yak_shave_score(analysis)
    analysis.yak_shave_score = score
    analysis.score_breakdown = breakdown
    analysis.is_yak_shave = score > 40

    return analysis
