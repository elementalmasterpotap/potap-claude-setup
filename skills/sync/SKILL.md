---
name: sync
description: Синхронизировать кастомизации Claude — обновить Telegraph лонгрид, запушить в GitHub, обновить Telegram пост. Запускать после изменений в rules/, CLAUDE.md, settings.json, scripts/, templates/.
disable-model-invocation: true
allowed-tools: Bash
---

Синхронизируй все кастомизации Claude:

```bash
python -c "
import json, os, subprocess
s = json.load(open(os.path.expanduser('~/.claude/settings.json')))
env = dict(os.environ); env.update(s.get('env', {}))
r = subprocess.run(['python', os.path.expanduser('~/.claude/update_telegraph.py')], env=env, capture_output=True, text=True, timeout=120)
print(r.stdout)
if r.stderr: print(r.stderr)
"
```

> Токены инжектируются из settings.json (TELEGRAPH_TOKEN, GITHUB_TOKEN, TG_BOT_TOKEN).
> Если таймаут — **включи VPN** (telegra.ph и api.github.com блокируются без него).

## Что делает скрипт:

```
update_telegraph.py
  ├── editPage    → Telegraph лонгрид (контент + дата обновления)
  ├── git push    → GitHub potap-claude-setup (rules/, CLAUDE.md, scripts/, templates/)
  └── editMessage → Telegram пост #55 в @YOUR_CHANNEL (дата + ссылки)
```

После запуска — покажи результат:
- URL Telegraph
- GitHub: synced / no changes
- Telegram: message_id
