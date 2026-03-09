<div align="center">

[![](https://img.shields.io/badge/16_rules-0099CC?style=flat-square)](rules/)
[![](https://img.shields.io/badge/19_skills-7B61FF?style=flat-square)](skills/)
[![](https://img.shields.io/badge/48_hooks-FF6B35?style=flat-square)](scripts/)
[![](https://img.shields.io/badge/4_agents-22AA44?style=flat-square)](agents/)
[![](https://img.shields.io/badge/license-MIT-555555?style=flat-square)](LICENSE)

<br>

<details>
<summary>🇬🇧 English</summary>

**My full Claude Code customization stack — rules, hooks, agents, skills, templates.**

A personal setup that makes Claude Code behave like a teammate who knows your stack,
catches your mistakes before they happen, and routes tasks to the right model automatically.

## What's inside

| Component | Count | Purpose |
|---|---|---|
| `CLAUDE.md` | 1 | Session algorithm, task router — the brain |
| `rules/*.md` | 16 | Domain modules: GitHub, Telegram, Windows, HLSL, Haiku economy, vibe coding... |
| `agents/*.md` | 4 | Subagent profiles: code-reviewer, codebase-explorer, opus-reasoner, shader-expert |
| `skills/*/SKILL.md` | 19 | Slash-skills: action (commit, patchnote, sync) + knowledge (auto-loaded reference) |
| `scripts/*.py/.sh` | 48 | Pre/PostToolUse + Stop hooks — block destructive actions, enforce patterns |
| `templates/` | 6 | Starter files for new projects (CLAUDE_BASE, MEMORY_TEMPLATE, hookify...) |

## How it works

```
Task arrives
     │
     ├─ read CLAUDE.md task router
     ├─ load relevant rule module
     ├─ route simple search → Haiku subagent (saves ~70% tokens)
     └─ hooks enforce rules automatically:
           logo/ assets/  →  block
           rm -rf / push -f main  →  block
           --no-verify / reset --hard  →  warn
           new rule without hook  →  stop
```

## Quick start

```bash
# 1. Clone
git clone https://github.com/YOUR_GITHUB_USERNAME/potap-claude-setup ~/.claude/claude-setup

# 2. Copy what you want
cp -r ~/.claude/claude-setup/rules/* ~/.claude/rules/
cp -r ~/.claude/claude-setup/agents/* ~/.claude/agents/
cp -r ~/.claude/claude-setup/skills/* ~/.claude/skills/
cp -r ~/.claude/claude-setup/scripts/* ~/.claude/scripts/

# 3. Edit personal data in rules/communication.md, rules/workflow_universal.md
#    Replace [YOUR_NAME], YOUR_GITHUB_USERNAME, @YOUR_CHANNEL with your own values
```

## Key rules

| File | What it does |
|---|---|
| `rules/haiku-economy.md` | When to use Haiku vs Sonnet vs Opus — full routing table |
| `rules/communication.md` | Tone, pseudographics defaults, personal memes |
| `rules/workflow_universal.md` | Deploy cycle, patchnotes, Telegram announce, GitHub ops |
| `rules/lessons_universal.md` | Accumulated gotchas: PS, C#, Telegram Bot API, GitHub |
| `rules/windows_dev.md` | WinForms dark theme, PS installer patterns |
| `rules/vibe_coding.md` | Natural language → parameter mapping concept |

## Key hooks

| Script | Type | Blocks/warns |
|---|---|---|
| `pretool-safety.py` | PreToolUse | `rm -rf`, `push --force main`, `reset --hard` |
| `token-leak-check.py` | PreToolUse | Hardcoded tokens before Write |
| `new-rule-check.py` | Stop | New rule without accompanying hook |
| `plan-mode-check.py` | Stop | Multi-step plan without entering Plan Mode |
| `html-monolith-check.py` | PreToolUse | `<style>`/`<script>` inside HTML (token waste) |
| `haiku-suggest.py` | UPS | Injects `[HAIKU_ELIGIBLE]` / `[OPUS_ELIGIBLE]` hints |

</details>

<details open>
<summary>🇷🇺 Русский</summary>

**Полный стек кастомизации Claude Code — правила, хуки, агенты, скиллы, шаблоны.**

Личный сетап который превращает Claude Code в коллегу: знает твой стек,
ловит ошибки до того как они случились, автоматически роутит задачи на нужную модель.

## Что внутри

| Компонент | Кол-во | Назначение |
|---|---|---|
| `CLAUDE.md` | 1 | Алгоритм сессии, роутер задач — мозг системы |
| `rules/*.md` | 16 | Модули: GitHub, Telegram, Windows, HLSL, Haiku-экономия, вайбкодинг... |
| `agents/*.md` | 4 | Профили субагентов: code-reviewer, codebase-explorer, opus-reasoner, shader-expert |
| `skills/*/SKILL.md` | 19 | Скиллы: action (commit, patchnote, sync) + knowledge (автозагружаемые справочники) |
| `scripts/*.py/.sh` | 48 | Pre/PostToolUse + Stop хуки — блокируют деструктивные действия, enforce паттерны |
| `templates/` | 6 | Стартовые файлы для новых проектов (CLAUDE_BASE, MEMORY_TEMPLATE, hookify...) |

## Как работает

```
Задача получена
     │
     ├─ читаем CLAUDE.md роутер
     ├─ загружаем нужный модуль rules/
     ├─ простой поиск → Haiku субагент (~70% экономии токенов)
     └─ хуки enforce правила автоматически:
           logo/ assets/  →  блок
           rm -rf / push -f main  →  блок
           --no-verify / reset --hard  →  предупреждение
           новое правило без хука  →  стоп
```

## Быстрый старт

```bash
# 1. Клонировать
git clone https://github.com/YOUR_GITHUB_USERNAME/potap-claude-setup ~/.claude/claude-setup

# 2. Скопировать нужные файлы
cp -r ~/.claude/claude-setup/rules/* ~/.claude/rules/
cp -r ~/.claude/claude-setup/agents/* ~/.claude/agents/
cp -r ~/.claude/claude-setup/skills/* ~/.claude/skills/
cp -r ~/.claude/claude-setup/scripts/* ~/.claude/scripts/

# 3. Отредактировать личные данные в rules/communication.md, rules/workflow_universal.md
#    Заменить [YOUR_NAME], YOUR_GITHUB_USERNAME, @YOUR_CHANNEL на свои значения
```

## Ключевые правила

| Файл | Что делает |
|---|---|
| `rules/haiku-economy.md` | Когда Haiku vs Sonnet vs Opus — полная таблица маршрутизации |
| `rules/communication.md` | Тон, псевдографика по умолчанию, личные мемы |
| `rules/workflow_universal.md` | Цикл деплоя, патчноты, анонс в Telegram, GitHub API |
| `rules/lessons_universal.md` | Накопленные грабли: PS, C#, Telegram Bot API, GitHub |
| `rules/windows_dev.md` | WinForms тёмная тема, паттерны PS-установщика |
| `rules/vibe_coding.md` | Концепция: человеческий язык → изменение параметров |

## Ключевые хуки

| Скрипт | Тип | Блокирует/предупреждает |
|---|---|---|
| `pretool-safety.py` | PreToolUse | `rm -rf`, `push --force main`, `reset --hard` |
| `token-leak-check.py` | PreToolUse | Захардкоженные токены перед Write |
| `new-rule-check.py` | Stop | Новое правило без сопровождающего хука |
| `plan-mode-check.py` | Stop | Многошаговый план без входа в Plan Mode |
| `html-monolith-check.py` | PreToolUse | `<style>`/`<script>` внутри HTML (трата токенов) |
| `haiku-suggest.py` | UPS | Инжектирует `[HAIKU_ELIGIBLE]` / `[OPUS_ELIGIBLE]` подсказки |

## Структура rules/

```
├─ communication.md      тон/стиль общения, мемы
├─ workflow_universal.md деплой → патчнот → коммит → анонс
├─ haiku-economy.md      когда Haiku / Sonnet / Opus — полный роутер
├─ token-budget.md       управление Pro лимитом, compact стратегии
├─ github_ops.md         GitHub API без gh CLI (чистый PowerShell)
├─ github_formatting.md  README, бейджи, topics, оформление репо
├─ bilingual.md          EN+RU README через <details> секции
├─ lessons_universal.md  PS / C# / TG / GitHub — накопленные ловушки
├─ windows_dev.md        WinForms тёмная тема, PS installer
├─ telegraph.md          публикация Telegraph статей через Python
├─ hlsl.md               HLSL шейдеры — безопасный стиль правок
├─ vibe_coding.md        вайбкодинг — концепция и паттерн
├─ preferences.md        визуал, структура файлов, BAT vs Python
├─ subagent-context.md   правила передачи контекста субагентам
├─ haiku-setup.md        чеклист инициализации Haiku в новом проекте
└─ plan-mode.md          автоматический Plan Mode для сложных задач
```

</details>
</div>
