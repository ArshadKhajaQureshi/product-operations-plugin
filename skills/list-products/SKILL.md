---
description: >
  List products from the Product Management API catalogue.
  Use when asked to show, display, list, or browse products.
  Supports optional filters: category, status, minPrice, maxPrice, inStock, search.
---

# List Products

Fetch the current product catalogue from the Product Management API.

## Arguments

User may provide optional filters in $ARGUMENTS, for example:
  - 'electronics'               → filter by category
  - 'active under $50'          → filter by status and maxPrice
  - 'in stock'                  → filter by inStock=true
  - 'search: wireless keyboard' → partial-match search

## Instructions

1. Parse any filters from $ARGUMENTS.
2. Use the list_products MCP tool on the Product Management MCP server
3. Format the results as a readable table with columns:
   Name | SKU | Category | Price | Stock | Status
4. If the catalogue is empty, say so clearly.
5. End with the total product count.
