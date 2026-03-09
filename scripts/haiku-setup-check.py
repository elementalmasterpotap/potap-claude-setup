#!/usr/bin/env python3
"""
Stop хук: проверяет что при создании нового проекта была добавлена секция ## Haiku.

Срабатывает если ответ содержит признаки инициализации проекта (создал CLAUDE.md,
инициализировал структуру) но НЕ содержит упоминания Haiku / .claudeignore.
Консервативен — лучше промолчать, чем ложный позитив.
"""
import sys, json, re

try:
    payload = json.loads(sys.stdin.read())
    msg = payload.get("last_assistant_message", "")

    # Признаки создания нового проекта
    init_re = re.compile(
        r'(создал\s+CLAUDE\.md'
        r'|инициализировал\s+проект'
        r'|создал\s+структуру\s+проекта'
        r'|\.claude/CLAUDE\.md.*создан'
        r'|новый\s+проект.*готов)',
        re.IGNORECASE
    )
    is_init = bool(init_re.search(msg))

    # Упоминание Haiku-настройки
    haiku_setup_re = re.compile(
        r'(##\s*haiku'
        r'|секцию?\s+haiku'
        r'|haiku\s+субагент'
        r'|codebase.explorer'
        r'|\.claudeignore)',
        re.IGNORECASE
    )
    has_haiku = bool(haiku_setup_re.search(msg))

    if is_init and not has_haiku:
        print(
            "💡 Новый проект создан, но секция ## Haiku не добавлена в .claude/CLAUDE.md. "
            "Добавь шаблон из ~/.claude/rules/haiku-setup.md — экономия токенов с первого дня."
        )
        sys.exit(2)

except Exception:
    pass

sys.exit(0)
