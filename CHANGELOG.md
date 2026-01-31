# 更新日志 / Changelog

## [1.1.0] - 2026-01-31

### 🎉 重大更新 / Major Updates

#### 从 OpenAI 迁移到 DeepSeek / Migrated from OpenAI to DeepSeek
- 添加 DeepSeek API 支持（OpenAI 兼容）/ Added DeepSeek API support (OpenAI-compatible)
- 更低的 API 成本 / Lower API costs
- 保持向后兼容 OpenAI / Maintains backward compatibility with OpenAI

#### 添加 Supabase 数据库支持 / Added Supabase Database Support
- 集成 Supabase PostgreSQL 数据库 / Integrated Supabase PostgreSQL database
- 云端托管，自动备份 / Cloud-hosted with automatic backups
- 保持向后兼容 SQLite 和其他数据库 / Maintains backward compatibility with SQLite and other databases

### ✨ 新增功能 / Added Features

- 自定义 API 基础 URL 支持 / Custom API base URL support
- Supabase 客户端集成 / Supabase client integration
- PostgreSQL 数据库驱动 / PostgreSQL database driver
- 综合迁移指南 / Comprehensive migration guide
- 集成测试脚本 / Integration test script

### 📝 文件更改 / Changed Files

#### 配置文件 / Configuration Files
- `requirements.txt` - 添加新依赖 / Added new dependencies
  - `openai>=1.0.0`
  - `supabase>=2.0.0`
  - `psycopg2-binary>=2.9.0`
- `.env.example` - 更新环境变量模板 / Updated environment variables template
  - 添加 `DEEPSEEK_API_KEY`
  - 添加 `DEEPSEEK_BASE_URL`
  - 添加 `SUPABASE_URL`
  - 添加 `SUPABASE_KEY`
  - 更新 `DATABASE_URL` 示例

#### 核心代码 / Core Code
- `src/text_to_sql/utils/config.py`
  - 添加 `base_url` 字段到 `LLMConfig`
  - 更新配置加载逻辑支持 DeepSeek
  - 支持 `DEEPSEEK_API_KEY` 环境变量
  
- `src/text_to_sql/core/sql_generator.py`
  - 添加自定义 `base_url` 支持
  - 更新文档说明 DeepSeek 兼容性
  - 改进初始化逻辑

#### 文档 / Documentation
- `README.md` - 全面更新
  - 添加 DeepSeek 设置说明
  - 添加 Supabase 配置指南
  - 更新技术栈信息
  - 添加 API 密钥获取指南
  
- `QUICK_START.md` - 更新快速开始指南
  - 更新环境变量引用
  - 添加 DeepSeek 相关说明
  
- `MIGRATION_GUIDE.md` - 新增迁移指南
  - 详细的迁移步骤
  - 故障排除指南
  - 最佳实践建议

#### 测试 / Tests
- `test_deepseek_supabase.py` - 新增集成测试
  - 配置验证
  - 组件初始化测试
  - 环境变量状态检查
  - 使用示例展示

### 🔧 技术改进 / Technical Improvements

- 改进的配置管理 / Improved configuration management
- 更好的错误处理 / Better error handling
- 增强的日志记录 / Enhanced logging
- 全面的文档 / Comprehensive documentation

### 🔒 安全性 / Security

- ✅ CodeQL 扫描通过：0 个漏洞 / CodeQL scan passed: 0 vulnerabilities
- ✅ 代码审查反馈已解决 / Code review feedback addressed
- ✅ 安全的密钥管理实践 / Secure key management practices

### ⚠️ 重要变更 / Breaking Changes

无破坏性变更！所有现有代码继续工作。

No breaking changes! All existing code continues to work.

### 🔄 迁移说明 / Migration Notes

现有用户可以继续使用 OpenAI API 和 SQLite。要迁移到 DeepSeek 和 Supabase：

Existing users can continue using OpenAI API and SQLite. To migrate to DeepSeek and Supabase:

1. 安装新依赖：`pip install -r requirements.txt`
2. 更新 `.env` 文件
3. 查看 `MIGRATION_GUIDE.md` 获取详细说明

1. Install new dependencies: `pip install -r requirements.txt`
2. Update `.env` file
3. See `MIGRATION_GUIDE.md` for detailed instructions

### 📊 测试结果 / Test Results

- ✅ 所有现有测试通过 / All existing tests pass
- ✅ 新集成测试通过 / New integration tests pass
- ✅ 配置加载验证 / Configuration loading verified
- ✅ 数据库连接测试 / Database connection tested

### �� 致谢 / Acknowledgments

感谢以下项目使这次更新成为可能：

Thanks to the following projects that made this update possible:
- [DeepSeek](https://www.deepseek.com/) - 高性能语言模型
- [Supabase](https://supabase.com/) - 开源 Firebase 替代品
- [LangChain](https://www.langchain.com/) - LLM 应用框架

---

## [1.0.0] - 2024-01-31

### 初始版本 / Initial Release

- 基于 LangGraph 的 Text-to-SQL 智能体 / LangGraph-based Text-to-SQL agent
- OpenAI GPT-3.5 集成 / OpenAI GPT-3.5 integration
- SQLite 数据库支持 / SQLite database support
- 模块化架构 / Modular architecture
- 中英文支持 / Chinese and English support
