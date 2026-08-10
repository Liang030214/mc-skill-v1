# -*- coding: utf-8 -*-
"""付费引导页面模块

V1.0.2: 付费功能已禁用，显示"敬请期待"占位页面。
后续版本将实现完整的付费订阅功能。
"""

import os
from datetime import datetime
from pathlib import Path

from core.i18n import t

# === 资源目录 ===
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_OUTPUT_DIR = _PROJECT_ROOT / "output"


def _build_placeholder_html(reason: str = "") -> str:
    """生成付费功能占位页面（敬请期待）"""

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MC Skill V1 - {t("payment.title")}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: -apple-system, "Microsoft YaHei", "Segoe UI", sans-serif;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    color: #333; min-height: 100vh; padding: 20px;
    display: flex; align-items: center; justify-content: center;
  }}
  .container {{
    max-width: 500px; width: 100%; text-align: center;
    background: #fff; border-radius: 16px; padding: 40px 30px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
  }}
  .icon {{
    font-size: 64px; margin-bottom: 20px;
  }}
  h1 {{
    font-size: 24px; color: #1a1a2e; margin-bottom: 12px;
    background: linear-gradient(90deg, #3a7bd5, #00d2ff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  }}
  .subtitle {{
    font-size: 14px; color: #666; margin-bottom: 24px; line-height: 1.6;
  }}
  .reason {{
    background: #fff3e0; border: 1px solid #ff9800; border-radius: 8px;
    padding: 12px 16px; margin-bottom: 20px; color: #e65100; font-size: 14px;
  }}
  .info-box {{
    background: #f5f5fa; border-radius: 10px; padding: 20px;
    text-align: left; margin-bottom: 20px;
  }}
  .info-box h3 {{
    font-size: 16px; color: #1a1a2e; margin-bottom: 12px;
  }}
  .info-box p {{
    font-size: 13px; color: #666; line-height: 1.8;
  }}
  .feature-list {{
    list-style: none; padding: 0;
  }}
  .feature-list li {{
    padding: 8px 0; font-size: 13px; color: #555;
    border-bottom: 1px solid #eee;
  }}
  .feature-list li:last-child {{
    border-bottom: none;
  }}
  .feature-list li::before {{
    content: "✓ "; color: #4caf50; font-weight: bold;
  }}
  .btn {{
    display: inline-block; padding: 12px 32px; border-radius: 25px;
    text-decoration: none; font-size: 15px; font-weight: 600;
    background: linear-gradient(90deg, #3a7bd5, #00d2ff);
    color: #fff; border: none; cursor: pointer;
    transition: all 0.3s; margin: 5px;
  }}
  .btn:hover {{
    transform: scale(1.05); box-shadow: 0 4px 15px rgba(58, 123, 213, 0.4);
  }}
  .footer {{
    margin-top: 24px; font-size: 12px; color: #999;
  }}
</style>
</head>
<body>
<div class="container">
  <div class="icon">🚧</div>
  <h1>{t("payment.coming_soon_title")}</h1>
  <p class="subtitle">{t("payment.coming_soon_subtitle")}</p>

  {"<div class='reason'>⚠️ " + reason + "</div>" if reason else ""}

  <div class="info-box">
    <h3>{t("payment.whats_included")}</h3>
    <ul class="feature-list">
      <li>{t("payment.feature_unlimited")}</li>
      <li>{t("payment.feature_priority")}</li>
      <li>{t("payment.feature_exclusive")}</li>
      <li>{t("payment.feature_support")}</li>
    </ul>
  </div>

  <button class="btn" onclick="window.close()">{t("payment.btn_close")}</button>

  <div class="footer">
    {t("payment.current_time")}: {now}
  </div>
</div>
</body>
</html>"""
    return html


def show_payment_page(reason: str = "") -> bool:
    """显示付费功能占位页面（V1.0.2: 仅生成HTML，不打开浏览器）

    Args:
        reason: 触发原因（如"免费期已结束"、"今日使用次数已达上限"等）

    Returns:
        True 表示页面成功生成，False 表示失败
    """
    try:
        _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        html = _build_placeholder_html(reason)

        html_path = _OUTPUT_DIR / "payment_guide.html"
        html_path.write_text(html, encoding="utf-8")

        print(f"\n{'='*50}", flush=True)
        print(f"  {t('payment.coming_soon_title')}", flush=True)
        print(f"  {t('payment.page_path', path=str(html_path))}", flush=True)
        print(f"  {t('payment.coming_soon_notice')}", flush=True)
        print(f"{'='*50}", flush=True)
        return True

    except Exception as e:
        print(f"[Error] {t('payment.open_failed')}: {e}", flush=True)
        return False


if __name__ == "__main__":
    show_payment_page(reason="测试预览 - 付费功能敬请期待")
