"""Report formatting for yak shave analysis."""

import random
import re
from collections import defaultdict

from .models import SessionAnalysis


# Funny descriptions for different score ranges
SCORE_DESCRIPTIONS = {
    (0, 10): [
        "Surgical precision. In and out, no casualties.",
        "Like a ninja: swift, silent, done.",
        "You actually finished what you started. Rare.",
    ],
    (11, 30): [
        "Minor detours. Scenic route, but you got there.",
        "A few side quests, but the main quest prevailed.",
        "Only slightly distracted by shiny objects.",
    ],
    (31, 50): [
        "Started strong, got a bit... curious.",
        "The rabbit hole called. You answered.",
        "Scope creep is a feature, not a bug, right?",
    ],
    (51, 70): [
        "What started as a button fix became a journey.",
        "You touched files you didn't know existed.",
        "Your past self would not recognize this PR.",
    ],
    (71, 85): [
        "This was supposed to be a 5-minute fix.",
        "You've gone full yak. Never go full yak.",
        "At some point, you forgot what you came here for.",
    ],
    (86, 100): [
        "LEGENDARY yak shave. Bards will sing of this.",
        "You started fixing a typo and rewrote the universe.",
        "This session needs its own postmortem.",
        "The yak is fully shaved, groomed, and styled.",
    ],
}


def get_score_quip(score: int) -> str:
    """Get a funny description for a score."""
    for (low, high), quips in SCORE_DESCRIPTIONS.items():
        if low <= score <= high:
            return random.choice(quips)
    return "Impressive... in a concerning way."


def get_leaderboard_title(avg_score: float) -> str:
    """Get a funny title based on average yak shave score."""
    if avg_score >= 80:
        return "Legendary Yak Whisperer"
    elif avg_score >= 65:
        return "Chief Yak Shaver"
    elif avg_score >= 50:
        return "Senior Rabbit Hole Explorer"
    elif avg_score >= 35:
        return "Tangent Enthusiast"
    elif avg_score >= 20:
        return "Mostly On Track"
    else:
        return "Laser-Focused Legend"


def format_report(analyses: list[SessionAnalysis], args) -> str:
    """Format the analysis results as a human-readable report."""
    if not analyses:
        return "No sessions found in the specified date range. Your yaks remain unshaved."

    # Sort by yak shave score descending
    sorted_analyses = sorted(analyses, key=lambda a: a.yak_shave_score, reverse=True)

    # Compute stats
    avg_score = sum(a.yak_shave_score for a in analyses) / len(analyses)
    max_score = sorted_analyses[0].yak_shave_score if sorted_analyses else 0
    total_shifts = sum(len(a.domain_shifts) for a in analyses)

    # Check for multiple authors
    authors = defaultdict(list)
    for a in analyses:
        if a.author and a.author != "unknown":
            authors[a.author].append(a)

    # Header with flair
    if avg_score < 25:
        verdict = "Remarkably focused. Are you even human?"
    elif avg_score < 45:
        verdict = "Mostly on track. Room for more adventure."
    elif avg_score < 65:
        verdict = "Classic developer behavior detected."
    elif avg_score < 80:
        verdict = "You came for a bug fix, stayed for the refactor."
    else:
        verdict = "This is art. Chaotic, beautiful art."

    lines = [
        "=" * 60,
        "  YAK SHAVE REPORT",
        "  " + verdict,
        "=" * 60,
        "",
        f"  Sessions analyzed:    {len(analyses)}",
        f"  Average yak score:    {avg_score:.0f}/100",
        f"  Peak yak achieved:    {max_score}/100",
        f"  Total domain shifts:  {total_shifts}",
        "",
    ]

    # Calculate author stats (used in leaderboard and summary)
    author_stats = []
    for author, sessions in authors.items():
        avg = sum(s.yak_shave_score for s in sessions) / len(sessions)
        peak = max(s.yak_shave_score for s in sessions)
        author_stats.append((author, avg, peak, len(sessions)))
    # Sort by average score descending
    author_stats.sort(key=lambda x: x[1], reverse=True)

    # Leaderboard for multiple authors
    if len(authors) > 1:
        lines.append("TEAM YAK LEADERBOARD")
        lines.append("-" * 40)

        for rank, (author, avg, peak, count) in enumerate(author_stats[:5], 1):
            title = get_leaderboard_title(avg)
            # Truncate author name if too long
            display_name = author[:20] + "..." if len(author) > 20 else author
            lines.append(f"  {rank}. {display_name}")
            lines.append(f"     {title}")
            lines.append(f"     Avg: {avg:.0f}/100 | Peak: {peak}/100 | Sessions: {count}")
            lines.append("")

    # Dynamic sizing based on total sessions
    num_sessions = len(analyses)
    if num_sessions > 100:
        hall_of_fame_count = max(args.top, 7)
        hall_of_discipline_count = 5
    elif num_sessions > 50:
        hall_of_fame_count = max(args.top, 5)
        hall_of_discipline_count = 4
    else:
        hall_of_fame_count = args.top
        hall_of_discipline_count = 3

    # Top yak shaves
    lines.append("HALL OF FAME (Top Yak Shaves)")
    lines.append("-" * 60)

    for i, a in enumerate(sorted_analyses[:hall_of_fame_count], 1):
        domains = [s["to_domain"] for s in a.domain_shifts]

        # Truncate domain chain if too long
        if len(domains) > 5:
            domain_str = " -> ".join(domains[:3]) + f" -> ... -> {domains[-1]} ({len(domains)} total)"
        else:
            domain_str = " -> ".join(domains) if domains else "stayed focused"

        author_str = f" by {a.author}" if a.author and a.author != "unknown" else ""

        lines.append(f"{i}. [{a.yak_shave_score}/100] {a.timestamp[:10]}{author_str}")
        lines.append(f"   Session: \"{a.title or 'untitled'}\"")
        lines.append(f"   Filename: {a.filename}")
        lines.append(f"   ")
        lines.append(f"   Started with: \"{a.started_with}\"")
        if a.ended_with and a.ended_with != a.started_with:
            # Clean up ended_with - remove tool tags
            ended_clean = re.sub(r'<[^>]+>', '', a.ended_with).strip()
            lines.append(f"   Ended up at:  \"{ended_clean}\"")
        lines.append(f"   ")
        lines.append(f"   Domain journey: {domain_str}")
        lines.append(f"   Messages: {a.user_message_count} user / {a.agent_message_count} agent")
        if a.tool_calls:
            top_tools = sorted(a.tool_calls.items(), key=lambda x: x[1], reverse=True)[:4]
            tool_str = ", ".join(f"{t}({c})" for t, c in top_tools)
            lines.append(f"   Top tools: {tool_str}")
        lines.append(f"   ")
        lines.append(f"   \"{get_score_quip(a.yak_shave_score)}\"")
        lines.append("")

    # Most focused sessions (the heroes)
    focused = [a for a in sorted_analyses if a.yak_shave_score < 25]
    if focused:
        lines.append("HALL OF DISCIPLINE (Most Focused)")
        lines.append("-" * 60)
        lines.append("These developers stayed on target. Learn from them.")
        lines.append("")

        for a in list(reversed(focused))[:hall_of_discipline_count]:
            author_str = f" by {a.author}" if a.author and a.author != "unknown" else ""
            lines.append(f"  [{a.yak_shave_score}/100] {a.timestamp[:10]}{author_str}")
            lines.append(f"    Session: \"{a.title or 'untitled'}\"")
            lines.append(f"    Filename: {a.filename}")
            lines.append(f"    Goal: \"{a.started_with}\"")
            lines.append(f"    Messages: {a.user_message_count} user / {a.agent_message_count} agent | Domain shifts: {len(a.domain_shifts)}")
            lines.append(f"    \"{get_score_quip(a.yak_shave_score)}\"")
            lines.append("")

    # Fun stats
    if total_shifts > 0:
        most_common_domains = defaultdict(int)
        for a in analyses:
            for shift in a.domain_shifts:
                most_common_domains[shift["to_domain"]] += 1
        top_domain = max(most_common_domains.items(), key=lambda x: x[1])

        lines.append("FUN FACTS")
        lines.append("-" * 40)
        lines.append(f"  Most visited domain: {top_domain[0]} ({top_domain[1]} visits)")
        lines.append(f"  Avg shifts per session: {total_shifts / len(analyses):.1f}")

        # Find the biggest single-session journey
        biggest_journey = max(analyses, key=lambda a: len(a.domain_shifts))
        if len(biggest_journey.domain_shifts) > 3:
            lines.append(f"  Longest journey: {len(biggest_journey.domain_shifts)} domains in one session")
        lines.append("")

    # Score guide with personality
    lines.append("SCORE GUIDE")
    lines.append("-" * 40)
    lines.append("   0-20  Laser focused (teach us your ways)")
    lines.append("  21-40  Minor tangents (happens to the best)")
    lines.append("  41-60  Moderate drift (the spice of coding)")
    lines.append("  61-80  Significant yak (you're in deep now)")
    lines.append("  81-100 LEGENDARY (they'll write songs about this)")
    lines.append("")

    # Summary at the end
    lines.append("=" * 60)
    lines.append("SUMMARY")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"  Total sessions:       {num_sessions}")
    lines.append(f"  Average yak score:    {avg_score:.0f}/100")
    lines.append(f"  Peak yak achieved:    {max_score}/100")
    lines.append(f"  Total domain shifts:  {total_shifts}")
    lines.append("")

    # Compact leaderboard summary
    if len(authors) > 1:
        lines.append("  TEAM RANKINGS:")
        for rank, (author, avg, peak, count) in enumerate(author_stats[:5], 1):
            display_name = author[:25] + "..." if len(author) > 25 else author
            title = get_leaderboard_title(avg)
            lines.append(f"    {rank}. {display_name:<28} {avg:.0f}/100 avg  ({count} sessions) - {title}")
        lines.append("")

    # Quick stats
    yak_sessions = len([a for a in analyses if a.yak_shave_score >= 50])
    focused_sessions = len([a for a in analyses if a.yak_shave_score < 25])
    legendary_sessions = len([a for a in analyses if a.yak_shave_score >= 85])

    lines.append(f"  Legendary yak shaves (85+):  {legendary_sessions}")
    lines.append(f"  Significant yak shaves (50+): {yak_sessions}")
    lines.append(f"  Focused sessions (<25):       {focused_sessions}")
    lines.append("")
    lines.append(f"  Verdict: {verdict}")
    lines.append("")

    return "\n".join(lines)
