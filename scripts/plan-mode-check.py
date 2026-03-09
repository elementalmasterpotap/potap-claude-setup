#!/usr/bin/env python3
"""
Stop хук: проверяет что при сложной задаче Claude использовал Plan Mode.

Срабатывает если ответ содержит нумерованный план (1. ... 2. ... 3. ...)
длиннее 3 шагов, но НЕ содержит признаков входа в Plan Mode.
Консервативен — только при явно длинных планах.
"""
import sys, json, re

try:
    payload = json.loads(sys.stdin.read())
    msg = payload.get("last_assistant_message", "")

    # Признак: нумерованный план с 4+ шагами
    steps = re.findall(r'^\s*\d+[\.\)]\s+\S', msg, re.MULTILINE)
    has_long_plan = len(steps) >= 4

    if not has_long_plan:
        sys.exit(0)

    # Признаки что Plan Mode использовался
    plan_mode_re = re.compile(
        r'(EnterPlanMode|план\s+записан|waiting\s+for\s+approval'
        r'|plan\s+mode|одобри\s+план|approve\s+the\s+plan'
        r'|файл\s+плана|план\s+в\s+файл)',
        re.IGNORECASE
    )
    has_plan_mode = bool(plan_mode_re.search(msg))

    # [PLAN_MODE_REQUIRED] — уже был инжектирован сигнал
    was_triggered = '[PLAN_MODE_REQUIRED]' in msg

    if has_long_plan and not has_plan_mode and not was_triggered:
        print(
            "💡 Обнаружен многошаговый план без использования Plan Mode. "
            "При 4+ шагах — используй EnterPlanMode: запиши план в файл, "
            "дождись одобрения пользователя, потом выполняй."
        )
        sys.exit(2)

except Exception:
    pass

sys.exit(0)
