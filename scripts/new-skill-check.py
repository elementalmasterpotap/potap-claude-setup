#!/usr/bin/env python3
"""
PreToolUse hook: проверка дублей и хука при создании нового скилла.
Срабатывает на Write → skills/*/SKILL.md.

1. Если похожий скилл уже есть → блокировать, требовать обоснование.
2. Если content не содержит mention хука/НЕВОЗМОЖНО → предупредить.
"""
import sys, json, os, re

try:
    data = json.load(sys.stdin)
    tool_name = data.get('tool_name', '')
    tool_input = data.get('tool_input', {})

    if tool_name != 'Write':
        sys.exit(0)

    file_path = tool_input.get('file_path', '').replace('\\', '/')

    m = re.search(r'skills/([^/]+)/SKILL\.md$', file_path)
    if not m:
        sys.exit(0)

    new_skill = m.group(1).lower()
    content = tool_input.get('content', '')

    # --- Проверка дублей ---
    skills_dir = os.path.expanduser('~/.claude/skills')
    existing = []
    if os.path.exists(skills_dir):
        existing = [d for d in os.listdir(skills_dir)
                    if os.path.isdir(os.path.join(skills_dir, d)) and d.lower() != new_skill]

    new_tokens = set(re.split(r'[-_]', new_skill)) - {'ref', 'check', 'post', 'pre'}
    similar = [s for s in existing
               if new_tokens & (set(re.split(r'[-_]', s.lower())) - {'ref', 'check', 'post', 'pre'})]

    if similar:
        # Если в content явно объяснено почему не дубль — пропускаем
        if not re.search(r'не дубль|отличается от|объедин|вместо|replace', content, re.IGNORECASE):
            print(json.dumps({
                "decision": "block",
                "reason": (
                    f"⚠️ Похожие скиллы уже есть: {', '.join(similar)}\n"
                    "Стоит ли объединить?\n"
                    "Если нет — добавь в начало SKILL.md: `<!-- не дубль: <причина> -->`"
                )
            }, ensure_ascii=False))
            sys.exit(0)

    # ВАЖНО: <!-- Stop hook: ... --> комментарий должен быть В КОНЦЕ файла,
    # не после frontmatter — иначе action-скиллы показывают его как description

    # --- Проверка что хук запланирован ---
    has_hook_note = bool(re.search(
        r'Stop hook|хук|НЕВОЗМОЖНО|scripts/.*\.py|hook:',
        content, re.IGNORECASE
    ))
    if not has_hook_note:
        print(json.dumps({
            "decision": "block",
            "reason": (
                f"⚠️ Скилл '{new_skill}' создаётся без упоминания хука.\n"
                "Правило CLAUDE.md §Новое правило: нужен Stop/PreTool хук.\n"
                "Добавь в SKILL.md: `<!-- Stop hook: НЕВОЗМОЖНО — <причина> -->` или создай хук."
            )
        }, ensure_ascii=False))

except Exception:
    pass

sys.exit(0)
