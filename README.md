<div align="center">

[![](https://img.shields.io/badge/11_action_skills-0099CC?style=flat-square)](skills/)
[![](https://img.shields.io/badge/14_Stop_hooks-FF6B35?style=flat-square)](scripts/)
[![](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)](update_telegraph.py)
[![](https://img.shields.io/badge/license-MIT-22AA44?style=flat-square)](LICENSE)
[![](https://img.shields.io/badge/Telegram-channel-26A5E4?style=flat-square&logo=telegram&logoColor=white)](https://t.me/potap_attic)
[![](https://img.shields.io/badge/Telegraph-longread-009999?style=flat-square)](https://telegra.ph/Kak-ya-kastomiziruyu-Claude--pravila-pamyat-i-moduli-03-07)

<br>

<details>
<summary>English</summary>

**My Claude Code customization stack — rules, memory, hooks, skills.**

Auto-synced: every time I change something, the Telegraph article and this repo update automatically via `/sync`.

## What's inside

| Component | Purpose |
|---|---|
| `CLAUDE.md` | Session algorithm, task router |
| `rules/*.md` | Domain modules (GitHub, Telegram, Windows, vibe coding, Haiku economy...) |
| `agents/*.md` | Subagent profiles (code-reviewer, codebase-explorer, shader-expert) |
| `skills/*/SKILL.md` | Slash-skills (11 action + 8 knowledge) |
| `scripts/*.py` | Stop hooks — block/warn on destructive actions (14 hooks) |
| `templates/` | Starter files for new projects |

## How it works

```
customization changed
        ↓
/sync skill → update_telegraph.py
        ↓
editPage → Telegraph article updated
git push → this repo updated
editMessage → Telegram post updated
```

## Quick start

```bash
# Telegraph sync (requires TELEGRAPH_TOKEN env)
TELEGRAPH_TOKEN=your_token python update_telegraph.py
```

Get token: `curl "https://api.telegra.ph/createAccount?short_name=YourName&author_name=YourName"`

## Full docs

[Read the longread](https://telegra.ph/Kak-ya-kastomiziruyu-Claude--pravila-pamyat-i-moduli-03-07) — everything in one place, always up to date.

</details>

<details open>
<summary>Русский</summary>

**Мой стек кастомизаций Claude Code — правила, память, хуки, скиллы.**

Авто-синхронизация: когда что-то меняется, Telegraph-статья и этот репо обновляются через `/sync`.

## Что внутри

| Компонент | Назначение |
|---|---|
| `CLAUDE.md` | Алгоритм сессии, маршрутизатор задач |
| `rules/*.md` | Модули по доменам (GitHub, Telegram, Windows, вайбкодинг, Haiku-экономия...) |
| `agents/*.md` | Профили субагентов (code-reviewer, codebase-explorer, shader-expert) |
| `skills/*/SKILL.md` | Скиллы (11 action + 8 knowledge) |
| `scripts/*.py` | Stop-хуки — блок/предупреждение при деструктивных действиях (14 хуков) |
| `templates/` | Стартовые файлы для новых проектов |

## Как работает

```
кастомизация изменена
        ↓
/sync скилл → update_telegraph.py
        ↓
editPage → Telegraph статья обновлена
git push → этот репо обновлён
editMessage → пост в Telegram обновлён
```

## Запуск

```bash
# Синхронизация (нужен TELEGRAPH_TOKEN)
TELEGRAPH_TOKEN=your_token python update_telegraph.py
```

Получить токен: `curl "https://api.telegra.ph/createAccount?short_name=YourName&author_name=YourName"`

## Полная документация

[Читать лонгрид](https://telegra.ph/Kak-ya-kastomiziruyu-Claude--pravila-pamyat-i-moduli-03-07) — всё в одном месте, всегда актуально.

</details>

</div>
