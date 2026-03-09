#!/usr/bin/env python3
"""
Stop хук: проверяет что при создании/добавлении правила Claude создал хук.

Срабатывает если ответ содержит признаки "добавил правило" / "записал в rules/"
но НЕ содержит упоминания создания скрипта хука или регистрации в settings.json.

Логика: если Claude написал о новом правиле — должен был и хук создать.
"""
import sys, json, re

try:
    payload = json.loads(sys.stdin.read())
    msg = payload.get("last_assistant_message", "")

    # Признаки что Claude создал/добавил правило
    rule_created_re = re.compile(
        r'(добавил\s+(в\s+)?(rules/|CLAUDE\.md|правило|раздел)|'
        r'создал\s+(правило|файл\s+rules/)|'
        r'записал\s+(в\s+)?(rules/|CLAUDE\.md)|'
        r'обновил\s+(rules/|CLAUDE\.md)|'
        r'новое\s+правило\s+(добавлен|записан|создан)|'
        r'edit.*rules/.*\.md|write.*rules/.*\.md)',
        re.IGNORECASE
    )

    # Признаки что хук создан / упомянут
    hook_created_re = re.compile(
        r'(scripts/[\w-]+\.py|'
        r'зарегистрир|'
        r'settings\.json|'
        r'Stop\s+хук|'
        r'PostToolUse|PreToolUse|'
        r'хук\s+(создан|добавлен|зарегистрирован)|'
        r'НЕВОЗМОЖНО\s*—)',
        re.IGNORECASE
    )

    has_rule = bool(rule_created_re.search(msg))
    has_hook = bool(hook_created_re.search(msg))

    if has_rule and not has_hook:
        print(
            "⚠️ Правило добавлено без хука. "
            "Каждое правило требует хука — создай scripts/<name>-check.py "
            "и зарегистрируй в settings.json. "
            "Если автоматизация невозможна — объясни ПОЧЕМУ в комментарии правила. "
            "Добавь в конец ответа что делаешь с хуком для этого правила."
        )
        sys.exit(2)

except Exception:
    pass

sys.exit(0)
