#!/usr/bin/env python3
"""
Interactive CLI for the Text-to-SQL Agent
"""
import sys
from text_to_sql_agent import run_query


def main():
    """Main CLI interface"""
    print("=" * 80)
    print("🤖 LangGraph Text-to-SQL 智能体 / LangGraph Text-to-SQL Agent")
    print("=" * 80)
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
    print("=" * 80)
    print()
    
    while True:
        try:
            # Get user input
            user_input = input("\n💬 请输入你的问题 / Enter your question: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("\n👋 再见! / Goodbye!")
                break
            
            # Skip empty input
            if not user_input:
                continue
            
            # Run the query
            print("\n" + "=" * 80)
            result = run_query(user_input)
            print(result)
            print("=" * 80)
            
        except KeyboardInterrupt:
            print("\n\n👋 再见! / Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ 错误 / Error: {str(e)}")


if __name__ == "__main__":
    main()
