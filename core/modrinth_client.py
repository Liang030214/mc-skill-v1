# -*- coding: utf-8 -*-
"""Modrinth API 客户端 - 联网查询模组信息

用于在本地数据库未收录时，通过 Modrinth API 实时查询模组的最新版本。
支持：模组搜索、版本获取、文件下载链接生成。
"""

import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)

# Modrinth API 基础 URL
MODRINTH_API = "https://api.modrinth.com/v2"

# 加载器名称映射（内部名称 -> Modrinth 名称）
LOADER_MAP = {
    "neoforge": "neoforge",
    "forge": "forge",
    "fabric": "fabric",
    "quilt": "quilt",
    "liteloader": "liteloader",
}

# 请求超时时间（秒）
REQUEST_TIMEOUT = 10

# 全局缓存：避免重复 API 调用
_search_cache: Dict[str, Optional[Dict]] = {}
_version_cache: Dict[str, List[Dict]] = {}


def _http_get(url: str, headers: Optional[Dict] = None) -> Tuple[int, Any]:
    """发送 HTTP GET 请求

    Args:
        url: 请求 URL
        headers: 附加请求头

    Returns:
        (status_code, response_data) 元组；出错返回 (0, None)
    """
    default_headers = {
        "User-Agent": "MC-Skill/1.0 (crash-analyzer)",
        "Accept": "application/json",
    }
    if headers:
        default_headers.update(headers)

    req = Request(url, headers=default_headers)
    try:
        with urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return resp.status, data
    except URLError as e:
        logger.warning(f"网络请求失败: {url} - {e}")
        return 0, None
    except json.JSONDecodeError as e:
        logger.warning(f"JSON 解析失败: {url} - {e}")
        return 0, None


def search_mod(
    query: str,
    mc_version: str = "",
    loader: str = "",
    limit: int = 5,
    timeout: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """搜索模组（通过 Modrinth API）

    Args:
        query: 模组名称关键词，如 "create"
        mc_version: Minecraft 版本筛选（可选）
        loader: 加载器筛选，如 "neoforge"（可选）
        limit: 返回结果数量上限
        timeout: 本次请求超时时间（秒）

    Returns:
        匹配的模组项目列表，每个元素包含:
        - project_id: Modrinth 项目 ID
        - title: 显示名称
        - description: 简介
        - categories: 分类标签
        - versions: 支持的版本列表
        - loaders: 支持的加载器列表
        - downloads: 下载次数
        - slug: 项目 slug
    """
    cache_key = f"search:{query.lower()}:{mc_version}:{loader}:{limit}"
    if cache_key in _search_cache:
        if _search_cache[cache_key] is not None:
            return _search_cache[cache_key]
        return []

    params = {
        "query": query,
        "limit": limit,
        "facets": json.dumps([["project_type:mod"]]),
    }
    if mc_version:
        params["facets"] = json.dumps([
            ["project_type:mod"],
            [f"versions:{mc_version}"],
        ])
    if loader:
        loader_name = LOADER_MAP.get(loader, loader)
        facets_list = [["project_type:mod"]]
        if mc_version:
            facets_list.append([f"versions:{mc_version}"])
        facets_list.append([f"categories:{loader_name}"])
        params["facets"] = json.dumps(facets_list)

    url = f"{MODRINTH_API}/search?{urlencode(params)}"
    if timeout:
        global REQUEST_TIMEOUT
        old_timeout = REQUEST_TIMEOUT
        REQUEST_TIMEOUT = timeout

    status, data = _http_get(url)

    if timeout:
        REQUEST_TIMEOUT = old_timeout

    results = []
    if status == 200 and data:
        hits = data.get("hits", [])
        for hit in hits:
            results.append({
                "project_id": hit.get("project_id", ""),
                "title": hit.get("title", ""),
                "description": hit.get("description", ""),
                "categories": hit.get("categories", []),
                "versions": hit.get("versions", []),
                "loaders": hit.get("loaders", []),
                "downloads": hit.get("downloads", 0),
                "slug": hit.get("slug", ""),
            })

    _search_cache[cache_key] = results
    return results


def get_project_info(project_id: str) -> Optional[Dict[str, Any]]:
    """获取 Modrinth 项目详细信息

    Args:
        project_id: Modrinth 项目 ID 或 slug

    Returns:
        项目信息字典；失败返回 None
    """
    url = f"{MODRINTH_API}/project/{project_id}"
    status, data = _http_get(url)
    if status == 200 and data:
        return {
            "project_id": data.get("id", ""),
            "title": data.get("title", ""),
            "slug": data.get("slug", ""),
            "description": data.get("description", ""),
            "categories": data.get("categories", []),
            "client_side": data.get("client_side", ""),
            "server_side": data.get("server_side", ""),
            "downloads": data.get("downloads", 0),
            "follows": data.get("follows", 0),
        }
    return None


def get_versions(
    project_id: str,
    mc_version: str = "",
    loader: str = "",
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """获取模组版本列表

    Args:
        project_id: Modrinth 项目 ID 或 slug
        mc_version: MC 版本筛选（可选）
        loader: 加载器筛选（可选）
        limit: 返回数量上限

    Returns:
        版本信息列表，每个元素包含:
        - version_id: 版本 ID
        - version_number: 版本号
        - date_published: 发布日期
        - game_versions: 支持的 MC 版本
        - loaders: 支持的加载器
        - files: 文件列表
        - version_type: release/beta/alpha
        - downloads: 下载次数
    """
    cache_key = f"version:{project_id}:{mc_version}:{loader}:{limit}"
    if cache_key in _version_cache:
        return _version_cache[cache_key]

    params = {}
    if mc_version:
        params["game_versions"] = json.dumps([mc_version])
    if loader:
        loader_name = LOADER_MAP.get(loader, loader)
        params["loaders"] = json.dumps([loader_name])
    params["limit"] = str(limit)

    url = f"{MODRINTH_API}/project/{project_id}/version"
    if params:
        url += f"?{urlencode(params)}"

    status, data = _http_get(url)

    results = []
    if status == 200 and data:
        for ver in data:
            # 只统计 release 版本，排除 beta/alpha（除非没有 release）
            results.append({
                "version_id": ver.get("id", ""),
                "version_number": ver.get("version_number", ""),
                "date_published": ver.get("date_published", ""),
                "game_versions": ver.get("game_versions", []),
                "loaders": ver.get("loaders", []),
                "files": [
                    {
                        "hashes": f.get("hashes", {}),
                        "url": f.get("url", ""),
                        "filename": f.get("filename", ""),
                        "filesize": f.get("size", 0),
                        "primary": f.get("primary", False),
                    }
                    for f in ver.get("files", [])
                ],
                "version_type": ver.get("version_type", "release"),
                "downloads": ver.get("downloads", 0),
                "changelog": ver.get("changelog", "")[:200],
            })

    _version_cache[cache_key] = results
    return results


def get_latest_recommended_version(
    mod_id: str,
    mc_version: str,
    loader: str,
    max_cache_age: int = 86400,
) -> Optional[Dict[str, Any]]:
    """获取模组在指定环境下的最新推荐版本（综合搜索 + 版本查询）

    这是最常用的高级查询接口：
    1. 先通过名称搜索项目
    2. 再获取符合条件的版本列表
    3. 从中选出最优版本

    Args:
        mod_id: 模组 ID / 关键词，如 "create"
        mc_version: 目标 MC 版本，如 "1.21.1"
        loader: 目标加载器，如 "neoforge"
        max_cache_age: 缓存最大有效期（秒），默认1天

    Returns:
        推荐版本信息字典，包含:
        - mod_id: 原始请求的模组 ID
        - project_id: Modrinth 项目 ID
        - project_title: 项目显示名
        - latest_version: 最新发布版版本号
        - latest_version_id: 版本 ID（用于下载）
        - release_version: 最新 release 版版本号
        - beta_version: 最新 beta 版版本号（若有）
        - download_url: 主文件下载链接
        - matches: 列表，记录匹配过程
        - status: "ok" / "not_found" / "error"
        - note: 补充说明
        如果未找到则返回 None。
    """
    loader_name = LOADER_MAP.get(loader, loader)
    matches = []

    # Step 1: 搜索项目
    search_results = search_mod(mod_id, mc_version, loader_name, limit=5)
    if not search_results:
        # 放宽条件：只按名称搜索，不限版本/加载器
        search_results = search_mod(mod_id, limit=5)
        matches.append("放宽条件重新搜索")

    if not search_results:
        matches.append("未找到任何项目")
        return {
            "mod_id": mod_id,
            "status": "not_found",
            "note": f"Modrinth 上未找到与 '{mod_id}' 匹配的模组",
            "matches": matches,
        }

    # 选择最匹配的项目（优先按下载量排序）
    best = max(search_results, key=lambda x: x.get("downloads", 0))
    project_id = best["project_id"]
    project_title = best["title"]
    matches.append(f"选中项目: {project_title} ({project_id})")

    # Step 2: 获取版本列表（筛选 MC 版本 + 加载器）
    versions = get_versions(project_id, mc_version, loader_name, limit=20)
    if not versions:
        # 放宽：只按 MC 版本筛选
        versions = get_versions(project_id, mc_version, limit=20)
        matches.append("放宽条件获取版本（不限加载器）")
    if not versions:
        # 再次放宽：只按加载器筛选
        versions = get_versions(project_id, loader=loader_name, limit=20)
        matches.append("放宽条件获取版本（不限MC版本）")
    if not versions:
        versions = get_versions(project_id, limit=20)
        matches.append("放宽条件获取版本（不限MC版本和加载器）")

    if not versions:
        matches.append("未找到任何版本")
        return {
            "mod_id": mod_id,
            "project_id": project_id,
            "project_title": project_title,
            "status": "not_found",
            "note": f"项目存在但未找到适配 {mc_version} + {loader} 的版本",
            "matches": matches,
        }

    # Step 3: 分类版本类型
    release_versions = [v for v in versions if v.get("version_type") == "release"]
    beta_versions = [v for v in versions if v.get("version_type") == "beta"]
    alpha_versions = [v for v in versions if v.get("version_type") == "alpha"]

    latest_release = release_versions[0] if release_versions else None
    latest_beta = beta_versions[0] if beta_versions else None
    latest_alpha = alpha_versions[0] if alpha_versions else None
    latest_any = versions[0]

    recommended = latest_release or latest_beta or latest_alpha or latest_any
    download_file = None
    for f in recommended.get("files", []):
        if f.get("primary"):
            download_file = f
            break
    if not download_file and recommended.get("files"):
        download_file = recommended["files"][0]

    matches.append(f"最新 release: {latest_release['version_number'] if latest_release else '无'}")
    if latest_beta:
        matches.append(f"最新 beta: {latest_beta['version_number']}")

    return {
        "mod_id": mod_id,
        "project_id": project_id,
        "project_title": project_title,
        "latest_version": latest_any["version_number"],
        "latest_version_id": latest_any["version_id"],
        "release_version": latest_release["version_number"] if latest_release else None,
        "beta_version": latest_beta["version_number"] if latest_beta else None,
        "alpha_version": latest_alpha["version_number"] if latest_alpha else None,
        "recommended_version": recommended["version_number"],
        "recommended_version_id": recommended["version_id"],
        "download_url": download_file["url"] if download_file else "",
        "download_filename": download_file["filename"] if download_file else "",
        "download_size": download_file["filesize"] if download_file else 0,
        "game_versions": recommended.get("game_versions", []),
        "loaders": recommended.get("loaders", []),
        "matches": matches,
        "status": "ok",
        "note": f"来自 Modrinth 实时查询（联网）",
    }


def clear_cache() -> None:
    """清空所有缓存"""
    global _search_cache, _version_cache
    _search_cache.clear()
    _version_cache.clear()
    logger.info("Modrinth 查询缓存已清空")


def get_cache_stats() -> Dict[str, int]:
    """获取缓存统计信息"""
    return {
        "search_entries": len(_search_cache),
        "version_entries": len(_version_cache),
    }
