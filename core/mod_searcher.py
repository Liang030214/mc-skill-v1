# -*- coding: utf-8 -*-
"""F2: AI联网模组智能检索与精准下载

对接Modrinth和CurseForge官方API，按模组名称/关键词检索，
按MC版本和加载器过滤，自动匹配前置依赖，下载正版JAR文件，
生成适配清单。

使用方式:
    from core.mod_searcher import run
    import argparse
    args = argparse.Namespace(
        query="Create",
        mc_version="1.21.1",
        loader="neoforge",
        download=True,
        with_deps=True,
        platform="modrinth",
        output=None
    )
    result = run(args)
"""

import sys
import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import config
from utils.logger import get_logger
from utils.api_client import (
    get_modrinth_client,
    get_curseforge_client,
    LOADER_TO_CURSEFORGE,
)
from utils.report_gen import ReportGenerator, generate_unified_output

logger = get_logger("mod_searcher")


def search_modrinth(
    query: str, mc_version: str, loader: str, limit: int = 10
) -> List[Dict]:
    """从Modrinth搜索模组

    Args:
        query: 搜索关键词
        mc_version: MC版本
        loader: 加载器
        limit: 返回数量

    Returns:
        标准化后的模组列表
    """
    try:
        client = get_modrinth_client()
        raw = client.search(query, mc_version, loader, limit)

        results = []
        for hit in raw.get("hits", []):
            results.append({
                "source": "modrinth",
                "project_id": hit.get("project_id", ""),
                "slug": hit.get("slug", ""),
                "title": hit.get("title", ""),
                "description": hit.get("description", ""),
                "author": hit.get("author", ""),
                "categories": hit.get("categories", []),
                "versions": hit.get("versions", []),
                "downloads": hit.get("downloads", 0),
                "follows": hit.get("follows", 0),
                "date_created": hit.get("date_created", ""),
                "logo_url": hit.get("icon_url", ""),
            })

        logger.info(f"Modrinth搜索: {query} -> {len(results)} 个结果")
        return results

    except Exception as e:
        logger.error(f"Modrinth搜索失败: {e}")
        return []


def search_curseforge(
    query: str, mc_version: str, loader: str
) -> List[Dict]:
    """从CurseForge搜索模组

    Args:
        query: 搜索关键词
        mc_version: MC版本
        loader: 加载器

    Returns:
        标准化后的模组列表
    """
    try:
        client = get_curseforge_client()
        if not client.is_available():
            logger.warning("CurseForge API Key未配置，跳过CurseForge搜索")
            return []

        loader_type = LOADER_TO_CURSEFORGE.get(loader)
        raw = client.search(query, mc_version, loader_type)

        results = []
        for item in raw.get("data", []):
            results.append({
                "source": "curseforge",
                "project_id": str(item.get("id", "")),
                "slug": item.get("slug", ""),
                "title": item.get("name", ""),
                "description": item.get("summary", ""),
                "author": item.get("author", {}).get("name", "") if item.get("author") else "",
                "categories": [c.get("name", "") for c in item.get("categories", [])],
                "versions": [],
                "downloads": item.get("downloadCount", 0),
                "follows": 0,
                "date_created": item.get("dateCreated", ""),
                "logo_url": item.get("logoThumbnail", ""),
                "cf_mod_id": item.get("id"),
            })

        logger.info(f"CurseForge搜索: {query} -> {len(results)} 个结果")
        return results

    except Exception as e:
        logger.error(f"CurseForge搜索失败: {e}")
        return []


def merge_results(
    modrinth_results: List[Dict], curseforge_results: List[Dict]
) -> List[Dict]:
    """合并两个平台的搜索结果，按slug去重

    Args:
        modrinth_results: Modrinth结果
        curseforge_results: CurseForge结果

    Returns:
        合并后的结果列表
    """
    seen_slugs = set()
    merged = []

    for r in modrinth_results + curseforge_results:
        slug = r.get("slug", "")
        if slug and slug not in seen_slugs:
            seen_slugs.add(slug)
            merged.append(r)

    # 按下载量排序
    merged.sort(key=lambda x: x.get("downloads", 0), reverse=True)
    return merged


def get_version_info(
    slug: str, loader: str, mc_version: str, source: str = "modrinth"
) -> List[Dict]:
    """获取模组版本列表和依赖信息

    Args:
        slug: 模组slug
        loader: 加载器
        mc_version: MC版本
        source: 数据来源

    Returns:
        版本列表
    """
    try:
        if source == "modrinth":
            client = get_modrinth_client()
            versions = client.get_versions(slug, mc_version, loader)

            result = []
            for v in versions:
                files = v.get("files", [])
                primary_file = files[0] if files else {}
                result.append({
                    "version_id": v.get("id", ""),
                    "version_number": v.get("version_number", ""),
                    "date_published": v.get("date_published", ""),
                    "download_url": primary_file.get("url", ""),
                    "file_name": primary_file.get("filename", ""),
                    "file_size": primary_file.get("size", 0),
                    "dependencies": v.get("dependencies", []),
                    "game_versions": v.get("game_versions", []),
                    "loaders": v.get("loaders", []),
                    "release_type": v.get("version_type", ""),
                })

            return result

    except Exception as e:
        logger.error(f"获取版本信息失败 ({source}): {e}")
        return []


def resolve_dependencies(
    version_info: Dict, all_versions: Dict[str, List[Dict]]
) -> List[Dict]:
    """递归解析前置依赖

    Args:
        version_info: 版本信息
        all_versions: 已获取的所有版本信息缓存

    Returns:
        依赖列表
    """
    deps = []
    seen = set()

    def _resolve(dep_list, depth=0):
        if depth > 5:
            return  # 防止无限递归
        for dep in dep_list:
            dep_id = dep.get("project_id", "")
            if dep_id and dep_id not in seen:
                seen.add(dep_id)
                deps.append(dep)
                # 递归查找该依赖的依赖
                if dep_id in all_versions:
                    for v in all_versions[dep_id]:
                        if v.get("dependencies"):
                            _resolve(v["dependencies"], depth + 1)

    if version_info.get("dependencies"):
        _resolve(version_info["dependencies"])

    return deps


def download_mod(
    download_url: str, dest_dir: Path, file_name: str = None
) -> Optional[Path]:
    """下载模组JAR文件

    Args:
        download_url: 下载URL
        dest_dir: 目标目录
        file_name: 文件名（可选，从URL推断）

    Returns:
        下载文件的Path对象，失败返回None
    """
    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
        if not file_name:
            file_name = download_url.split("/")[-1].split("?")[0]
            if not file_name.endswith(".jar"):
                file_name += ".jar"

        dest_path = dest_dir / file_name
        client = get_modrinth_client()
        result = client.download(download_url, dest_path)
        return result

    except Exception as e:
        logger.error(f"下载失败: {file_name} - {e}")
        return None


def generate_search_html(
    query: str,
    mc_version: str,
    loader: str,
    results: List[Dict],
    downloaded: List[Dict],
    failed: List[Dict],
) -> str:
    """生成搜索结果HTML报告

    Args:
        query: 搜索关键词
        mc_version: MC版本
        loader: 加载器
        results: 搜索结果
        downloaded: 已下载模组
        failed: 下载失败模组

    Returns:
        HTML内容
    """
    gen = ReportGenerator(feature="mod_searcher")

    # 搜索参数
    info_rows = [
        ["搜索关键词", query],
        ["MC版本", mc_version],
        ["加载器", loader],
        ["结果数量", len(results)],
        ["已下载", len(downloaded)],
        ["下载失败", len(failed)],
    ]
    info_html = gen.render_table(["参数", "值"], info_rows)

    # 搜索结果列表
    if results:
        result_rows = []
        for r in results[:20]:
            result_rows.append([
                r["title"],
                r["source"],
                r["slug"],
                f"{r.get('downloads', 0):,}",
                r.get("description", "")[:80],
            ])
        results_html = gen.render_table(
            ["模组名", "来源", "Slug", "下载量", "描述"], result_rows
        )
    else:
        results_html = "<p class='muted'>未找到匹配的模组</p>"

    # 下载列表
    if downloaded:
        dl_rows = []
        for d in downloaded:
            dl_rows.append([
                d.get("title", ""),
                d.get("version", ""),
                d.get("file_name", ""),
                str(d.get("file_size", 0)),
                "✅",
            ])
        dl_html = gen.render_table(
            ["模组", "版本", "文件名", "大小", "状态"], dl_rows
        )
    else:
        dl_html = "<p class='muted'>未下载任何模组</p>"

    # 失败列表
    if failed:
        fail_rows = [
            [f["title"], f["error"]]
            for f in failed
        ]
        fail_html = gen.render_table(["模组", "错误信息"], fail_rows)
    else:
        fail_html = ""

    # 依赖关系提示
    dep_warning = ""
    if downloaded:
        dep_warning = gen.render_callout(
            "依赖关系",
            "<p>已下载的模组可能需要额外的前置依赖。"
            "请检查下载目录中的所有JAR文件，确保没有遗漏。"
            "如需自动解析依赖，请使用 --with-deps 参数。</p>",
            level="info",
        )

    content = gen.render_section("搜索参数", info_html, tag="search_info")
    content += gen.render_section("搜索结果", results_html, tag="results")
    if downloaded:
        content += gen.render_section("下载清单", dl_html, tag="downloaded")
    if fail_html:
        content += gen.render_section("下载失败", fail_html, tag="failed")
    if dep_warning:
        content += dep_warning

    return content


def run(args) -> Dict[str, Any]:
    """F2 模组检索下载主入口

    Args:
        args: argparse.Namespace，需包含:
            - query: 搜索关键词
            - mc_version: MC版本
            - loader: 加载器类型
            - download: 是否下载（默认True）
            - with_deps: 是否下载依赖（默认True）
            - platform: 平台偏好（modrinth/curseforge/both）
            - output: 输出目录

    Returns:
        统一返回结构字典
    """
    query = args.query
    mc_version = args.mc_version
    loader = args.loader
    do_download = getattr(args, "download", True)
    with_deps = getattr(args, "with_deps", True)
    platform = getattr(args, "platform", "modrinth")
    output = getattr(args, "output", None)

    # 1. 输入验证
    if not query:
        return config.build_result(
            feature="mod_searcher",
            status="error",
            input_summary={"query": query},
            result={},
            errors=["搜索关键词不能为空"],
        )

    if loader not in config.LOADERS:
        return config.build_result(
            feature="mod_searcher",
            status="error",
            input_summary={"query": query, "loader": loader},
            result={},
            errors=[f"无效的加载器类型: {loader}，支持: {', '.join(config.LOADERS)}"],
        )

    warnings = []
    logger.info(f"开始搜索: {query} (MC={mc_version}, Loader={loader})")

    # 2. 调用Modrinth搜索
    modrinth_results = []
    curseforge_results = []

    if platform in ("modrinth", "both"):
        modrinth_results = search_modrinth(query, mc_version, loader)

    if platform in ("curseforge", "both"):
        curseforge_results = search_curseforge(query, mc_version, loader)
        if not curseforge_results and not config.APIConfig.has_curseforge_key():
            warnings.append("CurseForge API Key未配置，仅使用Modrinth搜索")

    # 3. 合并结果
    all_results = merge_results(modrinth_results, curseforge_results)

    if not all_results:
        return config.build_result(
            feature="mod_searcher",
            status="error",
            input_summary={
                "query": query,
                "mc_version": mc_version,
                "loader": loader,
            },
            result={},
            warnings=warnings + ["两个平台均无匹配结果，建议更换关键词或版本"],
            errors=["无匹配结果"],
        )

    logger.info(f"合并后结果: {len(all_results)} 个模组")

    # 4. 获取版本信息（取前5个最相关的）
    top_results = all_results[:5]
    version_cache = {}
    downloaded = []
    failed = []
    dep_queue = []

    for mod in top_results:
        slug = mod["slug"]
        source = mod["source"]
        versions = get_version_info(slug, loader, mc_version, source)

        if versions:
            version_cache[slug] = versions
            latest = versions[0]

            if do_download and latest.get("download_url"):
                # 确定输出目录
                if output:
                    dl_dir = Path(output)
                else:
                    dl_dir = config.DOWNLOADS_DIR
                dl_dir.mkdir(parents=True, exist_ok=True)

                # 下载
                file_name = latest.get("file_name", f"{slug}.jar")
                result = download_mod(latest["download_url"], dl_dir, file_name)

                if result:
                    downloaded.append({
                        "title": mod["title"],
                        "slug": slug,
                        "version": latest["version_number"],
                        "file_name": result.name,
                        "file_size": result.stat().st_size,
                        "source": source,
                        "download_url": latest["download_url"],
                    })
                    logger.info(f"已下载: {file_name}")

                    # 收集依赖
                    if with_deps and latest.get("dependencies"):
                        dep_queue.extend(latest["dependencies"])
                else:
                    failed.append({
                        "title": mod["title"],
                        "slug": slug,
                        "error": "下载失败",
                    })

    # 5. 处理依赖下载（最多下载10个依赖）
    if with_deps and dep_queue:
        logger.info(f"发现 {len(dep_queue)} 个依赖需要处理")
        seen_dep_ids = set()
        dep_downloaded = 0

        for dep in dep_queue[:20]:
            dep_id = dep.get("project_id", "")
            if not dep_id or dep_id in seen_dep_ids:
                continue
            seen_dep_ids.add(dep_id)

            # 跳过Minecraft本身和加载器
            if dep_id.lower() in ("minecraft", "fabricloader", "forge", "neoforge", "quilt_loader"):
                continue

            if dep_downloaded >= 10:
                break

            # 尝试从Modrinth获取依赖的版本
            dep_versions = get_version_info(dep_id, loader, mc_version, "modrinth")
            if dep_versions and dep_versions[0].get("download_url"):
                dl_dir = config.DOWNLOADS_DIR
                dep_file = dep_versions[0].get("file_name", f"{dep_id}.jar")
                result = download_mod(dep_versions[0]["download_url"], dl_dir, dep_file)
                if result:
                    downloaded.append({
                        "title": dep_id,
                        "slug": dep_id,
                        "version": dep_versions[0]["version_number"],
                        "file_name": result.name,
                        "file_size": result.stat().st_size,
                        "source": "modrinth",
                        "is_dependency": True,
                    })
                    dep_downloaded += 1
                    logger.info(f"已下载依赖: {dep_file}")

        if dep_downloaded == 0 and with_deps:
            warnings.append("部分依赖可能需要手动下载，请查看报告中的依赖列表")

    # 6. 生成报告
    html_content = generate_search_html(
        query, mc_version, loader, all_results, downloaded, failed
    )

    # 7. 依赖清单（用于HTML展示）
    dependency_list = []
    for d in downloaded:
        if d.get("is_dependency"):
            dependency_list.append({
                "mod_id": d["slug"],
                "version": d["version"],
                "file": d["file_name"],
            })

    output_files = generate_unified_output(
        feature="mod_searcher",
        status="success",
        input_summary={
            "query": query,
            "mc_version": mc_version,
            "loader": loader,
            "platform": platform,
        },
        result={
            "search_results": all_results,
            "downloaded": downloaded,
            "failed": failed,
            "dependencies": dependency_list,
        },
        title=f"模组检索报告 - {query}",
        html_content=html_content,
        warnings=warnings,
    )

    return config.build_result(
        feature="mod_searcher",
        status="success" if not failed else "partial",
        input_summary={
            "query": query,
            "mc_version": mc_version,
            "loader": loader,
        },
        result={
            "search_results": all_results,
            "search_results_count": len(all_results),
            "downloaded_count": len(downloaded),
            "failed_count": len(failed),
            "downloaded": downloaded,
            "failed": failed,
        },
        warnings=warnings,
        output_files=output_files,
    )
