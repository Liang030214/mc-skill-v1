# MC Ecosystem Adaptation Engineer

> One-stop Minecraft mod ecosystem intelligent management tool.

## Overview

MC Ecosystem Adaptation Engineer is an AI-powered assistant tool for Minecraft mod players and modpack authors. It covers 10+ core capabilities including mod search, environment setup, Mixin conflict scanning, crash analysis, multi-language translation, and migration feasibility assessment. Supports Forge, NeoForge, Fabric, and Quilt loaders across MC versions 1.16.5 to 1.21.x.

## Key Features

| # | Feature | Description |
|---|---------|-------------|
| F1 | JAR Structure Parser | Parse mod JAR metadata (mcmod.info, fabric.mod.json, mods.toml) and generate Chinese feature documentation |
| F2 | Mod Search & Download | Search and download mods from Modrinth with version and loader filtering |
| F3 | Environment Setup Guide | Intelligently recommend MC version and loader combinations, auto-detect Java version and launcher paths |
| F4 | Mixin Conflict Scanner | Detect Mixin injection conflicts between multiple mods and identify compatibility risks |
| F5 | Resource Repacker | Repack and optimize mod resource files (textures, sounds, language files) |
| F6 | Save Sync | Backup and restore game saves with multi-device sync support |
| F7 | Multi-language Translation | Translate mod language files between 10 supported languages (ZH/EN/JA/KO/RU/ES/IT/EL/TH/HI) |
| F8 | Crash Fix | Intelligently analyze crash logs, identify 25+ error patterns, and provide fix suggestions |
| F8.1 | Auto Fix | One-click mod version upgrade, automatic backup and replacement with fix report generation |
| F9 | Migration Feasibility Assessment | Cross-version/cross-loader migration feasibility report with API/dependency/Mixin analysis |

## Technical Highlights

- **All-Loader Support**: Native support for Forge, NeoForge, Fabric, and Quilt
- **10 Languages**: Built-in language packs for Chinese, English, Japanese, Korean, Russian, Spanish, Italian, Greek, Thai, and Hindi
- **25+ Crash Patterns**: Comprehensive crash pattern database covering OOM, shader conflicts, Mixin conflicts, class loading failures, and more
- **Modrinth API Integration**: Real-time mod version queries via Modrinth API
- **Smart Caching**: Avoid redundant API calls for improved response speed
- **Safety Backups**: Forced backup before auto-fix operations with one-click rollback support
- **Mixin Injection Analysis**: Deep scan of Mixin injection points with target class compatibility assessment
- **Cross-Platform**: Windows, macOS, and Linux support

## Pricing

### Free Access

All features are currently free during the beta period.

Premium subscription options will be available in the future. Stay tuned for updates.

## Installation

### Prerequisites

- Python 3.10+
- Windows / macOS / Linux
- Network connection (required for mod search and version queries)

### Quick Start

```bash
# 1. Clone or download the project
cd mc-skill-v1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run interactively
python main.py

# Or use the startup script
# Windows: mc-skill-start.bat
```

### Command Line Usage

```bash
# Parse mod JAR structure
python main.py --feature jar_parser --jar-path "create.jar"

# Search and download mods
python main.py --feature mod_searcher --query "Create" --mc-version "1.21.1" --loader "neoforge"

# Analyze crash log
python main.py --feature crash_analyzer --crash-log "crash-report.txt"

# Auto-fix crash issues
python main.py --feature auto_fix --crash-log "crash.txt" --fix-mods-dir "~/.minecraft/mods"

# Assess migration feasibility
python main.py --feature migration_assess --jar-path "mod.jar" --from-mc-version "1.20.1" --to-mc-version "1.21.1" --from-loader "forge" --to-loader "neoforge"

# Translate mod language files
python main.py --feature translator --mods-dir "~/.minecraft/mods" --lang zh_cn

# Sync game saves
python main.py --feature save_sync --action sync --save-dir "~/.minecraft/saves"
```

## Author

- **Author**: Liang030214
- **Version**: v1.0.2
- **License**: MIT License
- **Homepage**: https://github.com/Liang030214/mc-skill-v1
- **Tags**: minecraft, mod, forge, fabric, neoforge, quilt, mixin, translation, crash-fix, migration, i18n

## Supported MC Versions

- 1.16.5 ~ 1.21.x

## Supported Loaders

- Forge (47.x+)
- NeoForge (21.1+)
- Fabric (0.15+)
- Quilt (0.23+)