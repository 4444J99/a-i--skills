"""Specstory Yak Shave Analyzer library modules."""

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
from .scoring import (
    infer_domain,
    detect_domain_shifts,
    compute_yak_shave_score,
    analyze_session,
)
from .report import format_report, get_score_quip, get_leaderboard_title
from .utils import (
    find_specstory_path,
    get_git_author,
    detect_platform,
    get_install_instructions,
)

__all__ = [
    "DomainShift",
    "SessionAnalysis",
    "parse_date_from_filename",
    "extract_title_from_filename",
    "extract_session_id",
    "extract_messages",
    "extract_file_refs",
    "extract_tool_calls",
    "summarize_message",
    "detect_goal",
    "infer_domain",
    "detect_domain_shifts",
    "compute_yak_shave_score",
    "analyze_session",
    "format_report",
    "get_score_quip",
    "get_leaderboard_title",
    "find_specstory_path",
    "get_git_author",
    "detect_platform",
    "get_install_instructions",
]
