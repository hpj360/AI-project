#!/usr/bin/env python3
"""OpenFoodFacts 酒类产品抓取器。

API: https://world.openfoodfacts.org/api/v2/search
使用 categories_tags 过滤器（OFF v2 API 的正确过滤参数）。
注意：OFF API 偶发 503 错误，已加重试与 User-Agent。
"""
import requests
import json
import time
from pathlib import Path

# 子类 → OFF 分类标签（已验证可返回真实酒类产品）
# 计数参考：beers 11849, red-wines 3210, white-wines 1653, sparkling-wines 1197,
#           champagnes 687, prosecco 318, vodkas 512, gins 345, rums 657,
#           tequilas 88, cognacs 117, brandies 75, sakes 56, liqueurs 1545,
#           ciders 1404, whisky 687
SEARCH_TAGS = {
    "whisky": ["whisky"],
    "wine_red": ["red-wines"],
    "wine_white": ["white-wines"],
    "wine_sparkling": ["sparkling-wines", "champagnes", "prosecco"],
    "beer": ["beers", "ales", "lagers", "ciders"],
    "sake": ["sakes"],
    "gin": ["gins"],
    "vodka": ["vodkas"],
    "rum": ["rums"],
    "tequila": ["tequilas"],
    "liqueur": ["liqueurs"],
    "brandy": ["cognacs", "brandies"],
}

HEADERS = {
    "User-Agent": "HermesKnowledgeBase/1.0 (educational; contact: dev@example.com)"
}

FIELDS = "code,product_name,product_name_en,brands,alcohol_content,origins,categories,image_url,quantity"


def fetch_page(tag, page=1, page_size=50, max_retries=4):
    """抓取一页数据，自动重试 503。"""
    url = "https://world.openfoodfacts.org/api/v2/search"
    params = {
        "categories_tags": tag,
        "page": page,
        "page_size": page_size,
        "fields": FIELDS,
    }
    for attempt in range(max_retries):
        try:
            r = requests.get(url, params=params, headers=HEADERS, timeout=30)
            if r.status_code == 200:
                return r.json()
            # 503 等错误重试
            time.sleep(2 + attempt)
        except Exception as e:
            print(f"  错误: {e}")
            time.sleep(2 + attempt)
    return None


def extract_product(p):
    """提取产品信息。"""
    name = p.get("product_name_en") or p.get("product_name") or ""
    if not name or not name.strip():
        return None
    abv = p.get("alcohol_content")
    if abv:
        try:
            abv = f"{float(abv)}%"
        except (TypeError, ValueError):
            abv = str(abv)
    else:
        abv = ""
    return {
        "barcode": p.get("code", ""),
        "name": name.strip(),
        "brands": p.get("brands", "") or "",
        "abv": abv,
        "origins": p.get("origins", "") or "",
        "categories": p.get("categories", "") or "",
        "image_url": p.get("image_url", "") or "",
        "quantity": p.get("quantity", "") or "",
    }


def crawl():
    all_products = []
    seen_barcodes = set()
    per_subcat_cap = 25  # 每个子类抓取上限，确保覆盖所有 12 个子类
    subcat_counts = {}
    for subcat, tags in SEARCH_TAGS.items():
        subcat_counts[subcat] = 0
        for tag in tags:
            if subcat_counts[subcat] >= per_subcat_cap:
                break
            print(f"抓取 {subcat} / tag={tag}...")
            for page in range(1, 4):  # 每标签最多 3 页
                data = fetch_page(tag, page=page)
                if not data or "products" not in data or not data["products"]:
                    break
                added = 0
                for p in data["products"]:
                    if subcat_counts[subcat] >= per_subcat_cap:
                        break
                    prod = extract_product(p)
                    if prod and prod["barcode"] and prod["barcode"] not in seen_barcodes:
                        seen_barcodes.add(prod["barcode"])
                        all_products.append({"subcategory": subcat, **prod})
                        subcat_counts[subcat] += 1
                        added += 1
                print(f"  page {page}: +{added} ({subcat}={subcat_counts[subcat]}/{per_subcat_cap}, 累计 {len(all_products)})")
                time.sleep(1)
                if subcat_counts[subcat] >= per_subcat_cap:
                    break
    # 去重
    seen = set()
    unique = []
    for p in all_products:
        if p["barcode"] not in seen:
            seen.add(p["barcode"])
            unique.append(p)
    print(f"\n总计: {len(unique)} 个唯一产品")
    # 保存
    out = Path("/workspace/Hermes/content-creation/scripts/external/openfoodfacts_raw.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(unique, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"保存到: {out}")
    # 子类分布
    from collections import Counter
    by_sub = Counter(p["subcategory"] for p in unique)
    print(f"子类分布: {dict(by_sub)}")


if __name__ == "__main__":
    crawl()
