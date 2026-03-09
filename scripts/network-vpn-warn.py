#!/usr/bin/env python3
"""
PostToolUse хук: предупреждает о необходимости VPN при сетевых ошибках.

Контекст: мы в России, многие сервисы заблокированы.
При ошибках сети в Bash output → stderr предупреждение включить VPN.

Покрывает: curl, fetch, npm, pip, git clone, wget и т.д.
"""
import sys, json, re

try:
    payload = json.loads(sys.stdin.read())
    tool = payload.get("tool_name", "")

    # Только Bash инструмент
    if tool != "Bash":
        sys.exit(0)

    # Получаем вывод инструмента
    result = payload.get("tool_result", {})
    output = ""
    if isinstance(result, str):
        output = result
    elif isinstance(result, dict):
        output = str(result.get("output", "")) + str(result.get("stderr", ""))
    elif isinstance(result, list):
        output = " ".join(str(r) for r in result)

    if not output:
        sys.exit(0)

    # Паттерны сетевых ошибок
    network_error_re = re.compile(
        r'(ECONNREFUSED|ECONNRESET|ENOTFOUND'
        r'|Connection timed out|Connection refused|Connection reset'
        r'|Temporary failure in name resolution'
        r'|Could not resolve host|Name or service not known'
        r'|ConnectTimeout|Connect Timeout|connect timeout'
        r'|curl: \(6\)|curl: \(7\)|curl: \(28\)|curl: \(35\)|curl: \(60\)'
        r'|SSL_ERROR|SSL handshake|certificate verify failed'
        r'|Network is unreachable|Network unreachable'
        r'|ERR_CONNECTION_TIMED_OUT|ERR_NAME_NOT_RESOLVED'
        r'|Failed to connect|Unable to connect'
        r'|getaddrinfo.*failed|nodename nor servname'
        r'|npm warn network|npm ERR! network'
        r'|pip.*ConnectTimeout|pip.*connection.*error'
        r'|git.*unable to connect|git.*Could not resolve'
        r'|302 Found.*cloudflare|blocked.*russia)',
        re.IGNORECASE
    )

    if network_error_re.search(output):
        print(
            "⚠️ Сетевая ошибка — скорее всего нужен VPN (мы в России, сервис заблокирован). "
            "Включи VPN и повтори запрос. "
            "Если VPN уже включён — попробуй другой сервер или протокол.",
            file=sys.stderr
        )

except Exception:
    pass

sys.exit(0)
