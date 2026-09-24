#!/usr/bin/env python3

import json
import re
import sys

PATTERNS = [
    ("Anthropic Key", r"sk-ant-[A-Za-z0-9_-]{20,}"),
    ("OpenAI Key", r"sk-[A-Za-z0-9]{20,}"),
    ("GitHub Token", r"ghp_[A-Za-z0-9]{30,}"),
    ("AWS Secret", r"(?i)aws.{0,20}secret.{0,20}[A-Za-z0-9/+]{20,}"),
    ("Password", r"(?i)password\s*[:=]\s*[\"']?.+[\"']?"),
    ("API key assignment", r"(?i)[A-Za-z0-9_]*(?:api[_-]?key|secret|token)\s*[:=]\s*[\"']?[^\s\"']+"),
]


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


try:
    data = json.load(sys.stdin)

    # Only scan what the tool is about to write, not the whole event
    text = json.dumps(data.get("tool_input", {}))

    for name, pattern in PATTERNS:
        if re.search(pattern, text):
            deny(f"Potential secret detected: {name}")
            sys.exit(0)

    # No output + exit 0 = allow, and the normal permission flow still applies

except Exception as e:
    # Fail open so a broken hook doesn't block legitimate work
    print(f"secret-guard error: {e}", file=sys.stderr)
