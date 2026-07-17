# System Report — полный аудит

> Дата аудита: 2026-07-18
> Аудит проведён без внесения изменений в систему.
> Основание: Requirements.md, AI-Workstation.md, Architecture.md.

---

## 1. Железо

### 1.1. CPU

| Параметр | Значение |
|----------|----------|
| Модель | AMD Ryzen 7 7800X3D 8-Core Processor |
| Ядра / Потоки | 8 / 8 |
| Базовая частота | 4201 MHz |
| L2 Cache | 8 MB |
| L3 Cache | 96 MB (3D V-Cache) |

### 1.2. RAM

| Параметр | Значение |
|----------|----------|
| Всего | 64 GB (63 GB доступно ОС) |
| Свободно | 46.6 GB |
| Тип | DDR5 (SMBIOSMemoryType: 34) |
| Конфигурация | 2 x 32 GB |
| Manufacturer | A-DATA Technology |
| Part Number | AX5U6400C3232G-DCLAWH |
| Speed | 6400 MHz (configured) |
| Max Capacity | 128 GB |

### 1.3. GPU

| Параметр | Значение |
|----------|----------|
| Модель | NVIDIA GeForce RTX 5070 |
| VRAM | 12227 MiB (12 GB) |
| Used VRAM | 2249 MiB (~2.25 GB) |
| Free VRAM | ~9.98 GB |
| Driver | 591.86 (32.0.15.9186) |
| Driver Date | 20.01.2026 |
| CUDA (driver) | 13.1 (reported by nvidia-smi) |
| Resolution | 2560 x 1440 @ 179 Hz |
| GPU-Util | 4% |
| Temperature | 41C |

**GPU-процессы (потребляют VRAM):**

| Процесс | PID |
|---------|-----|
| M365Copilot.exe | 1144 |
| Obsidian.exe | 4892 |
| ChatGPT.exe (x3 инстанса) | 5916, 11892, 20048 |
| Steam / steamwebhelper.exe | 6756, 19072 |
| Telegram.exe | 7772 |
| SystemSettings.exe | 8380 |
| msedgewebview2.exe (x2) | 9252, 19464 |
| browser.exe | 10772 |
| Code.exe (VS Code) | 15480 |
| wallpaper64.exe | 18576 |
| karing.exe | 22876 |
| explorer.exe | 22900 |
| HighStone.exe | 17280 |

> 25+ процессов используют GPU, ~2.25 GB VRAM занято фоновыми приложениями.

### 1.4. Диски

| Диск | Тип | Всего | Свободно | % свободно |
|------|-----|-------|----------|------------|
| C: | NVMe (Samsung 990 PRO) | 1861.5 GB | 1558.3 GB | 83.7% |
| D: | HDD (Seagate 4TB) | 3726 GB | 1550.2 GB | 41.6% |

---

## 2. Операционная система

| Параметр | Значение |
|----------|----------|
| ОС | Майкрософт Windows 11 Домашняя |
| Version | 10.0.26200 |
| Build | 26200 |
| Архитектура | 64-разрядная |
| Материнская плата | Gigabyte B850 AORUS STEALTH ICE |
| Last Boot | 17.07.2026 16:03:28 |
| Windows Update | KB5120102 (Security, 15.07.2026) — последний |

### 2.1. Windows Defender

| Параметр | Значение |
|----------|----------|
| RealTimeProtection | Enabled |
| Antivirus | Enabled |
| NISEnabled | Enabled |

### 2.2. Windows Firewall

| Профиль | Enabled | DefaultInboundAction | DefaultOutboundAction |
|---------|---------|----------------------|-----------------------|
| Domain | True | **NotConfigured** | NotConfigured |
| Private | True | **NotConfigured** | NotConfigured |
| Public | True | **NotConfigured** | NotConfigured |

> NotConfigured означает использование значения по умолчанию (Block для inbound),
> но это неявная конфигурация — не зафиксирована явно.

### 2.3. Ключевые службы

| Служба | Статус | StartType |
|--------|--------|-----------|
| WinDefend | Running | Automatic |
| MpsSvc (Firewall) | Running | Automatic |
| BITS | Running | Automatic |
| Schedule | Running | Automatic |
| com.docker.service | **Stopped** | Manual |
| wuauserv (Windows Update) | **Stopped** | Manual |
| Ollama | **NOT FOUND** (нет службы) | — |
| LxssManager | **NOT FOUND** | — |

---

## 3. WSL

| Параметр | Значение |
|----------|----------|
| Дистрибутив по умолчанию | docker-desktop |
| Версия WSL | 2 |
| Состояние | Stopped |
| Дополнительные дистрибутивы | Нет (только docker-desktop) |

> Нет Ubuntu/Debian или других дистрибутивов для прямой разработки в WSL2.

---

## 4. Docker

| Параметр | Значение |
|----------|----------|
| Docker CLI | 29.2.1 |
| Docker Compose | v5.0.2 |
| Docker Desktop (registry) | 4.63.0 |
| Состояние демона | **Stopped** (недоступен) |
| com.docker.service | Stopped, Manual |
| Контексты | desktop-linux |

> Docker CLI установлен, но демон не запущен.
> docker info и docker version (server part) не работают.

---

## 5. PowerShell

| Параметр | Значение |
|----------|----------|
| Версия (текущая, Windows PowerShell) | 5.1.26100.8875 |
| Edition | Desktop |
| PowerShell 7 (pwsh) | 7.5.8 (установлен, в PATH) |
| Путь к pwsh | C:\Program Files\PowerShell\7\ |

> Терминал по умолчанию использует Windows PowerShell 5.1, а не PowerShell 7.

---

## 6. Git

| Параметр | Значение |
|----------|----------|
| Версия | 2.53.0.windows.1 |
| user.name | jerigoledelamort |
| user.email | pu5sydestroer@yandex.ru |
| core.editor | VS Code (--wait) |
| core.autocrlf | **НЕ УСТАНОВЛЕН** |
| init.defaultBranch | **НЕ УСТАНОВЛЕН** |
| filter.lfs | Установлен (git-lfs) |
| git init в D:\Projects\ai | **НЕ ВЫПОЛНЕН** (нет .git) |

---

## 7. Python

| Параметр | Значение |
|----------|----------|
| Версия (по умолчанию) | 3.10.10 |
| Путь | C:\Users\egork\AppData\Local\Programs\Python\Python310\python.exe |
| pip | 26.0.1 |
| Python 3.14.2 | **Также установлен** (C:\Users\egork\AppData\Local\Python\bin\python3.14.exe) |
| WindowsApps python.exe | **Стуб-перенаправление** в PATH |

### 7.1. where.exe python (порядок разрешения)

| # | Путь | Версия |
|---|------|--------|
| 1 | C:\Users\egork\AppData\Local\Programs\Python\Python310\python.exe | 3.10.10 |
| 2 | C:\Users\egork\AppData\Local\Microsoft\WindowsApps\python.exe | Стуб Microsoft Store |
| 3 | C:\Users\egork\AppData\Local\Python\bin\python.exe | 3.14.2 |

### 7.2. Установленные pip-пакеты (AI-related)

| Пакет | Версия | Примечание |
|-------|--------|------------|
| torch | 2.7.1+**cu118** | CUDA 11.8 — несовпадение с CUDA Toolkit 12.8 |
| torchaudio | 2.7.1+cu118 | То же |
| torchvision | 0.22.1+cu118 | То же |
| litellm | 1.81.10 | Установлен в global pip, не в venv |
| openai | 2.20.0 | |
| numpy | 1.26.4 | |
| scikit-learn | 1.7.2 | |
| jupyter_client | 8.8.0 | |
| jupyter_core | 5.9.1 | |

---

## 8. Node.js

| Параметр | Значение |
|----------|----------|
| Node.js | **НЕ УСТАНОВЛЕН** |
| npm | **НЕ УСТАНОВЛЕН** |
| nvm | **НЕ УСТАНОВЛЕН** |
| Bun | **НЕ УСТАНОВЛЕН** |

---

## 9. CUDA

| Параметр | Значение |
|----------|----------|
| CUDA Toolkit | 12.8 (V12.8.61) |
| nvcc | Доступен, работает |
| CUDA_PATH | C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8 |
| CUDA_HOME | **НЕ УСТАНОВЛЕН** |
| nvidia-smi CUDA | 13.1 (версия драйвера) |
| Registry entries | **Не найдены** (но CUDA_PATH установлен и nvcc работает) |
| PyTorch CUDA | **cu118** (несовпадение с Toolkit 12.8) |

### 9.1. CUDA-компоненты в реестре (установленные)

| Компонент | Версия |
|-----------|--------|
| CUDA CCCL | 12.8 |
| CUDA Documentation | 12.8 |
| CUDA Profiler API | 12.8 |
| CUDA Profiler Tools | 12.8 |
| CUDART Runtime | 12.8 |
| CUDA Development | 12.8 |
| CUDA Visual Studio Integration | 12.8 |

---

## 10. GPU и драйверы

| Параметр | Значение |
|----------|----------|
| GPU | NVIDIA GeForce RTX 5070 |
| Driver Version | 591.86 |
| Driver Date | 20.01.2026 |
| Driver Model | WDDM |
| Compute Mode | Default |
| MIG | N/A |
| ECC | N/A |

---

## 11. Переменные окружения

### 11.1. AI/Dev-переменные

| Переменная | Machine | User | Статус |
|------------|---------|------|--------|
| OLLAMA_HOST | — | — | **НЕ УСТАНОВЛЕН** |
| OLLAMA_MODELS | — | — | **НЕ УСТАНОВЛЕН** (по умолчанию ~/.ollama/models) |
| OLLAMA_KEEP_ALIVE | — | — | **НЕ УСТАНОВЛЕН** |
| CUDA_PATH | C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8 | — | OK |
| CUDA_HOME | — | — | **НЕ УСТАНОВЛЕН** |
| JAVA_HOME | — | — | **НЕ УСТАНОВЛЕН** (Java 21 установлена) |
| PYTHONPATH | — | — | Не установлен (норма) |
| PYTHONHOME | — | — | Не установлен (норма) |
| DOCKER_HOST | — | — | Не установлен (норма для Docker Desktop) |
| HTTP_PROXY | — | — | Не установлен (норма) |
| HTTPS_PROXY | — | — | Не установлен (норма) |

---

## 12. PATH

### 12.1. Machine PATH

| # | Путь | Существует |
|---|------|------------|
| 1 | C:\Program Files\Eclipse Adoptium\jdk-21.0.11.10-hotspot\bin | OK |
| 2 | C:\VulkanSDK\1.4.341.1\Bin | OK |
| 3 | C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8\bin | OK |
| 4 | C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8\libnvvp | OK |
| 5 | C:\WINDOWS\system32 | OK |
| 6 | C:\WINDOWS | OK |
| 7 | C:\WINDOWS\System32\Wbem | OK |
| 8 | C:\WINDOWS\System32\WindowsPowerShell\v1.0\ | OK |
| 9 | C:\WINDOWS\System32\OpenSSH\ | OK |
| 10 | C:\Program Files\NVIDIA Corporation\NVIDIA App\NvDLISR | OK |
| 11 | C:\Program Files (x86)\NVIDIA Corporation\PhysX\Common | OK |
| 12 | C:\Program Files\NVIDIA Corporation\Nsight Compute 2025.1.0\ | OK |
| 13 | C:\Program Files\dotnet\ | OK |
| 14 | C:\Program Files\Cloudflare\Cloudflare WARP\ | OK |
| 15 | C:\Program Files\Docker\Docker\resources\bin | OK |
| 16 | C:\Program Files\Git\cmd | OK |
| 17 | C:\Program Files\CMake\bin | OK |
| 18 | C:\Program Files (x86)\Windows Kits\10\Windows Performance Toolkit\ | OK |
| 19 | D:\Applications\Coding\ | OK |
| 20 | C:\Program Files\PowerShell\7\ | OK |

### 12.2. User PATH

| # | Путь | Существует |
|---|------|------------|
| 1 | C:\Users\egork\AppData\Local\Programs\Python\Python310\Scripts\ | OK |
| 2 | C:\Users\egork\AppData\Local\Programs\Python\Python310\ | OK |
| 3 | C:\Users\egork\AppData\Local\Microsoft\WindowsApps | OK |
| 4 | D:\Applications\Coding\VS Code\Microsoft VS Code\bin | OK |
| 5 | C:\Users\egork\AppData\Local\Python\bin | OK (Python 3.14) |
| 6 | C:\Users\egork\AppData\Local\GitHubDesktop\bin | OK |
| 7 | C:\Users\egork\AppData\Local\Programs\Ollama | OK |
| 8 | C:\mingw64\mingw64\bin | OK |
| 9 | C:\Users\egork\.dotnet\tools | **ОТСУТСТВУЕТ** |
| 10 | D:\Applications\Coding\cursor\resources\app\bin | OK |

### 12.3. Дубликаты PATH

Дубликатов не обнаружено.

### 12.4. Проблемы PATH

| Проблема | Уровень |
|----------|---------|
| C:\Users\egork\.dotnet\tools — не существует | Low |
| WindowsApps\python.exe — стуб Microsoft Store в PATH перед Python 3.14 | Medium |
| Нет uv в PATH (не установлен) | Medium |
| Нет Node.js в PATH (не установлен) | Medium |

---

## 13. Порты

### 13.1. Слушающие порты

| Адрес | Порт | PID | Процесс | Привязка |
|-------|------|-----|---------|----------|
| 127.0.0.1 | 3057 | 15992 | karingService | localhost OK |
| 127.0.0.1 | 3065-3067 | 15992 | karingService | localhost OK |
| 127.0.0.1 | 11021 | 4 | System | localhost OK |
| **127.0.0.1** | **11434** | **7068** | **ollama** | **localhost OK** |
| **0.0.0.0** | **27036** | **19072** | **steam** | **ВСЕ ИНТЕРФЕЙСЫ** |
| 127.0.0.1 | 27060 | 19072 | steam | localhost OK |
| 127.0.0.1 | 31416 | 17404 | boinc | localhost OK |
| 127.0.0.1 | 50066 | 17860 | ollama app | localhost OK |
| 127.0.0.1 | 54263 | 24256 | Code | localhost OK |
| 127.0.0.1 | 54768 | 15992 | karingService | localhost OK |
| 127.0.0.1 | 62018-62019 | 19072 | steam | localhost OK |
| 0.0.0.0 | 135 | 1800 | svchost (RPC) | Все интерфейсы (системный) |
| 0.0.0.0 | 445 | 4 | System (SMB) | Все интерфейсы (системный) |
| 192.168.1.11 | 139 | 4 | System (NetBIOS) | Локальная сеть |
| 172.27.48.1 | 139 | 4 | System (NetBIOS) | WSL-мост |
| 0.0.0.0 | 5040 | 10040 | svchost | Все интерфейсы |
| 0.0.0.0 | 7680 | 23648 | svchost (WUDO) | Все интерфейсы |
| 0.0.0.0 | 49664-49689 | various | System services | Все интерфейсы (системные) |

### 13.2. AI-порты — firewall правила

| Порт | Назначение | Inbound rule | Статус |
|------|-----------|--------------|--------|
| 11434 | Ollama | Нет правила | Нет явного block-правила |
| 4000 | LiteLLM | Нет правила | Нет явного block-правила |
| 6333 | Qdrant REST | Нет правила | Нет явного block-правила |
| 6334 | Qdrant gRPC | Нет правила | Нет явного block-правила |
| 8080 | Open WebUI | Нет правила | Нет явного block-правила |
| 8000 | MkDocs | Нет правила | Нет явного block-правила |

> Все AI-порты не имеют явных firewall правил.
> Текущая защита — только неявный default inbound block (NotConfigured -> Block).

---

## 14. Установленное ПО (AI/Dev-related)

| ПО | Версия | Статус |
|----|--------|--------|
| Ollama | 0.32.0 | Запущен (процесс) |
| Docker Desktop | 4.63.0 (CLI 29.2.1) | Установлен, демон остановлен |
| Git | 2.53.0 | OK |
| GitHub CLI | 2.96.0 | OK |
| GitHub Desktop | 3.5.5 | OK |
| Python 3.10 | 3.10.10 | OK |
| Python 3.14 | 3.14.2 | Дополнительная версия |
| CUDA Toolkit | 12.8 | OK |
| Java (Temurin) | 21.0.11 | OK |
| VS Code | Установлен | OK |
| Cloudflare WARP | Установлен | OK |
| Vulkan SDK | 1.4.341.1 | OK |
| CMake | Установлен | OK |
| MinGW64 | Установлен | OK |
| Cursor | Установлен (в PATH) | OK |
| uv | — | НЕ УСТАНОВЛЕН |
| Node.js | — | НЕ УСТАНОВЛЕН |
| SOPS | — | НЕ УСТАНОВЛЕН |
| age | — | НЕ УСТАНОВЛЕН |
| Go | — | НЕ УСТАНОВЛЕН |
| Rust | — | НЕ УСТАНОВЛЕН |
| Conda/Miniconda | — | НЕ УСТАНОВЛЕН |

### 14.1. VS Code расширения

| Расширение | Назначение |
|------------|------------|
| koda.koda | AI-ассистент |
| gigacode.gigacode-vscode | AI-ассистент |
| ms-python.python | Python support |
| ms-python.debugpy | Python debugger |
| ms-python.vscode-pylance | Python language server |
| ms-python.vscode-python-envs | Python env manager |

> Dev Containers, Continue — НЕ УСТАНОВЛЕНЫ.

### 14.2. Ollama

| Параметр | Значение |
|----------|----------|
| Версия | 0.32.0 |
| API | http://127.0.0.1:11434 OK |
| Модели | 1 (qwen3:8b, 5.2 GB) |
| Размер моделей | 4.87 GB на диске |
| Путь моделей | C:\Users\egork\.ollama\models (по умолчанию) |
| Процесс | ollama (PID 7068, 52 MB RAM) + ollama app (PID 17860, 85 MB RAM) |
| Служба Windows | НЕ ЗАРЕГИСТРИРОВАНА |
| OLLAMA_HOST | НЕ УСТАНОВЛЕН (по умолчанию 127.0.0.1:11434) |

### 14.3. Другие AI-программы

| Программа | Назначение | Статус |
|-----------|-----------|--------|
| ChatGPT (desktop) | Облачный AI-чат | Запущен (3 инстанса, использует GPU) |
| M365Copilot | Microsoft Copilot | Запущен (использует GPU) |
| Obsidian | Заметки | Запущен (использует GPU) |
| BOINC | Распределённые вычисления | Запущен (порт 31416) |
| Cursor | AI IDE | Установлен (в PATH) |

---

## 15. Сводная таблица проблем

### CRITICAL (блокируют работу)

| # | Проблема | Компонент | Описание |
|---|----------|-----------|----------|
| C1 | Docker демон не запущен | Docker | com.docker.service — Stopped, Manual. Демон недоступен. Блокирует Qdrant, Open WebUI, DevContainers. |
| C2 | Ollama не зарегистрирован как служба | Ollama | Ollama работает как пользовательский процесс (ollama + ollama app). При выходе из системы / перезагрузке — остановится. Нет автозапуска. |

### HIGH (серьёзные риски)

| # | Проблема | Компонент | Описание |
|---|----------|-----------|----------|
| H1 | PyTorch CUDA несовпадение | Python/CUDA | PyTorch 2.7.1+cu118 установлен, но CUDA Toolkit 12.8. PyTorch не использует CUDA 12.8. Возможны ошибки при GPU-инференсе через PyTorch. |
| H2 | OLLAMA_HOST не установлен | Ollama | Переменная не задана. Ollama по умолчанию слушает 127.0.0.1, но это неявно. При обновлении или смене конфигурации может привязаться к 0.0.0.0. |
| H3 | Firewall DefaultInboundAction = NotConfigured | Windows Firewall | На всех 3 профилях (Domain/Private/Public) действие не задано явно. Default = Block, но не зафиксировано. |
| H4 | Нет явных firewall правил для AI-портов | Security | Порты 11434, 4000, 6333, 6334, 8080, 8000 — без явных inbound block-правил. Защита только неявным default. |
| H5 | Две версии Python (3.10 + 3.14) | Python | Python 3.10.10 и 3.14.2 установлены одновременно. where.exe python возвращает 3 записи (включая стуб Microsoft Store). Риск путаницы версий и конфликтов. |
| H6 | JAVA_HOME не установлен | Java | Java 21 (Temurin) установлена и в PATH, но JAVA_HOME не задана. Некоторые инструменты требуют JAVA_HOME. |
| H7 | Git core.autocrlf не настроен | Git | Не задан core.autocrlf. Риск CRLF/LF проблем в кроссплатформенных проектах и DevContainers. |
| H8 | Steam слушает на 0.0.0.0:27036 | Network/Security | Steam привязан ко всем интерфейсам на порту 27036. Внешний доступ из сети. |

### MEDIUM (влияют на качество/удобство)

| # | Проблема | Компонент | Описание |
|---|----------|-----------|----------|
| M1 | PowerShell 5.1 по умолчанию | PowerShell | Терминал использует Windows PowerShell 5.1, хотя PowerShell 7.5.8 установлен. PS 7 — быстрее, современнее, лучше поддержка UTF-8. |
| M2 | LiteLLM установлен в global pip | Python | litellm 1.81.10 установлен в глобальное окружение Python 3.10, а не в venv. Нарушает изоляцию и воспроизводимость. |
| M3 | uv не установлен | Python env | uv (менеджер окружений, выбранный в TDR-003) не установлен. |
| M4 | Node.js не установлен | Node.js | Node.js LTS (нужен для MCP-серверов) не установлен. |
| M5 | SOPS и age не установлены | Security | Инструменты шифрования секретов (TDR-004) не установлены. |
| M6 | Нет git init в проекте | Git | D:\Projects\ai не инициализирован как git-репозиторий. |
| M7 | Стуб Microsoft Store python в PATH | Python | C:\Users\egork\AppData\Local\Microsoft\WindowsApps\python.exe — стуб, который может перехватывать вызов python и открывать Microsoft Store вместо запуска. |
| M8 | CUDA_HOME не установлен | CUDA | CUDA_PATH установлен, но CUDA_HOME — нет. Некоторые инструменты проверяют CUDA_HOME. |
| M9 | Нет дистрибутива WSL2 для разработки | WSL | Единственный WSL-дистрибутив — docker-desktop. Нет Ubuntu/Debian для прямой разработки в WSL2. |
| M10 | Dev Containers не установлен | VS Code | Расширение Dev Containers (нужно для TDR-006) не установлено. |
| M11 | 25+ GPU-процессов потребляют VRAM | GPU | ~2.25 GB VRAM занято фоновыми приложениями (ChatGPT, Steam, Telegram, wallpaper engine и др.). Доступно ~9.98 GB вместо 12 GB. |
| M12 | Docker Desktop service — Manual | Docker | com.docker.service имеет StartType=Manual. Не запустится автоматически при старте системы. |

### LOW (косметика / минорные)

| # | Проблема | Компонент | Описание |
|---|----------|-----------|----------|
| L1 | PATH: .dotnet\tools не существует | PATH | C:\Users\egork\.dotnet\tools в User PATH, но директория не существует. |
| L2 | wuauserv — Stopped, Manual | Windows Update | Служба обновлений остановлена и переведена в Manual. Обновления не устанавливаются автоматически. |
| L3 | Git init.defaultBranch не установлен | Git | Не задано имя ветки по умолчанию. git init создаст master вместо main. |
| L4 | Нет scheduled tasks для AI | Automation | Нет запланированных задач для обслуживания AI-станции (бэкап, обновление моделей). |
| L5 | Git LFS установлен, но не настроен | Git | filter.lfs сконфигурирован глобально, но без .gitattributes в проекте. |
| L6 | Docker Desktop version: registry vs CLI | Docker | Registry: 4.63.0, CLI: 29.2.1. Это нормально (app version vs engine version), но может вызвать путаницу. |
| L7 | CUDA registry entries не найдены | CUDA | HKLM:\SOFTWARE\NVIDIA Corporation\GPU Computing Toolkit\Installations — пусто. Но CUDA_PATH установлен и nvcc работает. |
| L8 | Cursor в PATH | VS Code | D:\Applications\Coding\cursor\resources\app\bin в PATH. Cursor — другая AI IDE. Может конфликтовать с VS Code. |
| L9 | BOINC запущен | Resources | BOINC использует CPU для распределённых вычислений. Потребляет ресурсы, которые могли бы использоваться для CPU offload. |
| L10 | ChatGPT desktop (3 инстанса) | GPU/RAM | Три инстанса ChatGPT desktop запущены одновременно, потребляют GPU и RAM. |

---

## 16. Статистика проблем

| Уровень | Количество |
|---------|-----------|
| **Critical** | 2 |
| **High** | 8 |
| **Medium** | 12 |
| **Low** | 10 |
| **Всего** | **32** |

---

## 17. Сводка готовности системы

| Компонент | Статус | Блокеры |
|-----------|--------|---------|
| Windows 11 | Готова | — |
| GPU + драйверы | Готовы | M11 (VRAM занят фоновыми) |
| CUDA Toolkit | Установлен | H1 (PyTorch cu118) |
| Ollama | Частично | C2 (нет службы), H2 (нет OLLAMA_HOST) |
| Docker | Частично | C1 (демон остановлен), M12 (Manual) |
| Git | Частично | H7 (autocrlf), L3 (defaultBranch), M6 (нет init) |
| Python | Частично | H5 (две версии), M2 (global pip), M7 (Store stub) |
| PowerShell | Частично | M1 (PS 5.1 по умолчанию) |
| Node.js | Не установлен | M4 |
| uv | Не установлен | M3 |
| SOPS + age | Не установлены | M5 |
| VS Code | Частично | M10 (нет Dev Containers) |
| Firewall | Частично | H3, H4 (нет явных правил) |
| WSL2 | Частично | M9 (нет dev-дистрибутива) |

---

*Аудит проведён 2026-07-18. Изменения в систему не вносились.*
