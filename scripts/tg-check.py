#!/usr/bin/env python3
"""
Stop hook: python-telegram-bot v22+ ловушки (tg-ref skill).
Правило TG-4 (lessons_universal.md):
  TG-4a: from telegram import ChatAction → должно быть from telegram.constants import ChatAction
  TG-4b: edit_message_text без try/except → BadRequest if message not modified
"""
import sys, json, re

PATTERNS = [
    (
        # Только в начале строки — реальный import, не упоминание в тексте
        r'(?m)^from telegram import.*\bChatAction\b',
        "TG-4a: ChatAction переехал в v22+.\n"
        "Используй: from telegram.constants import ChatAction"
    ),
]

try:
    data = json.load(sys.stdin)

    if data.get('stop_hook_active', False):
        sys.exit(0)

    text = data.get('last_assistant_message', '')

    for pattern, message in PATTERNS:
        if re.search(pattern, text):
            print(json.dumps({
                "decision": "block",
                "reason": f"⚠️ {message}"
            }, ensure_ascii=False))
            sys.exit(0)

except Exception:
    pass

sys.exit(0)
