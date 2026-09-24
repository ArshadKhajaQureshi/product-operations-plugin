#!/usr/bin/env python3

import json
import re
import sys

PATTERNS = [
    ("Anthropic Key", r"sk-ant-[A-Za-z0-9_-]{20,}"),
    ("OpenAI Key", r"sk-[A-Za-z0-9]{20,}"),
    ("GitHub Token", r"ghp_[A-Za-z0-9]{30,}"),
    ("AWS Secret", r"(?i)aws.{0,20}secret.{0,20}[A-Za-z0-9/+]{20,}"),
    # The optional quote after the key lets these match JSON/YAML keys as well as env-style assignments.
    ("Password", r"(?i)password[\"']?\s*[:=]\s*[\"']?[^\s\"']+"),
    ("API key assignment", r"(?i)[A-Za-z0-9_]*(?:api[_-]?key|secret|token)[\"']?\s*[:=]\s*[\"']?[^\s\"']+"),
]

# Only the content being written is scanned; file_path and old_string are ignored.
WRITTEN_FIELDS = ("content", "new_string")


def deny(reason):
    # PreToolUse: hookSpecificOutput is the current format (top-level "decision" is deprecated)
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }
        )
    )


def written_text(tool_input):
    """Return the raw text a tool call is about to write (not JSON-escaped)."""
    parts = [tool_input.get(field, "") for field in WRITTEN_FIELDS]
    for edit in tool_input.get("edits", []):  # MultiEdit
        parts.append(edit.get("new_string", ""))
    return "\n".join(p for p in parts if isinstance(p, str))


try:
    data = json.load(sys.stdin)
    text = written_text(data.get("tool_input", {}))

    for name, pattern in PATTERNS:
        if re.search(pattern, text):
            deny(f"Potential secret detected: {name}")
            sys.exit(0)

    # No output + exit 0 = allow, and the normal permission flow still applies

except Exception as e:
    # Fail open so a broken hook doesn't block legitimate work
    print(f"secret-guard error: {e}", file=sys.stderr)
