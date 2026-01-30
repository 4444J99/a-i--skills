"""Data models for specstory session analysis."""

from dataclasses import dataclass, field


@dataclass
class DomainShift:
    """Represents a detected shift in topic/domain during a session."""
    from_domain: str
    to_domain: str
    trigger_line: int
    signal: str  # "file_ref_change", "tool_type_change", "goal_replacement"


@dataclass
class SessionAnalysis:
    """Analysis results for a single specstory session."""
    filename: str
    session_id: str
    timestamp: str
    title: str

    # Initial intent
    initial_message: str
    initial_message_summary: str
    detected_goal: str

    # Metrics
    user_message_count: int = 0
    agent_message_count: int = 0
    file_refs: list = field(default_factory=list)
    tool_calls: dict = field(default_factory=dict)
    domain_shifts: list = field(default_factory=list)

    # Scoring
    yak_shave_score: int = 0
    score_breakdown: dict = field(default_factory=dict)

    # Summary
    started_with: str = ""
    ended_with: str = ""
    is_yak_shave: bool = False

    # Author (from git blame)
    author: str = "unknown"
