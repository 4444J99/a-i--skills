---
name: conversation-content-pipeline
description: Transform AI conversations and chat transcripts into publishable content including blog posts, documentation, tutorials, and knowledge base entries. Covers extraction, restructuring, and editorial refinement. Triggers on conversation-to-content, transcript processing, or chat-to-doc requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - content-pipeline
  - conversation
  - transcript
  - publishing
  - knowledge-extraction
governance_phases: [build]
organ_affinity: [all]
triggers: [user-asks-about-conversation-content, context:transcript-to-content, context:chat-to-doc, context:session-to-article]
complements: [essay-publishing-pipeline, creative-writing-craft, technical-analytical-writing]
---

# Conversation-to-Content Pipeline

Extract publishable content from AI conversations, chat transcripts, and session logs.

## Pipeline Overview

```
Raw Conversation → Extract → Restructure → Refine → Format → Publish
       │                │           │          │         │
       │                │           │          │         └─ Markdown, HTML, PDF
       │                │           │          └─ Editorial polish, voice consistency
       │                │           └─ Organize by topic, add structure
       │                └─ Identify key insights, decisions, code
       └─ Chat logs, transcripts, session files
```

## Extraction Patterns

### Content Type Classification

| Content Type | Signal | Output |
|-------------|--------|--------|
| **Tutorial** | Step-by-step problem solving | How-to article |
| **Decision record** | Evaluating options, choosing approach | ADR or technical note |
| **Code walkthrough** | Explaining code, reviewing changes | Documentation |
| **Insight** | Novel observation, unexpected finding | Blog post or essay |
| **Q&A** | Repeated questions and answers | FAQ or knowledge base |
| **Debug log** | Troubleshooting process | Incident report |

### Key Moment Identification

```python
KEY_MOMENT_SIGNALS = {
    "insight": ["I realized", "The key insight is", "This means that", "Interesting —"],
    "decision": ["Let's go with", "The best approach", "I chose", "Decision:"],
    "learning": ["TIL", "I didn't know", "Turns out", "The important thing is"],
    "warning": ["Watch out for", "Don't forget", "Common mistake", "Anti-pattern"],
    "summary": ["In summary", "To recap", "The main takeaway", "Key points"],
}

def identify_key_moments(messages: list[dict]) -> list[dict]:
    moments = []
    for msg in messages:
        for moment_type, signals in KEY_MOMENT_SIGNALS.items():
            if any(signal.lower() in msg["content"].lower() for signal in signals):
                moments.append({
                    "type": moment_type,
                    "content": msg["content"],
                    "role": msg["role"],
                    "index": msg.get("index"),
                })
    return moments
```

## Restructuring

### Conversation to Article Structure

```markdown
## From Conversation:
- User asks about circuit breakers
- Agent explains the concept
- User asks about implementation
- Agent provides code
- User asks about testing
- Agent explains test strategy
- User confirms understanding

## To Article:
1. Introduction (from the question context)
2. What is a Circuit Breaker? (from explanation)
3. Implementation (from code example)
4. Testing Strategy (from testing discussion)
5. Key Takeaways (from summary moments)
```

### Code Extraction and Annotation

```python
def extract_code_blocks(conversation: list[dict]) -> list[dict]:
    blocks = []
    for msg in conversation:
        # Find fenced code blocks
        in_block = False
        current_block = {"language": "", "code": "", "context": ""}
        for line in msg["content"].split("\n"):
            if line.startswith("```"):
                if in_block:
                    blocks.append(current_block)
                    current_block = {"language": "", "code": "", "context": ""}
                    in_block = False
                else:
                    current_block["language"] = line[3:].strip()
                    in_block = True
            elif in_block:
                current_block["code"] += line + "\n"

        # Context is the text before the code block
        if blocks:
            blocks[-1]["context"] = extract_preceding_text(msg["content"], blocks[-1]["code"])

    return blocks
```

## Refinement

### Voice Normalization

Conversations mix casual chat with technical content. Normalize to a consistent editorial voice:

| Conversation | Published |
|-------------|-----------|
| "So basically what happens is..." | "The process works as follows:" |
| "Yeah, that's the key thing" | "This is the critical consideration." |
| "Let me try another approach" | *(remove — process artifact)* |
| "Oh wait, I was wrong about that" | *(keep the correction, remove the error)* |

### Content Quality Checklist

- [ ] All code examples tested and working
- [ ] Conversational artifacts removed (filler, corrections, tangents)
- [ ] Consistent voice throughout
- [ ] Technical accuracy verified
- [ ] Missing context filled in (assumptions made explicit)
- [ ] Links and references added
- [ ] Introduction provides motivation
- [ ] Conclusion summarizes key points

## Output Formats

### Blog Post Template

```markdown
---
title: "{Derived from conversation topic}"
date: {date}
tags: [{extracted-topics}]
source_session: "{session_id}"
---

# {Title}

{Hook paragraph derived from the initial question}

## {Section 1: Context/Problem}
{Restructured from early conversation}

## {Section 2: Solution/Approach}
{Code and explanations from the middle}

## {Section 3: Key Insights}
{Extracted insights and decisions}

## Conclusion
{Synthesized from final exchanges}
```

### Knowledge Base Entry

```markdown
# {Topic}

**Last updated:** {date}
**Source:** Conversation {session_id}

## Quick Answer
{The TL;DR from the conversation}

## Detailed Explanation
{Restructured explanation}

## Examples
{Extracted code blocks with context}

## See Also
- {Related topics from the conversation}
```

## Batch Processing

```python
async def process_session_archive(sessions_dir: str, output_dir: str):
    for session_file in Path(sessions_dir).glob("*.jsonl"):
        messages = load_session(session_file)
        moments = identify_key_moments(messages)

        if not moments:
            continue  # Skip sessions with no extractable content

        content_type = classify_content(moments)
        article = restructure(messages, moments, content_type)
        refined = refine(article)

        output = Path(output_dir) / f"{session_file.stem}.md"
        output.write_text(format_article(refined))
```

## Anti-Patterns

- **Publishing raw transcripts** — Always restructure and refine
- **Losing the narrative** — Conversations have implicit structure; make it explicit
- **Including errors without corrections** — Keep only the final correct version
- **No attribution** — Always note that content originated from AI conversation
- **Ignoring context** — Conversations assume shared context; make it explicit for readers
- **One-to-one mapping** — One conversation might yield multiple articles, or vice versa
