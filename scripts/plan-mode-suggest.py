#!/usr/bin/env python3
"""
UserPromptSubmit хук: автоматический выбор режима планирования.

Анализирует промпт пользователя. Если задача выглядит как многошаговая
(3+ действий, архитектурное решение, новый проект, рефакторинг системы) —
инжектирует требование войти в Plan Mode через EnterPlanMode.

Консервативен: лучше не срабатывать, чем ложный позитив.
"""
import sys, json, re

# ── Явные сигналы сложной задачи (план нужен) ───────────────────────────────
PLAN_SIGNALS = [
    r'\bсоздай\s+(проект|систему|приложение|сервис|бот|сайт|структуру)\b',
    r'\bразработай\b',
    r'\bс\s+нуля\b',
    r'\bот\s+нуля\b',
    r'\bрефакторинг\b',
    r'\bархитектур\w+\b',
    r'\bреализуй\b',
    r'\bнастрой\s+\w+\s+и\s+\w+',          # настрой X и Y
    r'\bсделай\s+\w+\s+и\s+\w+\s+и\b',     # сделай X и Y и Z
    r'\bпоэтапно\b',
    r'\bпо\s+шагам\b',
    r'\bнесколько\s+(шагов|файлов|компонент|модул)\b',
    r'\bмиграц\w+\b',
    r'\bдобавь\b.{0,40}\bи\b.{0,40}\bи\b',  # добавь ... и ... и
]

# ── Сигналы что план НЕ нужен (простые задачи) ──────────────────────────────
NO_PLAN_SIGNALS = [
    r'^\s*\?',                              # начинается с вопроса
    r'\bкакой\b|\bкак\s+работает\b|\bчто\s+такое\b|\bобъясни\b|\bрасскажи\b',
    r'\bнайди\b|\bпокажи\b|\bперечисли\b|\bпроверь\b|\bпрочитай\b',
    r'\bисправь\s+(только|одну|одно|эту)\b',  # точечный фикс
    r'\bдобавь\s+одну\b|\bизмени\s+одну\b',
]

# ── Множество задач в одном промпте ─────────────────────────────────────────
MULTI_TASK_RE = re.compile(
    r'\bтакже\b|\bкроме\s+того\b|\bплюс\s+к\s+этому\b'
    r'|\bдополнительно\b|\bещё\s+(нужно|надо|сделай)\b'
    r'|\bпотом\s+(сделай|добавь|настрой)\b',
    re.IGNORECASE
)


def count_action_verbs(text):
    """Считает количество императивных глаголов."""
    verbs = re.findall(
        r'\b(создай|сделай|добавь|настрой|реализуй|исправь|удали|перенеси'
        r'|напиши|разработай|установи|запусти|подключи|обнови|перепиши'
        r'|рефакторь|оптимизируй|задеплой|запусти)\b',
        text, re.IGNORECASE
    )
    return len(verbs)


try:
    payload = json.loads(sys.stdin.read())
    prompt = payload.get("user_message") or payload.get("prompt") or ""
    text = prompt.strip()

    # Короткий промпт — не анализировать
    if len(text) < 40:
        sys.exit(0)

    # Явные сигналы что план не нужен
    for p in NO_PLAN_SIGNALS:
        if re.search(p, text, re.IGNORECASE):
            sys.exit(0)

    # Подсчёт сигналов плана
    plan_score = sum(1 for p in PLAN_SIGNALS if re.search(p, text, re.IGNORECASE))
    multi_task = bool(MULTI_TASK_RE.search(text))
    verb_count = count_action_verbs(text)

    # СИЛЬНЫЙ триггер: явный сигнал плана
    strong = plan_score >= 1

    # СЛАБЫЙ триггер: много глаголов или multi-task
    weak = (verb_count >= 3) or (multi_task and verb_count >= 2)

    if strong or weak:
        hint = (
            "[PLAN_MODE_REQUIRED] Эта задача многошаговая или архитектурная. "
            "ОБЯЗАТЕЛЬНО: сначала вызови EnterPlanMode, напиши план в файл, "
            "получи одобрение пользователя — ТОЛЬКО ПОТОМ выполняй. "
            "Не начинай делать код до одобрения плана. "
            f"(plan_signals={plan_score}, verbs={verb_count}, multi={multi_task})"
        )
        print(json.dumps({"injectedSystemPrompt": hint}, ensure_ascii=False))

except Exception:
    pass

sys.exit(0)
