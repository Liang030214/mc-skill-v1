"""MC Ecosystem Adapt Engineer V1 - Main Entry Point

Features:
1. Command-line argument parsing (argparse)
2. JSON config file batch task support
3. Feature routing (F1-F9)
4. Unified output structure

Usage:
    # Command-line mode
    python main.py --feature jar_parser --jar-path "D:\\mods\\create.jar"

    # JSON config mode
    python main.py --config "task.json"
"""

import sys
import os
import argparse
import json
import html
from pathlib import Path
from typing import Optional

_PROJECT_ROOT = Path(__file__).resolve().parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import config
from utils.logger import get_logger
from utils.report_gen import generate_unified_output
from core.i18n import t, set_language, get_current_language, get_supported_languages, save_language_preference

logger = get_logger("main")


FEATURES = {
    "jar_parser": {
        "name": "F1 JAR Structure Parse",
        "module": "core.jar_parser",
        "function": "run",
        "status": "implemented",
    },
    "mod_searcher": {
        "name": "F2 Mod Search & Download",
        "module": "core.mod_searcher",
        "function": "run",
        "status": "implemented",
    },
    "env_builder": {
        "name": "F3 Environment Setup Guide",
        "module": "core.env_builder",
        "function": "run",
        "status": "implemented",
    },
    "mixin_scanner": {
        "name": "F4 Mixin Conflict Scan",
        "module": "core.mixin_scanner",
        "function": "run",
        "status": "implemented",
    },
    "repacker": {
        "name": "F5 Resource Repack",
        "module": "core.repacker",
        "function": "run",
        "status": "implemented",
    },
    "save_sync": {
        "name": "F6 Save Sync",
        "module": "core.save_sync",
        "function": "run",
        "status": "implemented",
    },
    "translator": {
        "name": "F7 Basic Localization",
        "module": "core.translator",
        "function": "run",
        "status": "implemented",
    },
    "crash_analyzer": {
        "name": "F8 Crash Analysis & Fix",
        "module": "core.crash_analyzer",
        "function": "run",
        "status": "implemented",
    },
    "auto_fix": {
        "name": "F8.1 Auto Fix",
        "module": "core.auto_fix",
        "function": "auto_fix_run",
        "status": "implemented",
    },
    "migration_assess": {
        "name": "F9 Migration Feasibility Assessment",
        "module": "core.migration_assessor",
        "function": "run",
        "status": "implemented",
    },
}


def dispatch_feature(feature: str, args: argparse.Namespace) -> int:
    """Dispatch a feature for execution.

    Args:
        feature: Feature identifier
        args: Command-line arguments

    Returns:
        Exit code 0=success 1=failure
    """
    if feature not in FEATURES:
        logger.error(f"Unknown feature: {feature}")
        logger.info(f"Available features: {', '.join(FEATURES.keys())}")
        return 1

    feat_info = FEATURES[feature]
    logger.info(f"Dispatching: {feat_info['name']} ({feature})")

    if feat_info["status"] != "implemented":
        return _render_not_implemented(feature, feat_info, args)

    try:
        from core.auth_manager import check_permission, record_usage, FUNC_AUTO, FUNC_SEMI
        func_type = FUNC_SEMI if feature in ("env_builder", "save_sync") else FUNC_AUTO
        perm = check_permission(feature, func_type)
        if not perm["allowed"]:
            logger.warning(f"Feature limited: {perm['reason']}")
            print(f"\n⚠️  {t('auth.feature_limited_warning', reason=perm['reason'])}", flush=True)
            print(f"   {t('auth.member_tier')}: {perm['tier']}", flush=True)
            print(f"   {t('auth.remaining')}: {perm['remaining']}/{perm['limit']}", flush=True)
            print(f"   {t('auth.upgrade_tip')}\n", flush=True)
            return 1
    except Exception as e:
        logger.debug(f"Permission check skipped: {e}")

    try:
        import importlib
        module = importlib.import_module(feat_info["module"])
        func = getattr(module, feat_info["function"])
        result = func(args)
        try:
            record_usage(feature)
        except Exception:
            pass
        return 0 if result.get("status") != "error" else 1
    except ImportError as e:
        logger.error(f"Module import failed: {feat_info['module']} - {e}")
        print(f"\n❌ {t('error.module_import_failed', module=feat_info['module'])}: {e}", flush=True)
        return _render_not_implemented(feature, feat_info, args)
    except Exception as e:
        logger.exception(f"Feature execution error: {feature}")
        print(f"\n❌ {t('error.feature_execution_failed')}: {e}", flush=True)
        generate_unified_output(
            feature=feature,
            status="error",
            input_summary=vars(args),
            result={},
            title=f"{feat_info['name']} - {t('not_implemented.error_report')}",
            html_content=(
                f'<div class="callout red">'
                f'<div class="callout-title">{t("not_implemented.error_report")}</div>'
                f'<p>{t("not_implemented.error_report")}: {html.escape(feature)}</p>'
                f'<div class="code-block">{html.escape(str(e))}</div>'
                f'</div>'
            ),
            errors=[str(e)],
        )
        return 1


def _render_not_implemented(
    feature: str, feat_info: dict, args: argparse.Namespace
) -> int:
    """Render a "feature not implemented" notice

    Args:
        feature: Feature identifier
        feat_info: Feature info
        args: Command-line arguments

    Returns:
        Exit code 1
    """
    logger.warning(f"Feature {feature} not yet implemented (module: {feat_info['module']})")

    print(f"\n{t('error.feature_not_implemented', feature=feat_info['name'])}")
    print(f"  {t('not_implemented.module_path')}: {feat_info['module']}")
    print(f"  {t('not_implemented.current_status')}: {t('error.current_status')}")
    print(f"  {t('not_implemented.planned_phases')}:")
    print(f"    {t('not_implemented.p2')}")
    print(f"    {t('not_implemented.p3')}")
    print(f"    {t('not_implemented.p4')}")
    print(f"    {t('not_implemented.p5')}")
    print(f"    {t('not_implemented.p6')}")
    print(f"  {t('not_implemented.reference')}\n")

    generate_unified_output(
        feature=feature,
        status="error",
        input_summary=vars(args) if args else {},
        result={},
        title=f"{feat_info['name']} - {t('error.feature_not_implemented', feature='')}",
        html_content=(
            f'<div class="callout yellow">'
            f'<div class="callout-title">{t("not_implemented.title")}</div>'
            f'<p>{t("not_implemented.message", name=html.escape(feat_info["name"]))}</p>'
            f'<p>{t("not_implemented.planned_phases")}:</p>'
            f'<ul>'
            f'<li>{t("not_implemented.p2")}</li>'
            f'<li>{t("not_implemented.p3")}</li>'
            f'<li>{t("not_implemented.p4")}</li>'
            f'<li>{t("not_implemented.p5")}</li>'
            f'<li>{t("not_implemented.p6")}</li>'
            f'</ul>'
            f'<p>{t("not_implemented.module_path")}: <code>{html.escape(feat_info["module"])}</code></p>'
            f'</div>'
        ),
        errors=[t("error.feature_not_implemented", feature=feature)],
    )
    return 1


def run_task_from_config(config_path: str) -> int:
    """Run tasks from a JSON config file in batch mode

    Config file format:
    {
        "tasks": [
            {
                "feature": "jar_parser",
                "args": {
                    "jar_path": "D:\\mods\\create.jar",
                    "output": "D:\\output"
                }
            },
            ...
        ]
    }

    Args:
        config_path: JSON config file path

    Returns:
        Exit code (0=all success, 1=has failures)
    """
    config_path = Path(config_path)
    if not config_path.exists():
        logger.error(f"Config file not found: {config_path}")
        print(f"❌ {t('error.config_not_found', path=config_path)}", flush=True)
        return 1

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            task_config = json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Config file JSON parse failed: {config_path} - {e}")
        print(f"❌ {t('error.config_parse_failed', path=config_path)}: {e}", flush=True)
        return 1

    tasks = task_config.get("tasks", [])
    if not tasks:
        logger.warning("No tasks in config file")
        print(f"⚠️  {t('common.no_data')}", flush=True)
        return 0

    logger.info(f"Loaded {len(tasks)} tasks from config file: {config_path.name}")
    print(f"\n📋 {t('examples.config')} ({config_path.name}): {len(tasks)} {t('common.import')}\n")

    exit_code = 0
    for i, task in enumerate(tasks, 1):
        feature = task.get("feature")
        task_args = task.get("args", {})

        if not feature:
            logger.warning(f"Task {i} missing feature field, skipping")
            print(f"  ⚠️  {t('warning.limited')}: task #{i} missing 'feature' field", flush=True)
            continue

        print(f"  ▶ [{i}/{len(tasks)}] {feature} ...", flush=True)

        args = argparse.Namespace(**task_args)
        if not hasattr(args, "output"):
            args.output = config.DEFAULTS["output_dir"]

        result = dispatch_feature(feature, args)
        if result != 0:
            exit_code = 1

    print()
    return exit_code


def build_arg_parser() -> argparse.ArgumentParser:
    """Build command-line argument parser

    Contains all F1-F9 feature parameters, specify the feature via --feature
    """
    parser = argparse.ArgumentParser(
        prog="mc-skill",
        description=t("banner.tagline"),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{t('examples.title')}
{t('examples.cmd')}
{t('examples.cmd_example')}

{t('examples.config')}
{t('examples.config_example')}

{t('examples.lang')}
{t('examples.lang_example')}

{t('examples.features_title')}
  jar_parser       {t('feature.f1.name')}
  mod_searcher     {t('feature.f2.name')}
  env_builder      {t('feature.f3.name')}
  mixin_scanner    {t('feature.f4.name')}
  repacker         {t('feature.f5.name')}
  save_sync        {t('feature.f6.name')}
  translator       {t('feature.f7.name')}
  crash_analyzer   {t('feature.f8.name')}
  auto_fix         {t('feature.f8_1.name')}
  migration_assess {t('feature.f9.name')}
        """,
    )

    parser.add_argument(
        "--feature",
        choices=list(FEATURES.keys()),
        help=t("help.feature"),
    )
    parser.add_argument(
        "--config",
        help=t("help.config"),
    )
    parser.add_argument(
        "--output",
        default=config.DEFAULTS["output_dir"],
        help=t("help.output", default=config.DEFAULTS["output_dir"]),
    )
    parser.add_argument(
        "--lang",
        choices=list(get_supported_languages().keys()),
        help=t("help.lang"),
    )

    parser.add_argument(
        "--jar-path",
        help=t("help.jar_path"),
    )
    parser.add_argument(
        "--detail-level",
        choices=["basic", "detailed"],
        default="basic",
        help=t("help.detail_level"),
    )

    parser.add_argument(
        "--query",
        help=t("help.query"),
    )
    parser.add_argument(
        "--mc-version",
        help=t("help.mc_version"),
    )
    parser.add_argument(
        "--loader",
        choices=config.LOADERS,
        help=t("help.loader"),
    )
    parser.add_argument(
        "--download",
        type=lambda x: x.lower() in ("true", "1", "yes"),
        default=True,
        help=t("help.download"),
    )
    parser.add_argument(
        "--with-deps",
        type=lambda x: x.lower() in ("true", "1", "yes"),
        default=True,
        help=t("help.with_deps"),
    )
    parser.add_argument(
        "--platform",
        choices=["modrinth", "curseforge", "both"],
        default="modrinth",
        help=t("help.platform"),
    )

    parser.add_argument(
        "--launcher",
        choices=config.LAUNCHERS,
        help=t("help.launcher"),
    )
    parser.add_argument(
        "--device",
        choices=config.DEVICES,
        default="pc",
        help=t("help.device"),
    )

    parser.add_argument(
        "--mods-dir",
        help=t("help.mods_dir"),
    )
    parser.add_argument(
        "--severity",
        choices=["summary", "full"],
        default="summary",
        help=t("help.severity"),
    )

    parser.add_argument(
        "--resources-dir",
        help=t("help.resources_dir"),
    )
    parser.add_argument(
        "--validate",
        type=lambda x: x.lower() in ("true", "1", "yes"),
        default=True,
        help=t("help.validate"),
    )

    parser.add_argument(
        "--action",
        choices=["setup", "backup", "restore"],
        help=t("help.action"),
    )
    parser.add_argument(
        "--sync-dir",
        help=t("help.sync_dir"),
    )

    parser.add_argument(
        "--target-lang",
        default="zh_cn",
        help=t("help.target_lang"),
    )
    parser.add_argument(
        "--patch-only",
        action="store_true",
        help=t("help.patch_only"),
    )

    parser.add_argument(
        "--crash-log",
        help=t("help.crash_log"),
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help=t("help.offline"),
    )

    parser.add_argument(
        "--fix-mods-dir",
        help=t("help.fix_mods_dir"),
    )
    parser.add_argument(
        "--auto-confirm",
        action="store_true",
        help=t("help.auto_confirm"),
    )

    parser.add_argument(
        "--from-mc-version",
        help=t("help.from_mc_version"),
    )
    parser.add_argument(
        "--to-mc-version",
        help=t("help.to_mc_version"),
    )
    parser.add_argument(
        "--from-loader",
        choices=["forge", "neoforge", "fabric", "quilt"],
        help=t("help.from_loader"),
    )
    parser.add_argument(
        "--to-loader",
        choices=["forge", "neoforge", "fabric", "quilt"],
        help=t("help.to_loader"),
    )

    parser.add_argument(
        "--auth-status",
        action="store_true",
        help=t("help.auth_status"),
    )
    parser.add_argument(
        "--activate",
        help=t("help.activate"),
    )
    parser.add_argument(
        "--set-tier",
        choices=["free", "normal", "premium"],
        help=t("help.set_tier"),
    )
    parser.add_argument(
        "--reset-usage",
        action="store_true",
        help=t("help.reset_usage"),
    )
    parser.add_argument(
        "--reset-free-period",
        action="store_true",
        help=t("help.reset_free_period"),
    )

    return parser


def print_banner():
    """Print program startup banner"""
    title = t("banner.title")
    subtitle = t("banner.subtitle")
    features = t("banner.features")
    banner = f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   {title}  {t('banner.version')}                                ║
║   {subtitle}                                                 ║
║                                                              ║
║   {features}                                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def main(argv: Optional[list] = None) -> int:
    """Main entry point

    Args:
        argv: List of command-line arguments, None means use sys.argv

    Returns:
        Exit code 0=success 1=failure
    """
    print_banner()

    config.ensure_output_dirs()

    parser = build_arg_parser()
    args = parser.parse_args(argv)

    if args.lang:
        set_language(args.lang)
        save_language_preference(args.lang)
        print(t("lang.set_success", lang=args.lang))
        print_banner()
        return 0

    if args.config:
        return run_task_from_config(args.config)

    if args.auth_status:
        from core.auth_manager import print_auth_status
        print_auth_status()
        return 0

    if args.activate:
        from core.auth_manager import activate_license
        result = activate_license(args.activate)
        print(f"{t('auth.activate_result')}: {result['message']}", flush=True)
        return 0 if result["success"] else 1

    if args.set_tier:
        from core.auth_manager import set_tier
        set_tier(args.set_tier)
        print(t("auth.tier_set", tier=args.set_tier), flush=True)
        return 0

    if args.reset_usage:
        from core.auth_manager import reset_usage
        reset_usage()
        print(t("auth.usage_reset"), flush=True)
        return 0

    if args.reset_free_period:
        from core.auth_manager import reset_free_period
        reset_free_period()
        print(t("auth.free_period_reset"), flush=True)
        return 0

    if not args.feature:
        parser.print_help()
        print(f"\n{t('error.missing_feature')}")
        return 1

    return dispatch_feature(args.feature, args)


if __name__ == "__main__":
    sys.exit(main())
