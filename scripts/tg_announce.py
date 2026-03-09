"""
Universal Telegram announcement sender.
~/.claude/scripts/tg_announce.py

Usage:
    python ~/.claude/scripts/tg_announce.py --text "post text" [--chat @YOUR_CHANNEL]

Or import:
    from tg_announce import send_post
    send_post("text with <b>html</b>")

- Always uses TG_BOT_TOKEN from settings.json
- Default channel: @YOUR_CHANNEL
- parse_mode: HTML (safer than Markdown for special chars)
- Returns message_id for future edits
"""

import argparse, json, os, sys, urllib.request

DEFAULT_CHAT = '@YOUR_CHANNEL'

def get_token():
    settings = os.path.expanduser('~/.claude/settings.json')
    return json.load(open(settings))['env']['TG_BOT_TOKEN']

def send_post(text, chat=DEFAULT_CHAT, preview=True):
    """Send HTML-formatted message. Returns message_id."""
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
        print(f'[TG] Sent to {chat}, message_id={msg_id}')
        return msg_id
    except urllib.error.HTTPError as e:
        err = json.loads(e.read())
        print(f'[TG] ERROR {e.code}: {err}')
        return None

def edit_post(message_id, text, chat=DEFAULT_CHAT):
    """Edit existing message by id."""
    token = get_token()
    data = json.dumps({
        'chat_id': chat,
        'message_id': message_id,
        'text': text,
        'parse_mode': 'HTML',
    }).encode('utf-8')
    req = urllib.request.Request(
        f'https://api.telegram.org/bot{token}/editMessageText',
        data=data,
        headers={'Content-Type': 'application/json; charset=utf-8'}
    )
    try:
        r = json.loads(urllib.request.urlopen(req, timeout=15).read())
        print(f'[TG] Edited message_id={message_id}')
        return True
    except urllib.error.HTTPError as e:
        err = json.loads(e.read())
        print(f'[TG] Edit ERROR {e.code}: {err}')
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--text', required=True)
    parser.add_argument('--chat', default=DEFAULT_CHAT)
    parser.add_argument('--no-preview', action='store_true')
    args = parser.parse_args()
    send_post(args.text, args.chat, preview=not args.no_preview)
