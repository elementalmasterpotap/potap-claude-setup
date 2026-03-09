#!/usr/bin/env python3
"""
PostToolUse хук: предупреждает когда Claude создаёт/перезаписывает файл >150 строк
без упоминания плана модульной разбивки.

Срабатывает на Write tool. Если файл > 150 строк — напоминает о монолите
и предлагает посмотреть шаблоны в haiku-economy.md.

Не блокирует — Write уже выполнен. Инжектирует напоминание в следующий промпт.
"""
import sys, json, os

try:
    payload = json.loads(sys.stdin.read())
    tool = payload.get("tool_name", "")

    if tool != "Write":
        sys.exit(0)

    inp = payload.get("tool_input", {})
    file_path = inp.get("file_path", "")
    content = inp.get("content", "")

    if not content or not file_path:
        sys.exit(0)

    # Считаем строки написанного контента
    line_count = content.count('\n') + 1

    THRESHOLD = 150

    if line_count > THRESHOLD:
        fname = os.path.basename(file_path)
        ext = os.path.splitext(fname)[1].lower()

        # Только для кодовых файлов, не для документации
        code_exts = {'.py', '.js', '.ts', '.cs', '.ps1', '.sh', '.bat', '.go', '.rs', '.java'}
        if ext not in code_exts:
            sys.exit(0)

        # Определяем тип проекта для подсказки
        type_hint = ""
        if ext == '.py':
            type_hint = "Python: main.py + handlers.py + config.py + utils.py (каждый < 150 строк)"
        elif ext == '.cs':
            type_hint = "C#: MainForm.cs (UI) + Logic.cs + Config.cs (каждый < 200 строк)"
        elif ext in ('.js', '.ts'):
            type_hint = "JS/TS: index.js + api.js + utils.js или components/"
        elif ext == '.ps1':
            type_hint = "PS: разбей на functions/ + menu.bat как точка входа"

        hint = (
            f"⚠️ Создан файл {fname} = {line_count} строк. "
            f"Монолит >150 строк: при следующих правках придётся читать весь файл. "
        )
        if type_hint:
            hint += f"Шаблон разбивки → {type_hint}. "
        hint += "Шаблоны для всех типов проектов: haiku-economy.md §Шаблоны модульных структур."

        # stderr — показывается как предупреждение в UI
        print(hint, file=sys.stderr)

except Exception:
    pass

sys.exit(0)
