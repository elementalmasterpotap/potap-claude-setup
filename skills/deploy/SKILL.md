---
name: deploy
description: Деплой проекта на GitHub + анонс в Telegram. Запускает deploy_github.py + tg_post_project.py для текущего проекта. Требует deploy.json и post.json в корне проекта.
disable-model-invocation: true
argument-hint: [--dir <path>]
---

# /deploy — Деплой проекта

Запускает полный цикл: GitHub + Telegram за один вызов.

## Требования

В корне проекта должны быть:
- `deploy.json` — параметры GitHub репо (repo, description, topics, tag, files...)
- `post.json` — параметры Telegram поста (emoji, title, features, github...)

Шаблоны: `~/.claude/rules/workflow_universal.md` раздел "GitHub деплой" и "Telegram анонс".

## Алгоритм

```
1. Проверить наличие deploy.json и post.json
2. Если deploy.json есть → запустить deploy_github.py
   python ~/.claude/scripts/deploy_github.py --config deploy.json
3. Если post.json есть → запустить tg_post_project.py
   python ~/.claude/scripts/tg_post_project.py --config post.json
4. Показать итог: ссылка на репо + message_id поста
```

## Если файлов нет

```
deploy.json не найден → создать по шаблону из workflow_universal.md, заполнить вместе с пользователем
post.json не найден   → создать по шаблону, заполнить вместе с пользователем
```

## Кастомизация под проект

Оба файла в `.gitignore` — не пушатся.
Переписывать скрипты (`deploy_github.py`, `tg_post_project.py`) НЕ нужно — только данные в JSON.
Исключение: нестандартный пост (медиа, кнопки) → использовать `tg_announce.py` напрямую.

## Быстрый старт

```bash
# Проверить что есть
ls deploy.json post.json

# Деплой
python ~/.claude/scripts/deploy_github.py --config deploy.json

# Анонс
python ~/.claude/scripts/tg_post_project.py --config post.json
```
