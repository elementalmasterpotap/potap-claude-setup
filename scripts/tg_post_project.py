"""
Universal project announcement post for Telegram @YOUR_CHANNEL.
~/.claude/scripts/tg_post_project.py

Usage:
    python ~/.claude/scripts/tg_post_project.py --config post.json

post.json schema (all fields optional except title + github):
{
    "emoji":      "🟠",
    "title":      "My Project",
    "tagline":    "One line — what it does",
    "body":       "2-3 lines of context. What it solves.",
    "features": [
        "feature 1",
        "feature 2",
        "feature 3"
    ],
    "github":     "https://github.com/user/repo",
    "chat":       "@YOUR_CHANNEL",
    "preview":    true
}

Generated HTML template:

    <b>{emoji} {title}</b>

    {tagline}

    {body}

    <b>Фишки:</b>
    — feature 1
    — feature 2

    → <a href="{github}">{github_short}</a>
"""

import argparse, json, os, sys, urllib.request, urllib.error

DEFAULT_CHAT = '@YOUR_CHANNEL'

def get_token():
    settings = os.path.expanduser('~/.claude/settings.json')
    return json.load(open(settings))['env']['TG_BOT_TOKEN']

def build_post(cfg):
    """Build HTML post text from config dict."""
    emoji   = cfg.get('emoji', '')
    title   = cfg['title']
    tagline = cfg.get('tagline', '')
    body    = cfg.get('body', '')
    features = cfg.get('features', [])
    github   = cfg.get('github', '')
    bot_link = cfg.get('bot_link', '')  # e.g. "https://t.me/MyBot"

    lines = []

    # Header
    header = f'<b>{emoji} {title}</b>' if emoji else f'<b>{title}</b>'
    lines.append(header)
    lines.append('')

    # Tagline
    if tagline:
        lines.append(tagline)
        lines.append('')

    # Body
    if body:
        lines.append(body)
        lines.append('')

    # Features
    if features:
        lines.append('<b>Фишки:</b>')
        for f in features:
            lines.append(f'— {f}')
        lines.append('')

    # Bot link (if it's a bot project)
    if bot_link:
        bot_name = bot_link.rstrip('/').split('/')[-1]
        lines.append(f'▶ <a href="{bot_link}">Попробовать — @{bot_name}</a>')

    # GitHub link
    if github:
        short = github.replace('https://', '').replace('http://', '')
        lines.append(f'→ <a href="{github}">{short}</a>')

    return '\n'.join(lines)

def send(text, chat, preview=True):
    token = get_token()
    data = json.dumps({
        'chat_id': chat,
        'text': text,
        'parse_mode': 'HTML',
        'disable_web_page_preview': not preview,
    }).encode('utf-8')
    req = urllib.request.Request(
        f'https://api.telegram.org/bot{token}/sendMessage',
        data=data,
        headers={'Content-Type': 'application/json; charset=utf-8'}
    )
    try:
        r = json.loads(urllib.request.urlopen(req, timeout=15).read())
        msg_id = r['result']['message_id']
        print(f'[TG] Sent to {chat} — message_id={msg_id}')
        return msg_id
    except urllib.error.HTTPError as e:
        err = json.loads(e.read())
        print(f'[TG] ERROR {e.code}: {err}')
        return None

def post_project(cfg):
    text  = build_post(cfg)
    chat  = cfg.get('chat', DEFAULT_CHAT)
    preview = cfg.get('preview', True)
    print('[POST PREVIEW]\n' + '-'*40)
    print(text)
    print('-'*40)
    return send(text, chat, preview)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='post.json')
    args = parser.parse_args()

    if not os.path.exists(args.config):
        # Print example config
        example = {
            "emoji":    "🟠",
            "title":    "My Project",
            "tagline":  "One line — what it does",
            "body":     "2-3 lines of context.",
            "features": ["feature 1", "feature 2"],
            "github":   "https://github.com/user/repo"
        }
        print(f'Config not found: {args.config}')
        print('Create post.json:')
        print(json.dumps(example, ensure_ascii=False, indent=2))
        sys.exit(1)

    cfg = json.load(open(args.config, encoding='utf-8'))
    post_project(cfg)
