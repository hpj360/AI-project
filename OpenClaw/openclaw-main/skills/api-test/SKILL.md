---
name: api-test
description: "通过 curl 和 httpie 测试 REST/GraphQL API。适用场景：(1) 发送 HTTP 请求验证 API 行为，(2) 检查响应状态码和头部，(3) 验证 JSON 响应结构，(4) 对端点执行冒烟测试，(5) 调试 API 问题。不适用于：压力测试（用 k6/wrk）、浏览器测试（用 browser 工具）、UI 测试。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🧪",
        "requires": { "bins": ["curl"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "httpie",
              "bins": ["http"],
              "label": "安装 HTTPie（brew）",
            },
            {
              "id": "pip",
              "kind": "pip",
              "package": "httpie",
              "bins": ["http"],
              "label": "安装 HTTPie（pip）",
            },
          ],
      },
  }
---

# API 测试技能

发送 HTTP 请求并验证 API 响应，用于测试和调试。

## 适用场景

✅ **使用此技能的场景：**

- 验证 API 端点行为
- 检查响应状态码和头部
- 验证 JSON 响应结构
- 测试认证流程
- 调试 API 错误
- 部署后执行冒烟测试

## 不适用场景

❌ **不使用此技能的场景：**

- 压力/性能测试 → 使用 k6、wrk 或 ab
- 浏览器端测试 → 使用 browser 工具
- UI 测试 → 使用专用 UI 测试框架
- API 模拟 → 使用 mock 服务器

## 基本请求

### curl

```bash
# GET 请求
curl -s https://api.example.com/users | jq

# POST JSON 请求体
curl -s -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d '{"name": "Alice", "email": "alice@example.com"}' | jq

# PUT 更新
curl -s -X PUT https://api.example.com/users/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d '{"name": "Alice Updated"}' | jq

# DELETE
curl -s -o /dev/null -w "%{http_code}" -X DELETE https://api.example.com/users/1 \
  -H "Authorization: Bearer $API_TOKEN"
```

### HTTPie（如已安装）

```bash
# GET
http GET https://api.example.com/users Authorization:"Bearer $API_TOKEN"

# POST
http POST https://api.example.com/users name=Alice email=alice@example.com Authorization:"Bearer $API_TOKEN"

# PUT
http PUT https://api.example.com/users/1 name="Alice Updated" Authorization:"Bearer $API_TOKEN"
```

## 响应验证

### 状态码检查

```bash
STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://api.example.com/health)
if [ "$STATUS" -eq 200 ]; then
  echo "✅ 健康检查通过 (200)"
else
  echo "❌ 健康检查失败 ($STATUS)"
fi
```

### JSON 结构验证

```bash
RESPONSE=$(curl -s https://api.example.com/users/1)

# 检查必填字段
echo "$RESPONSE" | jq -e '.id' > /dev/null && echo "✅ id 存在" || echo "❌ id 缺失"
echo "$RESPONSE" | jq -e '.name' > /dev/null && echo "✅ name 存在" || echo "❌ name 缺失"
echo "$RESPONSE" | jq -e '.email' > /dev/null && echo "✅ email 存在" || echo "❌ email 缺失"

# 检查字段类型
echo "$RESPONSE" | jq -e '.id | type == "number"' > /dev/null && echo "✅ id 为数字类型" || echo "❌ id 非数字类型"
```

### 响应时间检查

```bash
TIME=$(curl -s -o /dev/null -w "%{time_total}" https://api.example.com/users)
echo "响应时间: ${TIME}s"
if (( $(echo "$TIME < 1.0" | bc -l) )); then
  echo "✅ 低于 1s 阈值"
else
  echo "❌ 超过 1s 阈值"
fi
```

## 常见测试模式

### 认证流程

```bash
# 登录并提取令牌
TOKEN=$(curl -s -X POST https://api.example.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123"}' | jq -r '.token')

# 使用令牌发送认证请求
curl -s https://api.example.com/me -H "Authorization: Bearer $TOKEN" | jq
```

### 分页测试

```bash
# 测试第一页
PAGE1=$(curl -s "https://api.example.com/users?page=1&limit=10")
TOTAL=$(echo "$PAGE1" | jq '.total')
COUNT=$(echo "$PAGE1" | jq '.items | length')
echo "总数: $TOTAL, 本页条目: $COUNT"
```

### 错误响应测试

```bash
# 测试 404
STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://api.example.com/users/99999)
[ "$STATUS" -eq 404 ] && echo "✅ 资源不存在返回 404" || echo "❌ 期望 404，实际 $STATUS"

# 测试未认证 401
STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://api.example.com/me)
[ "$STATUS" -eq 401 ] && echo "✅ 未认证返回 401" || echo "❌ 期望 401，实际 $STATUS"

# 测试无效输入 400
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
  https://api.example.com/users -H "Content-Type: application/json" -d '{}')
[ "$STATUS" -eq 400 ] && echo "✅ 无效输入返回 400" || echo "❌ 期望 400，实际 $STATUS"
```

## GraphQL

```bash
curl -s -X POST https://api.example.com/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d '{"query": "{ users { id name email } }"}' | jq
```

## 注意事项

- curl 始终使用 `-s`（静默模式）抑制进度输出
- 使用 `| jq` 美化 JSON 响应
- 将基础 URL 存入变量：`BASE="https://api.example.com"`
- 使用 `-w "%{http_code}"` 提取状态码
- 敏感数据从环境变量读取，禁止硬编码
