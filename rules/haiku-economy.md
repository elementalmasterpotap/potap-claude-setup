# Haiku Economy — ультимативный пак экономии токенов

<!-- Stop hook: НЕВОЗМОЖНО — haiku-suggest.py уже покрывает UPS инжекцию -->
<!-- Skill: haiku-router/SKILL.md покрывает knowledge-routing -->

## Принцип — три уровня

```
Задача получена → оценить complexity
       │
       ├─ complexity LOW   → [HAIKU_ELIGIBLE]  → Haiku субагент (codebase-explorer)
       ├─ complexity MED   → Sonnet (default)
       ├─ complexity HIGH  → Sonnet + thinking (12K budget)
       └─ complexity CRIT  → [OPUS_ELIGIBLE]   → предложить переключить модель на Opus
```

`haiku-suggest.py` инжектирует `[HAIKU_ELIGIBLE]` и `[OPUS_ELIGIBLE]` автоматически через UPS хук.

**Формула выбора:**
```
Только читает, нет правок?         → Haiku субагент
Меняет файлы, обычная сложность?   → Sonnet
Архитектура / критический баг?     → Opus (предложить переключить)
Смешанная (найди + исправь)?       → Sonnet
Безопасность / аудит?              → Opus
```

---

## Opus — когда переключать

Opus = самая мощная модель. Жрёт Pro лимит больше Sonnet, но там где нужно — Sonnet не справится.

### Таблица: Opus vs Sonnet vs Haiku

| Задача | Модель | Почему |
|--------|--------|--------|
| Архитектура проекта с нуля | **Opus** | нужна глубина рассуждения |
| Критический баг в production | **Opus** | root cause analysis |
| Security audit кодовой базы | **Opus** | находит неочевидные уязвимости |
| Memory leak / deadlock / race condition | **Opus** | сложная причинно-следственная цепочка |
| Рефакторинг всего проекта | **Opus** | координация многих файлов + план |
| Сложный алгоритм (граф, DP, оптимизация) | **Opus** | математическая точность |
| Дизайн системы (system design) | **Opus** | trade-offs нужна экспертиза |
| "Почему это не работает" (непонятный баг) | **Opus** | deep reasoning |
| Написать новую фичу | **Sonnet** | стандартная задача |
| Исправить конкретный баг | **Sonnet** | понятная задача |
| Multi-file рефакторинг (локальный) | **Sonnet** | координация без глубины |
| Найти файлы / структуру | **Haiku** | read-only |
| Code review поверхностный | **Haiku** | анализ без правок |

### Явные триггеры [OPUS_ELIGIBLE]

```
· "архитектура всего проекта"
· "критический баг" / "production bug"
· "аудит безопасности" / "security audit"
· "memory leak" / "утечка памяти"
· "deadlock" / "дедлок" / "race condition"
· "рефакторинг проекта" (весь проект, не один файл)
· "дизайн системы" / "system design"
· "почему не работает" + непонятная ошибка
· "лучший способ" для критичной инфраструктуры
· "оптимизация алгоритма" + O-нотация
```

### Как переключить модель

```bash
# В Claude Code — через меню:
Esc → выбрать модель → claude-opus-4-6

# Вернуть Sonnet после задачи:
Esc → claude-sonnet-4-6

# Или через /model команду:
/model claude-opus-4-6
/model claude-sonnet-4-6
/model claude-haiku-4-5-20251001  # если нужен Haiku напрямую
```

Effort для каждого режима:
```
Haiku субагент  → effort: low   (экономия, subagents)
Sonnet обычный  → effort: medium (баланс)
Sonnet сложный  → effort: high   (max Sonnet)
Opus обычный    → effort: high   (deep reasoning)
Opus критичный  → effort: max    (ТОЛЬКО Opus, deepest possible)
```

**Правило:** Opus для одной сложной задачи → вернуть Sonnet после.
Не держать Opus постоянно — лимит сгорит быстро.

### Как Claude сигнализирует [OPUS_ELIGIBLE]

Когда `haiku-suggest.py` определяет Opus-задачу — инжектирует подсказку.
Claude ОБЯЗАН написать в начале ответа:

```
💡 [OPUS_ELIGIBLE] — задача лучше решается на Opus.
   Переключить? Esc → Model → claude-opus-4-6
   Продолжаю на Sonnet если не переключишь.
```

Если пользователь остаётся на Sonnet → решать максимально тщательно с thinking.

---

---

## Расширенная таблица: Haiku vs Sonnet

| Задача | Модель | Почему |
|--------|--------|--------|
| Найти файл / grep по коду | **Haiku** | read-only, простой поиск |
| Перечислить структуру директорий | **Haiku** | ls + tree |
| Прочитать и суммаризировать файл | **Haiku** | один файл, нет правок |
| Проверить синтаксис / lint | **Haiku** | только анализ |
| Поверхностный code review | **Haiku** | читает, не меняет |
| Найти все вызовы функции | **Haiku** | grep паттерн |
| Найти все импорты / зависимости | **Haiku** | grep/glob |
| Посчитать строки / файлы / функции | **Haiku** | wc + анализ |
| Сравнить два файла (diff) | **Haiku** | только чтение обоих |
| Показать git log / diff | **Haiku** | read-only git |
| Найти дубли / мёртвый код | **Haiku** | grep + анализ |
| Прочитать PATCHNOTES / README | **Haiku** | один файл |
| Проверить есть ли X в конфиге | **Haiku** | grep в файле |
| Описать архитектуру проекта | **Haiku** | только читает |
| Показать все env переменные | **Haiku** | grep по файлам |
| Написать новую фичу | **Sonnet** | Edit/Write нужен |
| Архитектурное решение | **Sonnet** | рассуждение + правка |
| Multi-file рефакторинг | **Sonnet** | координация изменений |
| Отладка сложного бага | **Sonnet** | причинно-следственный анализ |
| Работа с шейдером/детектором | **Sonnet** | высокий риск поломки |
| Найди И исправь | **Sonnet** | смешанная задача |
| Настройка CI/CD / инфра | **Sonnet** | сложные изменения |
| Написать патчнот / документацию | **Sonnet** | генерация текста с контекстом |
| Debugging с воспроизведением | **Sonnet** | может требовать правок |
| Установить зависимости / сборка | **Sonnet** | bash + проверка результата |

---

## Routing правило (когда предлагать переключение)

При получении задачи из колонки "Haiku" — предложить:
```
💡 Эта задача [HAIKU_ELIGIBLE] — хочешь запустить через Haiku субагент?
   Экономит ~70% токенов для этого типа задач.
   [y/n или просто продолжаю на Sonnet]
```

Если пользователь согласился — запомнить в MEMORY.md:
```
### Предпочтения Haiku
- [тип задачи] → Haiku (выбор 2026-XX-XX)
```

---

## Советы для веб-разработки (экономия токенов)

### Разбивка файлов
```
МОНОЛИТ (плохо):         РАЗБИВКА (хорошо):
index.html (2000 строк)  index.html   (~50 строк)
                         css/style.css (~400 строк)
                         js/main.js   (~300 строк)

При правке CSS: читаем только style.css (400 строк)
vs монолит: читаем всё (2000 строк) → 5× токенов лишних
```

Правило: `html-monolith-check.py` Stop хук уже блокирует монолиты.

### CSS-first подход
```
Менять цвета/отступы/анимации → ТОЛЬКО css/style.css
Не читать index.html и main.js при стилевых правках
```

### Шаблонная компонентизация
```python
# Плохо: читать весь файл ради одного компонента
# Хорошо: структурировать компоненты в отдельные файлы
components/
  header.html   # читается только при правке шапки
  footer.html   # читается только при правке футера
  nav.html
```

---

## Советы для Telegram-ботов (экономия токенов)

### Структура проекта
```
bot/
  main.py        # точка входа, только handlers
  handlers/
    commands.py  # /start, /help и т.д.
    messages.py  # обработка сообщений
    callbacks.py # inline keyboard callbacks
  utils/
    telegram.py  # send_message, send_photo обёртки
    formatting.py # текст, escape, parse_mode
  config.py      # только константы и env vars
```
При правке конкретного хендлера → читаем только 1 файл.

### Кэширование контекста в боте
```python
# Кэшировать тяжёлые запросы к API
from functools import lru_cache

@lru_cache(maxsize=128, typed=False)
def get_user_data(user_id: int) -> dict:
    return db.fetch_user(user_id)

# TTL-кэш для временных данных
import time
_cache = {}
def get_cached(key, ttl=300):
    if key in _cache and time.time() - _cache[key]['ts'] < ttl:
        return _cache[key]['val']
    return None
```

### Порог разбивки bot.py (критично!)

```
bot.py > ~300 строк → монолит выпадает из контекста после compaction
```

Симптом: система пишет "contents are too large to include. Use Read tool if you need to access it."
Это означает: при каждой правке придётся читать файл целиком = сотни токенов каждый раз.

**Решение — разбивать ДО достижения порога:**
```
bot/
  main.py         # только Application.run() + on_startup
  handlers.py     # команды (/start, /track, /cancel)
  callbacks.py    # inline keyboard callbacks
  monitor.py      # check_tx_job, get_confirmations, API calls
  persistence.py  # save/load tracking.json + history.json
  config.py       # токены, ноды, константы
```
При правке monitor.py → читаем только monitor.py (~100 строк), не 400+.

---

## Советы для Windows desktop tools (WinForms + Python)

### Изоляция GUI от логики

```
project/
  src/
    menu_gui.cs    ← ТОЛЬКО WinForms код
  build.py         ← запуск csc.exe, 15 строк
  bot.py / *.py   ← логика приложения
```

При правке бота → src/ не читается вообще.
При правке GUI → bot.py не читается вообще.
Экономия: изолированный src/ = читаем 1 файл из 3-4.

### Read с offset/limit для точечных правок

Вместо чтения всего файла — читать только нужный участок:
```python
# Плохо: Read("bot.py") → 400 строк в контекст
# Хорошо: Read("bot.py", offset=180, limit=25) → только нужная функция
```

Workflow:
1. `Grep("def on_callback", "bot.py")` → находим строку функции
2. `Read("bot.py", offset=<line-5>, limit=40)` → читаем только её
3. `Edit` → правим

Экономия: 10-20× меньше токенов при точечных правках в больших файлах.

### Windows service management — один файл = одна задача

```
install_service.ps1    ← Register-ScheduledTask
uninstall_service.ps1  ← Unregister-ScheduledTask
start.py               ← pythonw + проверка запуска
stop.py                ← kill по имени процесса
setup.py               ← pip install requirements
```

Каждый файл < 50 строк → читается быстро, правится точечно.
НЕ объединять install+uninstall в один файл с флагами.

---

## Кэширование токенов (Prompt Caching)

### Claude API — prompt caching
```python
# При повторяющихся длинных системных промптах
# использовать cache_control для экономии

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": длинный_системный_контекст,
                "cache_control": {"type": "ephemeral"}  # кэш на 5 минут
            },
            {"type": "text", "text": конкретный_вопрос}
        ]
    }
]
```

### Паттерны кэширования контекста
```
Длинный системный промпт → cache_control ephemeral → -90% токенов при повторе
RAG документы → один раз загрузить с кэшем → повторные запросы дёшевы
Few-shot примеры → кэшировать статичную часть → только запрос меняется
```

### Когда кэш не работает
```
· Динамические промпты (каждый раз разные) → не кэшируются
· Мелкие промпты (<1024 токенов) → overhead кэша > экономия
· Модели без поддержки caching → только claude-3.x+
```

---

## Ультимативный пак: когда токены кончаются

```
1. /compact-smart    → сжать сессию с умными инструкциями
2. /clear            → сбросить если задача сменилась
3. Субагент          → verbose операции в субагент (output там, не здесь)
4. .claudeignore     → исключить node_modules, lock файлы
5. /mcp              → отключить неиспользуемые MCP серверы
6. Haiku субагент    → для поиска/анализа (70% дешевле)
7. Разбить задачу    → на независимые подзадачи, очищать контекст между ними
```

---

## Модели — официальные ID и цены

```
Модель               API ID                          Цена (in/out MTok)  Множитель
─────────────────────────────────────────────────────────────────────────────────
Claude Haiku 4.5     claude-haiku-4-5-20251001       $1 / $5             1× (база)
Claude Sonnet 4.6    claude-sonnet-4-6               $3 / $15            3×
Claude Opus 4.6      claude-opus-4-6                 $5 / $25            5×
```

Haiku 4.5 официально: "near-frontier intelligence, fastest model" — не дешёвая игрушка.
Anthropic рекомендует Haiku для: "real-time apps, high-volume, sub-agent tasks, cost-sensitive with strong reasoning".

---

## Effort levels — официальный API параметр (источник: Anthropic docs)

```
Уровень   Описание                              Типичные задачи
──────────────────────────────────────────────────────────────────────
max       Максимум без ограничений              Только Opus 4.6! Deepest reasoning
high      Высокая мощность (default Sonnet 4.6) Complex reasoning, agentic coding
medium    Баланс скорость/качество              Agentic tasks, tool-heavy workflows
low       Максимальная экономия                 Subagents, chat, простые задачи
```

**Anthropic рекомендации для Sonnet 4.6:**
- `medium` — лучший баланс для большинства задач, agentic coding, генерация кода
- `low` — high-volume, latency-sensitive, chat и non-coding
- `high` — максимальная интеллигентность Sonnet когда реально нужна

**Haiku субагент → effort: low** (официальная рекомендация для subagents)
**Opus → effort: max** для deepest reasoning (уникальная опция только Opus 4.6)

Effort = поведенческий сигнал, не жёсткий бюджет. Haiku думает меньше при low, но всё ещё думает если задача требует.

---

## Adaptive thinking (Opus 4.6)

Opus 4.6 использует adaptive thinking — сам решает когда и сколько думать.
При `high`/`max` effort — почти всегда думает глубоко.
`budget_tokens` для Opus 4.6 **deprecated** — использовать `effort` вместо него.

Если Opus думает слишком долго → добавить в промпт:
```
"Choose an approach and commit to it. Avoid revisiting decisions unless
 you encounter new information. Pick one approach and see it through."
```

---

## Claude Pro — лимиты из практики

```
Окно:      rolling 5 часов от первого сообщения
Сброс:     не в полночь — через 5 часов после ПЕРВОГО сообщения
Лимит:     ~45 сообщений / окно (зависит от размера контекста)
Thinking:  MAX_THINKING_TOKENS=12000 (не 32K) — экономит бюджет
Sonnet:    жрёт лимит × 1.0
Haiku sub: жрёт лимит значительно меньше
MCP idle:  Linear MCP ~14 000 токенов даже не используемый

Тактика 3 окна в день:
  07:00 → первое сообщение (открывает окно)
  07:00–12:00 → окно 1 (тяжёлые задачи)
  12:00–17:00 → окно 2 (продолжение)
  17:00–22:00 → окно 3 (финализация)
```

**Сигналы приближения лимита:**
```
· Ответы становятся медленнее
· Появляется предупреждение о context length
· session-length-check.py срабатывает (каждые 5 длинных ответов)
→ Действие: /compact-smart НЕМЕДЛЕННО
```

---

## Pre-session чеклист (перед началом работы над проектом)

```
□ .claudeignore существует?          НЕТ → создать (шаблон ниже)
□ Главный файл > 200 строк?          ДА → план разбивки до правок
□ MCP серверы — только нужные?      НЕТ → /mcp отключить лишние
□ Thinking нужен для задачи?         НЕТ → Alt+T выключить
□ Задача read-only?                  ДА → Haiku субагент, не Sonnet
□ Verbose output ожидается?          ДА → субагент с начала
□ node_modules / .lock в проекте?   ДА → точно в .claudeignore
```

---

## Агрессивный .claudeignore — универсальный шаблон

```gitignore
# Зависимости
node_modules/
.pnp
.yarn/

# Lock файлы (огромные, не нужны Claude)
package-lock.json
yarn.lock
pnpm-lock.yaml
poetry.lock
Pipfile.lock
composer.lock
Gemfile.lock
cargo.lock

# Сборка
dist/
build/
out/
.next/
.nuxt/
__pycache__/
*.pyc
*.pyo
.pytest_cache/
*.egg-info/
.venv/
venv/
env/

# IDE
.vscode/
.idea/
*.suo
*.user

# OS
.DS_Store
Thumbs.db
desktop.ini

# Логи
*.log
logs/

# Бинарники
*.exe
*.dll
*.so
*.dylib
*.zip
*.7z
*.rar
*.tar.gz

# Медиа (если не нужны)
# *.png
# *.jpg
# assets/

# Временные
*.tmp
*.bak
*.swp
*~
.cache/

# Claude локальное
.claude/settings.local.json
```

Глобальный шаблон: `~/.claude/templates/.claudeignore`

---

## Claude setup — оптимизация ~/.claude/ самого по себе

Сам сетап Клода может жрать токены если не оптимизировать:

```
Файл                    Лимит     Статус
──────────────────────────────────────────────────────
CLAUDE.md               < 150 строк   (выполнено)
rules/*.md              каждый < 200 строк
memory/MEMORY.md        < 200 строк (truncated >200)
agents/*.md             читаются при Task() — держать сжатыми
skills/*/SKILL.md       lazy-load, не в контексте постоянно
telegraph_content.py    ~41KB — НЕ читать без нужды
update_telegraph.py     только при синхронизации
```

**Правило для новых rules/*.md:**
```
Новое правило → проверить размер: cat rules/new.md | wc -l
> 150 строк → разбить: детали в rules/sub/*.md, суть в rules/new.md
```

**Что НЕ загружается в контекст автоматически (экономия):**
```
skills/*/SKILL.md       → только при вызове скилла
agents/*.md             → только при Task()
templates/              → только когда явно читаются
scripts/*.py            → никогда (хуки, не контекст)
telegraph_content.py    → только при /sync
```

---

## Шаблоны модульных структур по типу проекта

### Python Telegram Bot

```
bot/
  main.py          < 50 строк   # Application.run() + регистрация
  handlers.py      < 150 строк  # /start, /help, основные команды
  callbacks.py     < 150 строк  # inline keyboard callbacks
  monitor.py       < 150 строк  # фоновые задачи, API calls
  persistence.py   < 100 строк  # save/load JSON
  config.py        < 50 строк   # токены, константы, env
  utils.py         < 100 строк  # форматирование, хелперы

Правило: каждый файл < 150 строк
При правке monitor.py → читаем только monitor.py
```

### Python CLI / утилита

```
src/
  main.py          < 50 строк   # точка входа, argparse
  core.py          < 200 строк  # основная логика
  cli.py           < 100 строк  # CLI интерфейс / меню
  config.py        < 50 строк   # константы
  utils.py         < 100 строк  # хелперы
menu.bat           < 30 строк   # только запуск python-скриптов
```

### C# WinForms

```
src/
  MainForm.cs      < 200 строк  # только UI инициализация, события
  Logic.cs         < 200 строк  # бизнес-логика
  Config.cs        < 50 строк   # константы, настройки
  Utils.cs         < 100 строк  # хелперы
build.py           < 30 строк   # запуск csc.exe
install.ps1        < 100 строк  # установщик

При правке Logic.cs → MainForm.cs не читается
```

### Web (HTML/CSS/JS)

```
index.html         < 60 строк   # только разметка, нет <style>/<script>
css/
  style.css        < 400 строк  # все стили
  animations.css   < 100 строк  # анимации отдельно если > 50 строк
js/
  main.js          < 300 строк  # логика
  api.js           < 150 строк  # API calls отдельно

При правке CSS → читаем только style.css (400 строк vs 2000 монолит)
```

### PowerShell scripts / сетап

```
setup.py           # pip install зависимостей
start.py           # запуск приложения
stop.py            # остановка
start_debug.py     # режим отладки
install.ps1        < 150 строк  # установщик (если сложный → разбить)
functions/
  ui.ps1           # box-drawing, меню
  install.ps1      # логика установки
  backup.ps1       # создание бэкапов
menu.bat           < 20 строк   # только точка входа
```

### HLSL шейдер

```
shaders/
  main.hlsl        # основной шейдер
  detector.hlsl    # детектор (НЕ ТРОГАТЬ без явного запроса)
docs/
  DEVELOPMENT_RULES.md  # что заморожено, что можно
  PATCHNOTES.md
install.ps1        # деплой
```

---

## Haiku субагент — copy-paste шаблоны вызова

```python
# Поиск файлов
Agent(
    subagent_type='codebase-explorer',
    prompt='Найди все файлы с функцией send_message в src/. Верни список путей.'
)

# Анализ структуры
Agent(
    subagent_type='codebase-explorer',
    prompt='Покажи структуру проекта в src/. Дерево файлов с количеством строк.'
)

# Code review
Agent(
    subagent_type='code-reviewer',
    prompt='Проверь handlers.py на антипаттерны и потенциальные баги.'
)

# Grep + суммаризация
Agent(
    subagent_type='codebase-explorer',
    prompt='Найди все вызовы db.execute() в проекте. Список файлов и строк.'
)
```

**Правило возврата:** субагент → summary (1-2 строки в main context), verbose остаётся там.

---

## Opus Reasoner агент

Для задач из колонки "Opus" — агент `opus-reasoner` (`~/.claude/agents/opus-reasoner.md`):

```python
# Root cause анализ
Agent(
    subagent_type='opus-reasoner',
    prompt='Разберись почему handler.py крашит при concurrent requests. Root cause + решение.'
)

# Security audit
Agent(
    subagent_type='opus-reasoner',
    prompt='Security audit auth.py — SQL injection, path traversal, insecure defaults.'
)

# Архитектурное решение
Agent(
    subagent_type='opus-reasoner',
    prompt='Как правильно разбить bot.py (400 строк) на модули? Trade-offs каждого варианта.'
)
```

**Правило:** Opus агент дороже в 5× → использовать только при `[OPUS_ELIGIBLE]` или явном запросе.

---

## Agent-based хуки (продвинутый паттерн)

Claude Code поддерживает `type: "agent"` хуки — субагент с инструментами (Grep/Read/Glob):

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write",
      "hooks": [{
        "type": "agent",
        "prompt": "Файл который пишется: {{tool_input.file_path}}. Проверь что он не нарушает правила: нет hardcoded токенов, размер <150 строк. Если нарушает — block с причиной.",
        "model": "claude-haiku-4-5-20251001"
      }]
    }]
  }
}
```

**Когда agent-хук лучше command-хука:**
```
command (python скрипт) → простые regex проверки, быстро, всегда точно
agent               → нужно понимание контекста кода, читать файлы, complex logic
```

**Паттерн prompt-хука** (LLM-оценка в Stop):
```json
{
  "type": "prompt",
  "prompt": "Проверь последний ответ: Claude создал правило без хука? Если да — exit 2 с объяснением."
}
```

→ Дороже command-хука, но ловит то что regex не поймает. Использовать для сложных проверок.

---

## Трекинг выбора Haiku

После того как пользователь выбрал Haiku для конкретного типа задач → записать в MEMORY.md:
```markdown
### Haiku preferences (подтверждённые пользователем)
- поиск файлов → Haiku ✅
- code review → Haiku ✅
- [добавлять по мере выборов]
```
