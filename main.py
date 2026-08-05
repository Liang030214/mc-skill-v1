"""MC全生态智能适配工程师 V1 - 主入口

功能：
1. 命令行参数解析（argparse）
2. JSON配置文件批量任务支持
3. 功能路由（F1-F8）
4. 统一返回结构输出

使用方式:
    # 命令行模式
    python main.py --feature jar_parser --jar-path "D:\\mods\\create.jar"

    # JSON配置模式
    python main.py --config "task.json"
"""

import sys
import os
import argparse
import json
import html
from pathlib import Path
from typing import Optional

# 将项目根目录加入sys.path，便于包导入
_PROJECT_ROOT = Path(__file__).resolve().parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import config
from utils.logger import get_logger
from utils.report_gen import generate_unified_output

logger = get_logger("main")


# === 功能路由表 ===
# 每个功能对应一个执行函数，未实现的功能显示提示
FEATURES = {
    "jar_parser": {
        "name": "F1 JAR结构解析",
        "module": "core.jar_parser",
        "function": "run",
        "status": "implemented",
    },
    "mod_searcher": {
        "name": "F2 模组检索下载",
        "module": "core.mod_searcher",
        "function": "run",
        "status": "implemented",
    },
    "env_builder": {
        "name": "F3 环境引导搭建",
        "module": "core.env_builder",
        "function": "run",
        "status": "implemented",
    },
    "mixin_scanner": {
        "name": "F4 Mixin冲突扫描",
        "module": "core.mixin_scanner",
        "function": "run",
        "status": "implemented",
    },
    "repacker": {
        "name": "F5 资源级重打包",
        "module": "core.repacker",
        "function": "run",
        "status": "implemented",
    },
    "save_sync": {
        "name": "F6 存档同步",
        "module": "core.save_sync",
        "function": "run",
        "status": "implemented",
    },
    "translator": {
        "name": "F7 基础汉化",
        "module": "core.translator",
        "function": "run",
        "status": "implemented",
    },
    "crash_analyzer": {
        "name": "F8 报错修复",
        "module": "core.crash_analyzer",
        "function": "run",
        "status": "implemented",
    },
    "auto_fix": {
        "name": "F8.1 自动修复",
        "module": "core.auto_fix",
        "function": "auto_fix_run",
        "status": "implemented",
    },
    "migration_assess": {
        "name": "F9 模组移植可行性评估",
        "module": "core.migration_assessor",
        "function": "run",
        "status": "implemented",
    },
}


def dispatch_feature(feature: str, args: argparse.Namespace) -> int:
    """调度指定功能

    Args:
        feature: 功能标识符
        args: 命令行参数

    Returns:
        退出码 0=成功 1=失败
    """
    if feature not in FEATURES:
        logger.error(f"未知的功能: {feature}")
        logger.info(f"可用功能: {', '.join(FEATURES.keys())}")
        return 1

    feat_info = FEATURES[feature]
    logger.info(f"调度功能: {feat_info['name']} ({feature})")

    if feat_info["status"] != "implemented":
        # 模块未实现，输出友好提示
        return _render_not_implemented(feature, feat_info, args)

    # === 权限检查 ===
    try:
        from core.auth_manager import check_permission, record_usage, FUNC_AUTO, FUNC_SEMI
        # 判断功能类型（全自动/半自动）
        func_type = FUNC_SEMI if feature in ("env_builder", "save_sync") else FUNC_AUTO
        perm = check_permission(feature, func_type)
        if not perm["allowed"]:
            logger.warning(f"功能使用受限: {perm['reason']}")
            print(f"\n⚠️  {perm['reason']}", flush=True)
            print(f"   会员等级: {perm['tier']}", flush=True)
            print(f"   今日剩余: {perm['remaining']}/{perm['limit']}次", flush=True)
            print(f"   升级会员可解锁更多次数\n", flush=True)
            return 1
    except Exception as e:
        logger.debug(f"权限检查跳过: {e}")

    try:
        # 动态导入功能模块
        import importlib
        module = importlib.import_module(feat_info["module"])
        func = getattr(module, feat_info["function"])
        result = func(args)
        # 记录使用次数
        try:
            record_usage(feature)
        except Exception:
            pass
        return 0 if result.get("status") != "error" else 1
    except ImportError as e:
        logger.error(f"功能模块导入失败: {feat_info['module']} - {e}")
        return _render_not_implemented(feature, feat_info, args)
    except Exception as e:
        logger.exception(f"功能执行异常: {feature}")
        # 生成错误报告
        generate_unified_output(
            feature=feature,
            status="error",
            input_summary=vars(args),
            result={},
            title=f"{feat_info['name']} - 执行异常",
            html_content=(
                f'<div class="callout red">'
                f'<div class="callout-title">执行异常</div>'
                f'<p>功能 {html.escape(feature)} 执行时发生异常:</p>'
                f'<div class="code-block">{html.escape(str(e))}</div>'
                f'<p>详情请查看运行日志。</p>'
                f'</div>'
            ),
            errors=[str(e)],
        )
        return 1


def _render_not_implemented(
    feature: str, feat_info: dict, args: argparse.Namespace
) -> int:
    """渲染"功能未实现"提示

    Args:
        feature: 功能标识符
        feat_info: 功能信息
        args: 命令行参数

    Returns:
        退出码 1
    """
    logger.warning(f"功能 {feature} 尚未实现 (模块: {feat_info['module']})")

    print(f"\n[提示] 功能 {feat_info['name']} 尚未实现")
    print(f"  模块路径: {feat_info['module']}")
    print(f"  当前状态: P1基础设施层已就绪，此功能将在后续P2-P6阶段实现")
    print(f"  请参考 V1开发指导文件.html 中的技术规格\n")

    # 同时生成HTML报告说明
    generate_unified_output(
        feature=feature,
        status="error",
        input_summary=vars(args) if args else {},
        result={},
        title=f"{feat_info['name']} - 功能尚未实现",
        html_content=(
            f'<div class="callout yellow">'
            f'<div class="callout-title">功能尚未实现</div>'
            f'<p>功能 <strong>{html.escape(feat_info["name"])}</strong> 当前处于未实现状态。</p>'
            f'<p>P1基础设施层已完成，此功能将在后续开发阶段实现：</p>'
            f'<ul>'
            f'<li>P2: F1 JAR结构解析 + F5 资源级重打包</li>'
            f'<li>P3: F2 模组检索下载 + F3 环境引导搭建</li>'
            f'<li>P4: F4 Mixin冲突扫描 + F8 基础报错修复</li>'
            f'<li>P5: F7 基础汉化</li>'
            f'<li>P6: F6 存档同步</li>'
            f'</ul>'
            f'<p>模块路径: <code>{html.escape(feat_info["module"])}</code></p>'
            f'</div>'
        ),
        errors=[f"功能 {feature} 尚未实现"],
    )
    return 1


def run_task_from_config(config_path: str) -> int:
    """从JSON配置文件批量运行任务

    配置文件格式:
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
        config_path: JSON配置文件路径

    Returns:
        退出码 (0=全部成功, 1=有失败)
    """
    config_path = Path(config_path)
    if not config_path.exists():
        logger.error(f"配置文件不存在: {config_path}")
        return 1

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            task_config = json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"配置文件JSON解析失败: {config_path} - {e}")
        return 1

    tasks = task_config.get("tasks", [])
    if not tasks:
        logger.warning("配置文件中无任务")
        return 0

    logger.info(f"从配置文件加载 {len(tasks)} 个任务: {config_path.name}")

    exit_code = 0
    for i, task in enumerate(tasks, 1):
        feature = task.get("feature")
        task_args = task.get("args", {})

        if not feature:
            logger.warning(f"任务 {i} 缺少 feature 字段，跳过")
            continue

        logger.info(f"--- 任务 {i}/{len(tasks)}: {feature} ---")

        # 将args dict转换为argparse Namespace
        args = argparse.Namespace(**task_args)
        # 补充默认值
        if not hasattr(args, "output"):
            args.output = config.DEFAULTS["output_dir"]

        result = dispatch_feature(feature, args)
        if result != 0:
            exit_code = 1

    return exit_code


def build_arg_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器

    包含所有F1-F8功能的参数，通过 --feature 指定要执行的功能
    """
    parser = argparse.ArgumentParser(
        prog="mc-skill",
        description="MC全生态智能适配工程师 V1 - 模组适配、汉化、修复工具集",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 命令行模式
  python main.py --feature jar_parser --jar-path "D:\\mods\\create.jar"

  # JSON配置模式
  python main.py --config "task.json"

可用功能 (feature):
  jar_parser     F1 JAR结构解析与中文释义
  mod_searcher   F2 模组检索与下载
  env_builder    F3 环境引导搭建
  mixin_scanner  F4 Mixin冲突扫描
  repacker       F5 资源级重打包
  save_sync      F6 存档同步
  translator     F7 基础汉化
  crash_analyzer F8 报错修复
  auto_fix       F8.1 自动修复
  migration_assess F9 模组移植可行性评估
        """,
    )

    # === 顶层参数 ===
    parser.add_argument(
        "--feature",
        choices=list(FEATURES.keys()),
        help="要执行的功能标识符",
    )
    parser.add_argument(
        "--config",
        help="JSON配置文件路径（批量任务模式）",
    )
    parser.add_argument(
        "--output",
        default=config.DEFAULTS["output_dir"],
        help=f"输出目录，默认: {config.DEFAULTS['output_dir']}",
    )

    # === F1: JAR结构解析 ===
    parser.add_argument(
        "--jar-path",
        help="JAR文件路径 (F1/F5/F7)",
    )
    parser.add_argument(
        "--detail-level",
        choices=["basic", "detailed"],
        default="basic",
        help="F1 释义详细度: basic(默认) / detailed(反编译.class提取类名和方法签名)",
    )

    # === F2: 模组检索下载 ===
    parser.add_argument(
        "--query",
        help="F2 模组名称或搜索关键词",
    )
    parser.add_argument(
        "--mc-version",
        help="目标MC版本，如 1.21.1 (F2/F3/F6)",
    )
    parser.add_argument(
        "--loader",
        choices=config.LOADERS,
        help="加载器类型 (F2/F3)",
    )
    parser.add_argument(
        "--download",
        type=lambda x: x.lower() in ("true", "1", "yes"),
        default=True,
        help="F2 是否自动下载JAR，默认 true",
    )
    parser.add_argument(
        "--with-deps",
        type=lambda x: x.lower() in ("true", "1", "yes"),
        default=True,
        help="F2 是否自动下载前置依赖，默认 true",
    )
    parser.add_argument(
        "--platform",
        choices=["modrinth", "curseforge", "both"],
        default="modrinth",
        help="F2 优先平台",
    )

    # === F3: 环境引导搭建 ===
    parser.add_argument(
        "--launcher",
        choices=config.LAUNCHERS,
        help="启动器类型 (F3/F6)",
    )
    parser.add_argument(
        "--device",
        choices=config.DEVICES,
        default="pc",
        help="设备类型 pc/mobile (F3/F6)",
    )

    # === F4: Mixin冲突扫描 ===
    parser.add_argument(
        "--mods-dir",
        help="F4 mods文件夹路径",
    )
    # --loader 参数已在F2/F3中定义，choices为config.LOADERS
    parser.add_argument(
        "--severity",
        choices=["summary", "full"],
        default="summary",
        help="F4 报告详细度",
    )

    # === F5: 资源级重打包 ===
    parser.add_argument(
        "--resources-dir",
        help="F5 修改后的资源文件目录",
    )
    parser.add_argument(
        "--validate",
        type=lambda x: x.lower() in ("true", "1", "yes"),
        default=True,
        help="F5 是否校验替换文件的格式，默认 true",
    )

    # === F6: 存档同步 ===
    parser.add_argument(
        "--action",
        choices=["setup", "backup", "restore"],
        help="F6 操作类型",
    )
    parser.add_argument(
        "--sync-dir",
        help="F6 百度网盘同步目录路径",
    )

    # === F7: 基础汉化 ===
    parser.add_argument(
        "--target-lang",
        default="zh_cn",
        help="F7 目标语言，默认 zh_cn",
    )
    parser.add_argument(
        "--patch-only",
        action="store_true",
        help="F7 仅生成汉化补丁文件，不固化进JAR",
    )

    # === F8: 报错修复 ===
    parser.add_argument(
        "--crash-log",
        help="F8 crash report或latest.log文件路径",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="F8 禁用联网查询，仅使用本地数据库",
    )

    # === F8.1: 自动修复 ===
    parser.add_argument(
        "--fix-mods-dir",
        help="F8.1 Minecraft的mods目录路径（用于自动修复）",
    )
    parser.add_argument(
        "--auto-confirm",
        action="store_true",
        help="F8.1 自动修复时跳过确认提示",
    )

    # === F9: 模组移植可行性评估 ===
    parser.add_argument(
        "--from-mc-version",
        help="F9 源MC版本（如 1.20.1）",
    )
    parser.add_argument(
        "--to-mc-version",
        help="F9 目标MC版本（如 1.21.1）",
    )
    parser.add_argument(
        "--from-loader",
        choices=["forge", "neoforge", "fabric", "quilt"],
        help="F9 源加载器",
    )
    parser.add_argument(
        "--to-loader",
        choices=["forge", "neoforge", "fabric", "quilt"],
        help="F9 目标加载器",
    )

    # === 授权管理 ===
    parser.add_argument(
        "--auth-status",
        action="store_true",
        help="查看当前授权状态和使用统计",
    )
    parser.add_argument(
        "--activate",
        help="激活授权码（如 --activate XXXX-XXXX-XXXX）",
    )
    parser.add_argument(
        "--set-tier",
        choices=["free", "normal", "premium"],
        help="设置会员等级（管理用）",
    )
    parser.add_argument(
        "--reset-usage",
        action="store_true",
        help="重置使用计数（调试用）",
    )
    parser.add_argument(
        "--reset-free-period",
        action="store_true",
        help="重置免费期（调试用，清除首次使用日期）",
    )

    return parser


def print_banner():
    """打印程序启动横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   MC全生态智能适配工程师  V1                                 ║
║   MC Ecosystem Adaptation Engineer                           ║
║                                                              ║
║   功能: JAR解析 · 模组检索 · 环境搭建 · 冲突扫描             ║
║         资源重打包 · 存档同步 · 基础汉化 · 报错修复          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def main(argv: Optional[list] = None) -> int:
    """主入口函数

    Args:
        argv: 命令行参数列表，None表示使用sys.argv

    Returns:
        退出码 0=成功 1=失败
    """
    print_banner()

    # 确保输出目录存在
    config.ensure_output_dirs()

    parser = build_arg_parser()
    args = parser.parse_args(argv)

    # JSON配置模式
    if args.config:
        return run_task_from_config(args.config)

    # === 授权管理命令 ===
    if args.auth_status:
        from core.auth_manager import print_auth_status
        print_auth_status()
        return 0

    if args.activate:
        from core.auth_manager import activate_license
        result = activate_license(args.activate)
        print(f"激活结果: {result['message']}", flush=True)
        return 0 if result["success"] else 1

    if args.set_tier:
        from core.auth_manager import set_tier
        set_tier(args.set_tier)
        print(f"会员等级已设置为: {args.set_tier}", flush=True)
        return 0

    if args.reset_usage:
        from core.auth_manager import reset_usage
        reset_usage()
        print("使用计数已重置", flush=True)
        return 0

    if args.reset_free_period:
        from core.auth_manager import reset_free_period
        reset_free_period()
        print("免费期已重置（首次使用日期已清除）", flush=True)
        return 0

    # 命令行模式
    if not args.feature:
        parser.print_help()
        print("\n错误: 必须指定 --feature 或 --config 参数")
        return 1

    return dispatch_feature(args.feature, args)


if __name__ == "__main__":
    sys.exit(main())
