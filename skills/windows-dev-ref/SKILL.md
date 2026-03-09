---
name: windows-dev-ref
description: C# 5/.NET 4.x и PowerShell паттерны для Windows разработки. Автоматически подгружается при задачах с C#, WinForms, csc.exe, PowerShell, Windows, GitHub API через PS, установщиками.
user-invocable: false
---

<!-- Stop hook: csharp-compat-check.py + ps-unicode-check.py (Stop) -->
## C# 5 — что НЕ работает (csc.exe / .NET 4.x)

| C# 6+ (не компилируется) | C# 5 (правильно) |
|--------------------------|-----------------|
| `string Foo() => value;` | `string Foo() { return value; }` |
| `{ get; set; } = Color.Red` | инициализировать в конструкторе |
| `$"Hello {name}"` | `string.Format("Hello {0}", name)` |
| `nameof(MyProp)` | `"MyProp"` (литерал) |

## Компиляция WinForms

```powershell
$csc = "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe"
& $csc /target:winexe /out:"App.exe" `
       /reference:System.Windows.Forms.dll `
       /reference:System.Drawing.dll `
       /reference:System.dll `
       /optimize+ "src\App.cs"
```

## Тёмная тема WinForms

```csharp
[DllImport("dwmapi.dll")]
static extern int DwmSetWindowAttribute(IntPtr hwnd, int attr, ref int v, int size);

protected override void OnHandleCreated(EventArgs e) {
    base.OnHandleCreated(e);
    int dark = 1;
    DwmSetWindowAttribute(Handle, 20, ref dark, 4);
}
```

Цвета:
```csharp
static readonly Color C_BG     = Color.FromArgb(28, 28, 28);
static readonly Color C_ACCENT = Color.FromArgb(0, 191, 255);   // #00BFFF cyan
static readonly Color C_DANGER = Color.FromArgb(204, 51, 51);
static readonly Color C_OK     = Color.FromArgb(40, 160, 80);
```

## Локализация C# 5

```csharp
bool isRu;  // инициализировать в конструкторе!
public MainForm() {
    isRu = System.Globalization.CultureInfo.InstalledUICulture
               .TwoLetterISOLanguageName == "ru";
    InitializeComponent();
}
string S(string ru, string en) { return isRu ? ru : en; }
```

---

## PS-1 — JSON + кириллица → одинарные кавычки

```
ПЛОХО:  $body = "@{key='значение'}" | ConvertTo-Json   ← \u → \\u, GitHub видит буквальный текст
ХОРОШО: $body = '{"key":"\u0437\u043d\u0430\u0447"}'   ← одинарные кавычки, \uXXXX как есть
```

Сгенерировать \uXXXX:
```powershell
$text = "Что нового"
-join ($text.ToCharArray() | % { $c=[int][char]$_; if($c -gt 127){'\u{0:X4}' -f $c}else{[string]$_} })
```

## PS-2 — Кракозябры в консоли ≠ повреждённые данные

Windows консоль (cp866/cp1251) показывает UTF-8 как мусор. Данные в порядке.
Проверять результат через браузер — не доверять консольному выводу.

## PS-3 — Сложные скрипты → файл

```
ПЛОХО:  powershell.exe -Command "длинный скрипт с кириллицей"
ХОРОШО: $script | Set-Content "_tmp.ps1" -Encoding UTF8
         powershell.exe -File "_tmp.ps1"
         Remove-Item "_tmp.ps1"
```

## GitHub upload endpoint

```
API:    api.github.com/repos/.../releases/{id}/assets     ← читать/листать
Upload: uploads.github.com/repos/.../releases/{id}/assets ← загружать файлы
```

```powershell
$bytes = [System.IO.File]::ReadAllBytes($file)
Invoke-RestMethod -Method POST "https://uploads.github.com/repos/$repo/releases/$id/assets?name=$name" `
    -Headers @{ Authorization='Bearer '+$token; 'Content-Type'='application/zip' } -Body $bytes
```

## Python на этой машине

```
python    → C:\Python\Python315\python.exe  ✅
python3   → Microsoft Store redirect        ❌
```
