---
name: db
description: "通过 CLI 客户端操作数据库：PostgreSQL（psql）、MySQL（mysql）、SQLite（sqlite3）和 Redis（redis-cli）。适用场景：(1) 查询数据，(2) 检查表结构，(3) 执行迁移，(4) 调试数据问题，(5) 管理用户/权限。不适用于：ORM 操作（用应用代码）、Schema 设计（用 diagram 技能）。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🗄️",
        "requires": { "bins": [] },
        "install":
          [
            {
              "id": "brew-pg",
              "kind": "brew",
              "formula": "libpq",
              "bins": ["psql"],
              "label": "安装 PostgreSQL 客户端（brew）",
            },
            {
              "id": "brew-sqlite",
              "kind": "brew",
              "formula": "sqlite",
              "bins": ["sqlite3"],
              "label": "安装 SQLite（brew）",
            },
            {
              "id": "brew-redis",
              "kind": "brew",
              "formula": "redis",
              "bins": ["redis-cli"],
              "label": "安装 Redis CLI（brew）",
            },
          ],
      },
  }
---

# 数据库技能

通过 CLI 客户端与数据库交互，支持查询、Schema 检查和管理操作。

## 适用场景

✅ **使用此技能的场景：**

- 执行临时查询检查数据
- 查看表结构和索引
- 调试数据不一致问题
- 执行数据库迁移
- 管理用户和权限
- 检查数据库健康和性能

## 不适用场景

❌ **不使用此技能的场景：**

- 应用层 ORM 操作 → 使用应用代码
- Schema 设计可视化 → 使用 diagram 技能
- 大批量数据导入/导出 → 使用专用 ETL 工具
- 未经审核的生产环境 Schema 变更 → 遵循变更管理流程

## PostgreSQL（psql）

### 连接

```bash
# 通过连接字符串
psql "postgresql://user:pass@host:5432/dbname"

# 通过环境变量
export PGHOST=localhost PGPORT=5432 PGUSER=admin PGDATABASE=myapp
psql

# 单次查询
psql -c "SELECT version();"

# 从文件执行
psql -f migration.sql
```

### Schema 检查

```bash
# 列出数据库
psql -c "\l"

# 列出表
psql -c "\dt"

# 查看表结构
psql -c "\d users"

# 查看索引
psql -c "\di"

# 查看表大小
psql -c "SELECT relname, pg_size_pretty(pg_total_relation_size(relid)) FROM pg_catalog.pg_statio_user_tables ORDER BY pg_total_relation_size(relid) DESC LIMIT 10;"
```

### 常用查询

```bash
# 统计行数
psql -c "SELECT COUNT(*) FROM users;"

# 最近记录
psql -c "SELECT * FROM users ORDER BY created_at DESC LIMIT 5;"

# 检查活跃连接
psql -c "SELECT pid, usename, application_name, state, query FROM pg_stat_activity WHERE state = 'active';"

# 检查锁
psql -c "SELECT locktype, relation::regclass, mode, pid FROM pg_locks WHERE NOT granted;"
```

### 迁移

```bash
# 创建迁移
psql -c "ALTER TABLE users ADD COLUMN phone VARCHAR(20);"

# 执行迁移文件
psql -f migrations/001_add_phone.sql

# 检查迁移状态（如果使用迁移表）
psql -c "SELECT * FROM schema_migrations ORDER BY version DESC LIMIT 5;"
```

## MySQL

### 连接

```bash
mysql -h host -u user -p dbname
```

### Schema 检查

```bash
mysql -e "SHOW DATABASES;"
mysql -e "SHOW TABLES;" dbname
mysql -e "DESCRIBE users;" dbname
mysql -e "SHOW INDEX FROM users;" dbname
```

## SQLite

### 连接

```bash
sqlite3 /path/to/database.db
```

### 常用操作

```bash
# 列出表
sqlite3 db.sqlite3 ".tables"

# 查看表结构
sqlite3 db.sqlite3 ".schema users"

# 带表头查询
sqlite3 -header -column db.sqlite3 "SELECT * FROM users LIMIT 5;"

# 导出为 CSV
sqlite3 -header -csv db.sqlite3 "SELECT * FROM users;" > users.csv

# 执行迁移
sqlite3 db.sqlite3 < migration.sql
```

## Redis

### 连接

```bash
redis-cli -h host -p 6379 -a password
```

### 常用操作

```bash
# 心跳检测
redis-cli ping

# 按模式扫描键
redis-cli --scan --pattern "session:*"

# 获取值
redis-cli GET "user:1"

# 设置带过期时间的值
redis-cli SET "key" "value" EX 3600

# 查看内存信息
redis-cli info memory

# 查看慢日志
redis-cli slowlog get 10
```

## 安全规则

- **UPDATE/DELETE 必须使用 WHERE** — 执行前确认条件
- **大表 SELECT 使用 LIMIT** — 避免全表扫描
- **破坏性操作尽量包裹事务** — 出错可回滚
- **迁移前先备份** — `pg_dump dbname > backup.sql`
- **禁止硬编码凭据** — 使用环境变量或 `.pgpass`
- **先在测试环境验证** — 禁止在生产环境执行未验证的查询

## 输出规范

- 迁移文件保存到 `shared/migrations/`，命名格式：`NNN_描述.sql`
- 查询结果按需保存到 `shared/queries/`
- 迁移文件中必须包含 `--` 注释说明变更内容
