# 迁移指南：从 OpenAI 到 DeepSeek + Supabase / Migration Guide: OpenAI to DeepSeek + Supabase

本指南帮助您将 Text-to-SQL 项目从 OpenAI GPT-3.5 迁移到 DeepSeek，并从 SQLite 迁移到 Supabase。

This guide helps you migrate the Text-to-SQL project from OpenAI GPT-3.5 to DeepSeek and from SQLite to Supabase.

## 📋 迁移前准备 / Pre-Migration Checklist

- [ ] 获取 DeepSeek API 密钥 / Obtain DeepSeek API key
- [ ] 创建 Supabase 项目 / Create Supabase project
- [ ] 备份现有数据（如有） / Backup existing data (if any)
- [ ] 更新依赖包 / Update dependencies

## 🔑 步骤 1: 获取 DeepSeek API 密钥 / Step 1: Get DeepSeek API Key

### DeepSeek 相比 OpenAI 的优势 / Advantages of DeepSeek over OpenAI:

1. **更低的成本** / **Lower Cost**: DeepSeek API 定价比 OpenAI 更实惠
2. **OpenAI 兼容** / **OpenAI Compatible**: 使用相同的 API 接口，迁移简单
3. **优秀的代码理解能力** / **Excellent Code Understanding**: DeepSeek-Coder 系列模型专为代码优化

### 获取步骤 / Steps to Obtain:

1. 访问 [DeepSeek Platform](https://platform.deepseek.com/)
2. 注册账号并登录 / Sign up and log in
3. 导航到 API 密钥页面 / Navigate to API Keys page
4. 创建新的 API 密钥 / Create a new API key
5. 保存密钥（只显示一次）/ Save the key (shown only once)

## 🗄️ 步骤 2: 设置 Supabase 数据库 / Step 2: Set Up Supabase Database

### Supabase 相比 SQLite 的优势 / Advantages of Supabase over SQLite:

1. **云端托管** / **Cloud Hosted**: 无需本地数据库服务器
2. **自动备份** / **Automatic Backups**: 内置备份和恢复功能
3. **扩展性** / **Scalability**: 轻松处理更大的数据量
4. **免费套餐** / **Free Tier**: 提供慷慨的免费使用额度
5. **PostgreSQL** / **PostgreSQL**: 完整的 PostgreSQL 功能支持

### 设置步骤 / Setup Steps:

1. 访问 [Supabase](https://supabase.com/) 并注册
2. 创建新项目 / Create a new project
   - 选择区域（建议选择离你最近的）/ Select region (closest to you)
   - 设置数据库密码 / Set database password
   - 等待项目初始化（约2分钟）/ Wait for initialization (~2 min)

3. 获取连接信息 / Get connection information:
   - 进入项目设置 → 数据库 / Go to Settings → Database
   - 找到 "Connection String" / Find "Connection String"
   - 选择 "URI" 格式 / Select "URI" format
   - 复制连接字符串 / Copy the connection string

4. 获取 API 密钥 / Get API keys:
   - 进入项目设置 → API / Go to Settings → API
   - 复制 "Project URL" 和 "anon public" 密钥 / Copy "Project URL" and "anon public" key

## ⚙️ 步骤 3: 更新配置 / Step 3: Update Configuration

### 3.1 更新依赖 / Update Dependencies

```bash
pip install -r requirements.txt
```

新的依赖包括 / New dependencies include:
- `openai>=1.0.0` - OpenAI 兼容 API 支持 / OpenAI-compatible API support
- `supabase>=2.0.0` - Supabase Python 客户端 / Supabase Python client
- `psycopg2-binary>=2.9.0` - PostgreSQL 数据库驱动 / PostgreSQL driver

### 3.2 更新环境变量 / Update Environment Variables

**旧配置 / Old Configuration** (`.env`):
```env
OPENAI_API_KEY=sk-xxx...
DATABASE_URL=sqlite:///./sample.db
```

**新配置 / New Configuration** (`.env`):
```env
# DeepSeek API 配置 / DeepSeek API Configuration
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-chat
LLM_TEMPERATURE=0.0

# Supabase 数据库配置 / Supabase Database Configuration
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_KEY=your_supabase_anon_key
DATABASE_URL=postgresql://postgres:your-password@db.your-project-ref.supabase.co:5432/postgres
```

### 3.3 配置说明 / Configuration Explanation

| 变量名 / Variable | 说明 / Description | 示例 / Example |
|-------------------|-------------------|----------------|
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | `sk-xxx...` |
| `DEEPSEEK_BASE_URL` | DeepSeek API 端点 | `https://api.deepseek.com` |
| `LLM_MODEL` | 使用的模型名称 | `deepseek-chat` |
| `LLM_TEMPERATURE` | 生成温度(0-2) | `0.0` (确定性) |
| `SUPABASE_URL` | Supabase 项目 URL | `https://xxx.supabase.co` |
| `SUPABASE_KEY` | Supabase 公开密钥 | `eyJxxx...` |
| `DATABASE_URL` | 数据库连接字符串 | 从 Supabase 获取 |

## 📊 步骤 4: 迁移数据 / Step 4: Migrate Data

### 4.1 初始化 Supabase 数据库 / Initialize Supabase Database

使用新的数据库连接初始化表结构：

Initialize table structure with new database connection:

```bash
# 确保 .env 文件已更新 / Ensure .env file is updated
python init_database.py
```

这将在 Supabase 中创建以下表：

This will create the following tables in Supabase:
- `users` - 用户表 / Users table
- `products` - 产品表 / Products table
- `orders` - 订单表 / Orders table

### 4.2 迁移现有数据（如果有）/ Migrate Existing Data (if any)

如果您有现有的 SQLite 数据需要迁移：

If you have existing SQLite data to migrate:

```python
# migrate_data.py
import sqlite3
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

# 连接到旧数据库 / Connect to old database
sqlite_conn = sqlite3.connect('sample.db')
sqlite_cursor = sqlite_conn.cursor()

# 连接到新数据库 / Connect to new database
new_engine = create_engine(os.getenv('DATABASE_URL'))

# 迁移用户 / Migrate users
users = sqlite_cursor.execute("SELECT * FROM users").fetchall()
with new_engine.connect() as conn:
    for user in users:
        conn.execute(text("""
            INSERT INTO users (id, name, email, age, created_at)
            VALUES (:id, :name, :email, :age, :created_at)
        """), {"id": user[0], "name": user[1], "email": user[2], 
               "age": user[3], "created_at": user[4]})
    conn.commit()

print("✅ 数据迁移完成！/ Data migration completed!")
```

## 🧪 步骤 5: 测试迁移 / Step 5: Test Migration

### 5.1 运行集成测试 / Run Integration Test

```bash
python test_deepseek_supabase.py
```

预期输出 / Expected output:
```
✓ LLM Model: deepseek-chat
✓ Database URL: postgresql://...
✓ All components initialized successfully!
```

### 5.2 运行数据库测试 / Run Database Tests

```bash
PYTHONPATH=src python tests/test_database.py
```

### 5.3 测试演示 / Test Demo

```bash
PYTHONPATH=src python demo.py
```

### 5.4 测试交互式 CLI / Test Interactive CLI

```bash
PYTHONPATH=src python cli.py
```

尝试查询 / Try queries:
- "显示所有用户" / "Show all users"
- "找出价格最高的产品" / "Find the most expensive product"
- "统计每个用户的订单数量" / "Count orders per user"

## 🔍 步骤 6: 验证功能 / Step 6: Verify Functionality

### 检查清单 / Checklist:

- [ ] DeepSeek API 连接正常 / DeepSeek API connects properly
- [ ] Supabase 数据库可以访问 / Supabase database is accessible
- [ ] SQL 生成功能正常 / SQL generation works correctly
- [ ] 查询执行成功 / Queries execute successfully
- [ ] 结果格式化正确 / Results format correctly
- [ ] 中英文查询都支持 / Both Chinese and English queries work

### 验证脚本 / Verification Script:

```bash
# 运行所有验证测试 / Run all verification tests
python3 << 'EOF'
import os
import sys
sys.path.insert(0, 'src')

print("🔍 验证配置 / Verifying Configuration...")

# 1. 检查环境变量 / Check environment variables
from dotenv import load_dotenv
load_dotenv()

required_vars = ['DEEPSEEK_API_KEY', 'DATABASE_URL']
for var in required_vars:
    if os.getenv(var):
        print(f"✓ {var} is set")
    else:
        print(f"✗ {var} is NOT set")

# 2. 检查配置加载 / Check config loading
from text_to_sql.utils.config import config
print(f"✓ LLM Model: {config.llm.model_name}")
print(f"✓ Database configured: {'postgresql' in config.database.url}")

# 3. 检查数据库连接 / Check database connection
from text_to_sql.database.manager import DatabaseManager
db = DatabaseManager()
schema = db.get_schema(use_cache=False)
print(f"✓ Database schema loaded: {len(schema)} characters")

print("\n✅ 所有验证通过！/ All verifications passed!")
EOF
```

## 🚨 故障排除 / Troubleshooting

### 问题 1: DeepSeek API 连接失败 / Issue 1: DeepSeek API Connection Failed

**症状 / Symptoms:**
```
Error: Could not connect to DeepSeek API
```

**解决方案 / Solutions:**
1. 检查 API 密钥是否正确 / Verify API key is correct
2. 确认 `DEEPSEEK_BASE_URL` 设置为 `https://api.deepseek.com`
3. 检查网络连接 / Check network connection
4. 验证 API 密钥有足够的配额 / Verify API key has sufficient quota

### 问题 2: Supabase 连接失败 / Issue 2: Supabase Connection Failed

**症状 / Symptoms:**
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**解决方案 / Solutions:**
1. 检查 `DATABASE_URL` 格式是否正确 / Verify DATABASE_URL format
2. 确认数据库密码正确（注意URL编码）/ Confirm password is correct (URL encoded)
3. 检查 Supabase 项目是否处于活动状态 / Check if Supabase project is active
4. 确认防火墙允许连接到 Supabase / Verify firewall allows Supabase connection

**正确的 URL 格式 / Correct URL Format:**
```
postgresql://postgres:PASSWORD@db.PROJECT_REF.supabase.co:5432/postgres
```

### 问题 3: 依赖包冲突 / Issue 3: Package Conflicts

**症状 / Symptoms:**
```
ERROR: pip's dependency resolver does not currently take into account...
```

**解决方案 / Solutions:**
```bash
# 创建新的虚拟环境 / Create new virtual environment
python -m venv venv_new
source venv_new/bin/activate  # Linux/Mac
# or
venv_new\Scripts\activate  # Windows

# 重新安装依赖 / Reinstall dependencies
pip install -r requirements.txt
```

### 问题 4: SSL/TLS 证书错误 / Issue 4: SSL/TLS Certificate Error

**症状 / Symptoms:**
```
ssl.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED]
```

**解决方案 / Solutions:**
```bash
# 更新证书 / Update certificates
pip install --upgrade certifi
```

## 💡 最佳实践 / Best Practices

### 1. 安全性 / Security

- ✅ 使用环境变量存储密钥，不要硬编码 / Use environment variables, don't hardcode keys
- ✅ 定期轮换 API 密钥 / Rotate API keys regularly
- ✅ 使用 Supabase Row Level Security (RLS) 保护数据 / Use Supabase RLS to protect data
- ✅ 不要将 `.env` 文件提交到版本控制 / Don't commit `.env` to version control

### 2. 性能优化 / Performance Optimization

- ✅ 启用模式缓存以减少数据库查询 / Enable schema caching to reduce DB queries
- ✅ 使用适当的 `LLM_TEMPERATURE` 值 / Use appropriate LLM_TEMPERATURE value
  - `0.0` = 最确定性 / Most deterministic
  - `0.7` = 平衡 / Balanced
  - `1.0+` = 更有创造性 / More creative

### 3. 成本控制 / Cost Control

- ✅ 监控 DeepSeek API 使用量 / Monitor DeepSeek API usage
- ✅ 使用 Supabase 免费套餐的限制 / Stay within Supabase free tier limits
- ✅ 实现查询缓存以减少 API 调用 / Implement query caching to reduce API calls

### 4. 可靠性 / Reliability

- ✅ 实现错误重试机制 / Implement error retry mechanisms
- ✅ 定期备份 Supabase 数据 / Regular backup of Supabase data
- ✅ 监控应用程序日志 / Monitor application logs

## 📚 额外资源 / Additional Resources

### 文档 / Documentation:
- [DeepSeek API 文档](https://platform.deepseek.com/docs)
- [Supabase 文档](https://supabase.com/docs)
- [SQLAlchemy PostgreSQL 文档](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html)

### 社区 / Community:
- [DeepSeek Discord](https://discord.gg/Tc7c45Zzu5)
- [Supabase Discord](https://discord.supabase.com/)

## 🎉 迁移完成！/ Migration Complete!

恭喜！您已成功将项目迁移到 DeepSeek 和 Supabase。

Congratulations! You have successfully migrated the project to DeepSeek and Supabase.

现在您可以享受：
- 更低的 API 成本 / Lower API costs
- 云端数据库 / Cloud database
- 更好的扩展性 / Better scalability

如有问题，请查看：
- README.md - 完整文档
- QUICK_START.md - 快速开始指南
- 本迁移指南

If you have questions, please check:
- README.md - Complete documentation
- QUICK_START.md - Quick start guide
- This migration guide

---

**版本 / Version:** 1.0.0  
**更新日期 / Updated:** 2026-01-31
