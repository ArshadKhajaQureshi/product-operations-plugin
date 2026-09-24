# Product Manager Plugin

Claude Code plugin for the Product Management API.

## Skills

| Skill | Invoke | What it does |
|-------|--------|--------------|
| list-products  | /product-manager-plugin:list-products [filters] | List the catalogue with optional filters |

## Installation

```
# User scope (personal, all projects):
claude --plugin-dir ./product-manager-plugin

# Project scope (shared with team via Git):
claude plugin install product-manager-plugin@your-marketplace --scope project
