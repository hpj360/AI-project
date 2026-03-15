#!/usr/bin/env python3
import sys
import os
import urllib.request
import zipfile
import tempfile
import shutil
from pathlib import Path

SKILLS = [
    "product-manager",
    "product-manager-skills", 
    "aipm-news-digest",
    "pskoett/self-improving-agent"
]

DOWNLOAD_URL = "https://lightmake.site/api/v1/download?slug={}"
INSTALL_DIR = Path("d:/AI项目/.trae/skills")

def install_skill(slug):
    print(f"正在安装: {slug}")
    
    # 创建目标目录
    target_dir = INSTALL_DIR / slug
    
    # 下载ZIP
    zip_url = DOWNLOAD_URL.format(slug)
    print(f"下载地址: {zip_url}")
    
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = Path(tmpdir) / f"{slug}.zip"
            
            # 下载文件
            print("正在下载...")
            urllib.request.urlretrieve(zip_url, zip_path)
            
            # 解压
            print("正在解压...")
            if target_dir.exists():
                shutil.rmtree(target_dir)
            target_dir.mkdir(parents=True, exist_ok=True)
            
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(target_dir)
            
            print(f"✓ 安装成功: {slug}")
            print()
            
    except Exception as e:
        print(f"✗ 安装失败: {slug}")
        print(f"错误: {e}")
        print()

def main():
    INSTALL_DIR.mkdir(parents=True, exist_ok=True)
    
    for skill in SKILLS:
        install_skill(skill)
    
    print("所有技能安装完成！")

if __name__ == "__main__":
    main()
