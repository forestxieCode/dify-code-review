# LangGraph Text-to-SQL 智能体 / LangGraph Text-to-SQL Agent

这是一个基于 LangGraph 构建的智能体，可以将用户的自然语言输入转换为 SQL 查询，并执行查询返回结果。

This is an intelligent agent built with LangGraph that converts natural language input to SQL queries and executes them to return results.

> 🎉 **最新更新**: 项目已按模块重新组织，结构更清晰！详见 [STRUCTURE.md](./STRUCTURE.md)
> 
> 🎉 **Latest Update**: Project reorganized by modules for better structure! See [STRUCTURE.md](./STRUCTURE.md)

> 📝 **优化历史**: 代码已进行全面重构优化，提升了可读性、可维护性和可扩展性。详见 [OPTIMIZATION_SUMMARY.md](./OPTIMIZATION_SUMMARY.md)
> 
> 📝 **Optimization History**: Code has been comprehensively refactored for better readability, maintainability, and extensibility. See [OPTIMIZATION_SUMMARY.md](./OPTIMIZATION_SUMMARY.md)

## ✨ 功能特点 / Features

- 🤖 **智能 SQL 生成**: 使用 DeepSeek 模型将自然语言转换为 SQL 查询
- 🔄 **自动执行**: 自动执行生成的 SQL 查询并返回结果
- 🛡️ **安全防护**: 默认只执行 SELECT 查询，防止数据被误删除或修改
- 📊 **结构化输出**: 以表格形式展示查询结果
- 🌐 **中英文支持**: 支持中英文自然语言查询
- 🔧 **模块化设计**: 清晰的模块分离，易于维护和扩展
- 📝 **专业日志**: 完整的日志系统，便于调试和监控
- 🗄️ **Supabase 支持**: 原生支持 Supabase PostgreSQL 数据库

## 🏗️ 架构 / Architecture

项目使用 LangGraph 构建了一个有向无环图 (DAG) 的工作流，并采用模块化设计：

The project uses LangGraph to build a DAG workflow with modular design:

```
用户输入 → 生成SQL → 执行SQL → 格式化输出
User Input → Generate SQL → Execute SQL → Format Output
```

### 核心组件 / Core Components

**工作流节点 / Workflow Nodes:**
1. **generate_sql**: 分析数据库结构，使用 LLM 生成 SQL 查询
2. **execute_sql**: 执行生成的 SQL 查询
3. **format_output**: 格式化输出结果

**模块架构 / Module Architecture:**

```
text_to_sql/
├── src/text_to_sql/          # 核心包 / Core package
│   ├── core/                 # 核心工作流 / Core workflow
│   │   ├── agent.py          # 主工作流 / Main workflow agent
│   │   └── sql_generator.py  # SQL生成逻辑 / SQL generation logic
│   ├── database/             # 数据库模块 / Database module
│   │   └── manager.py        # 数据库操作 / Database operations
│   └── utils/                # 工具模块 / Utility module
│       ├── config.py         # 配置管理 / Configuration management
│       ├── constants.py      # 常量定义 / Constants definition
│       ├── exceptions.py     # 自定义异常 / Custom exceptions
│       ├── formatter.py      # 输出格式化 / Output formatting
│       └── logger.py         # 日志系统 / Logging system
├── scripts/                  # 脚本工具 / Scripts
│   ├── cli.py                # 交互式命令行 / Interactive CLI
│   ├── demo.py               # 演示脚本 / Demo script
│   ├── init_database.py      # 数据库初始化 / Database initialization
│   └── visualize_workflow.py # 工作流可视化 / Workflow visualization
└── tests/                    # 测试 / Tests
    └── test_database.py      # 数据库测试 / Database tests
```

## 📦 安装 / Installation

### 1. 安装依赖 / Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量 / Configure Environment Variables

**获取 DeepSeek API 密钥 / Get DeepSeek API Key:**

1. 访问 [DeepSeek Platform](https://platform.deepseek.com/) 并注册账号
2. 创建 API 密钥
3. DeepSeek 提供 OpenAI 兼容的 API，价格更实惠

Visit [DeepSeek Platform](https://platform.deepseek.com/) to:
1. Sign up for an account
2. Create an API key
3. DeepSeek provides OpenAI-compatible API with more affordable pricing

**获取 Supabase 数据库 / Get Supabase Database:**

1. 访问 [Supabase](https://supabase.com) 并创建免费项目
2. 在项目设置中获取数据库连接字符串

Visit [Supabase](https://supabase.com) to:
1. Create a free project
2. Get database connection string from project settings

**配置文件 / Configure Files:**

复制 `.env.example` 到 `.env` 并配置你的 API 密钥：

Copy `.env.example` to `.env` and configure your API key:

```bash
cp .env.example .env
```

编辑 `.env` 文件 / Edit `.env` file:

```env
# DeepSeek API配置 / DeepSeek API Configuration
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-chat
LLM_TEMPERATURE=0.0

# Supabase数据库配置 / Supabase Database Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres

# 或使用SQLite进行本地开发 / Or use SQLite for local development
# DATABASE_URL=sqlite:///./sample.db
```

### 3. 初始化数据库 / Initialize Database

```bash
python init_database.py
```

这将创建一个示例数据库，包含：
- 用户表 (users)
- 产品表 (products)  
- 订单表 (orders)

This will create a sample database with:
- Users table
- Products table
- Orders table

## 🚀 使用方法 / Usage

### 快速演示 (无需 API Key) / Quick Demo (No API Key Required)

如果你想先看看系统如何工作，可以运行演示脚本：

If you want to see how the system works first, run the demo script:

```bash
python demo.py
```

这将展示智能体的完整工作流程，包括数据库结构获取、SQL 生成和执行。

This will demonstrate the complete agent workflow, including database schema retrieval, SQL generation, and execution.

### 交互式命令行 / Interactive CLI

```bash
python cli.py
```

然后输入你的自然语言查询，例如：
Then enter your natural language queries, for example:

```
显示所有用户
Show all users

找出购买了笔记本电脑的用户
Find users who bought laptops

统计每个产品的总销量
Count total sales for each product

显示价格最高的3个产品
Show top 3 most expensive products
```

### 作为 Python 模块使用 / Use as Python Module

```python
from text_to_sql import run_query

# 运行查询 / Run query
result = run_query("显示所有用户")
print(result)
```

或从特定模块导入 / Or import from specific modules:

```python
from text_to_sql.core import run_query
from text_to_sql.database import db_manager
from text_to_sql.utils import config, logger

# 自定义配置 / Custom configuration
logger.info("Starting query...")
result = run_query("显示所有用户")
```

## 📝 示例 / Examples

### 示例 1: 查询所有用户 / Query All Users

**输入 / Input:**
```
显示所有用户信息
```

**生成的 SQL / Generated SQL:**
```sql
SELECT * FROM users;
```

**输出 / Output:**
```
id      name    email                   age     created_at
1       张三    zhangsan@example.com    28      2024-01-31 10:00:00
2       李四    lisi@example.com        32      2024-01-31 10:00:01
3       王五    wangwu@example.com      25      2024-01-31 10:00:02
4       赵六    zhaoliu@example.com     35      2024-01-31 10:00:03
```

### 示例 2: 统计产品销量 / Count Product Sales

**输入 / Input:**
```
统计每个产品的总销量
```

**生成的 SQL / Generated SQL:**
```sql
SELECT p.name, SUM(o.quantity) as total_sales
FROM products p
JOIN orders o ON p.id = o.product_id
GROUP BY p.name
ORDER BY total_sales DESC;
```

### 示例 3: 查找特定条件的数据 / Find Specific Data

**输入 / Input:**
```
找出购买了笔记本电脑的用户名称和邮箱
```

**生成的 SQL / Generated SQL:**
```sql
SELECT DISTINCT u.name, u.email
FROM users u
JOIN orders o ON u.id = o.user_id
JOIN products p ON o.product_id = p.id
WHERE p.name LIKE '%笔记本电脑%';
```

## 🔧 自定义数据库 / Custom Database

你可以使用自己的数据库，只需修改 `.env` 文件中的 `DATABASE_URL`：

You can use your own database by modifying `DATABASE_URL` in `.env`:

```env
# Supabase (推荐 / Recommended)
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres

# SQLite (本地开发 / Local Development)
DATABASE_URL=sqlite:///./your_database.db

# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# MySQL
DATABASE_URL=mysql://user:password@localhost:3306/dbname
```

### 使用 Supabase / Using Supabase

Supabase 是一个开源的 Firebase 替代品，提供 PostgreSQL 数据库服务：

Supabase is an open-source Firebase alternative that provides PostgreSQL database service:

1. 在 [Supabase](https://supabase.com) 创建项目 / Create a project at [Supabase](https://supabase.com)
2. 获取数据库连接信息 / Get database connection information:
   - 访问项目设置 → 数据库 / Go to Project Settings → Database
   - 复制连接字符串 / Copy the connection string
3. 在 `.env` 中配置 / Configure in `.env`:
   ```env
   DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
   SUPABASE_URL=https://[YOUR-PROJECT-REF].supabase.co
   SUPABASE_KEY=your_supabase_anon_key
   ```

## 🛡️ 安全性 / Security

- 默认情况下，智能体只生成和执行 SELECT 查询
- 不会执行 DROP, DELETE, UPDATE 等修改数据的操作（除非明确要求）
- 使用参数化查询防止 SQL 注入

- By default, the agent only generates and executes SELECT queries
- Won't execute DROP, DELETE, UPDATE or other data-modifying operations (unless explicitly requested)
- Uses parameterized queries to prevent SQL injection

## 🔍 工作原理 / How It Works

1. **获取数据库结构**: 智能体首先获取数据库的表结构和字段信息
2. **生成 SQL**: 使用 LLM (DeepSeek) 根据数据库结构和用户问题生成 SQL 查询
3. **执行查询**: 使用 SQLAlchemy 执行生成的 SQL 查询
4. **格式化结果**: 将查询结果格式化为易读的表格形式

1. **Get Database Schema**: The agent first retrieves the database table structure and field information
2. **Generate SQL**: Uses LLM (DeepSeek) to generate SQL queries based on the database schema and user question
3. **Execute Query**: Uses SQLAlchemy to execute the generated SQL query
4. **Format Results**: Formats query results into a readable table format

## 📚 技术栈 / Tech Stack

- **LangGraph**: 用于构建智能体工作流
- **LangChain**: 用于 LLM 集成
- **DeepSeek**: 用于自然语言理解和 SQL 生成（支持 OpenAI 兼容 API）
- **Supabase**: PostgreSQL 数据库服务（也支持其他数据库）
- **SQLAlchemy**: 用于数据库操作
- **Python 3.9+**: 编程语言

- **LangGraph**: For building agent workflows
- **LangChain**: For LLM integration
- **DeepSeek**: For natural language understanding and SQL generation (OpenAI-compatible API)
- **Supabase**: PostgreSQL database service (also supports other databases)
- **SQLAlchemy**: For database operations
- **Python 3.9+**: Programming language

## 🤝 贡献 / Contributing

欢迎提交 Issue 和 Pull Request！

Issues and Pull Requests are welcome!

## 📄 许可证 / License

MIT License

---

## 原有功能 / Original Features

本项目原本是一个基于 GitHub Actions 和 Dify 的 AI 代码审查工具。新增的 Text-to-SQL 功能是一个独立的模块，不影响原有的代码审查功能。

This project was originally an AI code review tool based on GitHub Actions and Dify. The newly added Text-to-SQL feature is an independent module that does not affect the original code review functionality.

### AI 代码审查 / AI Code Review

请参考 `.github/scripts/ai_reviewer.py` 和 `.github/workflows/blank.yml` 了解如何使用 AI 代码审查功能。

Please refer to `.github/scripts/ai_reviewer.py` and `.github/workflows/blank.yml` to learn how to use the AI code review feature.
