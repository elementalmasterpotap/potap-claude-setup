# Уроки — универсальные (не привязаны к домену)

Выкачано из MPC-BE Ambient Shaders. Применимо в любом проекте.

---

## PowerShell / Windows

### PS-1 — ConvertTo-Json двойное экранирование \uXXXX
**Проблема:** `@{body="текст"} | ConvertTo-Json` экранирует `\` в `\\` → `\u0427` становится `\\u0427` → GitHub/API получает буквальный текст `\u0427`.
**Решение:** сырая JSON-строка в одинарных кавычках `$body = '{"key":"value \u0427"}'` — PS не интерпретирует одинарные кавычки, `\u` попадает в JSON как есть.
**Правило:** для API с Unicode-escape — только сырые одинарные кавычки, никогда `ConvertTo-Json`.

### PS-2 — Кракозябры в консоли ≠ повреждённые данные
**Проблема:** PowerShell показывает `вЂ"` или `??` вместо кириллицы — кажется что данные испорчены.
**Причина:** консоль Windows работает в cp866/cp1251, данные UTF-8 — визуально мусор, но в памяти и на сервере всё правильно.
**Правило:** проверять результат через браузер или WebFetch, не доверять консольному выводу кириллицы.
**Фикс (если нужен читаемый вывод в окне):** два места одновременно:
```bat
:: menu.bat — первая строка после @echo off
chcp 65001 >nul
```
```powershell
# script.ps1 — после $ErrorActionPreference
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null
```
Нужно оба — только bat или только ps1 не даёт результата.

### PS-4 — BAT: скобки и кириллица в echo ломают cmd

**Проблема 1:** `echo текст (в скобках)` → cmd парсит скобки как часть синтаксиса → `'ка)' is not recognized`.
**Решение:** убрать скобки из echo полностью, или экранировать: `echo текст ^(в скобках^)`.
**Правило:** в .bat echo — никаких `(` `)` без экранирования `^`.

**Проблема 2:** кириллица в echo без установки кодировки → кракозябры или краш строки.
**Решение:** либо `chcp 65001` в начале bat файла, либо использовать только ASCII в echo.
**Правило:** если нужна кириллица в bat — `chcp 65001 >nul` первой строкой. Иначе только ASCII.

### PS-3 — inline -Command ломается на сложных скриптах
**Проблема:** длинный скрипт в `powershell.exe -Command "..."` через bash — конфликты кавычек, потеря переносов строк.
**Решение:** писать в `.ps1` файл, запускать через `powershell.exe -File script.ps1`, удалять после.
**Правило:** сложнее 2 строк — всегда через файл.

### PS-5 — python -c многострочный через bash ломается аналогично
**Проблема:** `python -c "import json\n..."` через Bash tool → bash интерпретирует строки Python как shell-команды → `bot.py: command not found`, `using: command not found`.
**Причина:** bash видит многострочную строку и выполняет каждую строку как shell-команду.
**Решение:** то же что PS-3 — писать во временный файл, запускать, удалять:
```python
# Write temp script
with open('_tmp.py', 'w') as f:
    f.write(python_code)
# Run
subprocess.run(['python', '_tmp.py'])
# или через Bash:
# python _tmp.py && rm _tmp.py
```
Или использовать Write tool → Bash `python file.py` → Bash `rm file.py`.
**Правило:** python -c сложнее 1 строки → всегда через временный файл.

---

## C# / csc.exe (.NET Framework 4.x / C# 5)

### CS-1 — Expression-bodied members не поддерживаются в C# 5
**Проблема:** `string S(string a, string b) => isRu ? a : b;` — синтаксис C# 6+, csc.exe из .NET 4.x не компилирует.
**Решение:** `string S(string a, string b) { return isRu ? a : b; }` — классический блочный синтаксис.

### CS-2 — Auto-property initializers не поддерживаются в C# 5
**Проблема:** `public Color AccentColor { get; set; } = Color.Gray;` — синтаксис C# 6+.
**Решение:** инициализировать в конструкторе: `AccentColor = Color.Gray;`

### CS-3 — csc.exe путь на Windows
```
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe
```
Компиляция WinForms:
```powershell
& $csc /target:winexe /out:"App.exe" /reference:System.Windows.Forms.dll /reference:System.Drawing.dll /reference:System.dll /optimize+ "src\App.cs"
```

---

## Telegram Bot API

### TG-4 — python-telegram-bot v22+: три ловушки

**TG-4a — ChatAction переехал в constants**
`from telegram import ChatAction` → `ImportError` в v22+.
**Решение:** `from telegram.constants import ChatAction`

**TG-4b — edit_message_text крашит callback если контент не изменился**
`BadRequest: Message is not modified` → необработанное исключение роняет весь callback handler.
**Решение:** оборачивать в try/except:
```python
async def _edit(query, text, parse_mode="Markdown", reply_markup=None):
    try:
        await query.edit_message_text(text, parse_mode=parse_mode, reply_markup=reply_markup)
    except Exception as e:
        if "not modified" not in str(e).lower():
            raise
```

**TG-4c — chat_id str vs int**
Telegram всегда даёт int, но при сохранении в JSON и чтении обратно тип может потеряться.
**Решение:** всегда `int(chat_id)` при сравнении и записи в persistence-файлы.

---

### TG-1 — Caption limit 1024 символа (Premium не помогает)
**Проблема:** фото + подпись через Bot API ограничены 1024 символами, даже если у владельца канала Telegram Premium.
**Причина:** Premium расширяет лимит для ручной отправки через приложение (до 2048), но Bot API — отдельный лимит, 1024 фиксировано.
**Решение варианты:**
- Два сообщения: `sendPhoto` (без caption или краткая) + `sendMessage` (полный текст)
- Пользователь постит вручную через приложение с Premium (2048 символов — влезает большинство постов)

### TG-2 — sendPhoto vs sendMessage
```
sendPhoto — photo + caption (≤1024)
sendMessage — только текст, но можно вставить preview картинку через URL
sendMediaGroup — несколько медиа, caption только на первый элемент
```

### TG-3 — Отправка через Bot API
```powershell
$botToken = '123456:ABC...'
$chatId   = '@channel_username'  # или числовой ID

# Текст
Invoke-RestMethod "https://api.telegram.org/bot$botToken/sendMessage" -Method POST -Body @{
    chat_id    = $chatId
    text       = $text
    parse_mode = 'Markdown'
}

# Фото из файла
$form = @{ chat_id=$chatId; parse_mode='Markdown'; caption=$caption }
Invoke-RestMethod "https://api.telegram.org/bot$botToken/sendPhoto" -Method POST `
    -Form ($form + @{ photo=Get-Item $photoPath })
```

---

## GitHub API

### GH-1 — Успешный деплой ≠ рабочий результат
Деплой/пуш/релиз могут завершиться без ошибок, но результат — не рабочий (runtime-компиляция, неверный файл, неверная ветка). Всегда проверять руками.

### GH-2 — Upload endpoint отличается от API endpoint
- API: `api.github.com/repos/.../releases`
- Upload ассетов: `uploads.github.com/repos/.../releases/{id}/assets`

### GH-3 — Release notes с кириллицей
Подробно в `rules/github_ops.md` раздел 7. Короткий вывод: сырая JSON-строка с `\uXXXX`, никакого `ConvertTo-Json`.

### GH-4 — Неправильный email в git config → чужой контрибьютор
**Проблема:** `potap@users.noreply.github.com` → GitHub резолвит на юзера `potap` (чужой аккаунт), не на `YOUR_GITHUB_USERNAME`. В Contributors репо появляется чужое имя.
**Причина:** локальный `.git/config` репо переопределяет глобальный email неправильным noreply-адресом.
**Правильный noreply-адрес Потапа:** `YOUR_GITHUB_ID+YOUR_GITHUB_USERNAME@users.noreply.github.com`
**Диагностика:** `git log --format="%an <%ae>" | sort -u` → если email не `YOUR_GITHUB_USERNAME@gmail.com` и не `YOUR_GITHUB_ID+YOUR_GITHUB_USERNAME@...` → проблема.
**Фикс существующих коммитов:**
```bash
FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch -f --env-filter '
OLD_EMAIL="potap@users.noreply.github.com"
NEW_EMAIL="YOUR_GITHUB_ID+YOUR_GITHUB_USERNAME@users.noreply.github.com"
[ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ] && export GIT_AUTHOR_EMAIL="$NEW_EMAIL"
[ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ] && export GIT_COMMITTER_EMAIL="$NEW_EMAIL"
' --tag-name-filter cat -- --branches --tags
git push --force origin main
```
**Правило при создании нового репо:** сразу проверить `git config --local user.email` — должен быть пустым (наследует глобальный) или `YOUR_GITHUB_ID+YOUR_GITHUB_USERNAME@users.noreply.github.com`.

---

## Универсальные принципы из практики

### U-1 — Не добавлять несколько рискованных изменений за раз
Если поломка — непонятно что сломало. Одно изменение → проверка → следующее.

### U-2 — Всегда иметь откат до начала правки
`cp file.backup file` — 30 секунд, но спасает часы работы.

### U-3 — "Успешно установлено" ≠ "правильно работает"
Любой install/deploy скрипт только копирует файлы. Реальная проверка — запустить и посмотреть руками.

### U-4 — Не менять сигнатуры функций без обновления всех вызовов
Один несинхронизированный вызов → ошибка компиляции/runtime → всё перестаёт работать. Проще добавить параметр по умолчанию или передавать через closure/глобальную переменную.

---

## Claude Code Хуки

### HK-1 — Stop хуки читают `last_assistant_message`, не `transcript`
**Проблема:** тестирование с `{"transcript":[{"role":"assistant","content":"..."}]}` → хук молчит, кажется что не работает.
**Причина:** Stop хуки получают плоский JSON с полем `last_assistant_message` (строка), не вложенный массив транскрипта.
**Правильная структура для теста:**
```bash
echo '{"stop_hook_active":false,"last_assistant_message":"текст ответа"}' | python3 hook.py
```
**Правило:** при написании/тестировании Stop хука всегда использовать `last_assistant_message`.

### HK-2 — `claude plugin list` зависает без TTY
**Проблема:** `claude plugin list 2>&1` в скрипте/хуке → виснет, ничего не возвращает.
**Причина:** команда ждёт интерактивного TTY.
**Решение:** в скриптах читать `enabledPlugins` из settings.json напрямую, не через CLI.
