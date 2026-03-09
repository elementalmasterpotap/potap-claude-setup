# Universal Rules
# Копия: .claude/universal-rules.md · Память: ~/.claude/memory/MEMORY.md → .claude/universal-memory.md

## Алгоритм сессии

```
ИНИТ (один раз):
  communication.md прочитан? НЕТ──► читать (БЛОКЕР — без него стоп)
  MEMORY.md прочитан?        НЕТ──► читать ──► активировать триггеры
                             ДА──► продолжать

ЗАДАЧА ПОЛУЧЕНА:
  ┌── разговор / вопрос       ──► отвечать напрямую
  ├── shaders/ + детектор     ──► lessons.md + DEVELOPMENT_RULES.md ──► [ВЫСОКИЙ РИСК]
  ├── shaders/ без детектора  ──► hlsl.md
  ├── деплой / патчнот        ──► workflow.md · workflow_universal.md
  ├── вайбкодинг              ──► VIBE.md + hlsl.md · vibe_coding.md
  ├── GitHub / релиз / API    ──► github_ops.md
  ├── GitHub оформление / README / бейджи ──► github_formatting.md
  ├── Telegram / бот / пост   ──► lessons_universal.md (TG-1..TG-3)
  ├── Telegraph / статья      ──► telegraph.md
  ├── C# / PowerShell / Windows ──► lessons_universal.md (PS-1..PS-3, CS-1..CS-3)
  ├── PS installer / WinForms тёмная тема ──► windows_dev.md
  ├── новый проект (старт с нуля) ──► [БЛОКЕР] сначала создать структуру:
  │     .claude/CLAUDE.md (по CLAUDE_BASE.md) · .claude/memory/MEMORY.md (по MEMORY_TEMPLATE.md)
  │     VIBE.md · docs/PATCHNOTES.md · tasks/lessons.md · .claudeignore — ТОЛЬКО ПОТОМ писать код
  │     ──► добавить секцию ## Haiku в .claude/CLAUDE.md (haiku-setup.md) [ОБЯЗАТЕЛЬНО]
  ├── новый веб-сайт / HTML-страница ──► html+css+js сразу, не монолит (preferences.md §Разбивка)
  ├── правило / память        ──► CLAUDE.md "Новые записи" ──► проверить дубли
  ├── токены / Pro лимит / compact ──► token-budget.md
  ├── Haiku / экономия / субагент ──► haiku-economy.md · subagent-context.md
  ├── GitHub двуязычность / EN+RU ──► bilingual.md
  └── структура / цвет        ──► preferences.md

  3+ шагов или архит. решение? ──► Plan mode (включая верификацию, не только построение)
  Параллельный анализ нужен?   ──► Subagents — один subagent, одна задача; main context чистым
  Неоднозначность?             ──► допущение в ответ, не вопрос  [→ "Неоднозначность"]
  Риск потери работы / крит.?  ──► спросить перед действием

ВЫПОЛНЕНИЕ:
  [ВЫСОКИЙ РИСК]?      ──► озвучить план и допущения явно перед правкой
  Заблокирован?        ──► паттерн в коде ──► docs/ ──► альтернатива  [→ "Блокировка"]
  План пошёл не так?   ──► СТОП ──► перепланировать немедленно, не толкать дальше

ПОСЛЕ ЗАДАЧИ:
  поломка / урок?          ДА──► tasks/lessons.md
  новый паттерн Потапа?    ДА──► MEMORY.md
  визуальное изменение?    ДА──► docs/PATCHNOTES.md
  новое правило?           ДА──► карта владения ──► проверить дубли
  добавлена/удалена/изм. глоб. кастомизация? ДА──► сверить лонгрид с реальным состоянием:
    settings.json (deny/mcpServers/hooks/plugins/alwaysThinking) · rules/ · agents/ · templates/ · skills/
    ──► обновить контент telegraph_content.py ──► синхронизировать через /sync или явный запрос
    ──► скрипт пушит и в GitHub (github.com/YOUR_GITHUB_USERNAME/potap-claude-setup) — только по /sync
    Кастомизация = rules/ · scripts/ · agents/ · templates/ · skills/ · settings.json · CLAUDE.md · MEMORY.md
  изменён CLAUDE/MEMORY?   ДА──► синхронизировать копии в проекте
  готово?                  ──► доказать что работает перед отметкой выполненным
```

## Блокировка → не стоп
1. Паттерн в коде  2. `docs/` / история решений  3. Альтернативный подход · допущения → в ответ.

## Сеть / VPN (Россия)
Любая сетевая ошибка → **включить VPN, потом повторить** (не ретраить без VPN).
Блокировки: anthropic.com · npmjs.com · github.com (иногда). Stop hook: `network-vpn-warn.py`.

## Деплой
NoPrompt/--yes · ширина консоли `powershell -c '$Host.UI.RawUI.WindowSize.Width'` ≥80=ПК <80=молча.

## Permissions
`src/` `shaders/` `lib/` — свободно · `docs/` `README` — дополнять, не переписывать · `CI` `infra/` `*.yml` — спрашивать · `logo/` `assets/` — не трогать
Enforcement через hookify: `logo/` `assets/` → block · `CI/` `infra/` `*.yml` → warn · `rm -rf` / `push -f main` → block · `--no-verify` / `reset --hard` → warn
Шаблоны для новых проектов: `templates/hookify/` (6 файлов, скопировать в `.claude/`)

## Commits
`type(scope): description` · feat/fix/refactor/docs/style/chore · не амендить опубликованные

## Pre-push аудит (ОБЯЗАТЕЛЬНО перед любым git push)
```
grep -rn "ghp_[A-Za-z0-9]\{36\}\|[0-9]\{10\}:AA[A-Za-z0-9_-]\{33\}\|475c06[a-f0-9]\{50\}\|edit\.telegra\.ph/auth" \
  . --include="*.py" --include="*.md" --include="*.json" --include="*.ps1" | grep -v ".git/"
```
Плейсхолдеры (XXXX, your_token, $TOKEN) — ок. Реальные значения — СТОП, не пушить.

## Принципы
Минимальный импакт · root cause не симптом · трогать только нужное · не хакать · не дублировать
Нетривиальная правка → спросить себя "есть более элегантный путь?" перед отправкой · объяснять изменения кратко на каждом шаге
Баг-репорт → фиксить автономно, без запроса доп. контекста у пользователя

## Версии зависимостей — всегда latest/next
npm→@next · pip→без ==X.Y.Z · Claude Code→@next (auto-update.sh) · Плагины→claude plugin update
Фиксировать только при явном обосновании совместимости. Stop hook: version-check.py

## Предпочтения (визуал / UX)
Цвет: насыщенные, живые — склоняться к большей насыщенности, не зажимать без причины (артефакт, клиппинг)
UI: тёмная тема по умолчанию для Windows приложений · псевдографика ВЕЗДЕ как дефолт (Stop hook enforce)
Документация: неформально, мат ок, от первого лица — не корпоративно

## Новые записи (правила и память) — воркфлоу
Читать цель → читать смежные (карта ниже) → дубль? ссылка : писать сжато
После изменения `CLAUDE.md` / `MEMORY.md` → синхронизировать копии в проекте

## Новое правило → обязательный комплект [БЛОКЕР]
Каждое новое правило требует ТРЁХ артефактов. Без хука — правило не считается созданным:
```
правило (rules/*.md или CLAUDE.md)
  ├── Stop/PreToolUse/PostToolUse/UPS хук (scripts/*.py)
  │   ОБЯЗАТЕЛЬНО — создать хук и зарегистрировать в settings.json
  │   Нет машинного паттерна? → Stop хук на текст ответа (last_assistant_message)
  │   Нет вообще варианта?   → написать в комментарии ПОЧЕМУ + предложить альтернативу
  │   НЕВОЗМОЖНО без причины — не принимается
  └── Skill (skills/*/SKILL.md) — action или knowledge (user-invocable: false)
      Нет ручного invoke? → user-invocable: false (knowledge скилл)
```
Порядок создания: 1) правило → 2) скрипт хука → 3) settings.json → 4) skill
После: синхронизировать через `/sync` скилл (Telegraph + GitHub + Telegram за один запуск).

Карта правил:
`communication.md` стиль/тон · `MEMORY.md` характер/паттерны · `workflow_universal.md` деплой/патчнот
`github_ops.md` API · `github_formatting.md` README/бейджи · `bilingual.md` EN+RU
`lessons_universal.md` TG/PS/CS ловушки · `windows_dev.md` installer/WinForms · `telegraph.md` статьи
`haiku-economy.md` токены/модели · `haiku-setup.md` новый проект+Haiku · `plan-mode.md` Plan Mode
`subagent-context.md` субагенты · `hlsl.md` шейдеры · `preferences.md` структура/цвет
`vibe_coding.md` вайбкод · `templates/` шаблоны · `templates/hookify/` hookify-шаблоны
скиллы → `~/.claude/skills/<name>/SKILL.md` · проектное → `.claude/CLAUDE.md`

Карта памяти (`MEMORY.md`): паттерны Потапа · практические инсайты · мемы
НЕ писать: стиль/тон → `communication.md` · workflow → `CLAUDE.md`
