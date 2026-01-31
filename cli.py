#!/usr/bin/env python3
"""
Interactive CLI for the Text-to-SQL Agent.
"""
import sys
from text_to_sql_agent import run_query
from constants import (
    OUTPUT_SEPARATOR,
    CLI_WELCOME,
    CLI_GOODBYE,
    CLI_PROMPT,
    CLI_EXIT_COMMANDS
)


def main():
    """Main CLI interface."""
    print(OUTPUT_SEPARATOR)
    print(CLI_WELCOME)
    print(OUTPUT_SEPARATOR)
    print("\n提示 / Tips:")
    print("  - 用自然语言描述你想查询的内容")
    print("  - Describe what you want to query in natural language")
    print("  - 输入 'quit' 或 'exit' 退出程序")
    print("  - Type 'quit' or 'exit' to quit")
    print("\n示例问题 / Example questions:")
    print("  - 显示所有用户 / Show all users")
    print("  - 找出购买了笔记本电脑的用户 / Find users who bought laptops")
    print("  - 统计每个产品的总销量 / Count total sales for each product")
    print("  - 显示价格最高的3个产品 / Show top 3 most expensive products")
    print(OUTPUT_SEPARATOR)
    print()
    
    while True:
        try:
            # Get user input
            user_input = input(f"\n{CLI_PROMPT}").strip()
            
            # Check for exit commands
            if user_input.lower() in CLI_EXIT_COMMANDS:
                print(f"\n{CLI_GOODBYE}")
                break
            
            # Skip empty input
            if not user_input:
                continue
            
            # Run the query
            print(f"\n{OUTPUT_SEPARATOR}")
            result = run_query(user_input)
            print(result)
            print(OUTPUT_SEPARATOR)
            
        except KeyboardInterrupt:
            print(f"\n\n{CLI_GOODBYE}")
            break
        except Exception as e:
            print(f"\n❌ 错误 / Error: {str(e)}")


if __name__ == "__main__":
    main()
