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

# === 资源目录 ===
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_PAYMENT_DIR = _PROJECT_ROOT / "data" / "payment"
_OUTPUT_DIR = _PROJECT_ROOT / "output"

# === 二维码图片路径 ===
QR_FILES = {
    "wechat_official": _PAYMENT_DIR / "wechat_official.png",   # 微信公众号
    "afdian":          _PAYMENT_DIR / "afdian.png",              # 爱发电
    "personal_pay":    _PAYMENT_DIR / "personal_pay.png",       # 支付宝/微信个人付款
    "merchant":        _PAYMENT_DIR / "merchant.png",            # 小红书/微信商户
}

# === 二维码显示信息 ===
QR_INFO = {
    "wechat_official": {
        "title": "微信公众号",
        "subtitle": "关注获取最新动态",
        "desc": "关注公众号，获取功能更新、使用教程和优惠信息",
    },
    "afdian": {
        "title": "爱发电",
        "subtitle": "赞助开发者",
        "desc": "在爱发电平台选择月度赞助或一次性发电，支持项目持续开发",
    },
    "personal_pay": {
        "title": "扫码赞赏",
        "subtitle": "微信 / 支付宝",
        "desc": "扫码直接赞赏任意金额，感谢您的支持",
    },
    "merchant": {
        "title": "商户付款",
        "subtitle": "小红书 / 微信商户",
        "desc": "通过商户平台付款，可获取电子凭证",
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
    # 占位图
    info = QR_INFO.get(key, {})
    return _generate_placeholder_svg(info.get("title", "二维码"), "待替换")


def _build_html(reason: str = "") -> str:
    """生成完整的 HTML 付费引导页面"""

    # 获取4个二维码数据
    qr_data = {key: _get_qr_data(key) for key in QR_FILES}

    # 会员定价表
    pricing_rows = """
    <tr><td>单月包月</td><td>8.88 元/月</td><td>单次付费，到期手动续费</td></tr>
    <tr><td>连续包月</td><td>8.88 元/月</td><td>自动续费，可随时取消</td></tr>
    <tr><td>包季</td><td>23.88 元/季</td><td>相比月付省约 2.76 元</td></tr>
    <tr><td>包年</td><td>88.88 元/年</td><td>相比月付省约 17.68 元</td></tr>
    """

    # 各等级次数对比
    tier_rows = """
    <tr><td>免费用户</td><td>20 次/日</td><td>8 次/日</td><td>1 次/日</td></tr>
    <tr class="highlight"><td>普通会员</td><td>100 次/日</td><td>50 次/日</td><td>5 次/日</td></tr>
    """

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MC Skill V1 - 升级普通会员</title>
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
    <h1>MC 全生态智能适配工程师</h1>
    <p>升级普通会员，解锁更多次数与高级功能</p>
  </div>

  <!-- 提醒 -->
  <div class="alert">
    {'⚠️ ' + reason if reason else '⚠️ 您的免费额度已用完，升级普通会员可继续使用'}
    <br><small>当前时间: {now}</small>
  </div>

  <!-- 会员等级对比 -->
  <div class="section">
    <h2>会员等级对比</h2>
    <table>
      <thead>
        <tr><th>等级</th><th>全自动功能</th><th>半自动功能</th><th>移植评估</th></tr>
      </thead>
      <tbody>
        {tier_rows}
      </tbody>
    </table>
    <div class="tip-box">
      普通会员全自动 100次/日（是免费用户的 5 倍），半自动 50次/日，移植评估 5次/日
    </div>
  </div>

  <!-- 4个二维码 -->
  <div class="section">
    <h2>扫码付费 / 赞助</h2>
    <p style="color:#666; font-size:14px; margin-bottom:15px;">
      选择以下任意方式完成付费，截图发送至公众号即可激活普通会员:
    </p>
    <div class="qr-grid">

      <!-- 1. 微信公众号 -->
      <div class="qr-card">
        <img src="{qr_data['wechat_official']}" alt="微信公众号">
        <div class="qr-title">{QR_INFO['wechat_official']['title']}</div>
        <div class="qr-sub">{QR_INFO['wechat_official']['subtitle']}</div>
        <div class="qr-desc">{QR_INFO['wechat_official']['desc']}</div>
      </div>

      <!-- 2. 爱发电 -->
      <div class="qr-card">
        <img src="{qr_data['afdian']}" alt="爱发电">
        <div class="qr-title">{QR_INFO['afdian']['title']}</div>
        <div class="qr-sub">{QR_INFO['afdian']['subtitle']}</div>
        <div class="qr-desc">{QR_INFO['afdian']['desc']}</div>
      </div>

      <!-- 3. 个人付款码 -->
      <div class="qr-card">
        <img src="{qr_data['personal_pay']}" alt="个人付款码">
        <div class="qr-title">{QR_INFO['personal_pay']['title']}</div>
        <div class="qr-sub">{QR_INFO['personal_pay']['subtitle']}</div>
        <div class="qr-desc">{QR_INFO['personal_pay']['desc']}</div>
      </div>

      <!-- 4. 商户付款码 -->
      <div class="qr-card">
        <img src="{qr_data['merchant']}" alt="商户付款码">
        <div class="qr-title">{QR_INFO['merchant']['title']}</div>
        <div class="qr-sub">{QR_INFO['merchant']['subtitle']}</div>
        <div class="qr-desc">{QR_INFO['merchant']['desc']}</div>
      </div>

    </div>
  </div>

  <!-- 定价表 -->
  <div class="section">
    <h2>普通会员定价</h2>
    <table>
      <thead>
        <tr><th>订阅方式</th><th>价格</th><th>说明</th></tr>
      </thead>
      <tbody>
        {pricing_rows}
      </tbody>
    </table>
    <div class="tip-box">
      付费后请截图发送至微信公众号，或联系作者获取授权码。输入授权码后立即激活普通会员权限。
    </div>
  </div>

  <!-- 操作按钮 -->
  <div class="section" style="text-align:center;">
    <div class="btn-row">
      <a href="#" class="btn btn-primary" onclick="window.close();return false;">我已扫码付款</a>
      <a href="#" class="btn btn-outline" onclick="window.close();return false;">稍后再说</a>
    </div>
  </div>

  <!-- 底部 -->
  <div class="footer">
    MC Skill V1 - MC 全生态智能适配工程师<br>
    免费期 60 天 | 免费用户也可长期使用（每日有限次数）<br>
    付费仅为解锁更高次数限制和进阶服务<br>
    <br>
    生成时间: {now}
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
        # 确保输出目录存在
        _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        # 生成 HTML
        html = _build_html(reason)

        # 保存 HTML 文件
        html_path = _OUTPUT_DIR / "payment_guide.html"
        html_path.write_text(html, encoding="utf-8")

        # 在浏览器中打开
        url = html_path.resolve().as_uri()
        webbrowser.open(url)

        print(f"\n{'='*50}", flush=True)
        print(f"  已打开付费引导页面", flush=True)
        print(f"  页面路径: {html_path}", flush=True)
        print(f"  浏览器应已自动打开，如未打开请手动访问上述路径", flush=True)
        print(f"{'='*50}", flush=True)
        return True

    except Exception as e:
        print(f"[错误] 无法打开付费页面: {e}", flush=True)
        return False


if __name__ == "__main__":
    # 测试：直接运行此模块预览页面
    show_payment_page(reason="测试预览 - 付费引导页面")
