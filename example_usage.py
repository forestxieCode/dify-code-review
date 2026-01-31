#!/usr/bin/env python3
"""
Example usage of the text_to_sql package.

This script demonstrates how to use the reorganized package.
"""
import sys
import os

# Add src to path for direct execution (not needed if package is installed)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Example 1: Import and use the main function
print("=" * 80)
print("Example 1: Using the main run_query function")
print("=" * 80)

from text_to_sql import run_query

# Note: This requires OPENAI_API_KEY to be set
# result = run_query("显示所有用户")
# print(result)
print("Function imported successfully: run_query")
print("To use it, set OPENAI_API_KEY environment variable and call run_query()")

# Example 2: Import specific modules
print("\n" + "=" * 80)
print("Example 2: Importing specific modules")
print("=" * 80)

from text_to_sql.database import db_manager
from text_to_sql.utils import config, logger
from text_to_sql.utils.formatter import OutputFormatter

print(f"✅ Database manager imported")
print(f"   Database URL: {config.database.url}")

# Get database schema
schema = db_manager.get_schema()
print(f"\n✅ Database schema retrieved:")
print(schema[:200] + "..." if len(schema) > 200 else schema)

# Example 3: Use the formatter
print("\n" + "=" * 80)
print("Example 3: Using the OutputFormatter")
print("=" * 80)

sample_data = [
    {"name": "张三", "age": 28, "city": "北京"},
    {"name": "李四", "age": 32, "city": "上海"},
    {"name": "王五", "age": 25, "city": "广州"},
]

formatted = OutputFormatter.format_table(sample_data)
print(formatted)

print("\n" + "=" * 80)
print("✅ All examples completed successfully!")
print("=" * 80)
