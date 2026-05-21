$skillSlug = "pskoett/self-improving-agent"
$installDir = "d:\AI项目\.trae\skills\$skillSlug"
$downloadUrl = "https://lightmake.site/api/v1/download?slug=$skillSlug"
$tempZip = "$env:TEMP\$skillSlug.zip"

Write-Host "正在安装: $skillSlug"
Write-Host "下载地址: $downloadUrl"

# 创建目标目录
if (-not (Test-Path $installDir)) {
    New-Item -ItemType Directory -Path $installDir -Force
}

# 下载ZIP文件
Write-Host "正在下载..."
try {
    Invoke-WebRequest -Uri $downloadUrl -OutFile $tempZip
    Write-Host "下载完成"
    
    # 解压ZIP文件
    Write-Host "正在解压..."
    Expand-Archive -Path $tempZip -DestinationPath $installDir -Force
    Write-Host "解压完成"
    
    # 清理临时文件
    Remove-Item $tempZip -Force
    
    Write-Host "✓ 安装成功: $skillSlug"
} catch {
    Write-Host "✗ 安装失败: $skillSlug"
    Write-Host "错误: $($_.Exception.Message)"
}
