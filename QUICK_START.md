# 快速开始指南 / Quick Start Guide

本指南帮助你快速了解和使用重组后的项目。
This guide helps you quickly understand and use the reorganized project.

## 🎯 项目结构一览 / Project Structure Overview

```
text_to_sql/
├── 📦 src/text_to_sql/          核心包 / Core Package
│   ├── 🎯 core/                 业务逻辑 / Business Logic
│   ├── 💾 database/             数据库 / Database
│   └── 🔧 utils/                工具 / Utilities
├── 🎬 scripts/                  脚本 / Scripts
├── ✅ tests/                    测试 / Tests
└── 📝 文档 / Documentation
```

## ⚡ 5分钟快速开始 / 5-Minute Quick Start

### 1️⃣ 安装依赖 / Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ 初始化数据库 / Initialize Database
```bash
python init_database.py
```

### 3️⃣ 运行演示 / Run Demo
```bash
python demo.py
```

### 4️⃣ 使用交互式CLI (需要API Key) / Use Interactive CLI (API Key Required)
```bash
# 设置环境变量 / Set environment variable
export DEEPSEEK_API_KEY=your_key_here

# 运行CLI / Run CLI
python cli.py
```

## 📚 使用示例 / Usage Examples

### 作为Python包使用 / Use as Python Package

```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 导入主要功能 / Import main functions
from text_to_sql import run_query, db_manager, config

# 运行查询 / Run query (需要 API Key / Requires API Key)
result = run_query("显示所有用户")
print(result)

# 获取数据库schema / Get database schema
schema = db_manager.get_schema()
print(schema)
```

### 运行测试 / Run Tests

```bash
# 数据库测试 / Database tests
python test_database.py

# 可视化工作流 / Visualize workflow
python visualize_workflow.py

# 查看使用示例 / See usage examples
python example_usage.py
```

## 🔍 项目文件导航 / File Navigation

### 想要...? / Want to...?

| 目标 / Goal | 文件位置 / File Location |
|------------|-------------------------|
| 了解整体架构 / Understand architecture | `README.md` |
| 查看项目结构 / See project structure | `STRUCTURE.md` |
| 了解重组变化 / Learn about reorganization | `REORGANIZATION_SUMMARY.md` |
| 修改核心工作流 / Modify core workflow | `src/text_to_sql/core/agent.py` |
| 修改SQL生成逻辑 / Modify SQL generation | `src/text_to_sql/core/sql_generator.py` |
| 修改数据库操作 / Modify database ops | `src/text_to_sql/database/manager.py` |
| 修改配置 / Modify configuration | `src/text_to_sql/utils/config.py` |
| 添加新的异常 / Add new exception | `src/text_to_sql/utils/exceptions.py` |
| 修改输出格式 / Modify output format | `src/text_to_sql/utils/formatter.py` |
| 修改日志行为 / Modify logging | `src/text_to_sql/utils/logger.py` |
| 运行CLI / Run CLI | `cli.py` 或 `scripts/cli.py` |
| 查看演示 / See demo | `demo.py` 或 `scripts/demo.py` |
| 添加测试 / Add tests | `tests/` |

## 🛠️ 开发指南 / Development Guide

### 添加新功能 / Adding New Features

1. **确定模块** / Determine module
   - 核心业务逻辑 → `src/text_to_sql/core/`
   - 数据库相关 → `src/text_to_sql/database/`
   - 工具函数 → `src/text_to_sql/utils/`

2. **创建文件** / Create file
   ```bash
   # 例如，添加新的数据库适配器 / e.g., add new database adapter
   touch src/text_to_sql/database/postgres_adapter.py
   ```

3. **更新 __init__.py** / Update __init__.py
   ```python
   # src/text_to_sql/database/__init__.py
   from .postgres_adapter import PostgresAdapter
   ```

4. **添加测试** / Add tests
   ```bash
   touch tests/test_postgres_adapter.py
   ```

### 运行现有脚本 / Running Existing Scripts

所有脚本都可以从根目录直接运行：
All scripts can be run directly from root:

```bash
# 方式1: 直接运行 / Method 1: Direct run
python cli.py
python demo.py
python init_database.py
python visualize_workflow.py
python test_database.py

# 方式2: 从scripts目录 / Method 2: From scripts directory
python scripts/cli.py
python scripts/demo.py
python scripts/init_database.py
python scripts/visualize_workflow.py
```

## 📦 安装为包 / Installing as Package

```bash
# 开发模式安装 / Install in development mode
pip install -e .

# 安装后可以使用命令 / After installation, use commands
text-to-sql              # 运行 CLI
text-to-sql-demo         # 运行演示
text-to-sql-init         # 初始化数据库
text-to-sql-visualize    # 可视化工作流
```

## 🎓 学习路径 / Learning Path

### 初学者 / Beginners
1. 阅读 `README.md` 了解项目概述
2. 运行 `python demo.py` 查看演示
3. 阅读 `STRUCTURE.md` 理解项目结构
4. 查看 `example_usage.py` 学习如何使用

### 开发者 / Developers
1. 查看 `STRUCTURE.md` 了解架构
2. 阅读核心模块代码 (`src/text_to_sql/core/`)
3. 查看数据库模块 (`src/text_to_sql/database/`)
4. 了解工具模块 (`src/text_to_sql/utils/`)
5. 运行测试并添加新测试

### 贡献者 / Contributors
1. 阅读 `REORGANIZATION_SUMMARY.md` 了解重组变化
2. 理解模块职责和边界
3. 遵循现有的代码结构和风格
4. 添加测试和文档

## 🔧 常见任务 / Common Tasks

### 修改提示词 / Modify Prompts
编辑 / Edit: `src/text_to_sql/utils/constants.py`

### 支持新的数据库 / Support New Database
添加新的适配器到 / Add new adapter to: `src/text_to_sql/database/`

### 修改输出格式 / Modify Output Format
编辑 / Edit: `src/text_to_sql/utils/formatter.py`

### 添加新的日志级别 / Add New Log Level
编辑 / Edit: `src/text_to_sql/utils/logger.py`

### 修改配置 / Modify Configuration
编辑 / Edit: `src/text_to_sql/utils/config.py`

## 🚀 部署 / Deployment

### 作为库使用 / Use as Library
```bash
# 构建分发包 / Build distribution
python setup.py sdist bdist_wheel

# 安装 / Install
pip install dist/text_to_sql-1.0.0-py3-none-any.whl
```

### 作为服务运行 / Run as Service
可以基于 `cli.py` 创建 Web 服务或 API
You can create web service or API based on `cli.py`

## 📞 获取帮助 / Getting Help

- 📖 查看文档 / Check documentation: `README.md`, `STRUCTURE.md`
- 💡 查看示例 / See examples: `example_usage.py`
- 🐛 报告问题 / Report issues: GitHub Issues
- 📝 查看优化历史 / See optimization history: `OPTIMIZATION_SUMMARY.md`

## ✨ 最佳实践 / Best Practices

1. ✅ 导入时使用完整路径 / Use full paths when importing
   ```python
   from text_to_sql.core import run_query  # 好 / Good
   from agent import run_query             # 差 / Bad
   ```

2. ✅ 保持模块职责单一 / Keep module responsibilities single
3. ✅ 在正确的模块添加代码 / Add code in the right module
4. ✅ 更新相关的 `__init__.py` / Update relevant `__init__.py`
5. ✅ 添加测试 / Add tests
6. ✅ 更新文档 / Update documentation

## 🎉 下一步 / Next Steps

1. 浏览代码，理解结构 / Browse code, understand structure
2. 运行所有示例 / Run all examples
3. 尝试修改和扩展 / Try modifying and extending
4. 添加你自己的功能 / Add your own features
5. 贡献代码！ / Contribute code!

---

**版本 / Version:** 1.0.0  
**更新日期 / Updated:** 2026-01-31
