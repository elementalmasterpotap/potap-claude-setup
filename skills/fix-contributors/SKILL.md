---
name: fix-contributors
description: Исправить Contributors на GitHub — перезаписать email коммитов через filter-branch и force push
user-invocable: true
---

<!-- Stop hook: НЕВОЗМОЖНО — ручная repair-команда, не требует enforcement -->

## Когда использовать

В репо в Contributors появился чужой аккаунт вместо Потапа.
Причина: коммиты сделаны с неправильным noreply-email (см. GH-4 в lessons_universal.md).

## Алгоритм

### 1. Диагностика

```bash
git log --format="%an <%ae>" | sort -u
```

Если email НЕ `YOUR_GITHUB_USERNAME@gmail.com` и НЕ `YOUR_GITHUB_ID+YOUR_GITHUB_USERNAME@users.noreply.github.com` — проблема подтверждена.

### 2. Зафиксировать неправильный email

```bash
WRONG_EMAIL=$(git log --format="%ae" | sort -u | grep -v "YOUR_GITHUB_ID\|YOUR_GITHUB_USERNAME@gmail")
echo "Неправильный email: $WRONG_EMAIL"
```

### 3. Исправить историю

```bash
git stash  # если есть изменения

FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch -f --env-filter "
OLD_EMAIL=\"$WRONG_EMAIL\"
NEW_EMAIL=\"YOUR_GITHUB_ID+YOUR_GITHUB_USERNAME@users.noreply.github.com\"
[ \"\$GIT_AUTHOR_EMAIL\" = \"\$OLD_EMAIL\" ] && export GIT_AUTHOR_EMAIL=\"\$NEW_EMAIL\"
[ \"\$GIT_COMMITTER_EMAIL\" = \"\$OLD_EMAIL\" ] && export GIT_COMMITTER_EMAIL=\"\$NEW_EMAIL\"
" --tag-name-filter cat -- --branches --tags

git stash pop 2>/dev/null || true
```

### 4. Проверить результат

```bash
git log --format="%an <%ae>" | sort -u
# Должно быть: YOUR_GITHUB_USERNAME <YOUR_GITHUB_ID+YOUR_GITHUB_USERNAME@users.noreply.github.com>
```

### 5. Force push

```bash
git push --force origin main
```

### 6. Зафиксировать локальный config

```bash
git config --local user.email "YOUR_GITHUB_ID+YOUR_GITHUB_USERNAME@users.noreply.github.com"
```

GitHub обновит Contributors через несколько минут после force push.

## Правильные email Потапа

| Тип | Email |
|-----|-------|
| Основной (глобальный) | `YOUR_GITHUB_USERNAME@gmail.com` |
| noreply (для репо) | `YOUR_GITHUB_ID+YOUR_GITHUB_USERNAME@users.noreply.github.com` |
