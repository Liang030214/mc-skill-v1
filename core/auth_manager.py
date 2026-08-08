# -*- coding: utf-8 -*-
"""授权管理模块 - 付费体系框架

功能：
1. 机器码生成 - 唯一标识用户设备
2. 使用次数计数 - 本地JSON存储，每日重置
3. 会员等级判断 - free / normal（premium 为"敬请期待"）
4. 60天免费期机制 - 首次使用算起60天内除移植评估外全部免费
5. 在线验证接口 - 预留HTTP验证URL
6. 全局开关 - ENABLE_PAYMENT 控制是否显示付费提示和允许升级

付费体系（V1）：
- 免费用户：全自动20次/日，半自动8次/日（免费期结束后自动应用）
- 普通会员：8.88元/月 | 23.88元/季 | 88.88元/年（连续包月）
- 高级会员：敬请期待（不开放）
- 单次按需：9.9/49.9/89.9/39.9元

免费期规则：
- 从首次使用当天算起60天
- 期间除"模组移植可行性评估报告"外所有功能免费
- "模组移植可行性评估报告"：首次免费，之后每天1次
- 60天后自动开启付费机制（免费用户20次/天，普通会员100次/天）
"""

import hashlib
import json
import logging
import os
import platform
import socket
import uuid
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import Any, Dict, Optional

from core.i18n import t

logger = logging.getLogger(__name__)

# === 付费全局开关 ===
# False = 付费机制未正式开启（仍限制次数，但显示友好提示）
# True  = 付费机制已正式开启（显示升级选项，允许购买会员）
# 注意：此开关只控制是否显示付费提示，不控制次数限制
# 次数限制在免费期结束后自动应用
ENABLE_PAYMENT = False

# === 在线验证服务器（预留，后续填写）===
AUTH_SERVER_URL = ""  # 如 "https://api.mc-skill.com/v1/auth"
AUTH_SERVER_TIMEOUT = 10  # 超时秒数

# === 免费期天数 ===
FREE_PERIOD_DAYS = 60  # 首次使用后60天免费期

# === 会员等级 ===
TIER_FREE = "free"        # 免费用户
TIER_NORMAL = "normal"    # 普通会员 8.88元/月
TIER_PREMIUM = "premium"  # 高级会员（敬请期待，暂不开放）

# === 会员等级显示名称（通过 t() 动态获取翻译）===
_TIER_NAME_KEYS = {
    TIER_FREE: "auth.tier.free",
    TIER_NORMAL: "auth.tier.member",
    TIER_PREMIUM: "auth.tier.coming_soon",
}

def _get_tier_name(tier: str) -> str:
    """根据等级获取本地化名称"""
    return t(_TIER_NAME_KEYS.get(tier, "common.unknown"))

# === 功能类型 ===
FUNC_AUTO = "auto"        # 全自动功能（F2/F4/F7/F8等）
FUNC_SEMI = "semi"        # 半自动功能（F3/F6等）

# === 特殊功能：模组移植可行性评估报告 ===
# 免费期内：首次免费，之后每天1次
# 付费期后：免费用户每天1次，普通会员每天5次
SPECIAL_FEATURE_MIGRATION_ASSESS = "migration_assess"

# === 各等级次数限制（免费期结束后自动生效）===
DAILY_LIMITS = {
    TIER_FREE: {
        FUNC_AUTO: 20,       # 全自动每日20次
        FUNC_SEMI: 8,        # 半自动每日8次
        SPECIAL_FEATURE_MIGRATION_ASSESS: 1,  # 移植评估每天1次
    },
    TIER_NORMAL: {
        FUNC_AUTO: 100,      # 普通会员每日100次
        FUNC_SEMI: 50,       # 普通会员每日50次
        SPECIAL_FEATURE_MIGRATION_ASSESS: 5,  # 移植评估每天5次
    },
    # 高级会员敬请期待，不开放
}

# === 普通会员定价 ===
PRICING = {
    "monthly": {
        "name": t("auth.pricing_monthly"),
        "price": 8.88,
        "unit": "元/月",
        "desc": t("auth.pricing_desc_monthly"),
    },
    "monthly_auto": {
        "name": t("auth.pricing_monthly_auto"),
        "price": 8.88,
        "unit": "元/月",
        "desc": t("auth.pricing_desc_monthly_auto"),
    },
    "quarterly": {
        "name": t("auth.pricing_quarterly"),
        "price": 23.88,
        "unit": "元/季",
        "desc": t("auth.pricing_desc_quarterly"),
    },
    "yearly": {
        "name": t("auth.pricing_yearly"),
        "price": 88.88,
        "unit": "元/年",
        "desc": t("auth.pricing_desc_yearly"),
    },
}

# === 单次按需定价 ===
PAY_PER_USE = {
    "migration_assess": {"name": t("auth.per_use_migration_assess"), "price": 9.9},
    "shallow_adapt": {"name": t("auth.per_use_shallow_adapt"), "price": 49.9},
    "deep_diagnosis": {"name": t("auth.per_use_deep_diagnosis"), "price": 89.9},
    "crash_fix": {"name": t("auth.per_use_crash_fix"), "price": 39.9},
}

# === 作者测试设备列表 (仅这些设备会显示完整付费信息) ===
# 普通用户看不到单次按需付费（V1阶段还未实现），使整体更划算
_AUTHOR_MACHINE_IDS = [
    "5184c91c54610b2852a9369f68332286",  # 作者主设备
]


def _is_author_device() -> bool:
    """判断当前设备是否为作者测试设备"""
    # 方式1: 机器码匹配
    if _get_machine_id() in _AUTHOR_MACHINE_IDS:
        return True
    # 方式2: 环境变量 (AUTHOR_MODE=1)
    if os.environ.get("MC_SKILL_AUTHOR_MODE", "0") == "1":
        return True
    return False

# === 本地数据存储 ===
_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
_AUTH_FILE = _DATA_DIR / "auth_state.json"


def _get_machine_id() -> str:
    """生成机器唯一标识码"""
    raw = ""
    try:
        raw += str(uuid.getnode())
    except Exception:
        pass
    try:
        raw += socket.gethostname()
    except Exception:
        pass
    try:
        raw += platform.system() + platform.machine()
    except Exception:
        pass
    return hashlib.md5(raw.encode("utf-8")).hexdigest()[:32]


def _default_auth_state() -> Dict[str, Any]:
    """默认授权状态"""
    return {
        "machine_id": _get_machine_id(),
        "tier": TIER_FREE,
        "license_key": "",
        "license_expires": "",
        "subscription_type": "",  # monthly / monthly_auto / quarterly / yearly
        "first_use_date": "",    # 首次使用日期（YYYY-MM-DD）
        "free_period_end": "",   # 免费期结束日期
        "daily_usage": {},
        "last_reset_date": datetime.now().strftime("%Y-%m-%d"),
        "total_usage": {},
        "migration_assess_first_used": False,  # 移植评估是否已使用过首次免费
    }


def _load_auth_state() -> Dict[str, Any]:
    """加载本地授权状态"""
    if not _AUTH_FILE.exists():
        return _default_auth_state()
    try:
        with open(_AUTH_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
        # 检查是否需要重置每日计数
        today = datetime.now().strftime("%Y-%m-%d")
        if state.get("last_reset_date") != today:
            state["daily_usage"] = {}
            state["last_reset_date"] = today
            _save_auth_state(state)
        return state
    except Exception as e:
        logger.warning(f"加载授权状态失败: {e}")
        return _default_auth_state()


def _save_auth_state(state: Dict[str, Any]) -> None:
    """保存授权状态到本地"""
    try:
        _DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(_AUTH_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.warning(f"保存授权状态失败: {e}")


def _get_today_key() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def _ensure_first_use_recorded(state: Dict[str, Any]) -> Dict[str, Any]:
    """确保首次使用日期已记录

    如果是首次使用，记录当天日期并设置60天后的免费期结束日期
    """
    if not state.get("first_use_date"):
        today = date.today()
        state["first_use_date"] = today.strftime("%Y-%m-%d")
        free_end = today + timedelta(days=FREE_PERIOD_DAYS)
        state["free_period_end"] = free_end.strftime("%Y-%m-%d")
        _save_auth_state(state)
        logger.info(f"记录首次使用日期: {state['first_use_date']}, 免费期至: {state['free_period_end']}")
    return state


def is_in_free_period() -> bool:
    """判断当前是否在免费期内

    Returns:
        True = 在免费期内（前60天）
        False = 免费期已过，需要付费
    """
    state = _load_auth_state()
    state = _ensure_first_use_recorded(state)

    free_end_str = state.get("free_period_end", "")
    if not free_end_str:
        return True  # 没有记录结束日期，视为免费期

    try:
        free_end = datetime.strptime(free_end_str, "%Y-%m-%d").date()
        return date.today() <= free_end
    except Exception:
        return True


def get_free_period_info() -> Dict[str, Any]:
    """获取免费期信息"""
    state = _load_auth_state()
    state = _ensure_first_use_recorded(state)

    first_use = state.get("first_use_date", "")
    free_end_str = state.get("free_period_end", "")

    if not free_end_str:
        return {
            "in_free_period": True,
            "first_use_date": first_use,
            "free_period_end": "",
            "days_remaining": FREE_PERIOD_DAYS,
        }

    try:
        free_end = datetime.strptime(free_end_str, "%Y-%m-%d").date()
        today = date.today()
        # 使用 ceil 逻辑：最后一天显示剩余1天而不是0天
        days_remaining = (free_end - today).days
        if days_remaining <= 0 and today <= free_end:
            days_remaining = 1
        else:
            days_remaining = max(0, days_remaining)
        return {
            "in_free_period": today <= free_end,
            "first_use_date": first_use,
            "free_period_end": free_end_str,
            "days_remaining": days_remaining,
        }
    except Exception:
        return {
            "in_free_period": True,
            "first_use_date": first_use,
            "free_period_end": free_end_str,
            "days_remaining": FREE_PERIOD_DAYS,
        }


def get_current_tier() -> str:
    """获取当前会员等级"""
    state = _load_auth_state()
    return state.get("tier", TIER_FREE)


def get_machine_id() -> str:
    """获取当前机器码"""
    return _get_machine_id()


def get_usage_stats() -> Dict[str, Any]:
    """获取使用统计"""
    state = _load_auth_state()
    state = _ensure_first_use_recorded(state)
    tier = state.get("tier", TIER_FREE)
    daily = state.get("daily_usage", {})
    total = state.get("total_usage", {})
    limits = DAILY_LIMITS.get(tier, DAILY_LIMITS[TIER_FREE])
    free_info = get_free_period_info()

    return {
        "machine_id": state.get("machine_id", ""),
        "tier": tier,
        "tier_name": _get_tier_name(tier),
        "daily_usage": daily,
        "total_usage": total,
        "daily_limits": limits,
        "payment_enabled": ENABLE_PAYMENT,
        "license_key": state.get("license_key", ""),
        "license_expires": state.get("license_expires", ""),
        "subscription_type": state.get("subscription_type", ""),
        "first_use_date": state.get("first_use_date", ""),
        "free_period_end": state.get("free_period_end", ""),
        "in_free_period": free_info["in_free_period"],
        "days_remaining": free_info["days_remaining"],
        "pricing": PRICING,
        "premium_status": t("auth.tier.coming_soon"),
    }


def check_permission(feature: str, func_type: str = FUNC_AUTO) -> Dict[str, Any]:
    """检查功能使用权限

    权限判断逻辑：
    1. 如果在免费期内（前60天）：
       - 移植评估功能：首次免费，之后每天1次
       - 其他功能：不限次数
    2. 如果免费期已过：
       - 自动应用基础限制（免费用户20次/天，普通会员100次/天）
       - ENABLE_PAYMENT 只控制是否显示付费提示和允许升级
    """
    state = _load_auth_state()
    state = _ensure_first_use_recorded(state)

    # === 特殊功能：模组移植可行性评估 ===
    if feature == SPECIAL_FEATURE_MIGRATION_ASSESS:
        return _check_migration_assess_permission(state)

    # === 免费期内：其他功能不限 ===
    free_info = get_free_period_info()
    if free_info["in_free_period"]:
        return {
            "allowed": True,
            "tier": state.get("tier", TIER_FREE),
            "remaining": -1,
            "limit": -1,
            "reason": t("auth.free_period_remaining", days=free_info['days_remaining']),
        }

    # === 免费期过后：自动应用基础限制 ===
    tier = state.get("tier", TIER_FREE)
    limits = DAILY_LIMITS.get(tier, DAILY_LIMITS[TIER_FREE])
    limit = limits.get(func_type, 20)

    daily = state.get("daily_usage", {})
    used = daily.get(feature, 0)

    if used >= limit:
        # 构建提示信息
        if ENABLE_PAYMENT:
            upgrade_hint = t("auth.upgrade_hint_enable", max=100)
            try:
                from core.payment_page import show_payment_page
                show_payment_page(reason=f"{t('auth.limit_reached', used=limit, limit=limit)}, {t('auth.upgrade_hint_enable', max=100)}")
            except Exception:
                pass
        else:
            upgrade_hint = t("auth.upgrade_hint_disable")
        return {
            "allowed": False,
            "tier": tier,
            "remaining": 0,
            "limit": limit,
            "reason": f"{t('auth.limit_reached', used=limit, limit=limit)}, {upgrade_hint}",
        }

    return {
        "allowed": True,
        "tier": tier,
        "remaining": limit - used,
        "limit": limit,
        "reason": "",
    }


def _check_migration_assess_permission(state: Dict[str, Any]) -> Dict[str, Any]:
    """检查模组移植可行性评估功能的权限

    规则：
    - 免费期内：首次免费，之后每天1次
    - 付费期后：免费用户每天1次，普通会员每天5次
    """
    free_info = get_free_period_info()
    tier = state.get("tier", TIER_FREE)

    # 首次使用免费
    first_used = state.get("migration_assess_first_used", False)
    today = _get_today_key()
    daily = state.get("daily_usage", {})
    today_used = daily.get(SPECIAL_FEATURE_MIGRATION_ASSESS, 0)

    if free_info["in_free_period"]:
        # 免费期内
        if not first_used:
            # 首次使用，免费
            return {
                "allowed": True,
                "tier": tier,
                "remaining": 1,
                "limit": 1,
                "reason": t("auth.migration_assess_first_free"),
                "is_first_use": True,
            }
        else:
            if today_used >= 1:
                return {
                    "allowed": False,
                    "tier": tier,
                    "remaining": 0,
                    "limit": 1,
                    "reason": t("auth.migration_assess_limit_reached", count=1),
                    "is_first_use": False,
                }
            return {
                "allowed": True,
                "tier": tier,
                "remaining": 1 - today_used,
                "limit": 1,
                "reason": t("auth.migration_assess_daily_free", count=1),
                "is_first_use": False,
            }
    else:
        # 付费期（免费期结束后自动应用限制）
        limits = DAILY_LIMITS.get(tier, DAILY_LIMITS[TIER_FREE])
        limit = limits.get(SPECIAL_FEATURE_MIGRATION_ASSESS, 1)

        if today_used >= limit:
            if ENABLE_PAYMENT:
                upgrade_hint = t("auth.upgrade_hint_enable", max=5)
            else:
                upgrade_hint = t("auth.upgrade_hint_disable")
            return {
                "allowed": False,
                "tier": tier,
                "remaining": 0,
                "limit": limit,
                "reason": f"{t('auth.limit_reached', used=limit, limit=limit)}, {upgrade_hint}",
                "is_first_use": not first_used,
            }

        return {
            "allowed": True,
            "tier": tier,
            "remaining": limit - today_used,
            "limit": limit,
            "reason": "",
            "is_first_use": not first_used,
        }


def record_usage(feature: str) -> None:
    """记录一次功能使用"""
    state = _load_auth_state()
    state = _ensure_first_use_recorded(state)
    daily = state.get("daily_usage", {})
    total = state.get("total_usage", {})

    daily[feature] = daily.get(feature, 0) + 1
    total[feature] = total.get(feature, 0) + 1

    # 移植评估特殊：标记首次使用
    if feature == SPECIAL_FEATURE_MIGRATION_ASSESS:
        state["migration_assess_first_used"] = True

    state["daily_usage"] = daily
    state["total_usage"] = total
    _save_auth_state(state)

    logger.debug(f"记录使用: {feature}, 今日={daily[feature]}, 总计={total[feature]}")


def activate_license(license_key: str, tier: str = TIER_NORMAL,
                     expires: str = "", subscription_type: str = "monthly") -> Dict[str, Any]:
    """激活授权码

    Args:
        license_key: 授权码
        tier: 会员等级（目前仅支持 normal，premium 为敬请期待）
        expires: 过期时间（YYYY-MM-DD）
        subscription_type: 订阅类型 monthly/monthly_auto/quarterly/yearly
    """
    if tier == TIER_PREMIUM:
        return {
            "success": False,
            "tier": tier,
            "message": t("auth.premium_coming_soon"),
        }

    state = _load_auth_state()
    state["tier"] = tier
    state["license_key"] = license_key
    state["license_expires"] = expires
    state["subscription_type"] = subscription_type

    _save_auth_state(state)
    logger.info(f"授权激活成功: tier={tier}, expires={expires}, sub={subscription_type}")

    sub_name = PRICING.get(subscription_type, {}).get("name", subscription_type)
    return {
        "success": True,
        "tier": tier,
        "license_key": license_key,
        "expires": expires,
        "subscription_type": subscription_type,
        "message": t("auth.activate_success", tier=_get_tier_name(tier), subscription=sub_name, expires=expires),
    }


def verify_license_online(license_key: str) -> Dict[str, Any]:
    """在线验证授权码（预留接口）"""
    if not AUTH_SERVER_URL:
        logger.info("未配置在线验证服务器，使用本地验证")
        return {
            "success": False,
            "online": False,
            "reason": "在线验证服务暂未开放，请使用本地激活",
        }

    try:
        from urllib.request import Request, urlopen
        req_data = json.dumps({
            "license_key": license_key,
            "machine_id": _get_machine_id(),
        }).encode("utf-8")

        req = Request(
            f"{AUTH_SERVER_URL}/verify",
            data=req_data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "MC-Skill-V1/1.0",
            },
            method="POST",
        )

        with urlopen(req, timeout=AUTH_SERVER_TIMEOUT) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result

    except Exception as e:
        logger.error(f"在线验证失败: {e}")
        return {
            "success": False,
            "online": True,
            "reason": f"验证服务连接失败: {str(e)}",
        }


def reset_usage() -> None:
    """重置使用计数（调试用）"""
    state = _load_auth_state()
    state["daily_usage"] = {}
    state["total_usage"] = {}
    state["last_reset_date"] = _get_today_key()
    _save_auth_state(state)
    logger.info("使用计数已重置")


def set_tier(tier: str) -> None:
    """设置会员等级（调试/管理用）"""
    state = _load_auth_state()
    state["tier"] = tier
    _save_auth_state(state)
    logger.info(f"会员等级已设置为: {tier}")


def reset_free_period() -> None:
    """重置免费期（调试用，清除首次使用日期）"""
    state = _load_auth_state()
    state["first_use_date"] = ""
    state["free_period_end"] = ""
    state["migration_assess_first_used"] = False
    _save_auth_state(state)
    logger.info("免费期已重置")


def enable_payment() -> None:
    """启用付费限制（全局）"""
    global ENABLE_PAYMENT
    ENABLE_PAYMENT = True
    logger.info("付费限制已启用")


def disable_payment() -> None:
    """禁用付费限制（全局）"""
    global ENABLE_PAYMENT
    ENABLE_PAYMENT = False
    logger.info("付费限制已禁用")


def print_auth_status() -> None:
    """打印当前授权状态"""
    stats = get_usage_stats()
    print("=" * 55, flush=True)
    print(f"  {t('banner.title')} - {t('auth.title')}", flush=True)
    print("=" * 55, flush=True)
    print(f"  {t('auth.machine_id')}: {stats['machine_id']}", flush=True)
    print(f"  {t('auth.member_tier')}: {stats['tier_name']}", flush=True)
    print(f"  {t('auth.payment_methods')}: {'✅' if stats['payment_enabled'] else '⏳'}", flush=True)
    print(f"  {t('auth.auth_code')}: {stats['license_key'] or t('auth.not_activated')}", flush=True)
    print(f"  {t('auth.expiry_date')}: {stats['license_expires'] or '—'}", flush=True)

    # 免费期信息
    if stats["in_free_period"]:
        print(f"\n  ┌─────────────────────────────────", flush=True)
        print(f"  │  {t('auth.free_period')} ({t('auth.remaining')} {stats['days_remaining']} days)", flush=True)
        print(f"  │  {t('auth.first_use_date')}: {stats['first_use_date'] or '—'}", flush=True)
        print(f"  │  {t('auth.free_until')}: {stats['free_period_end'] or '—'}", flush=True)
        print(f"  └─────────────────────────────────", flush=True)
    else:
        print(f"\n  ┌─────────────────────────────────", flush=True)
        print(f"  │  {t('auth.free_period')}: {t('auth.expired')} ({stats['free_period_end']})", flush=True)
        print(f"  │  {t('auth.tier.free')}: {stats['daily_limits'].get('auto', 20)}/day", flush=True)
        print(f"  └─────────────────────────────────", flush=True)

    # 使用统计
    print(f"\n  {t('auth.today_usage')}:", flush=True)
    for feat, count in stats["daily_usage"].items():
        feat_name = {"migration_assess": t("feature.f9.name")}.get(feat, feat)
        limit = stats["daily_limits"].get(feat, stats["daily_limits"].get("auto", 20))
        if limit > 0:
            print(f"    {feat_name}: {count}/{limit}", flush=True)
        else:
            print(f"    {feat_name}: {count} ({t('auth.unlimited')})", flush=True)
    if not stats["daily_usage"]:
        print(f"    ({t('common.no_data')})", flush=True)

    print(f"\n  {t('auth.total_usage')}:", flush=True)
    for feat, count in stats["total_usage"].items():
        feat_name = {"migration_assess": t("feature.f9.name")}.get(feat, feat)
        print(f"    {feat_name}: {count}", flush=True)
    if not stats["total_usage"]:
        print(f"    ({t('common.no_data')})", flush=True)

    # 定价信息
    print(f"\n  {t('auth.member_subscription')}:", flush=True)
    for key, info in stats["pricing"].items():
        print(f"    {info['name']}: {info['price']}{info['unit']} ({info['desc']})", flush=True)

    # 单次按需付费：仅作者设备可见（V1阶段功能未实现，对普通用户隐藏）
    if _is_author_device():
        print(f"\n  {t('auth.per_use_payment')} {t('auth.author_test_only')}:", flush=True)
        for key, info in PAY_PER_USE.items():
            print(f"    {info['name']}: {info['price']} CNY/use", flush=True)

    print(f"\n  {t('auth.premium_coming_soon')}", flush=True)
    print("=" * 55, flush=True)
