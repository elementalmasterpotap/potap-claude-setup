---
name: bilingual-ref
description: Двуязычное оформление GitHub репозиториев (EN+RU). Автоматически подгружается при задачах с README, GitHub оформлением, двуязычностью.
user-invocable: false
---

<!-- Stop hook: НЕВОЗМОЖНО — стилевые правила README, нет машинных паттернов -->
## Структура двуязычного README

```markdown
<div align="center">
  <!-- лого, бейджи -->

  <details>
  <summary>🇬🇧 English</summary>

  **One-line description in English.**

  ## Features
  | Feature | Description |
  |---------|-------------|
  | ... | ... |

  </details>

  <details open>
  <summary>🇷🇺 Русский</summary>

  **Описание одной строкой на русском.**

  ## Что делает
  | Функция | Описание |
  |---------|----------|
  | ... | ... |

  </details>
</div>
```

`<details open>` — русская версия открыта по умолчанию (аудитория Потапа).

## Description и topics репо

```
description → английский (GitHub лучше индексирует)
topics      → строчные, дефисы: python, windows, telegram-bot
```

## Правила

| Файл | Язык |
|------|------|
| README.md | EN + RU (две details) |
| docs/PATCHNOTES.md | RU (внутренняя документация) |
| Код, комментарии | EN (международный стандарт) |
| description, topics | EN |
