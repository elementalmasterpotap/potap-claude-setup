#!/usr/bin/env python3
"""
PostToolUse хук: при создании/редактировании правила — проверить наличие хука.

Покрывает:
  - Write на rules/*.md           (новый файл правила)
  - Edit на rules/*.md            (правка существующего)
  - Write/Edit на CLAUDE.md       (правило прямо в главном файле)

Правило CLAUDE.md §Новое правило [БЛОКЕР]:
  каждое правило → Stop/PTU/PostTU/UPS хук (обязательно)
  НЕВОЗМОЖНО без причины — не принимается
"""
import sys, json, os, re

try:
    data = json.load(sys.stdin)
    tool_name = data.get('tool_name', '')
    tool_input = data.get('tool_input', {})

    if tool_name not in ('Write', 'Edit'):
        sys.exit(0)

    file_path = tool_input.get('file_path', '').replace('\\', '/')

    # Покрываем: rules/*.md и CLAUDE.md
    is_rule_file = bool(re.search(r'rules/[\w-]+\.md$', file_path))
    is_claude_md = file_path.endswith('CLAUDE.md')

    if not is_rule_file and not is_claude_md:
        sys.exit(0)

    # Для Edit — проверяем new_string (добавляемый контент)
    if tool_name == 'Edit':
        check_content = tool_input.get('new_string', '')
        # Короткие правки (опечатки, форматирование) — не проверяем
        if len(check_content.strip()) < 100:
            sys.exit(0)
    else:
        check_content = tool_input.get('content', '')

    if not check_content:
        sys.exit(0)

    # Хук упомянут? (любой тип)
    has_hook = bool(re.search(
        r'(Stop hook|PreToolUse|PostToolUse|UserPromptSubmit'
        r'|scripts/[\w-]+\.py'
        r'|НЕВОЗМОЖНО\s*—'
        r'|hook:)',
        check_content, re.IGNORECASE
    ))

    if not has_hook:
        fname = os.path.basename(file_path)
        action = "создан" if tool_name == 'Write' else "отредактирован"
        print(json.dumps({
            "decision": "block",
            "reason": (
                f"⚠️ Файл правила {fname} {action} без хука.\n"
                "Обязательный комплект: правило + скрипт хука + settings.json.\n"
                "Шаги:\n"
                "  1. Создай scripts/<name>-check.py (Stop / PreToolUse / PostToolUse)\n"
                "  2. Зарегистрируй в settings.json hooks\n"
                "  3. Добавь комментарий в правило: <!-- Stop hook: scripts/name.py -->\n"
                "Если автоматизация НЕВОЗМОЖНА → добавь: <!-- Stop hook: НЕВОЗМОЖНО — <причина> -->"
            )
        }, ensure_ascii=False))

except Exception:
    pass

sys.exit(0)
