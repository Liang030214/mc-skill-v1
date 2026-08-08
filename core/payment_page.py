# -*- coding: utf-8 -*-
"""付费引导页面模块

当用户免费期结束或次数用完时，自动生成 HTML 页面并在浏览器中打开。
页面展示4个二维码：
1. 微信公众号二维码
2. 爱发电平台二维码
3. 支付宝/微信个人付款联合二维码
4. 小红书/微信商户平台二维码

使用方式：
    from core.payment_page import show_payment_page
    show_payment_page(reason="免费期已结束")
"""

import base64
import os
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

from core.i18n import t

# === 资源目录 ===
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_PAYMENT_DIR = _PROJECT_ROOT / "data" / "payment"
_OUTPUT_DIR = _PROJECT_ROOT / "output"

# === 二维码图片路径 ===
QR_FILES = {
    "wechat_official": _PAYMENT_DIR / "wechat_official.png",
    "afdian":          _PAYMENT_DIR / "afdian.png",
    "personal_pay":    _PAYMENT_DIR / "personal_pay.png",
    "merchant":        _PAYMENT_DIR / "merchant.png",
}

# === 二维码显示信息 ===
QR_INFO = {
    "wechat_official": {
        "title": t("payment.qr_wechat_title"),
        "subtitle": t("payment.qr_wechat_subtitle"),
        "desc": t("payment.qr_wechat_desc"),
    },
    "afdian": {
        "title": t("payment.qr_afdian_title"),
        "subtitle": t("payment.qr_afdian_subtitle"),
        "desc": t("payment.qr_afdian_desc"),
    },
    "personal_pay": {
        "title": t("payment.qr_personal_title"),
        "subtitle": t("payment.qr_personal_subtitle"),
        "desc": t("payment.qr_personal_desc"),
    },
    "merchant": {
        "title": t("payment.qr_merchant_title"),
        "subtitle": t("payment.qr_merchant_subtitle"),
        "desc": t("payment.qr_merchant_desc"),
    },
}


def _image_to_base64(img_path: Path) -> str:
    """将图片文件转为 base64 编码（嵌入 HTML，避免文件路径问题）"""
    if not img_path.exists():
        return ""
    try:
        with open(img_path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        ext = img_path.suffix.lstrip(".").lower()
        if ext == "jpg":
            ext = "jpeg"
        return f"data:image/{ext};base64,{data}"
    except Exception:
        return ""


def _generate_placeholder_svg(text: str, subtext: str = "") -> str:
    """生成占位 SVG 图片（当二维码图片不存在时使用）"""
    lines = text.split("\n")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">
  <rect width="200" height="200" fill="#f0f0f0" stroke="#ccc" stroke-width="2" rx="8"/>
  <text x="100" y="90" text-anchor="middle" font-size="14" fill="#999" font-family="sans-serif">{lines[0] if lines else "二维码"}</text>
  <text x="100" y="115" text-anchor="middle" font-size="12" fill="#bbb" font-family="sans-serif">{subtext}</text>
  <text x="100" y="150" text-anchor="middle" font-size="10" fill="#ccc" font-family="sans-serif">请替换为实际二维码</text>
</svg>'''
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode("utf-8")


def _get_qr_data(key: str) -> str:
    """获取二维码图片数据（base64），如果文件不存在则返回占位图"""
    img_path = QR_FILES.get(key)
    if img_path and img_path.exists():
        return _image_to_base64(img_path)
    info = QR_INFO.get(key, {})
    return _generate_placeholder_svg(info.get("title", "二维码"), "待替换")


def _build_html(reason: str = "") -> str:
    """生成完整的 HTML 付费引导页面"""

    qr_data = {key: _get_qr_data(key) for key in QR_FILES}

    pricing_rows = f"""
    <tr><td>{t("auth.pricing_monthly")}</td><td>{t("payment.pricing_monthly_price")}</td><td>{t("payment.pricing_monthly_desc")}</td></tr>
    <tr><td>{t("auth.pricing_monthly_auto")}</td><td>{t("payment.pricing_monthly_auto_price")}</td><td>{t("payment.pricing_monthly_auto_desc")}</td></tr>
    <tr><td>{t("auth.pricing_quarterly")}</td><td>{t("payment.pricing_quarterly_price")}</td><td>{t("payment.pricing_quarterly_desc")}</td></tr>
    <tr><td>{t("auth.pricing_yearly")}</td><td>{t("payment.pricing_yearly_price")}</td><td>{t("payment.pricing_yearly_desc")}</td></tr>
    """

    tier_rows = f"""
    <tr><td>{t("payment.tier_free")}</td><td>20 次/日</td><td>8 次/日</td><td>1 次/日</td></tr>
    <tr class="highlight"><td>{t("payment.tier_normal")}</td><td>100 次/日</td><td>50 次/日</td><td>5 次/日</td></tr>
    """

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
  }}
  .container {{ max-width: 900px; margin: 0 auto; }}
  .header {{
    text-align: center; padding: 40px 20px; color: #fff;
  }}
  .header h1 {{
    font-size: 28px; margin-bottom: 10px;
    background: linear-gradient(90deg, #00d2ff, #3a7bd5);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  }}
  .header p {{ font-size: 14px; color: #aaa; }}
  .alert {{
    background: rgba(255, 193, 7, 0.15); border: 1px solid rgba(255, 193, 7, 0.4);
    border-radius: 8px; padding: 16px 24px; margin: 20px auto; max-width: 600px;
    text-align: center; color: #ffc107; font-size: 15px;
  }}
  .section {{
    background: #fff; border-radius: 12px; padding: 30px;
    margin-bottom: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  }}
  .section h2 {{
    font-size: 20px; margin-bottom: 20px; padding-bottom: 10px;
    border-bottom: 2px solid #e8e8e8; color: #1a1a2e;
  }}
  /* 二维码网格 */
  .qr-grid {{
    display: grid; grid-template-columns: repeat(2, 1fr);
    gap: 20px; margin-top: 10px;
  }}
  .qr-card {{
    background: #f9f9fc; border-radius: 10px; padding: 20px;
    text-align: center; transition: transform 0.2s;
    border: 2px solid transparent;
  }}
  .qr-card:hover {{
    transform: translateY(-3px); border-color: #3a7bd5;
    box-shadow: 0 4px 15px rgba(58, 123, 213, 0.2);
  }}
  .qr-card img {{
    width: 180px; height: 180px; border-radius: 8px;
    margin-bottom: 12px; border: 1px solid #e0e0e0;
  }}
  .qr-card .qr-title {{
    font-size: 16px; font-weight: 600; color: #1a1a2e; margin-bottom: 4px;
  }}
  .qr-card .qr-sub {{
    font-size: 13px; color: #3a7bd5; margin-bottom: 8px;
  }}
  .qr-card .qr-desc {{
    font-size: 12px; color: #888; line-height: 1.5;
  }}
  /* 定价表 */
  table {{
    width: 100%; border-collapse: collapse; margin-top: 10px;
  }}
  th, td {{
    padding: 12px 16px; text-align: left;
    border-bottom: 1px solid #e8e8e8; font-size: 14px;
  }}
  th {{
    background: #f5f5fa; font-weight: 600; color: #1a1a2e;
  }}
  tr.highlight td {{
    background: rgba(58, 123, 213, 0.08); font-weight: 600;
  }}
  .price-tag {{
    color: #e53935; font-weight: 700;
  }}
  /* 按钮 */
  .btn {{
    display: inline-block; padding: 12px 32px; border-radius: 25px;
    text-decoration: none; font-size: 15px; font-weight: 600;
    transition: all 0.3s; margin: 5px;
  }}
  .btn-primary {{
    background: linear-gradient(90deg, #3a7bd5, #00d2ff); color: #fff;
  }}
  .btn-primary:hover {{
    transform: scale(1.05); box-shadow: 0 4px 15px rgba(58, 123, 213, 0.4);
  }}
  .btn-outline {{
    border: 2px solid #3a7bd5; color: #3a7bd5; background: transparent;
  }}
  .btn-outline:hover {{
    background: #3a7bd5; color: #fff;
  }}
  .btn-row {{
    text-align: center; padding: 20px 0;
  }}
  .footer {{
    text-align: center; color: #666; font-size: 12px;
    padding: 20px; line-height: 1.8;
  }}
  .footer a {{ color: #3a7bd5; text-decoration: none; }}
  .tip-box {{
    background: #e8f5e9; border-left: 4px solid #4caf50;
    padding: 12px 20px; margin: 15px 0; border-radius: 4px;
    font-size: 14px; color: #2e7d32;
  }}
  @media (max-width: 600px) {{
    .qr-grid {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>
<div class="container">

  <!-- 标题 -->
  <div class="header">
    <h1>{t("payment.header_title")}</h1>
    <p>{t("payment.header_subtitle")}</p>
  </div>

  <!-- 提醒 -->
  <div class="alert">
    {'⚠️ ' + reason if reason else '⚠️ ' + t("payment.free_expired")}
    <br><small>{t("payment.current_time")}: {now}</small>
  </div>

  <!-- 会员等级对比 -->
  <div class="section">
    <h2>{t("payment.compare_tiers")}</h2>
    <table>
      <thead>
        <tr><th>{t("payment.column_tier")}</th><th>{t("payment.column_auto")}</th><th>{t("payment.column_semi")}</th><th>{t("payment.column_migration")}</th></tr>
      </thead>
      <tbody>
        {tier_rows}
      </tbody>
    </table>
    <div class="tip-box">
      {t("payment.tip_normal")}
    </div>
  </div>

  <!-- 4个二维码 -->
  <div class="section">
    <h2>{t("payment.scan_title")}</h2>
    <p style="color:#666; font-size:14px; margin-bottom:15px;">
      {t("payment.scan_desc")}
    </p>
    <div class="qr-grid">

      <!-- 1. 微信公众号 -->
      <div class="qr-card">
        <img src="{qr_data['wechat_official']}" alt="WeChat Official">
        <div class="qr-title">{QR_INFO['wechat_official']['title']}</div>
        <div class="qr-sub">{QR_INFO['wechat_official']['subtitle']}</div>
        <div class="qr-desc">{QR_INFO['wechat_official']['desc']}</div>
      </div>

      <!-- 2. 爱发电 -->
      <div class="qr-card">
        <img src="{qr_data['afdian']}" alt="Afdian">
        <div class="qr-title">{QR_INFO['afdian']['title']}</div>
        <div class="qr-sub">{QR_INFO['afdian']['subtitle']}</div>
        <div class="qr-desc">{QR_INFO['afdian']['desc']}</div>
      </div>

      <!-- 3. 个人付款码 -->
      <div class="qr-card">
        <img src="{qr_data['personal_pay']}" alt="Personal Pay">
        <div class="qr-title">{QR_INFO['personal_pay']['title']}</div>
        <div class="qr-sub">{QR_INFO['personal_pay']['subtitle']}</div>
        <div class="qr-desc">{QR_INFO['personal_pay']['desc']}</div>
      </div>

      <!-- 4. 商户付款码 -->
      <div class="qr-card">
        <img src="{qr_data['merchant']}" alt="Merchant">
        <div class="qr-title">{QR_INFO['merchant']['title']}</div>
        <div class="qr-sub">{QR_INFO['merchant']['subtitle']}</div>
        <div class="qr-desc">{QR_INFO['merchant']['desc']}</div>
      </div>

    </div>
  </div>

  <!-- 定价表 -->
  <div class="section">
    <h2>{t("payment.pricing_title")}</h2>
    <table>
      <thead>
        <tr><th>{t("payment.column_subscription")}</th><th>{t("payment.column_price")}</th><th>{t("payment.column_desc")}</th></tr>
      </thead>
      <tbody>
        {pricing_rows}
      </tbody>
    </table>
    <div class="tip-box">
      {t("payment.pricing_tip")}
    </div>
  </div>

  <!-- 操作按钮 -->
  <div class="section" style="text-align:center;">
    <div class="btn-row">
      <a href="#" class="btn btn-primary" onclick="window.close();return false;">{t("payment.btn_paid")}</a>
      <a href="#" class="btn btn-outline" onclick="window.close();return false;">{t("payment.btn_later")}</a>
    </div>
  </div>

  <!-- 底部 -->
  <div class="footer">
    {t("payment.footer_title")}<br>
    {t("payment.footer_info1")}<br>
    {t("payment.footer_info2")}<br>
    <br>
    {t("payment.current_time")}: {now}
  </div>

</div>
</body>
</html>"""
    return html


def show_payment_page(reason: str = "") -> bool:
    """生成付费引导页面并在浏览器中打开

    Args:
        reason: 触发原因（如"免费期已结束"、"今日使用次数已达上限"等）

    Returns:
        True 表示页面成功打开，False 表示失败
    """
    try:
        _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        html = _build_html(reason)

        html_path = _OUTPUT_DIR / "payment_guide.html"
        html_path.write_text(html, encoding="utf-8")

        url = html_path.resolve().as_uri()
        webbrowser.open(url)

        print(f"\n{'='*50}", flush=True)
        print(f"  {t('payment.opened')}", flush=True)
        print(f"  {t('payment.page_path', path=str(html_path))}", flush=True)
        print(f"  {t('payment.browser_not_opened')}", flush=True)
        print(f"{'='*50}", flush=True)
        return True

    except Exception as e:
        print(f"[Error] {t('payment.open_failed')}: {e}", flush=True)
        return False


if __name__ == "__main__":
    show_payment_page(reason="测试预览 - 付费引导页面")