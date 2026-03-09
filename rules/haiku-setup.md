# Haiku Setup — переход на Haiku в новом проекте

<!-- Stop hook: scripts/haiku-setup-check.py — проверяет что новый проект имеет Haiku конфиг -->
<!-- Skill: haiku-setup/SKILL.md (knowledge, user-invocable: false) -->

## Принцип

Каждый новый проект должен иметь явные правила использования Haiku.
Экономия токенов с первого дня, не после того как Pro лимит кончится.

---

## Чеклист при старте нового проекта [ОБЯЗАТЕЛЬНО]

```
□ .claude/CLAUDE.md содержит секцию ## Haiku (шаблон ниже)
□ .claudeignore создан (node_modules, *.lock, dist/, build/)
□ Задача "найди / перечисли / покажи / структура" → через субагент, не в main
□ Правки файлов → Sonnet, не субагент
```

---

## Шаблон ## Haiku для нового .claude/CLAUDE.md

```markdown
## Haiku
Анализ / поиск / структура → codebase-explorer (Haiku субагент).
Правки файлов → Sonnet (main context).
[→ Haiku] писать перед каждым вызовом субагента.
Детали маппинга → ~/.claude/rules/haiku-economy.md
```

Место: сразу после `## Проект` в `.claude/CLAUDE.md`.

---

## Маппинг задача → что использовать

| Задача | Что использовать |
|--------|-----------------|
| найди файлы / grep / структура | codebase-explorer (Haiku) |
| прочитай и суммаризируй файл | codebase-explorer (Haiku) |
| code review перед коммитом | code-reviewer (Haiku) |
| написать / исправить код | Sonnet (main context) |
| архитектурное решение | Sonnet + thinking |
| root cause / security audit | Opus (переключить через Esc) |

---

## Правило: всегда при инициализации

При любом `новый проект` / `init` / `создай структуру`:
1. Создать `.claude/CLAUDE.md` по `CLAUDE_BASE.md`
2. **Добавить секцию `## Haiku`** (шаблон выше)
3. Создать `.claudeignore` (шаблон из `haiku-economy.md` §Агрессивный .claudeignore)

Без секции `## Haiku` — проект неполностью настроен.

---

## Оптимизация существующего проекта

Нет `## Haiku` секции в `.claude/CLAUDE.md`:
1. Прочитать файл
2. Добавить секцию после `## Проект`
3. Создать `.claudeignore` если нет

---

## .claudeignore — минимальный стартер

```gitignore
node_modules/
package-lock.json
yarn.lock
pnpm-lock.yaml
dist/
build/
__pycache__/
*.pyc
.venv/
venv/
*.log
*.exe
*.dll
*.zip
.DS_Store
Thumbs.db
```
