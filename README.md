# LangGraph Text-to-SQL 智能体 / LangGraph Text-to-SQL Agent

这是一个基于 LangGraph 构建的智能体，可以将用户的自然语言输入转换为 SQL 查询，并执行查询返回结果。

This is an intelligent agent built with LangGraph that converts natural language input to SQL queries and executes them to return results.

> 🎉 **最新更新**: 代码已进行全面重构优化，提升了可读性、可维护性和可扩展性。详见 [OPTIMIZATION_SUMMARY.md](./OPTIMIZATION_SUMMARY.md)
> 
> 🎉 **Latest Update**: Code has been comprehensively refactored for better readability, maintainability, and extensibility. See [OPTIMIZATION_SUMMARY.md](./OPTIMIZATION_SUMMARY.md)

## ✨ 功能特点 / Features

- 🤖 **智能 SQL 生成**: 使用 GPT 模型将自然语言转换为 SQL 查询
- 🔄 **自动执行**: 自动执行生成的 SQL 查询并返回结果
- 🛡️ **安全防护**: 默认只执行 SELECT 查询，防止数据被误删除或修改
- 📊 **结构化输出**: 以表格形式展示查询结果
- 🌐 **中英文支持**: 支持中英文自然语言查询
- 🔧 **模块化设计**: 清晰的模块分离，易于维护和扩展
- 📝 **专业日志**: 完整的日志系统，便于调试和监控

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
- `config.py` - 配置管理 / Configuration management
- `constants.py` - 常量定义 / Constants definition
- `exceptions.py` - 自定义异常 / Custom exceptions
- `logger.py` - 日志系统 / Logging system
- `database.py` - 数据库操作 / Database operations
- `sql_generator.py` - SQL生成逻辑 / SQL generation logic
- `formatter.py` - 输出格式化 / Output formatting
- `text_to_sql_agent.py` - 主要工作流 / Main workflow

## 📦 安装 / Installation

### 1. 安装依赖 / Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量 / Configure Environment Variables

复制 `.env.example` 到 `.env` 并配置你的 API 密钥：

Copy `.env.example` to `.env` and configure your API key:

```bash
cp .env.example .env
```

编辑 `.env` 文件 / Edit `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./sample.db
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
from text_to_sql_agent import run_query

# 运行查询
result = run_query("显示所有用户")
print(result)
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
# SQLite
DATABASE_URL=sqlite:///./your_database.db

# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# MySQL
DATABASE_URL=mysql://user:password@localhost:3306/dbname
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
2. **生成 SQL**: 使用 LLM (GPT-3.5) 根据数据库结构和用户问题生成 SQL 查询
3. **执行查询**: 使用 SQLAlchemy 执行生成的 SQL 查询
4. **格式化结果**: 将查询结果格式化为易读的表格形式

1. **Get Database Schema**: The agent first retrieves the database table structure and field information
2. **Generate SQL**: Uses LLM (GPT-3.5) to generate SQL queries based on the database schema and user question
3. **Execute Query**: Uses SQLAlchemy to execute the generated SQL query
4. **Format Results**: Formats query results into a readable table format

## 📚 技术栈 / Tech Stack

- **LangGraph**: 用于构建智能体工作流
- **LangChain**: 用于 LLM 集成
- **OpenAI GPT-3.5**: 用于自然语言理解和 SQL 生成
- **SQLAlchemy**: 用于数据库操作
- **Python 3.9+**: 编程语言

- **LangGraph**: For building agent workflows
- **LangChain**: For LLM integration
- **OpenAI GPT-3.5**: For natural language understanding and SQL generation
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
