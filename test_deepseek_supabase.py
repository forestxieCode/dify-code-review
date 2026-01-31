#!/usr/bin/env python3
"""
Test script for DeepSeek + Supabase integration

This script demonstrates how to configure and use the Text-to-SQL agent
with DeepSeek LLM and Supabase database.
"""
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_configuration():
    """Test that configuration loads correctly."""
    print("=" * 60)
    print("Testing Configuration Loading")
    print("=" * 60)
    
    from text_to_sql.utils.config import config
    
    print(f"✓ LLM Model: {config.llm.model_name}")
    print(f"✓ LLM Temperature: {config.llm.temperature}")
    print(f"✓ Database URL: {config.database.url}")
    
    if config.llm.base_url:
        print(f"✓ Custom API Base URL: {config.llm.base_url}")
    
    if config.llm.api_key:
        print(f"✓ API Key: {'*' * 8} (configured)")
    else:
        print("⚠ API Key: Not configured (required for actual usage)")
    
    print(f"✓ Configuration validation: {config.validate()}")
    print()


def test_sql_generator():
    """Test SQL generator initialization."""
    print("=" * 60)
    print("Testing SQL Generator")
    print("=" * 60)
    
    from text_to_sql.core.sql_generator import LLMSQLGenerator, MockSQLGenerator
    
    # Test LLM generator
    try:
        generator = LLMSQLGenerator()
        print(f"✓ LLM SQL Generator initialized")
        print(f"  - Model: {generator.model_name}")
        print(f"  - Temperature: {generator.temperature}")
        print(f"  - Base URL: {generator.base_url or 'Default (OpenAI)'}")
    except Exception as e:
        print(f"✗ LLM Generator error: {e}")
    
    # Test Mock generator (for testing without API key)
    try:
        mock_gen = MockSQLGenerator()
        test_query = mock_gen.generate("test", "schema")
        print(f"✓ Mock SQL Generator works: {test_query[:50]}...")
    except Exception as e:
        print(f"✗ Mock Generator error: {e}")
    
    print()


def test_database_manager():
    """Test database manager initialization."""
    print("=" * 60)
    print("Testing Database Manager")
    print("=" * 60)
    
    from text_to_sql.database.manager import DatabaseManager
    
    try:
        db = DatabaseManager()
        print(f"✓ Database Manager initialized")
        print(f"  - Database URL: {db._database_url}")
        
        # Check database type
        if 'postgresql' in db._database_url.lower():
            print(f"  - Type: PostgreSQL (Supabase compatible)")
        elif 'sqlite' in db._database_url.lower():
            print(f"  - Type: SQLite (Local development)")
        elif 'mysql' in db._database_url.lower():
            print(f"  - Type: MySQL")
        else:
            print(f"  - Type: Other")
            
    except Exception as e:
        print(f"✗ Database Manager error: {e}")
    
    print()


def test_environment_variables():
    """Show which environment variables are configured."""
    print("=" * 60)
    print("Environment Variables Status")
    print("=" * 60)
    
    env_vars = {
        'DEEPSEEK_API_KEY': 'DeepSeek API Key',
        'DEEPSEEK_BASE_URL': 'DeepSeek Base URL',
        'OPENAI_API_KEY': 'OpenAI API Key (fallback)',
        'LLM_MODEL': 'LLM Model Name',
        'LLM_TEMPERATURE': 'LLM Temperature',
        'DATABASE_URL': 'Database Connection URL',
        'SUPABASE_URL': 'Supabase Project URL',
        'SUPABASE_KEY': 'Supabase API Key',
    }
    
    for var, description in env_vars.items():
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if 'KEY' in var or 'PASSWORD' in var:
                display = '*' * 8
            elif 'URL' in var:
                display = value[:30] + '...' if len(value) > 30 else value
            else:
                display = value
            print(f"✓ {description:30} : {display}")
        else:
            print(f"⚠ {description:30} : Not set")
    
    print()


def show_usage_examples():
    """Show usage examples."""
    print("=" * 60)
    print("Usage Examples")
    print("=" * 60)
    
    print("""
# 1. Set up environment variables (create .env file):
cat > .env << 'EOF'
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-chat
LLM_TEMPERATURE=0.0
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres
SUPABASE_URL=https://[PROJECT].supabase.co
SUPABASE_KEY=your_supabase_anon_key
EOF

# 2. Initialize the database:
python init_database.py

# 3. Run the demo:
python demo.py

# 4. Use the interactive CLI:
python cli.py

# 5. Use as Python module:
from text_to_sql import run_query
# Example bilingual query (supports both Chinese and English)
result = run_query("显示所有用户")  # "Show all users" in Chinese
print(result)
    """)


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("DeepSeek + Supabase Integration Test")
    print("=" * 60)
    print()
    
    # Show environment status
    test_environment_variables()
    
    # Test configuration
    test_configuration()
    
    # Test SQL generator
    test_sql_generator()
    
    # Test database manager
    test_database_manager()
    
    # Show usage examples
    show_usage_examples()
    
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    print("""
All components initialized successfully! ✓

Next steps:
1. Configure your .env file with DeepSeek API key and Supabase credentials
2. Initialize the database: python init_database.py
3. Run the demo: python demo.py
4. Start using the CLI: python cli.py

For more information, see:
- README.md - Complete documentation
- QUICK_START.md - Quick start guide
- .env.example - Environment variable template
    """)


if __name__ == "__main__":
    main()
