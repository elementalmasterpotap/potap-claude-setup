#!/usr/bin/env python3
"""
PostToolUse хук: предупреждает о большом выводе Glob/Grep.

Если Glob вернул >30 файлов или Grep >40 строк — это verbose.
Рекомендует более точный паттерн или субагент codebase-explorer.
"""
import sys, json

GLOB_LIMIT = 30   # файлов
GREP_LIMIT = 40   # строк совпадений

try:
    payload = json.loads(sys.stdin.read())
    tool = payload.get("tool_name", "")
    output = payload.get("tool_response", "") or ""
    if isinstance(output, dict):
        output = str(output)

    if tool == "Glob":
        lines = [l for l in output.splitlines() if l.strip()]
        if len(lines) > GLOB_LIMIT:
            print(
                f"⚠️ Glob вернул {len(lines)} файлов — это много токенов в main context. "
                "Используй более точный паттерн (например src/**/*.py вместо **/*) "
                "или делегируй поиск через codebase-explorer субагент."
            )
            sys.exit(2)

    elif tool == "Grep":
        lines = [l for l in output.splitlines() if l.strip()]
        if len(lines) > GREP_LIMIT:
            print(
                f"⚠️ Grep вернул {len(lines)} совпадений. "
                "Уточни паттерн или путь поиска, "
                "или делегируй через codebase-explorer субагент."
            )
            sys.exit(2)

except Exception:
    pass

sys.exit(0)
