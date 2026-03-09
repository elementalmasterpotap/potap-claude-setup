#!/usr/bin/env python3
"""
Stop хук: проверяет что Claude не делал read-only анализ в main context
без предложения Haiku субагента.

Срабатывает если ответ содержит признаки листинга файлов (5+ путей с расширениями)
но НЕ содержит упоминания Haiku / субагента / codebase-explorer.
Намеренно консервативен — лучше промолчать, чем ложный позитив.
"""
import sys, json, re

try:
    payload = json.loads(sys.stdin.read())
    msg = payload.get("last_assistant_message", "")

    # Признаки что Claude сам делал листинг файлов
    file_path_re = re.compile(
        r'\b\w[\w/\\-]*\.(py|js|ts|cs|ps1|html|css|json|yaml|yml|md|hlsl|bat|sh)\b',
        re.IGNORECASE
    )
    file_paths = file_path_re.findall(msg)

    # Признаки дерева директорий в ответе
    tree_re = re.compile(r'[├└│]', re.UNICODE)
    has_tree = bool(tree_re.search(msg))

    # Признаки что это был листинг/анализ структуры (не просто упоминание)
    analysis_re = re.compile(
        r'(вот\s+(файлы|структура|список)|файлы\s+в\s+папке|найдено\s+\d+\s+файл'
        r'|структура\s+проекта|directory\s+structure|files\s+found)',
        re.IGNORECASE
    )
    is_analysis = bool(analysis_re.search(msg))

    # Упоминания Haiku / субагента — если есть, всё ок
    haiku_mention_re = re.compile(
        r'(haiku|codebase.explorer|субагент|subagent|\[→\s*haiku\]|haiku_eligible)',
        re.IGNORECASE
    )
    has_haiku = bool(haiku_mention_re.search(msg))

    # Срабатываем только если: много файлов ИЛИ дерево + анализ, без Haiku
    triggered = (
        not has_haiku
        and is_analysis
        and (len(file_paths) >= 5 or has_tree)
    )

    if triggered:
        print(
            "💡 Read-only анализ файловой структуры лучше делать через Haiku субагент. "
            "В следующий раз при задаче 'найди / перечисли / покажи структуру' — "
            "используй Task(subagent_type='codebase-explorer'). "
            "Добавь в ответ: '[→ Haiku] <что делаю>' перед вызовом субагента."
        )
        sys.exit(2)

except Exception:
    pass

sys.exit(0)
