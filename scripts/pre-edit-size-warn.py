#!/usr/bin/env python3
"""
PreToolUse хук: предупреждает при чтении файлов > 200 строк без offset.

Срабатывает на Read без offset/limit когда файл большой.
Напоминает паттерн: Grep → Read(offset, limit) → Edit

Не блокирует — только warn (exit 0, но пишет в stderr для Claude).
"""
import sys, json, os, subprocess

try:
    payload = json.loads(sys.stdin.read())
    tool = payload.get("tool_name", "")
    inp = payload.get("tool_input", {})

    # Только Read без offset
    if tool != "Read":
        sys.exit(0)

    file_path = inp.get("file_path", "")
    offset = inp.get("offset")
    limit = inp.get("limit")

    # Если offset/limit уже заданы — всё хорошо
    if offset is not None or limit is not None:
        sys.exit(0)

    if not file_path or not os.path.isfile(file_path):
        sys.exit(0)

    # Считаем строки быстро
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            line_count = sum(1 for _ in f)
    except Exception:
        sys.exit(0)

    THRESHOLD = 200

    if line_count > THRESHOLD:
        reason = (
            f"Файл {os.path.basename(file_path)} = {line_count} строк. "
            f"Читать целиком = {line_count} строк в контекст (лишние токены). "
            f"Паттерн экономии 10-20×: "
            f"1) Grep('нужная_функция', '{file_path}') → найди строку N, "
            f"2) Read('{file_path}', offset=N-5, limit=40) → только нужный кусок, "
            f"3) Edit → правь. "
            f"Если НУЖНО читать весь файл — перезапусти Read этого же файла явно."
        )
        print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))

except Exception:
    pass

sys.exit(0)
