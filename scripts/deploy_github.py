"""
Universal GitHub deploy script.
~/.claude/scripts/deploy_github.py

Usage (from project root):
    python ~/.claude/scripts/deploy_github.py --config deploy.json

Or import and call deploy() with params dict.

deploy.json example:
{
    "repo":        "my-repo-name",
    "description": "Short description in English",
    "homepage":    "https://t.me/YOUR_CHANNEL",
    "topics":      ["python", "windows", "tool"],
    "tag":         "v1.0.0",
    "release_name":"v1.0.0",
    "release_body":"Release notes (plain text or unicode escaped)",
    "files":       ["bot.py", "README.md", "requirements.txt", "src/"],
    "commit_msg":  "feat: initial release",
    "branch":      "main"
}

Steps performed:
  1. Pre-push audit (no real tokens in tracked files)
  2. git init (if no .git), add files, commit
  3. Create GitHub repo (skip if exists)
  4. git remote + push
  5. Set description, topics, homepage
  6. Create release with tag
"""

import argparse, json, os, subprocess, sys, urllib.request, urllib.error
from pathlib import Path

# ── GitHub API ────────────────────────────────────────────────────────────────

def get_token():
    settings = os.path.expanduser('~/.claude/settings.json')
    return json.load(open(settings))['env']['GITHUB_TOKEN']

def api(token, method, url, body=None):
    H = {
        'Authorization': 'Bearer ' + token,
        'User-Agent': 'deploy_github.py',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json',
    }
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request('https://api.github.com' + url, data=data, headers=H, method=method)
    try:
        r = urllib.request.urlopen(req, timeout=20)
        return json.loads(r.read()), r.status
    except urllib.error.HTTPError as e:
        return json.loads(e.read()), e.code

def get_username(token):
    r, _ = api(token, 'GET', '/user')
    return r['login']

# ── Git helpers ───────────────────────────────────────────────────────────────

def git(args, cwd, check=True):
    r = subprocess.run(['git'] + args, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0 and check:
        print(f'[git] ERR: {r.stderr.strip()[:200]}')
    elif r.stdout.strip():
        print(f'[git] {r.stdout.strip()[:120]}')
    return r.returncode, r.stdout.strip()

# ── Pre-push audit ────────────────────────────────────────────────────────────

SECRET_PATTERNS = [
    r'ghp_[A-Za-z0-9]{36}',
    r'[0-9]{10}:AA[A-Za-z0-9_-]{33}',
    r'475c06[a-f0-9]{50}',
    r'edit\.telegra\.ph/auth',
]

def audit(project_dir):
    """Return list of suspicious lines found in tracked source files."""
    import re
    hits = []
    exts = {'.py', '.md', '.json', '.ps1', '.bat', '.cs', '.txt'}
    for f in Path(project_dir).rglob('*'):
        if f.is_dir() or f.suffix not in exts:
            continue
        rel = f.relative_to(project_dir).as_posix()
        if any(x in rel for x in ['.git/', 'config.py', '.env', '__pycache__']):
            continue
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        for line in content.splitlines():
            for pat in SECRET_PATTERNS:
                if re.search(pat, line):
                    hits.append(f'{rel}: {line.strip()[:80]}')
    return hits

# ── Main deploy ───────────────────────────────────────────────────────────────

def deploy(cfg, project_dir=None):
    project_dir = project_dir or os.getcwd()
    token = get_token()
    user  = get_username(token)
    repo  = cfg['repo']
    branch = cfg.get('branch', 'main')

    print(f'\n=== Deploy: {user}/{repo} ===\n')

    # 1. Audit
    print('[1/6] Pre-push audit...')
    hits = audit(project_dir)
    if hits:
        print('BLOCKED — secrets found:')
        for h in hits:
            print(' ', h)
        sys.exit(1)
    print('  Clean.')

    # 2. Git init + commit
    print('[2/6] Git...')
    git_dir = os.path.join(project_dir, '.git')
    if not os.path.exists(git_dir):
        git(['init', '-b', branch], project_dir)
    git(['config', 'user.email', f'{user}@users.noreply.github.com'], project_dir)
    git(['config', 'user.name', user], project_dir)

    files = cfg.get('files', ['.'])
    for f in files:
        git(['add', f], project_dir, check=False)

    msg = cfg.get('commit_msg', 'feat: initial release')
    git(['commit', '-m', msg + '\n\nCo-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>'], project_dir, check=False)

    # 3. Create repo on GitHub
    print('[3/6] GitHub repo...')
    resp, status = api(token, 'POST', '/user/repos', {
        'name': repo,
        'description': cfg.get('description', ''),
        'private': cfg.get('private', False),
        'auto_init': False,
    })
    if status == 201:
        print(f'  Created: {resp["html_url"]}')
    elif status == 422:
        print(f'  Already exists — skipping create')
    else:
        print(f'  ERROR {status}: {resp}')
        sys.exit(1)

    # 4. Push
    print('[4/6] Push...')
    remote = f'https://{token}@github.com/{user}/{repo}.git'
    git(['remote', 'remove', 'origin'], project_dir, check=False)
    git(['remote', 'add', 'origin', remote], project_dir)
    git(['push', '-u', 'origin', branch], project_dir)
    git(['remote', 'set-url', 'origin', f'https://github.com/{user}/{repo}.git'], project_dir)

    # 5. Topics + homepage
    print('[5/6] Metadata...')
    if 'topics' in cfg:
        api(token, 'PUT', f'/repos/{user}/{repo}/topics', {'names': cfg['topics']})
        print(f'  Topics: {cfg["topics"]}')
    patch = {}
    if 'homepage' in cfg: patch['homepage'] = cfg['homepage']
    if patch:
        api(token, 'PATCH', f'/repos/{user}/{repo}', patch)

    # 6. Release
    if 'tag' in cfg:
        print('[6/6] Release...')
        resp, status = api(token, 'POST', f'/repos/{user}/{repo}/releases', {
            'tag_name': cfg['tag'],
            'name': cfg.get('release_name', cfg['tag']),
            'body': cfg.get('release_body', ''),
            'draft': False,
            'prerelease': False,
        })
        if status == 201:
            print(f'  Release: {resp["html_url"]}')
        else:
            print(f'  Release {status}: {resp.get("errors", resp)[:100]}')
    else:
        print('[6/6] Release: skipped (no tag in config)')

    print(f'\nDone! https://github.com/{user}/{repo}\n')
    return f'https://github.com/{user}/{repo}'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='deploy.json')
    parser.add_argument('--dir', default=os.getcwd())
    args = parser.parse_args()

    if not os.path.exists(args.config):
        print(f'Config not found: {args.config}')
        print('Create deploy.json with repo, description, topics, tag, files...')
        sys.exit(1)

    cfg = json.load(open(args.config))
    deploy(cfg, args.dir)
