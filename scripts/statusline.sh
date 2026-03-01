#!/bin/bash
# Claude Code statusline — git ветка + изменения

BRANCH=$(git branch --show-current 2>/dev/null)
if [ -n "$BRANCH" ]; then
    MODIFIED=$(git diff --name-only 2>/dev/null | wc -l | tr -d ' ')
    STAGED=$(git diff --cached --name-only 2>/dev/null | wc -l | tr -d ' ')
    if [ "$STAGED" -gt 0 ] || [ "$MODIFIED" -gt 0 ]; then
        echo "${BRANCH} [${STAGED}↑ ${MODIFIED}~]"
    else
        echo "${BRANCH} ✓"
    fi
else
    echo "no git"
fi
