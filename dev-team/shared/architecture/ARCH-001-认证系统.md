# ARCH-001: 认证系统架构设计

## 概述
本文档描述用户认证系统的技术架构设计，包括认证流程、会话管理、安全策略等。

## 架构图
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   Gateway   │────▶│ Auth Service│
│  (Browser)  │     │   (Nginx)   │     │   (Node.js) │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    │                          │                          │
                    ▼                          ▼                          ▼
            ┌─────────────┐           ┌─────────────┐           ┌─────────────┐
            │    Redis    │           │  PostgreSQL │           │   WeChat    │
            │  (Session)  │           │   (User)    │           │    API      │
            └─────────────┘           └─────────────┘           └─────────────┘
```

## 模块说明

### 1. Gateway (网关层)
- 职责：请求路由、限流、日志记录
- 接口：HTTP/HTTPS
- 依赖：Auth Service

### 2. Auth Service (认证服务)
- 职责：用户认证、会话管理、Token签发
- 接口：REST API
- 依赖：Redis、PostgreSQL、WeChat API

### 3. Session Store (会话存储)
- 职责：存储用户会话信息
- 技术：Redis
- TTL：7天（开启记住我）或 24小时

## 技术选型
| 组件 | 技术选择 | 理由 |
|------|----------|------|
| 认证方案 | JWT + Redis | 无状态 + 支持主动失效 |
| 密码加密 | bcrypt | 业界标准，安全性高 |
| 验证码 | Redis + SMS服务 | 高性能，支持过期 |

## API设计

### 登录接口
```
POST /api/v1/auth/login
Request:
{
  "username": "string",
  "password": "string",
  "rememberMe": boolean
}

Response:
{
  "code": 0,
  "data": {
    "token": "jwt_token",
    "expiresIn": 86400
  }
}
```

### 刷新Token
```
POST /api/v1/auth/refresh
Headers: Authorization: Bearer <token>

Response:
{
  "code": 0,
  "data": {
    "token": "new_jwt_token",
    "expiresIn": 86400
  }
}
```

## 安全策略
1. 密码传输使用HTTPS加密
2. Token存储使用HttpOnly Cookie
3. 防暴力破解：IP限流 + 账户锁定
4. 敏感操作需要二次验证

## 非功能性需求
- 性能：登录响应时间 < 500ms
- 可用性：99.9%
- 安全性：符合OWASP标准

## 风险与对策
| 风险 | 影响 | 对策 |
|------|------|------|
| Token泄露 | 账户被盗 | 短有效期 + 刷新机制 |
| Redis宕机 | 无法登录 | Redis集群 + 降级方案 |

## 更新记录
| 日期 | 版本 | 更新内容 | 作者 |
|------|------|----------|------|
| 2026-03-15 | 1.0 | 初始版本 | architect |
