#!/usr/bin/env bash
# extract_discounts.sh — pull products with discount >= threshold from a
# browser-snapshot file (saved by browser_snapshot under
# AppData/Local/hermes/cache/web/browser-snapshot-*.txt).
#
# Usage:  extract_discounts.sh <snapshot_file> [min_percent]
#   min_percent  default 20
#
# Matches silpo.ua product-card lines of the form:
#   link "... стара ціна NNN гривень, знижка P%, нова ціна M гривень" [ref=eNNN]
# Prints:  "P% | <product name up to first comma>"
# Sorted by discount descending.
#
# Example:
#   extract_discounts.sh "C:/Users/Stefan/AppData/Local/hermes/cache/web/browser-snapshot-7bdc20ca41.txt" 20
set -euo pipefail

SNAP="${1:?Usage: extract_discounts.sh <snapshot_file> [min_percent]}"
MIN="${2:-20}"

grep -oE '"[^"]+, [0-9]+г?, стара ціна [0-9.]+ гривень, знижка [0-9]+%, нова ціна [0-9.]+ гривень"' "$SNAP" \
  | sed 's/^"//; s/"$//' \
  | awk -F', знижка ' -v min="$MIN" '
      { split($2,a,"%"); pct=a[1]+0; if (pct >= min) print pct"% | "$1 }
    ' \
  | sort -rn
